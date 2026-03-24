"""Shared Mini-Agent + minimax_search MCP runner (CLI and Telegram use this)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]
_EXAMPLES_PY = _REPO_ROOT / "examples_python"
if str(_EXAMPLES_PY) not in sys.path:
    sys.path.insert(0, str(_EXAMPLES_PY))

from _env import load_repo_dotenv  # noqa: E402

from mini_agent.agent import Agent  # noqa: E402
from mini_agent.config import Config  # noqa: E402
from mini_agent.llm import LLMClient  # noqa: E402
from mini_agent.retry import RetryConfig as LLMRetryConfig  # noqa: E402
from mini_agent.schema import LLMProvider  # noqa: E402
from mini_agent.tools.mcp_loader import (  # noqa: E402
    cleanup_mcp_connections,
    load_mcp_tools_async,
    set_mcp_timeout_config,
)

_MCP_ENV_KEYS = frozenset({"MINIMAX_API_KEY", "SERPER_API_KEY", "JINA_API_KEY"})


def default_config_dir() -> Path:
    return Path(__file__).resolve().parent / "config"


def ensure_websearch_env() -> None:
    """Load repo .env and force MCP-related keys from file (see run_websearch_bot docstring)."""
    load_repo_dotenv()
    _force_api_keys_from_repo_dotenv()


def _force_api_keys_from_repo_dotenv() -> None:
    path = _REPO_ROOT / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if key not in _MCP_ENV_KEYS:
            continue
        val = val.strip().strip("'").strip('"')
        if val:
            os.environ[key] = val


def _resolve_config_yaml(config_dir: Path) -> Path:
    for name in ("config.yaml", "config-example.yaml"):
        p = config_dir / name
        if p.is_file():
            return p
    raise FileNotFoundError(
        f"No config.yaml or config-example.yaml in {config_dir}"
    )


def load_config(config_dir: Path) -> Config:
    load_repo_dotenv()
    src = _resolve_config_yaml(config_dir)
    data = yaml.safe_load(src.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Invalid YAML: expected mapping at root")

    env_key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if env_key:
        data["api_key"] = env_key
    if os.environ.get("MINIMAX_TEXT_MODEL", "").strip():
        data["model"] = os.environ["MINIMAX_TEXT_MODEL"].strip()
    if os.environ.get("MINIMAX_API_BASE", "").strip():
        data["api_base"] = os.environ["MINIMAX_API_BASE"].strip()

    api_key = data.get("api_key", "")
    if not api_key or str(api_key).startswith("YOUR_"):
        raise ValueError(
            "Set MINIMAX_API_KEY in repo-root .env or api_key in config.yaml"
        )

    fd, tmp_path = tempfile.mkstemp(suffix=".yaml", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True)
        return Config.from_yaml(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _prepare_mcp_config_path(
    config_dir: Path, mcp_config_filename: str
) -> tuple[str, Path | None]:
    primary = config_dir / mcp_config_filename
    src = primary if primary.is_file() else config_dir / "mcp-example.json"
    if not src.is_file():
        return str(primary), None

    data = json.loads(src.read_text(encoding="utf-8"))
    extra = {k: os.environ[k] for k in _MCP_ENV_KEYS if os.environ.get(k, "").strip()}
    if not extra:
        return str(primary), None

    for srv in data.get("mcpServers", {}).values():
        if srv.get("disabled"):
            continue
        merged = dict(srv.get("env") or {})
        merged.update(extra)
        srv["env"] = merged

    fd, tmp = tempfile.mkstemp(suffix=".json", text=True)
    tmp_path = Path(tmp)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return str(tmp_path), tmp_path


def _llm_client(config: Config) -> LLMClient:
    r = config.llm.retry
    retry = LLMRetryConfig(
        enabled=r.enabled,
        max_retries=r.max_retries,
        initial_delay=r.initial_delay,
        max_delay=r.max_delay,
        exponential_base=r.exponential_base,
    )
    prov = (
        LLMProvider.ANTHROPIC
        if config.llm.provider.lower() == LLMProvider.ANTHROPIC.value
        else LLMProvider.OPENAI
    )
    return LLMClient(
        api_key=config.llm.api_key,
        provider=prov,
        api_base=config.llm.api_base,
        model=config.llm.model,
        retry_config=retry,
    )


async def run_query(query: str, config_dir: Path) -> str:
    """Run one agent turn: Mini-Agent + MCP web search, return final assistant text."""
    config = load_config(config_dir)
    set_mcp_timeout_config(
        connect_timeout=config.tools.mcp.connect_timeout,
        execute_timeout=config.tools.mcp.execute_timeout,
        sse_read_timeout=config.tools.mcp.sse_read_timeout,
    )

    mcp_resolved, mcp_temp = _prepare_mcp_config_path(
        config_dir, config.tools.mcp_config_path
    )
    try:
        tools = await load_mcp_tools_async(mcp_resolved)
        if not tools:
            raise RuntimeError(
                "No MCP tools loaded. Check mcp-example.json / mcp.json, `uv` on PATH, and server logs above."
            )

        sp_path = config_dir / config.agent.system_prompt_path
        system_prompt = (
            sp_path.read_text(encoding="utf-8")
            if sp_path.is_file()
            else "You are a helpful assistant with web search tools."
        )

        with tempfile.TemporaryDirectory() as workspace:
            agent = Agent(
                llm_client=_llm_client(config),
                system_prompt=system_prompt,
                tools=tools,
                max_steps=config.agent.max_steps,
                workspace_dir=workspace,
            )
            agent.add_user_message(query)
            try:
                return await agent.run()
            finally:
                await cleanup_mcp_connections()
    finally:
        if mcp_temp is not None:
            mcp_temp.unlink(missing_ok=True)
