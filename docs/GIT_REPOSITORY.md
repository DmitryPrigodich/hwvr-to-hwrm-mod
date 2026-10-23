# Репозитории кода

Разделение от 23 октября 2026: **hwrm-mp-patch → hwrm-hw1-races-reimogined → hwvr-to-hwrm-mod**. [Ответственность и сборка](MOD_LAYERS.md), машинные границы — `mod-layers.json`.

- [hwrm-mp-patch](https://github.com/DmitryPrigodich/hwrm-mp-patch): общие исправления и оригинальные расы; ветка `codex/hwrm-mp-patch`.
- [hwrm-hw1-races-reimogined](https://github.com/DmitryPrigodich/hwrm-hw1-races-reimogined): новые расы, их наука/стройка и баланс; ветка `codex/hwrm-hw1-races-reimogined`.
- [hwvr-to-hwrm-mod](https://github.com/DmitryPrigodich/hwvr-to-hwrm-mod): существующая кампания, ветка `codex/homeworld-vast-reaches`. Название, remote origin и история сохранены.

Зависимости подключаются submodules: второй фиксирует первый в `dependencies/mp-patch`, кампания — второй в `dependencies/hw1-races`. Каждый потребитель также проверяет `dependencies.lock.json`. Новые папки находятся рядом с `Homeworld Vast Reaches`; вложенные зависимости нужны сборкам, а собственные изменения делаются в отдельном репозитории владельца.

После клонирования:

```powershell
git submodule update --init --recursive
```

Проверенное обновление сначала коммитим и отправляем у владельца, затем явно обновляем gitlink и lock потребителя и проверяем его сборку. Самостоятельная сборка общей основы не обновляет кампанию.

В Git входят Python, Lua, определения, карты, локализация и документы. Модели, геометрия, текстуры, изображения, речь/музыка, видео, BIG/ZIP/APK/OBB, EXE/DLL, извлечённые ресурсы, окружения и каталоги local/exports исключены. assets.json второго слоя содержит только пути/хеши восьми локальных ресурсов. Файлы игры не перемещались и не публиковались.

Резерв перед разделением: `local/repository-split/before-split-history.bundle` (вся прежняя история), `before-split-code.zip` и `before-split.json` (код с незакоммиченными правками). Прежние совмещённые каталоги/генераторы сохранены в `local/repository-split/legacy-project`. Прежние ручные заметки о Новотаииданах перенесены без изменения в репозиторий рас. Указатели оставлены по старым документальным путям.

Первый коммит кампании — `51371ed`; состояние перед разделением — `90e1eb61ca4264022b2745eb6d7385d03f8496e1`. История кампании не переписывается. Исходные данные прежней пустой .git по-прежнему лежат в local/git-history-backups и не публикуются.

Кандидат кампании готовится командой `python tools/build_mod_layers.py --package-candidate` в **local/VastReachesLayered-release**. Основной release **9c48be0d…** и установленная игра **e67bd447…** не заменены. Сборка и публикация кода не означают установку или нативную проверку.
