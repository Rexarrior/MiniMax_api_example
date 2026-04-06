# AGENTS.md

## Repo structure

Two independent projects in one repo:

| Project | Location | Tech |
|---------|----------|------|
| MiniMax API examples | root, `examples/`, `examples_python/` | Python 3 + bash, `httpx` |
| Roguelike game | `app_examples/roguelike/` | C++17, Raylib 5.5, GoogleTest |

## MiniMax API examples

- **Env**: copy `.env.example` → `.env`, set `MINIMAX_API_KEY`.
- **Python examples**: always run with `PYTHONPATH=examples_python` from repo root.
- **Outputs**: all artifacts go to `out/` (mp3, mp4, jpeg, txt).
- **Image generation**: `examples_python/10_roguelike_assets.py` generates 26 pixel art PNGs → `out/roguelike_assets/`.
- **Quota warning**: `scripts/run_token_plan_models.sh` requires `WARNING_READED=1` to proceed.

## Roguelike game

### Build

Use the provided scripts:
```bash
# Windows
app_examples/roguelike/build.bat

# Linux/macOS
bash app_examples/roguelike/build.sh
```

Or manually:
```bash
cd app_examples/roguelike
cmake -B build -DCMAKE_TOOLCHAIN_FILE=<vcpkg_root>/scripts/buildsystems/vcpkg.cmake
cmake --build build --config Release
```

**vcpkg location on this machine**: `S:\programming\my\vcpkg`

### Running

```bash
# From roguelike dir:
build/Release/roguelike.exe    # Windows
build/roguelike                # Linux/macOS
```

**DLLs on Windows**: `raylib.dll` and `glfw3.dll` must be in `build/Release/` (build scripts copy them automatically).

### Tests

```bash
build/Release/roguelike_tests.exe          # Windows
build/roguelike_tests                      # Linux/macOS
```

88 tests, 14 suites. Tests use `USE_RAYLIB_STUB` to avoid raylib dependency — `tests/raylib_stub.h` provides minimal stub types.

### Rendering

- All game rendering uses `BeginMode2D(camera)` / `EndMode2D()` — **do not** use `GetWorldToScreen2D` for game entities.
- Tile textures are full 1024×1024 images scaled to `TILE_SIZE` via `DrawTexturePro`.
- Entity sprite sheets are 2×2 grids (512×512 per quadrant); extract one quadrant and scale to `TILE_SIZE`.
- `TILE_SIZE = 64`, `MAP_WIDTH = 40`, `MAP_HEIGHT = 25`.

### Assets

Generated pixel art lives in `out/roguelike_assets/`. Game loads them via relative path `../../../../out/roguelike_assets` from `build/Release/`.

### PowerShell Core issue (Windows)

vcpkg downloads PowerShell Core 7.5.4 which fails with CLR error on this machine. Fixed by replacing `pwsh.exe` with PowerShell 7.2.18 in `vcpkg/downloads/tools/powershell-core-7.5.4-windows/`.

## Git

- `build/` is gitignored for roguelike.
- `.env`, `__pycache__/`, `*.pyc` are gitignored.
- Mini-Agent config files (`config.yaml`, `mcp.json`, `workspace/`) are gitignored.
