# minimax_explore

> **Реферальная ссылка на Token Plan**  
> Если вы решите оформить подписку, мне будет приятно, если вы воспользуетесь [моей реферальной ссылкой](https://platform.minimax.io/subscribe/token-plan?code=KBrJm5Rkwj&source=link).  
> По условиям MiniMax: **вам** — скидка **10%** на подписку и статус dev ambassador (в т.ч. dev community); **мне** — **10%** обратно **ваучером на API** за каждую успешную оплаченную реферальную подписку (на все модели), плюс приоритетный доступ к мероприятиям и превью моделей. Текст условий и детали — на стороне MiniMax при оформлении.

Минимальные примеры вызова [MiniMax API](https://platform.minimax.io/docs/guides/models-intro): **bash** (`examples/*.sh`) и зеркало на **Python** ([`examples_python/`](examples_python/)) с общим модулем [`examples_python/minimax_http.py`](examples_python/minimax_http.py) (`httpx`). Текст — через Anthropic-совместимый шлюз.

## Подготовка

1. Скопируйте `.env.example` в `.env` и укажите `MINIMAX_API_KEY` ([ключ в кабинете](https://platform.minimax.io/user-center/basic-information/interface-key)).
2. `pip install -r requirements.txt` (`anthropic`, `httpx`).
3. Для shell-примеров: `bash`, `curl`, `python3` (в скриптах для JSON/hex).
4. Python-скрипты при запуске из корня репозитория подхватывают корневой `.env` через [`examples_python/_env.py`](examples_python/_env.py) (переменные, которых ещё нет в окружении).

Лимиты вашего **Token Plan** — в [`config/token_plan_limits.yaml`](config/token_plan_limits.yaml) (справочник, скрипты его не читают).

В публичном индексе документации MiniMax отдельного API **транскрипции речи (speech-to-text)** не видно — примера STT здесь нет.

## Примеры (bash)

| Файл | Что делает |
|------|------------|
| [`examples/02_speech_t2a_sync.sh`](examples/02_speech_t2a_sync.sh) | Синхронный TTS `POST /v1/t2a_v2` → `out/t2a_sync.mp3` |
| [`examples/03_speech_t2a_async.sh`](examples/03_speech_t2a_async.sh) | Async TTS: create → query → `GET /v1/files/retrieve` → URL в консоль |
| [`examples/04_video_t2v.sh`](examples/04_video_t2v.sh) | Text-to-video, печатает `task_id` |
| [`examples/05_video_i2v.sh`](examples/05_video_i2v.sh) | Image-to-video (`MiniMax-Hailuo-2.3-Fast`), печатает `task_id` |
| [`examples/06_video_poll.sh`](examples/06_video_poll.sh) | Опрос `GET /v1/query/video_generation`, при успехе — скачивание по `download_url` |
| [`examples/07_music_generation.sh`](examples/07_music_generation.sh) | `POST /v1/music_generation` (опционально `MINIMAX_RAW_JSON=1`) |
| [`examples/08_lyrics_generation.sh`](examples/08_lyrics_generation.sh) | `POST /v1/lyrics_generation` |
| [`examples/09_image_t2i.sh`](examples/09_image_t2i.sh) | Text-to-image `image-01` |

Пример **image-to-image** (`image-01-live`) вынесен в [`archive/token_plan_deprecated/`](archive/token_plan_deprecated/README.md) — в [таблице Token Plan](https://platform.minimax.io/docs/token-plan/intro) для картинок указан только **image-01**.

## Примеры (Python)

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
| [`examples_python/08_lyrics_generation.py`](examples_python/08_lyrics_generation.py) | Генерация текста песни |
| [`examples_python/09_image_t2i.py`](examples_python/09_image_t2i.py) | Text-to-image |

Image-to-image — в [`archive/token_plan_deprecated/examples_python/10_image_i2i.py`](archive/token_plan_deprecated/examples_python/10_image_i2i.py) (см. [архив](archive/token_plan_deprecated/README.md)).

Запуск из корня репозитория:

```bash
bash examples/02_speech_t2a_sync.sh
python3 examples_python/01_text_anthropic.py
python3 examples_python/02_speech_t2a_sync.py
```

(`chmod +x examples/*.sh` при желании вызывать `./examples/...`.)

Для видео: `python3 examples_python/04_video_t2v.py`, затем `TASK_ID=... python3 examples_python/06_video_poll.py`.

**Длинные тексты под музыку.** В [доке MiniMax](https://platform.minimax.io/docs/api-reference/music-generation) у поля `lyrics` есть лимит длины (для **Music-2.5** в Token Plan — до **3500** символов; у других идентификаторов см. доку). Отдельного параметра «продолжить предыдущий аудиофайл» в Music Generation **нет**; «продолжение» в смысле текста относится к [`/v1/lyrics_generation`](https://platform.minimax.io/docs/api-reference/lyrics-generation) (`mode: edit`). Чтобы озвучить весь ваш текст, скрипт [`07_music_from_lyrics_file.py`](examples_python/07_music_from_lyrics_file.py) режет размеченный файл на части и вызывает API несколько раз; при наличии `ffmpeg` можно собрать `music_<model>_all.mp3`:

```bash
PYTHONPATH=examples_python python3 examples_python/07_music_from_lyrics_file.py my_liryc_tagged.txt --model music-2.5 --concat
```

## App examples: агент с веб-поиском (Mini-Agent)

В каталоге [`app_examples/mini_agent_websearch/`](app_examples/mini_agent_websearch/) — пример **интерфейса к одному и тому же пайплайну**: фреймворк [Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent), LLM MiniMax через Anthropic-совместимый API и MCP-сервер [minimax_search](https://github.com/MiniMax-AI/minimax_search) (поиск в интернете). Отдельно от корневого `requirements.txt` ставятся зависимости:

```bash
pip install -r app_examples/requirements-mini-agent.txt
```

Подробные шаги, переменные `.env`, CLI и Telegram-бот — в [`app_examples/mini_agent_websearch/README.md`](app_examples/mini_agent_websearch/README.md).

| Компонент | Назначение |
|-----------|------------|
| [`websearch_agent.py`](app_examples/mini_agent_websearch/websearch_agent.py) | Загрузка конфига, MCP, один вызов `Agent.run()` |
| [`run_websearch_bot.py`](app_examples/mini_agent_websearch/run_websearch_bot.py) | CLI: один запрос из аргументов |
| [`telegram_agent_bot.py`](app_examples/mini_agent_websearch/telegram_agent_bot.py) | Telegram: текст пользователя → тот же `run_query` |
| [`config/config-example.yaml`](app_examples/mini_agent_websearch/config/config-example.yaml) | Урезанный набор инструментов (только MCP), модель как в `01_text_anthropic.py` |
| [`config/mcp-example.json`](app_examples/mini_agent_websearch/config/mcp-example.json) | Запуск `minimax_search` через `uvx` |

### Откуда взято в документации и примерах

- **[Mini-Agent в документации MiniMax](https://platform.minimax.io/docs/solutions/mini-agent)** — описание цикла агента (восприятие → рассуждение → действие → обратная связь), роли конфигурации `config.yaml`, включение MCP и указание `mcp.json`, установка через `uv` / `uv sync`, запуск `python -m mini_agent.cli`. Отсюда же согласована идея: провайдер `anthropic`, `api_base` для глобального endpoint MiniMax, отдельный файл с системным промптом.
- **Репозиторий [MiniMax-AI/Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent)** (исходники фреймворка):
  - структура и поля конфига — по образцу [`mini_agent/config/config-example.yaml`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/config-example.yaml) (в нашем примере отключены file/bash/note/skills, оставлен только MCP);
  - фрагмент MCP — по [`mini_agent/config/mcp-example.json`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/mini_agent/config/mcp-example.json) (сервер `minimax_search`, `uvx`, `git+https://github.com/MiniMax-AI/minimax_search`);
  - сценарий «поднять конфиг, собрать инструменты, создать `Agent`, вызвать `run()`» — по духу примера [`examples/04_full_agent.py`](https://github.com/MiniMax-AI/Mini-Agent/blob/main/examples/04_full_agent.py) (`LLMClient`, `load_mcp_tools_async`, `cleanup_mcp_connections`).
- **Репозиторий [MiniMax-AI/minimax_search](https://github.com/MiniMax-AI/minimax_search)** — описание инструментов `search` / `browse` и обязательных переменных окружения (`SERPER_API_KEY`, для чтения страниц — `JINA_API_KEY`, для LLM при browse — `MINIMAX_API_KEY`), как в их README.

Индекс страниц доки MiniMax: [llms.txt](https://platform.minimax.io/docs/llms.txt).

## Прогон всех моделей Token Plan (без STT)

Скрипт [`scripts/run_token_plan_models.sh`](scripts/run_token_plan_models.sh) по очереди вызывает текст, **Speech 2.8** (hd + turbo, sync и при необходимости async), видео из [таблицы Token Plan](https://platform.minimax.io/docs/token-plan/intro) (Hailuo-2.3 T2V, Hailuo-2.3-Fast I2V 768P 6s), **Music-2.5**, lyrics и text-to-image **image-01**. Результаты — в `out/`.

Старые прогоны (Speech 2.6 / 02, **MiniMax-Hailuo-02**, `music-2.5+` / `music-2.0`, **image-01-live**) см. [`archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh`](archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh).

**Предупреждение о квоте.** При первом запуске скрипт не выполняет прогон: печатает предупреждение и выходит с кодом 1. Полный прогон заметно расходует дневные/оконные квоты Token Plan — имеет смысл гонять примеры по частям. Чтобы явно согласиться и продолжить, задайте **`WARNING_READED=1`** в окружении (например, в командной строке) или добавьте ту же строку в `.env`.

```bash
WARNING_READED=1 bash scripts/run_token_plan_models.sh
# быстрее (без долгих видео и без async TTS):
WARNING_READED=1 SKIP_VIDEO=1 SKIP_ASYNC_SPEECH=1 bash scripts/run_token_plan_models.sh
```

У скриптов `07`–`10` при `MINIMAX_RAW_JSON=1` на stdout уходит одна строка JSON (удобно для пайпов); раннер выставляет её сам.

Каждый пример сам пишет артефакты в `out/` (stderr: строка `Wrote …`): **02** mp3, **03** async mp3 по `download_url`, **04/05** `last_video_task_id.txt`, **06** mp4, **07** `music_<model>.mp3`, **08** `lyrics_<slug>.txt`, **09** `image_t2i_*.jpeg`. **01** (Python): `last_text_reply.txt`. Раннер только кратко суммирует stdout; дублирования записи нет.

Ссылки на картинки в JSON протухают (~24 h по доке); локальные jpeg уже сохранены.

## Документация

- [Models overview](https://platform.minimax.io/docs/guides/models-intro)
- Полный индекс: [llms.txt](https://platform.minimax.io/docs/llms.txt)
