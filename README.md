# minimax_explore

> **Реферальная ссылка на Token Plan**  
> Если вы решите оформить подписку, мне будет приятно, если вы воспользуетесь [моей реферальной ссылкой](https://platform.minimax.io/subscribe/token-plan?code=KBrJm5Rkwj&source=link).  
> По условиям MiniMax: **вам** — скидка **10%** на подписку и статус dev ambassador (в т.ч. dev community); **мне** — **10%** обратно **ваучером на API** за каждую успешную оплаченную реферальную подписку (на все модели), плюс приоритетный доступ к мероприятиям и превью моделей. Текст условий и детали — на стороне MiniMax при оформлении.

Минимальные примеры вызова [MiniMax API](https://platform.minimax.io/docs/guides/models-intro) (REST + один пример через Anthropic-совместимый шлюз для текста).

## Подготовка

1. Скопируйте `.env.example` в `.env` и укажите `MINIMAX_API_KEY` ([ключ в кабинете](https://platform.minimax.io/user-center/basic-information/interface-key)).
2. Для текста: `pip install -r requirements.txt`.
3. Для shell-примеров нужны `bash`, `curl`, `python3` (для разбора JSON и декода hex-аудио).

Лимиты вашего **Token Plan** — в [`config/token_plan_limits.yaml`](config/token_plan_limits.yaml) (справочник, скрипты его не читают).

В публичном индексе документации MiniMax отдельного API **транскрипции речи (speech-to-text)** не видно — примера STT здесь нет.

## Примеры

| Файл | Что делает |
|------|------------|
| [`examples/01_text_anthropic.py`](examples/01_text_anthropic.py) | Чат, модель `MiniMax-M2.7` через [Anthropic-compatible API](https://platform.minimax.io/docs/api-reference/text-anthropic-api) |
| [`examples/02_speech_t2a_sync.sh`](examples/02_speech_t2a_sync.sh) | Синхронный TTS `POST /v1/t2a_v2` → `out/t2a_sync.mp3` |
| [`examples/03_speech_t2a_async.sh`](examples/03_speech_t2a_async.sh) | Async TTS: create → query → `GET /v1/files/retrieve` → URL в консоль |
| [`examples/04_video_t2v.sh`](examples/04_video_t2v.sh) | Text-to-video, печатает `task_id` |
| [`examples/05_video_i2v.sh`](examples/05_video_i2v.sh) | Image-to-video (`MiniMax-Hailuo-2.3-Fast`), печатает `task_id` |
| [`examples/06_video_poll.sh`](examples/06_video_poll.sh) | Опрос `GET /v1/query/video_generation`, при успехе — скачивание по `download_url` |
| [`examples/07_music_generation.sh`](examples/07_music_generation.sh) | `POST /v1/music_generation` (опционально `MINIMAX_RAW_JSON=1`) |
| [`examples/08_lyrics_generation.sh`](examples/08_lyrics_generation.sh) | `POST /v1/lyrics_generation` |
| [`examples/09_image_t2i.sh`](examples/09_image_t2i.sh) | Text-to-image `image-01` |
| [`examples/10_image_i2i.sh`](examples/10_image_i2i.sh) | Image-to-image `image-01-live` + референс |

Запуск из корня репозитория:

```bash
bash examples/02_speech_t2a_sync.sh
set -a && source .env && set +a && python3 examples/01_text_anthropic.py
```

(Либо `chmod +x examples/*.sh examples/01_text_anthropic.py` и вызывать `./examples/...`.)

Для видео: сначала `bash examples/04_video_t2v.sh`, затем `TASK_ID=... bash examples/06_video_poll.sh`.

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

После прогона раннер сохраняет в `out/`: `music_<model>.mp3` (из hex в ответе), `lyrics_<title>.txt`, `image_t2i_0.jpeg`, `image_i2i_0.jpeg`. Ссылки на картинки в логе протухают (~24 h по доке); скачивание по URL — это уже OSS, не расход MiniMax inference.

## Документация

- [Models overview](https://platform.minimax.io/docs/guides/models-intro)
- Полный индекс: [llms.txt](https://platform.minimax.io/docs/llms.txt)
