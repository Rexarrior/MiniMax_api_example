# minimax_explore

Minimal examples for calling [MiniMax API](https://platform.minimax.io/docs/guides/models-intro) using **bash** (`examples/*.sh`) and **Python** mirror ([`examples_python/`](examples_python/)) with shared module [`examples_python/minimax_http.py`](examples_python/minimax_http.py) (`httpx`). Text via Anthropic-compatible gateway.

---

## Referral Link

If you decide to subscribe, I'd appreciate you using [my referral link](https://platform.minimax.io/subscribe/token-plan?code=KBrJm5Rkwj&source=link).
By MiniMax terms: **you** get **10%** off subscription and dev ambassador status; **I** get **10%** back as **API voucher**.

---

## Setup

1. Copy `.env.example` → `.env` and set `MINIMAX_API_KEY` ([get key here](https://platform.minimax.io/user-center/basic-information/interface-key))
2. `pip install -r requirements.txt` (`anthropic`, `httpx`)
3. For shell examples: `bash`, `curl`, `python3`
4. Python scripts run from repo root load root `.env` via [`examples_python/_env.py`](examples_python/_env.py)

---

## Token Plan Models

| Model | Identifier | Description |
|-------|------------|-------------|
| M2.7 / M2.7-highspeed | MiniMax-M2.7 | Text chat (highspeed — separate High-Speed subscription) |
| Speech 2.8 | speech-2.8-hd | TTS |
| Video | MiniMax-Hailuo-2.3, MiniMax-Hailuo-2.3-Fast | T2V / I2V |
| Music | music-2.5 | Music generation |
| Image | image-01 | Text-to-image |

**M2.7-highspeed** — high-speed inference, available only on High-Speed plans. Standard plans include only M2.7.

Your Token Plan limits — [`config/token_plan_limits.yaml`](config/token_plan_limits.yaml).

---

## Bash Examples

| File | What it does |
|------|--------------|
| [`examples/02_speech_t2a_sync.sh`](examples/02_speech_t2a_sync.sh) | Sync TTS `POST /v1/t2a_v2` → `out/t2a_sync.mp3` |
| [`examples/03_speech_t2a_async.sh`](examples/03_speech_t2a_async.sh) | Async TTS: create → query → `GET /v1/files/retrieve` → URL to console |
| [`examples/04_video_t2v.sh`](examples/04_video_t2v.sh) | Text-to-video, prints `task_id` |
| [`examples/05_video_i2v.sh`](examples/05_video_i2v.sh) | Image-to-video (`MiniMax-Hailuo-2.3-Fast`), prints `task_id` |
| [`examples/06_video_poll.sh`](examples/06_video_poll.sh) | Poll `GET /v1/query/video_generation`, on success — download via `download_url` |
| [`examples/07_music_generation.sh`](examples/07_music_generation.sh) | `POST /v1/music_generation` (optional `MINIMAX_RAW_JSON=1`) |
| [`examples/09_image_t2i.sh`](examples/09_image_t2i.sh) | Text-to-image `image-01` |

---

## Python Examples

| File | What it does |
|------|--------------|
| [`examples_python/01_text_anthropic.py`](examples_python/01_text_anthropic.py) | Chat `MiniMax-M2.7` via [Anthropic-compatible API](https://platform.minimax.io/docs/api-reference/text-anthropic-api) |
| [`examples_python/02_speech_t2a_sync.py`](examples_python/02_speech_t2a_sync.py) | Sync TTS → `out/t2a_sync.mp3` |
| [`examples_python/03_speech_t2a_async.py`](examples_python/03_speech_t2a_async.py) | Async TTS → URL |
| [`examples_python/04_video_t2v.py`](examples_python/04_video_t2v.py) | Text-to-video → `task_id` |
| [`examples_python/05_video_i2v.py`](examples_python/05_video_i2v.py) | Image-to-video → `task_id` |
| [`examples_python/06_video_poll.py`](examples_python/06_video_poll.py) | Poll video and download to `out/` |
| [`examples_python/07_music_generation.py`](examples_python/07_music_generation.py) | `MINIMAX_RAW_JSON=1` — single JSON line |
| [`examples_python/07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) | Long text: multiple `POST /v1/music_generation`, optional `ffmpeg` → one mp3 |
| [`examples_python/09_image_t2i.py`](examples_python/09_image_t2i.py) | Text-to-image |

---

## Quick Start

Run a single example from repo root:

```bash
bash examples/02_speech_t2a_sync.sh
python3 examples_python/01_text_anthropic.py
python3 examples_python/02_speech_t2a_sync.py
```

(`chmod +x examples/*.sh` if you want to call `./examples/...`)

For video: `python3 examples_python/04_video_t2v.py`, then `TASK_ID=... python3 examples_python/06_video_poll.py`.

**Long lyrics.** Per [MiniMax docs](https://platform.minimax.io/docs/api-reference/music-generation), `lyrics` field has a length limit (for **Music-2.5** in Token Plan — up to **3500** characters). There is **no** "continue previous audio" parameter in Music Generation. To voice your entire text, script [`07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) splits a tagged file into parts and calls API multiple times; with `ffmpeg` available it can assemble `music_<model>_all.mp3`:

```bash
PYTHONPATH=examples_python python3 examples_python/07_music_from_lyrics_file.py my_liryc_tagged.txt --model music-2.5 --concat
```

---

## Run All Token Plan Models

Script [`scripts/run_token_plan_models.sh`](scripts/run_token_plan_models.sh) calls in sequence:

- Text: MiniMax-M2.7
- Speech 2.8: hd (sync + async)
- Video: Hailuo-2.3 T2V, Hailuo-2.3-Fast I2V
- Music: music-2.5
- Image: image-01

```bash
WARNING_READED=1 bash scripts/run_token_plan_models.sh
# faster (no video and no async TTS):
WARNING_READED=1 SKIP_VIDEO=1 SKIP_ASYNC_SPEECH=1 bash scripts/run_token_plan_models.sh
```

**Quota warning.** On first run, the script prints a warning and exits with code 1. Full run significantly consumes Token Plan daily/window quotas — it makes sense to run examples in parts. To explicitly agree and continue, set **`WARNING_READED=1`** in environment (e.g., in command line) or add the same line to `.env`.

Scripts `07`, `09` with `MINIMAX_RAW_JSON=1` output single JSON line to stdout (convenient for pipes); the runner sets it itself.

Each example writes artifacts to `out/` (stderr: line `Wrote …`): **02** mp3, **03** async mp3 via `download_url`, **04/05** `last_video_task_id.txt`, **06** mp4, **07** `music_<model>.mp3`, **09** `image_t2i_*.jpeg`. **01** (Python): `last_text_reply.txt`. Runner only briefly summarizes stdout; no duplicate writes.

---

<details>
<summary>Legacy models (not in current Token Plan)</summary>

For models not in current plan (Speech 2.6/02, Hailuo-02, music-2.5+/2.0, image-01-live, lyrics_generation) see:
[`archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh`](archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh)
</details>

---

## App Examples: Web Search Agent (Mini-Agent)

Directory [`app_examples/mini_agent_websearch/`](app_examples/mini_agent_websearch/) — example **interface to the same pipeline**: [Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent) framework, MiniMax LLM via Anthropic-compatible API and [minimax_search](https://github.com/MiniMax-AI/minimax_search) MCP server (web search). Dependencies installed separately from root `requirements.txt`:

```bash
pip install -r app_examples/requirements-mini-agent.txt
```

Details, `.env` variables, CLI and Telegram bot — in [`app_examples/mini_agent_websearch/README.md`](app_examples/mini_agent_websearch/README.md).

| Component | Purpose |
|-----------|---------|
| [`websearch_agent.py`](app_examples/mini_agent_websearch/websearch_agent.py) | Load config, MCP, single `Agent.run()` call |
| [`run_websearch_bot.py`](app_examples/mini_agent_websearch/run_websearch_bot.py) | CLI: single query from arguments |
| [`telegram_agent_bot.py`](app_examples/mini_agent_websearch/telegram_agent_bot.py) | Telegram: user text → same `run_query` |
| [`config/config-example.yaml`](app_examples/mini_agent_websearch/config/config-example.yaml) | Trimmed toolset (MCP only), model as in `01_text_anthropic.py` |
| [`config/mcp-example.json`](app_examples/mini_agent_websearch/config/mcp-example.json) | Launch `minimax_search` via `uvx` |

### Documentation Sources

- **[Mini-Agent in MiniMax docs](https://platform.minimax.io/docs/solutions/mini-agent)** — agent loop description, `config.yaml` config roles, MCP enabling and `mcp.json` specifying, install via `uv` / `uv sync`, run `python -m mini_agent.cli`.
- **[MiniMax-AI/Mini-Agent repo](https://github.com/MiniMax-AI/Mini-Agent):**
  - config structure and fields — based on [`mini_agent/config/config-example.yaml`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/config-example.yaml) (disabled file/bash/note/skills in our example, MCP only);
  - MCP fragment — based on [`mini_agent/config/mcp-example.json`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/mcp-example.json) (`minimax_search` server, `uvx`, `git+https://github.com/MiniMax-AI/minimax_search`);
  - "raise config, assemble tools, create `Agent`, call `run()`" scenario — inspired by [`examples/04_full_agent.py`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/examples/04_full_agent.py) (`LLMClient`, `load_mcp_tools_async`, `cleanup_mcp_connections`).
- **[MiniMax-AI/minimax_search repo](https://github.com/MiniMax-AI/minimax_search)** — `search` / `browse` tools and required env vars (`SERPER_API_KEY`, for page reading — `JINA_API_KEY`, for LLM on browse — `MINIMAX_API_KEY`).

MiniMax docs index: [llms.txt](https://platform.minimax.io/docs/llms.txt).

---

## Documentation

- [Models overview](https://platform.minimax.io/docs/guides/models-intro)
- [Token Plan](https://platform.minimax.io/docs/token-plan/intro)
- Full index: [llms.txt](https://platform.minimax.io/docs/llms.txt)

---

## Русский / Russian

Минимальные примеры вызова [MiniMax API](https://platform.minimax.io/docs/guides/models-intro): **bash** (`examples/*.sh`) и зеркало на **Python** ([`examples_python/`](examples_python/)) с общим модулем [`examples_python/minimax_http.py`](examples_python/minimax_http.py) (`httpx`). Текст — через Anthropic-совместимый шлюз.

### Реферальная ссылка

Если вы решите оформить подписку, мне будет приятно, если вы воспользуетесь [моей реферальной ссылкой](https://platform.minimax.io/subscribe/token-plan?code=KBrJm5Rkwj&source=link).
По условиям MiniMax: **вам** — скидка **10%** на подписку и статус dev ambassador; **мне** — **10%** обратно **ваучером на API**.

### Подготовка

1. Скопируйте `.env.example` в `.env` и укажите `MINIMAX_API_KEY` ([ключ в кабинете](https://platform.minimax.io/user-center/basic-information/interface-key))
2. `pip install -r requirements.txt` (`anthropic`, `httpx`)
3. Для shell-примеров: `bash`, `curl`, `python3`
4. Python-скрипты при запуске из корня репозитория подхватывают корневой `.env` через [`examples_python/_env.py`](examples_python/_env.py)

### Модели Token Plan

| Модель | Идентификатор | Описание |
|--------|--------------|----------|
| M2.7 / M2.7-highspeed | MiniMax-M2.7 | Text chat (highspeed — отдельная High-Speed подписка) |
| Speech 2.8 | speech-2.8-hd | TTS |
| Video | MiniMax-Hailuo-2.3, MiniMax-Hailuo-2.3-Fast | T2V / I2V |
| Music | music-2.5 | Music generation |
| Image | image-01 | Text-to-image |

**M2.7-highspeed** — высокоскоростной инференс, доступен только на High-Speed планах. Standard-планы включают только M2.7.

Лимиты вашего Token Plan — в [`config/token_plan_limits.yaml`](config/token_plan_limits.yaml).

### Примеры (bash)

| Файл | Что делает |
|------|------------|
| [`examples/02_speech_t2a_sync.sh`](examples/02_speech_t2a_sync.sh) | Синхронный TTS `POST /v1/t2a_v2` → `out/t2a_sync.mp3` |
| [`examples/03_speech_t2a_async.sh`](examples/03_speech_t2a_async.sh) | Async TTS: create → query → `GET /v1/files/retrieve` → URL в консоль |
| [`examples/04_video_t2v.sh`](examples/04_video_t2v.sh) | Text-to-video, печатает `task_id` |
| [`examples/05_video_i2v.sh`](examples/05_video_i2v.sh) | Image-to-video (`MiniMax-Hailuo-2.3-Fast`), печатает `task_id` |
| [`examples/06_video_poll.sh`](examples/06_video_poll.sh) | Опрос `GET /v1/query/video_generation`, при успехе — скачивание по `download_url` |
| [`examples/07_music_generation.sh`](examples/07_music_generation.sh) | `POST /v1/music_generation` (опционально `MINIMAX_RAW_JSON=1`) |
| [`examples/09_image_t2i.sh`](examples/09_image_t2i.sh) | Text-to-image `image-01` |

### Примеры (Python)

| Файл | Что делает |
|------|------------|
| [`examples_python/01_text_anthropic.py`](examples_python/01_text_anthropic.py) | Чат `MiniMax-M2.7` через [Anthropic-compatible API](https://platform.minimax.io/docs/api-reference/text-anthropic-api) |
| [`examples_python/02_speech_t2a_sync.py`](examples_python/02_speech_t2a_sync.py) | Синхронный TTS → `out/t2a_sync.mp3` |
| [`examples_python/03_speech_t2a_async.py`](examples_python/03_speech_t2a_async.py) | Async TTS → URL |
| [`examples_python/04_video_t2v.py`](examples_python/04_video_t2v.py) | Text-to-video → `task_id` |
| [`examples_python/05_video_i2v.py`](examples_python/05_video_i2v.py) | Image-to-video → `task_id` |
| [`examples_python/06_video_poll.py`](examples_python/06_video_poll.py) | Опрос видео и скачивание в `out/` |
| [`examples_python/07_music_generation.py`](examples_python/07_music_generation.py) | `MINIMAX_RAW_JSON=1` — одна строка JSON |
| [`examples_python/07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) | Длинный текст: несколько `POST /v1/music_generation`, опционально `ffmpeg` → один mp3 |
| [`examples_python/09_image_t2i.py`](examples_python/09_image_t2i.py) | Text-to-image |

### Быстрый запуск

Запуск одного примера из корня репозитория:

```bash
bash examples/02_speech_t2a_sync.sh
python3 examples_python/01_text_anthropic.py
python3 examples_python/02_speech_t2a_sync.py
```

(`chmod +x examples/*.sh` при желании вызывать `./examples/...`.)

Для видео: `python3 examples_python/04_video_t2v.py`, затем `TASK_ID=... python3 examples_python/06_video_poll.py`.

**Длинные тексты под музыку.** В [доке MiniMax](https://platform.minimax.io/docs/api-reference/music-generation) у поля `lyrics` есть лимит длины (для **Music-2.5** в Token Plan — до **3500** символов). Отдельного параметра «продолжить предыдущий аудиофайл» в Music Generation **нет**. Чтобы озвучить весь ваш текст, скрипт [`07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) режет размеченный файл на части и вызывает API несколько раз; при наличии `ffmpeg` можно собрать `music_<model>_all.mp3`:

```bash
PYTHONPATH=examples_python python3 examples_python/07_music_from_lyrics_file.py my_liryc_tagged.txt --model music-2.5 --concat
```

### Прогон всех моделей Token Plan

Скрипт [`scripts/run_token_plan_models.sh`](scripts/run_token_plan_models.sh) по очереди вызывает:

- Text: MiniMax-M2.7
- Speech 2.8: hd (sync + async)
- Video: Hailuo-2.3 T2V, Hailuo-2.3-Fast I2V
- Music: music-2.5
- Image: image-01

```bash
WARNING_READED=1 bash scripts/run_token_plan_models.sh
# быстрее (без видео и без async TTS):
WARNING_READED=1 SKIP_VIDEO=1 SKIP_ASYNC_SPEECH=1 bash scripts/run_token_plan_models.sh
```

**Предупреждение о квоте.** При первом запуске скрипт не выполняет прогон: печатает предупреждение и выходит с кодом 1. Полный прогон заметно расходует дневные/оконные квоты Token Plan. Чтобы явно согласиться и продолжить, задайте **`WARNING_READED=1`** в окружении или добавьте ту же строку в `.env`.

У скриптов `07`, `09` при `MINIMAX_RAW_JSON=1` на stdout уходит одна строка JSON (удобно для пайпов); раннер выставляет её сам.

Каждый пример сам пишет артефакты в `out/` (stderr: строка `Wrote …`): **02** mp3, **03** async mp3 по `download_url`, **04/05** `last_video_task_id.txt`, **06** mp4, **07** `music_<model>.mp3`, **09** `image_t2i_*.jpeg`. **01** (Python): `last_text_reply.txt`. Раннер только кратко суммирует stdout; дублирования записи нет.

<details>
<summary>Архивные модели (не в Token Plan)</summary>

Для моделей не из текущего плана (Speech 2.6/02, Hailuo-02, music-2.5+/2.0, image-01-live, lyrics_generation) см.:
[`archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh`](archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh)
</details>

### Агент с веб-поиском (Mini-Agent)

Каталог [`app_examples/mini_agent_websearch/`](app_examples/mini_agent_websearch/) — пример **интерфейса к одному и тому же пайплайну**: фреймворк [Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent), LLM MiniMax через Anthropic-совместимый API и MCP-сервер [minimax_search](https://github.com/MiniMax-AI/minimax_search) (поиск в интернете). Зависимости ставятся отдельно от корневого `requirements.txt`:

```bash
pip install -r app_examples/requirements-mini-agent.txt
```

Подробные шаги, переменные `.env`, CLI и Telegram-бот — в [`app_examples/mini_agent_websearch/README.md`](app_examples/mini_agent_websearch/README.md).

| Компонент | Назначение |
|-----------|-----------|
| [`websearch_agent.py`](app_examples/mini_agent_websearch/websearch_agent.py) | Загрузка конфига, MCP, один вызов `Agent.run()` |
| [`run_websearch_bot.py`](app_examples/mini_agent_websearch/run_websearch_bot.py) | CLI: один запрос из аргументов |
| [`telegram_agent_bot.py`](app_examples/mini_agent_websearch/telegram_agent_bot.py) | Telegram: текст пользователя → тот же `run_query` |
| [`config/config-example.yaml`](app_examples/mini_agent_websearch/config/config-example.yaml) | Урезанный набор инструментов (только MCP), модель как в `01_text_anthropic.py` |
| [`config/mcp-example.json`](app_examples/mini_agent_websearch/config/mcp-example.json) | Запуск `minimax_search` через `uvx` |

### Источники в документации и примерах

- **[Mini-Agent в документации MiniMax](https://platform.minimax.io/docs/solutions/mini-agent)** — описание цикла агента (восприятие → рассуждение → действие → обратная связь), роли конфигурации `config.yaml`, включение MCP и указание `mcp.json`, установка через `uv` / `uv sync`, запуск `python -m mini_agent.cli`.
- **Репозиторий [MiniMax-AI/Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent)** (исходники фреймворка):
  - структура и поля конфига — по образцу [`mini_agent/config/config-example.yaml`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/config-example.yaml) (в нашем примере отключены file/bash/note/skills, оставлен только MCP);
  - фрагмент MCP — по [`mini_agent/config/mcp-example.json`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/mcp-example.json) (сервер `minimax_search`, `uvx`, `git+https://github.com/MiniMax-AI/minimax_search`);
  - сценарий «поднять конфиг, собрать инструменты, создать `Agent`, вызвать `run()`» — по духу примера [`examples/04_full_agent.py`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/examples/04_full_agent.py) (`LLMClient`, `load_mcp_tools_async`, `cleanup_mcp_connections`).
- **Репозиторий [MiniMax-AI/minimax_search](https://github.com/MiniMax-AI/minimax_search)** — описание инструментов `search` / `browse` и обязательных переменных окружения (`SERPER_API_KEY`, для чтения страниц — `JINA_API_KEY`, для LLM при browse — `MINIMAX_API_KEY`), как в их README.

Индекс страниц доки MiniMax: [llms.txt](https://platform.minimax.io/docs/llms.txt).

### Документация

- [Models overview](https://platform.minimax.io/docs/guides/models-intro)
- [Token Plan](https://platform.minimax.io/docs/token-plan/intro)
- Полный индекс: [llms.txt](https://platform.minimax.io/docs/llms.txt)

---

## 中文 / Chinese

[MiniMax API](https://platform.minimax.io/docs/guides/models-intro) 的最小化调用示例：**bash** (`examples/*.sh`) 和 **Python** 版本 ([`examples_python/`](examples_python/))，共享模块 [`examples_python/minimax_http.py`](examples_python/minimax_http.py) (`httpx`)。文本通过 Anthropic 兼容网关。

### 推荐链接

如果您决定订阅，请使用[我的推荐链接](https://platform.minimax.io/subscribe/token-plan?code=KBrJm5Rkwj&source=link)。
MiniMax 条款：您享受 **10%** 订阅折扣和 dev ambassador 身份；我获得 **10%** API 代金券返还。

### 设置

1. 复制 `.env.example` → `.env` 并设置 `MINIMAX_API_KEY`（[在此获取](https://platform.minimax.io/user-center/basic-information/interface-key)）
2. `pip install -r requirements.txt`（`anthropic`、`httpx`）
3. Shell 示例需要：`bash`、`curl`、`python3`
4. Python 脚本从仓库根目录运行，通过 [`examples_python/_env.py`](examples_python/_env.py) 加载根目录 `.env`

### Token Plan 模型

| 模型 | 标识符 | 描述 |
|------|--------|------|
| M2.7 / M2.7-highspeed | MiniMax-M2.7 | 文本聊天（highspeed — 独立 High-Speed 订阅） |
| Speech 2.8 | speech-2.8-hd | TTS |
| Video | MiniMax-Hailuo-2.3, MiniMax-Hailuo-2.3-Fast | T2V / I2V |
| Music | music-2.5 | 音乐生成 |
| Image | image-01 | 文本生成图像 |

**M2.7-highspeed** — 高速推理，仅在 High-Speed 套餐中可用。标准套餐仅包含 M2.7。

您的 Token Plan 限制 — 见 [`config/token_plan_limits.yaml`](config/token_plan_limits.yaml)。

### Bash 示例

| 文件 | 功能 |
|------|------|
| [`examples/02_speech_t2a_sync.sh`](examples/02_speech_t2a_sync.sh) | 同步 TTS `POST /v1/t2a_v2` → `out/t2a_sync.mp3` |
| [`examples/03_speech_t2a_async.sh`](examples/03_speech_t2a_async.sh) | 异步 TTS：create → query → `GET /v1/files/retrieve` → URL 输出到控制台 |
| [`examples/04_video_t2v.sh`](examples/04_video_t2v.sh) | 文本生成视频，输出 `task_id` |
| [`examples/05_video_i2v.sh`](examples/05_video_i2v.sh) | 图像生成视频（`MiniMax-Hailuo-2.3-Fast`），输出 `task_id` |
| [`examples/06_video_poll.sh`](examples/06_video_poll.sh) | 轮询 `GET /v1/query/video_generation`，成功则通过 `download_url` 下载 |
| [`examples/07_music_generation.sh`](examples/07_music_generation.sh) | `POST /v1/music_generation`（可选 `MINIMAX_RAW_JSON=1`） |
| [`examples/09_image_t2i.sh`](examples/09_image_t2i.sh) | 文本生成图像 `image-01` |

### Python 示例

| 文件 | 功能 |
|------|------|
| [`examples_python/01_text_anthropic.py`](examples_python/01_text_anthropic.py) | 通过 [Anthropic 兼容 API](https://platform.minimax.io/docs/api-reference/text-anthropic-api) 使用 `MiniMax-M2.7` 聊天 |
| [`examples_python/02_speech_t2a_sync.py`](examples_python/02_speech_t2a_sync.py) | 同步 TTS → `out/t2a_sync.mp3` |
| [`examples_python/03_speech_t2a_async.py`](examples_python/03_speech_t2a_async.py) | 异步 TTS → URL |
| [`examples_python/04_video_t2v.py`](examples_python/04_video_t2v.py) | 文本生成视频 → `task_id` |
| [`examples_python/05_video_i2v.py`](examples_python/05_video_i2v.py) | 图像生成视频 → `task_id` |
| [`examples_python/06_video_poll.py`](examples_python/06_video_poll.py) | 轮询视频并下载到 `out/` |
| [`examples_python/07_music_generation.py`](examples_python/07_music_generation.py) | `MINIMAX_RAW_JSON=1` — 单行 JSON |
| [`examples_python/07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) | 长文本：多次 `POST /v1/music_generation`，可选 `ffmpeg` → 一个 mp3 |
| [`examples_python/09_image_t2i.py`](examples_python/09_image_t2i.py) | 文本生成图像 |

### 快速开始

从仓库根目录运行单个示例：

```bash
bash examples/02_speech_t2a_sync.sh
python3 examples_python/01_text_anthropic.py
python3 examples_python/02_speech_t2a_sync.py
```

（如需调用 `./examples/...`，请 `chmod +x examples/*.sh`）

视频处理：先运行 `python3 examples_python/04_video_t2v.py`，然后 `TASK_ID=... python3 examples_python/06_video_poll.py`。

**长歌词。** 根据 [MiniMax 文档](https://platform.minimax.io/docs/api-reference/music-generation)，`lyrics` 字段有长度限制（**Music-2.5** 在 Token Plan 中最多 **3500** 字符）。Music Generation **没有**「继续上一个音频」参数。脚本 [`07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) 可将带标签的文件分割成多个部分并多次调用 API；如果有 `ffmpeg` 可以合并为 `music_<model>_all.mp3`：

```bash
PYTHONPATH=examples_python python3 examples_python/07_music_from_lyrics_file.py my_liryc_tagged.txt --model music-2.5 --concat
```

### 运行所有 Token Plan 模型

脚本 [`scripts/run_token_plan_models.sh`](scripts/run_token_plan_models.sh) 按顺序调用：

- 文本：MiniMax-M2.7
- 语音 2.8：hd（同步 + 异步）
- 视频：Hailuo-2.3 T2V、Hailuo-2.3-Fast I2V
- 音乐：music-2.5
- 图像：image-01

```bash
WARNING_READED=1 bash scripts/run_token_plan_models.sh
# 更快（无视频和无异步 TTS）：
WARNING_READED=1 SKIP_VIDEO=1 SKIP_ASYNC_SPEECH=1 bash scripts/run_token_plan_models.sh
```

**配额警告。** 首次运行时，脚本会打印警告并以代码 1 退出。完整运行会显著消耗 Token Plan 的每日/窗口配额——建议分批运行示例。如需继续，请设置 **`WARNING_READED=1`** 环境变量或将其添加到 `.env`。

脚本 `07`、`09` 设置 `MINIMAX_RAW_JSON=1` 时输出单行 JSON 到 stdout（便于管道传递）；运行器自行设置。

每个示例将产物写入 `out/`（stderr：`Wrote …` 行）：**02** mp3、**03** 通过 `download_url` 下载的异步 mp3、**04/05** `last_video_task_id.txt`、**06** mp4、**07** `music_<model>.mp3`、`09` `image_t2i_*.jpeg`。**01**（Python）：`last_text_reply.txt`。运行器仅简要汇总 stdout；无重复写入。

<details>
<summary>旧版模型（不在当前 Token Plan 中）</summary>

对于不在当前计划中的模型（Speech 2.6/02、Hailuo-02、music-2.5+/2.0、image-01-live、lyrics_generation），参见：
[`archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh`](archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh)
</details>

### 网络搜索智能体 (Mini-Agent)

目录 [`app_examples/mini_agent_websearch/`](app_examples/mini_agent_websearch/) — 同一流程的接口示例：[Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent) 框架，通过 Anthropic 兼容 API 调用 MiniMax LLM，以及 [minimax_search](https://github.com/MiniMax-AI/minimax_search) MCP 服务器（网络搜索）。依赖项与根目录 `requirements.txt` 分开安装：

```bash
pip install -r app_examples/requirements-mini-agent.txt
```

详细步骤、`.env` 变量、CLI 和 Telegram 机器人 — 见 [`app_examples/mini_agent_websearch/README.md`](app_examples/mini_agent_websearch/README.md)。

| 组件 | 用途 |
|------|------|
| [`websearch_agent.py`](app_examples/mini_agent_websearch/websearch_agent.py) | 加载配置、MCP，单次 `Agent.run()` 调用 |
| [`run_websearch_bot.py`](app_examples/mini_agent_websearch/run_websearch_bot.py) | CLI：从参数获取单个查询 |
| [`telegram_agent_bot.py`](app_examples/mini_agent_websearch/telegram_agent_bot.py) | Telegram：用户文本 → 相同的 `run_query` |
| [`config/config-example.yaml`](app_examples/mini_agent_websearch/config/config-example.yaml) | 精简工具集（仅 MCP），模型同 `01_text_anthropic.py` |
| [`config/mcp-example.json`](app_examples/mini_agent_websearch/config/mcp-example.json) | 通过 `uvx` 启动 `minimax_search` |

### 文档来源

- **[MiniMax 文档中的 Mini-Agent](https://platform.minimax.io/docs/solutions/mini-agent)** — 智能体循环描述、`config.yaml` 配置角色、MCP 启用和 `mcp.json` 指定、通过 `uv` / `uv sync` 安装、运行 `python -m mini_agent.cli`。
- **[MiniMax-AI/Mini-Agent 仓库](https://github.com/MiniMax-AI/Mini-Agent)：**
  - 配置结构和字段 — 基于 [`mini_agent/config/config-example.yaml`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/config-example.yaml)（本例中禁用了 file/bash/note/skills，仅保留 MCP）；
  - MCP 片段 — 基于 [`mini_agent/config/mcp-example.json`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/mcp-example.json)（`minimax_search` 服务器、`uvx`、`git+https://github.com/MiniMax-AI/minimax_search`）；
  -「提升配置、组装工具、创建 `Agent`、调用 `run()`」场景 — 灵感来自 [`examples/04_full_agent.py`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/examples/04_full_agent.py)（`LLMClient`、`load_mcp_tools_async`、`cleanup_mcp_connections`）。
- **[MiniMax-AI/minimax_search 仓库](https://github.com/MiniMax-AI/minimax_search)** — `search` / `browse` 工具及必需的环境变量（`SERPER_API_KEY`、页面读取用 `JINA_API_KEY`、browse 时 LLM 用 `MINIMAX_API_KEY`）。

MiniMax 文档索引：[llms.txt](https://platform.minimax.io/docs/llms.txt)。

### 文档

- [模型概览](https://platform.minimax.io/docs/guides/models-intro)
- [Token Plan](https://platform.minimax.io/docs/token-plan/intro)
- 完整索引：[llms.txt](https://platform.minimax.io/docs/llms.txt)
