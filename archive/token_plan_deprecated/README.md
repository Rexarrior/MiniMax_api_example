# Архив: примеры под модели вне текущего Token Plan

По [Token Plan Overview](https://platform.minimax.io/docs/token-plan/intro) в подписке перечислены квоты на:

- **Speech 2.8** (не Speech 2.6 / Speech 02);
- **Hailuo-2.3** и **Hailuo-2.3-Fast** (768P 6s), без отдельной строки для **Hailuo-02**;
- **Music-2.5** (без **Music-2.0** / **Music-2.5+** в таблице плана);
- **image-01** (без **image-01-live** в таблице плана).

Сами API-модели могут оставаться в общей [сводке моделей](https://platform.minimax.io/docs/guides/models-intro); здесь отложены **примеры репозитория**, которые ориентировались на идентификаторы, не входящие в актуальную таблицу Token Plan.

| Что в архиве | Зачем |
|--------------|--------|
| [`examples/08_lyrics_generation.sh`](examples/08_lyrics_generation.sh), [`examples_python/08_lyrics_generation.py`](examples_python/08_lyrics_generation.py) | `POST /v1/lyrics_generation` — не входит в Token Plan. |
| [`examples/10_image_i2i.sh`](examples/10_image_i2i.sh), [`examples_python/10_image_i2i.py`](examples_python/10_image_i2i.py) | Image-to-image с `image-01-live`. |
| [`examples/07_music_generation_music-2.5plus_instrumental.sh`](examples/07_music_generation_music-2.5plus_instrumental.sh), [`examples_python/07_music_generation_music-2.5plus.py`](examples_python/07_music_generation_music-2.5plus.py) | Старая ветка `music-2.5+` + `INSTRUMENTAL` / `is_instrumental` (в корневых `examples/07_*` остался только **Music-2.5** с текстом). |
| [`scripts/run_legacy_token_plan_extras.sh`](scripts/run_legacy_token_plan_extras.sh) | Прогон TTS (6 моделей), видео Hailuo-02, музыка `music-2.5+` / `music-2.0`, I2I, lyrics — для ключа **pay-as-you-go** или когда модели снова попадут в план. |

Для **music-2.0** лимит `lyrics` короче (~3000 символов); в активном [`07_music_from_lyrics_file.py`](../../examples_python/07_music_from_lyrics_file.py) задан дефолт под **music-2.5** — для 2.0 задайте `MAX_LYRICS_CHARS=2950` при ручном `--model music-2.0` (pay-as-you-go).

Запуск устаревшего прогона из корня репозитория:

```bash
WARNING_READED=1 bash archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh
```

Актуальные примеры под Token Plan — в корневых `examples/`, `examples_python/` и `scripts/run_token_plan_models.sh`.
