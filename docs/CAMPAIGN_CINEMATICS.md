# Ролики HWVR — подготовка к переносу

Подготовлены12исходных сцен: общий пролог, десять других вступлений и финал;24RU/EN WebM и отдельная штатная речь. Пролог и начало обучения подтверждены пользователем. Остальные сцены не считаются проверенными в игре. Текущая реализация — [речь и портреты](CAMPAIGN_SPEECH.md), статус установки — [оглавление](CAMPAIGN_README.md). Ниже — справочник исходных пакетов.

Для каждой сцены: оригинальные изображения, речевые WAV, музыка/окружение WEM и WAV, новый RU и EN SRT, голосовой референс по исходным таймингам, сценические привязки, материалы панорам, переходы/сигналы и SHA256. У общего пролога сохранён прежний формат пакета.

| Сцена | Длительность | Реплик | Изображений | Файлов музыки/окружения | Пакет |
|---|---:|---:|---:|---:|---|
| T1 — вступление | 2:23.250 | 8 | 27 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/prologue/manifest.json>) |
| M7 — вступление | 1:46.401 | 15 | 14 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M7_intro/manifest.json>) |
| M3 — вступление | 1:15.033 | 13 | 8 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M3_intro/manifest.json>) |
| M4 — вступление | 0:40.767 | 8 | 6 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M4_intro/manifest.json>) |
| M5 — вступление | 1:01.053 | 9 | 9 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M5_intro/manifest.json>) |
| M6 — вступление | 1:07.433 | 10 | 7 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M6_intro/manifest.json>) |
| M9 — вступление | 1:47.350 | 20 | 19 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M9_intro/manifest.json>) |
| M10 — вступление | 1:04.483 | 9 | 7 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M10_intro/manifest.json>) |
| M11 — вступление | 1:01.050 | 10 | 6 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M11_intro/manifest.json>) |
| M8 — вступление | 0:57.083 | 9 | 6 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M8_intro/manifest.json>) |
| M13 — вступление | 1:02.450 | 10 | 7 | 2 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M13_intro/manifest.json>) |
| M13 — финал | 0:58.250 | 4 | 19 | 1 | [Состав](<C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/cinematics/Mission_M13_outro/manifest.json>) |

**Исправлена принадлежность реплик:** сцены M7 и M9 используют один sharedassets30.assets. Ранее 35 клипов попадали в M7, а M9 получала пустой список. Теперь по привязке PlayableDirector разделены 15 клипов M7 и 20 клипов M9. Общее число 125 клипов не изменилось; изменилось распределение по главам.

Четырёхканальное окружение оставлено в исходном виде. Громкости Wwise и момент старта звука относительно перехода сцены пока не восстановлены. Голосовой референс не включает музыку; при наложении голосов фиксированное уменьшение уровня отмечено в manifest.json. Исходные отдельные WAV не изменяются.

В M13-финале ambience-event не задан: это сохранённая исходная конфигурация. Отсутствующую дорожку не заменяли другой. Панорамы и портреты не воспроизводят сами по себе движение кораблей: 3D-постановка, проекция, переходы и финальное сведение ещё требуют работы.

Связь с HWRM: [план подключения перед T1](reference/PROLOGUE_SOURCES.md). Остальные вступления подключать к соответствующей главе через postload, финал — при успешном окончании M13. T1/M4 уже подключены в установленной тройке; остальные вызовы находятся в подготовке полной кампании. Текущий статус — в [отчёте о подключении](CAMPAIGN_SPEECH.md).

Воспроизведение подготовки: `.venv\Scripts\python.exe -X utf8 tools\prepare_campaign_cinematics.py`. Общая сводка — `campaign-export/cinematics/index.json`. Для повторного включения общего пролога в новый формат есть `--include-prologue`; существующий пакет prologue по умолчанию сохраняется.
