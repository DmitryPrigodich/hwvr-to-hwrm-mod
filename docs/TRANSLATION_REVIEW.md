# Перевод: внесённые правки

Обновлено 22 октября 2026. Ниже — текущие формулировки после замечаний Дмитрия. Это изменения текста; установка новой сборки учитывается отдельно в [состоянии кампании](CAMPAIGN_README.md).

Название главы: **M0. Обучение / M0. Tutorial**. Внутренний ID `T01_Training` сохранён.

## Формулировка о Дайамиде и одиночестве хиигарян.

`M01_010_030_A_HA`

**RU сейчас:** Таииданская империя пала, но хиигарян, едва вернувшихся домой, застала врасплох короткая и смертоносная война с Тварью. Дайамид, правящий совет Хиигары, болезненно осознавал, насколько хиигаряне одиноки в Галактике. Поэтому предложение Радаа — межзвёздных торговцев, владевших собственными загадочными технологиями, — заключить союз и наладить обмен встретило самый тёплый приём.

*Внесена правка пользователя · 21 октября 2026*

<details><summary>English original</summary>

Though the Taiidani empire had fallen, the new Hiigarans were caught off guard by the short but deadly BeastWar. The Daiamid, the ruling council of the Hiigaran people, were painfully aware that they were alone in the Galaxy. So when the Radaa - interstellar traders with their own mysterious technology - approached with offers of an alliance and exchange, the Daiamid was very receptive.

</details>

## Commander Amma — Коммандер Амма.

`M01_010_040_A_HA`

**RU сейчас:** Радаа считали, что долгий мир делает нас всё уязвимее. Их предводительница, Коммандер Амма, предупреждала: осколки Таииданской империи, превратившиеся во владения военных вождей, снова вооружаются, и возникновение новой империи вполне возможно. В обмен на разрешение строить и добывать ресурсы в системе Хиигары Коммандер Амма предложила помочь нашему флоту вступить в новую эпоху развития и перевооружения.

*Внесена правка пользователя · 21 октября 2026*

<details><summary>English original</summary>

The Radaa believed that the longer we were at peace, the more vulnerable we became. Their leader, Commander Amma, warned that former Taiidani bandit kingdoms were re-arming and a new Empire was a real possibility.  In exchange for permission to build and mine in the Hiigaran star system, Commander Amma offered to shepherd the Hiigaran Fleet through a new era of modernization and growth.

</details>

## Командующий Флотом, Тирра Собан и её боевой опыт; убран случайный повтор «в в».

`M01_010_070_A_HA`

**RU сейчас:** Роль Командующего Флотом переняла Тирра Собан. Закалённый в боях ветеран, она прошла через множество битв в разваливающейся Таииданской Империи и разгромила десятки банд рейдеров.

*Внесена правка пользователя · 21 октября 2026*

<details><summary>English original</summary>

The role of Fleet Command fell to Tyrra Soban. A peerless military veteran, she had fought countless battles in the splintering remains of the Taiidani empire, and had broken up dozens of Raider groups.

</details>

## Материнский Корабль — боевое судно без всяких оговорок.

`M01_010_080_A_HA`

**RU сейчас:** Чтобы принять командование Материнским кораблём и флотом, Тирра прошла ту же процедуру, что и Каран С’Джет за несколько десятилетий до неё. Она была опытным бойцом, и всем было понятно, что Материнский Корабль теперь — боевое судно без всяких оговорок. Тирра Собан стала второй Освобождённой среди нашего народа.

*Внесена правка пользователя · 21 октября 2026*

<details><summary>English original</summary>

To take command of the Mothership and the Fleet, she underwent the same process that Karan S'jet had decades before. She was a trained warrior and that would make it clear to anyone that the Mothership was now a warship, pure and direct.Tyrra Soban was only the second of our people to become unbound.

</details>

## Согласованное звание Коммандер Амма распространено на приветствие Гиитана.

`M01_030_010_GR`

**RU сейчас:** Приветствую хиигарское командование. Говорит адмирал Гиитан Радаа. Наша Коммандер Амма передаёт свои пожелания долгого и плодотворного сотрудничества с народом Хиигары.

*Внесена правка пользователя · 21 октября 2026*

<details><summary>English original</summary>

Greetings, Hiigaran Command, this is Radaa Admiral Giitan. Our Commander Amma relays her wishes for our long and fruitful partnership with the Hiigaran people.

</details>

## Как обновляем дальше

Редактируем соответствующую часть в `localization/ru/early.json`, `late.json` или `shared.json`; `campaign.json` — объединённый результат. Согласованные изменения отмечаем в `localization/reviewed_changes.json`.

Синхронизация: `.venv\Scripts\python.exe -X utf8 tools/sync_campaign_documents.py`. Проверка без изменения файлов: та же команда с `--check`.

Команда обновляет сценарии, HTML и текущие RU-блоки разборов миссий, сохраняя ручные заметки. RAW и буквальный EN не переписываются. Игра и установленные файлы мода не затрагиваются.
