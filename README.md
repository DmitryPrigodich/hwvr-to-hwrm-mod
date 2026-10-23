# Vast Reaches → Homeworld Remastered

Рабочий проект кампании Vast Reaches для HWRM. Актуальные материалы — в [оглавлении кампании](docs/CAMPAIGN_README.md).

Для текущей читки:

- [M0. Обучение / Tutorial](docs/missions/T01_Training.md) — пролог, EN/RU, исходные ветви и подготовка миссии.
- [M1. Испытательный полигон](docs/missions/M01_ProvingGrounds.md).
- [Уже внесённые правки перевода](docs/TRANSLATION_REVIEW.md) и [глоссарий](localization/GLOSSARY.md).
- [HTML-сценарий с портретами и исходной озвучкой](campaign-export/index.html#chapter0).

На23октября установлена без запуска **e67bd447…**: M0 без строительства, W-маршрут через A/B, безопасный сброс попытки и усиление Тирры. Точный текущий статус — [NEXT_SESSION.md](NEXT_SESSION.md).

Реализована [трёхуровневая зависимость](docs/MOD_LAYERS.md): **[hwrm-mp-patch](https://github.com/DmitryPrigodich/hwrm-mp-patch) → [hwrm-hw1-races-reimogined](https://github.com/DmitryPrigodich/hwrm-hw1-races-reimogined) → [hwvr-to-hwrm-mod](https://github.com/DmitryPrigodich/hwvr-to-hwrm-mod)**. Основа исправлений, затем новые расы/баланс, затем кампания. Зависимости закреплены submodules и lock-файлами. Отдельный кандидат — `local/VastReachesLayered-release`; основной release и установленная игра не заменены.

Запуск: **Vast Reaches Campaign Demo.cmd → Extra Missions → Vast Reaches Campaign Demo**. Подробности — [запуск мода](docs/LAUNCHER_MOD.md). Перенос флота между главами ещё не реализован; полный экспорт не является готовой кампанией.

Код: [публичный GitHub-репозиторий](https://github.com/DmitryPrigodich/hwvr-to-hwrm-mod). Игровые модели, текстуры, звук, видео и BIG в Git не включаются.

Ранний импорт моделей, сравнения флотов, прежние инструкции и буквальные старые переводы доступны в [архиве и справочных материалах](docs/archive/README.md). Они не описывают текущее состояние кампании.
