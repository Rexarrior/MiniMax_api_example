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
| [`examples/10_image_i2i.sh`](examples/10_image_i2i.sh) | Image-to-image `image-01-live` + референс |

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
| [`examples_python/08_lyrics_generation.py`](examples_python/08_lyrics_generation.py) | Генерация текста песни |
| [`examples_python/09_image_t2i.py`](examples_python/09_image_t2i.py) | Text-to-image |
| [`examples_python/10_image_i2i.py`](examples_python/10_image_i2i.py) | Image-to-image |

Запуск из корня репозитория:

```bash
bash examples/02_speech_t2a_sync.sh
python3 examples_python/01_text_anthropic.py
python3 examples_python/02_speech_t2a_sync.py
```

(`chmod +x examples/*.sh` при желании вызывать `./examples/...`.)

Для видео: `python3 examples_python/04_video_t2v.py`, затем `TASK_ID=... python3 examples_python/06_video_poll.py`.

## Прогон всех моделей Token Plan (без STT)

Скрипт [`scripts/run_token_plan_models.sh`](scripts/run_token_plan_models.sh) по очереди вызывает текст, все 6 speech-моделей (sync + async), варианты видео из плана (Hailuo 2.3, 02 в разных разрешениях, 2.3-Fast I2V), музыку (`music-2.5+`, `music-2.5`, `music-2.0`), lyrics и оба image-примера. Результаты — в `out/`.

**Предупреждение о квоте.** При первом запуске скрипт не выполняет прогон: печатает предупреждение и выходит с кодом 1. Полный прогон может израсходовать порядка **25 000–30 000** обращений к API по вашей квоте — имеет смысл гонять примеры по частям. Чтобы явно согласиться и продолжить, задайте **`WARNING_READED=1`** в окружении (например, в командной строке) или добавьте ту же строку в `.env`.

Для **MiniMax-Hailuo-02** разрешение **512P** в API допустимо только вместе с **`first_frame_image`** (image-to-video); в раннере для 512P используется `05_video_i2v.sh`, а не text-to-video.

```bash
WARNING_READED=1 bash scripts/run_token_plan_models.sh
# быстрее (без долгих видео и без 6× async TTS):
WARNING_READED=1 SKIP_VIDEO=1 SKIP_ASYNC_SPEECH=1 bash scripts/run_token_plan_models.sh
```

У скриптов `07`–`10` при `MINIMAX_RAW_JSON=1` на stdout уходит одна строка JSON (удобно для пайпов); раннер выставляет её сам.

Каждый пример сам пишет артефакты в `out/` (stderr: строка `Wrote …`): **02** mp3, **03** async mp3 по `download_url`, **04/05** `last_video_task_id.txt`, **06** mp4, **07** `music_<model>.mp3`, **08** `lyrics_<slug>.txt`, **09/10** `image_t2i_*.jpeg` / `image_i2i_*.jpeg`. **01** (Python): `last_text_reply.txt`. Раннер только кратко суммирует stdout; дублирования записи нет.

Ссылки на картинки в JSON протухают (~24 h по доке); локальные jpeg уже сохранены.

## Документация

- [Models overview](https://platform.minimax.io/docs/guides/models-intro)
- Полный индекс: [llms.txt](https://platform.minimax.io/docs/llms.txt)
