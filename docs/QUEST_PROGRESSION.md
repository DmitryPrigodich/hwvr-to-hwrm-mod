# Quest: флот, строительная прогрессия и появления в полной кампании

Составлено по **уже извлечённой полной Quest-версии** 17 октября 2026 года. Это отдельный источник; параметры Steam-демки сюда не перенесены. Здесь 11 миссий полной кампании и T1 отдельно. Тексты всех сцен см. в `QUEST_SCENARIOS.md`; ниже — флот, ресурсы и реальные узлы скриптов.

## Как читать числа и степень подтверждения

Запись Members в GroupInitialization — слот отряда, а не обязательно один физический корпус. Размер взят **из Quest ShipDefinition**, `_staticData.<SquadronCount>k__BackingField`. Например, перехватчик/бомбардировщик — по 5 корпусов в отряде, разведчик — 3, инженер — 1. Таблицы показывают оба числа.

**Carryover=true:** DefaultGroups и DefaultRU — резервный/начальный состав определения, а не гарантированное фактическое состояние обычного прохождения. Фактические корабли и RU зависят от выжившего флота предыдущей главы, AdditionalGroups, уровня сложности и правил переноса. Поэтому численный baseline ниже — DefaultGroups + AdditionalGroups + автоматические дружеские размещения карты **без выдуманного состояния сохранения**. AdditionalRU и MinimumCatchupValue приведены отдельно.

Числа, ссылки, whitelist/blacklist-поля, графы и их рёбра прочитаны из Quest-ассетов. Код из `decompiled-demo` используется только как **вспомогательная модель значения имён классов/полей**, а не как доказательство побайтно одинакового исполнения другой версии. В частности, предполагаемая семантика режимов BuildCommandList (1=Whitelist, 0=Blacklist), debug-флага и Carryover соответствует этой модели и согласуется с содержимым списков. Игровой запуск Quest здесь не проводился.

В сыром Quest-аудите есть ошибки чтения некоторых VFX/HUD/AbilityDefinition; используемые здесь MissionDatabase, MissionDefinition, ShipDefinition, BuildDefinition, ObjectiveDefinition и графы прочитаны. Отсутствие совместимости AbilityDefinition не подменено способностями Steam-версии.

## Порядок MissionDatabase и стартовые параметры

Порядок ниже задан `_campaignMissions`, а не сортировкой номеров M*. T1 хранится отдельно в `_tutorialMissions`.

| № | Миссия | DefaultRU | FleetCap | Carryover | AdditionalRU | MinimumCatchupValue | Baseline: отрядов/корпусов | Типов по стартовому BuildController |
|---:|---|---:|---:|---|---:|---:|---:|---:|
| 1 | Mission_M1 — Испытательный полигон Хиигары | 100 | 30 | False | 0 | 0 | 9 / 37 | 4 |
| 2 | Mission_M7 — Тёмная сторона Ангельской Луны | 0 | 30 | False | 0 | 0 | 13 / 49 | 4 |
| 3 | Mission_M3 — Рейд на Гиббас | 1200 | 30 | True | 600 | 1200 | 8 / 28 | 5 |
| 4 | Mission_M4 — Потерянный эсминец | 1200 | 33 | True | 600 | 1200 | 15 / 45 | 6 |
| 5 | Mission_M5 — Верфь Хиигары | 3000 | 33 | True | 600 | 3000 | 19 / 67 | 7 |
| 6 | Mission_M6 — Оружие | 4000 | 33 | True | 600 | 4000 | 19 / 63 | 8 |
| 7 | Mission_M9 — Система Тенхаузер | 500 | 36 | False | 0 | 0 | 8 / 24 | 9 |
| 8 | Mission_M10 — Добывающий комплекс Внешнего рифа | 3500 | 36 | True | 600 | 3500 | 25 / 53 | 10 |
| 9 | Mission_M11 — Создатели оружия | 3500 | 36 | True | 600 | 3500 | 24 / 48 | 11 |
| 10 | Mission_M8 — Наступление на Гиббас | 4000 | 36 | True | 600 | 4000 | 20 / 20 | 12 |
| 11 | Mission_M13 — Возвращение на Хиигару | 5000 | 40 | True | 600 | 5000 | 24 / 24 | 13 |
| отдельно | Mission_T1 — Обучение | 5000 | 30 | False | 0 | 0 | 1 / 1 | 1 |

Источник порядка: MissionDatabase `711b49b85337cea49bc8e0c3a86b35ad:1`. BuildController показывает начальную настройку списка; в M7 и M9 строительство затем блокируется/восстанавливается отдельными узлами.

## Что здесь является исследованием

В этих данных **не обнаружено отдельной очереди оплачиваемых Research-технологий** с ценой, длительностью и зависимостями, подобной HWRM. Найдены реальные **скриптовые открытия/восстановления строительства** и сюжетные объявления новых корпусов. Это нужно переносить как правила миссии/разрешение постройки либо сознательно превратить в исследования HWRM при адаптации.

Подтверждённые управляющими рёбрами примеры:

- **M7:** `DisableBuildSystem:219` после `OnSimReady:194`. После цели `M07_Objective_02a` («Harvest 2000 total RU to restore construction sytems.»), событие `OnObjectiveCompleted:251` идёт в `SetBuildByBuildList:337`, `_enable=true`, `CanScrap=true`.
- **M9:** во вступительной цепочке есть `DisableBuildSystem:313`. После передачи технологий Бентуси, реплика `M09_020_060_BN` (`Mission_M9_v2:587`) ведёт в `SetBuildByBuildList:205`, `_enable=true`, `CanScrap=true`.
- Объявления `FI_Unlock*` действительно подключены в графах, однако обычно новый тип уже включён в список соответствующей сцены. Реплика сама по себе не равна отдельному платному исследованию; ниже указаны и граф, и строительный список.

## 1. Mission_M1 — Испытательный полигон Хиигары

Определение: `f43761a426e901e4897580ed0dc94979:1`; карта `level1`; граф `Mission_M1` — `sharedassets1.assets:4137`.

DefaultRU **100**, FleetCap **30**, Carryover **False**, AdditionalRU **0**, MinimumCatchupValue **0**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M1_Default_1` | 3 отр. / 15 корп. × Перехватчик (`Ship_Kus_Interceptor`) | `374b54d6b83704b40aade82ac17d6e7e:3` |
| default_groups | `Group_M1_Default_2` | 1 отр. / 5 корп. × Перехватчик (`Ship_Kus_Interceptor`); 3 отр. / 15 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | `9fb036ed99d7e6f4187946181be3014f:3` |
| default_groups | `Group__RCx1` | 1 отр. / 1 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `f4d4145be93cb344eb849d7d678a8c0f:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level1:408` |

Baseline игрока (без других команд): **9 / 37 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level1:506`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M1:88` — cutscene | `Pat_InfiltrationFrigPatrol1`, `level1:487` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:432` |
| `Mission_M1:112` — HSG spawns | `Spawn_HyperspaceGate`, `level1:446` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level1:446` |
| `Mission_M1:158` — spawn scaries | `Frigate1`, `level1:469` | Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:469` |
| `Mission_M1:158` — spawn scaries | `Frigate2`, `level1:490` | Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:490` |
| `Mission_M1:158` — spawn scaries | `Frigate4`, `level1:473` | Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:473` |
| `Mission_M1:158` — spawn scaries | `Frigate3`, `level1:467` | Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:467` |
| `Mission_M1:158` — spawn scaries | `Group_EndShips`, `level1:412` | Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 2 корп. × Эсминец Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level1:412` |
| `Mission_M1:268` — HSG spawns | `Pat_Patrol1D`, `level1:497` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level1:420` |
| `Mission_M1:292` — Build Scout, added bc of beta (HERC-4467) | `Group1C`, `level1:468` | Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level1:468` |
| `Mission_M1:302` — spawn patrol A (3) | `Pat_Patrol1A`, `level1:493` | Патруль, один вариант: Computer1: 3 отр. / 15 корп. × Штурмовик Радаа; `level1:537` |
| `Mission_M1:318` — cutscene | `Pat_InfiltrationFrigPatrol2`, `level1:410` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:409` |
| `Mission_M1:334` — spawn backup every 60 seconds | `Pat_Patrol1E`, `level1:476` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level1:501` |
| `Mission_M1:553` — cutscene | `Pat_InfiltrationFrigPatrol3`, `level1:479` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level1:461` |
| `Mission_M1:581` — Build Scout | `Spawn_Shipyards`, `level1:442` | нейтральная/None: 1 отр. / 1 корп. × Верфь Радаа; `level1:442` |
| `Mission_M1:605` — spawn patrol B (2) | `Pat_Patrol1B`, `level1:426` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; `level1:405` |

### Объявление нового корпуса

Подключённой реплики FI_Unlock* в этом миссионном графе не найдено. Сюжетные упоминания ремонта/технологий не приравнены к исследованию.

## 2. Mission_M7 — Тёмная сторона Ангельской Луны

Определение: `66adb7078ddb522448ddc9de037c9d07:1`; карта `level11`; граф `Mission_M7` — `sharedassets11.assets:45`.

DefaultRU **0**, FleetCap **30**, Carryover **False**, AdditionalRU **0**, MinimumCatchupValue **0**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M7_Default_1` | 1 отр. / 5 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 10 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`) | `ea4d22613cdd3ff4f84e733b558df92b:3` |
| default_groups | `Group_M7_Default_2` | 1 отр. / 5 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 10 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`) | `f0b4130af5557ad40aa583281960b460:3` |
| default_groups | `Group__RCx2+Interceptors` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `11f203724a0ae63499a3284abb0c1568:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level11:382` |

Baseline игрока (без других команд): **13 / 49 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level11:513`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| `Mission_M7:219` | DisableBuildSystem: `{"CanScrap": false}` | OnSimReady:194 |
| `Mission_M7:337` | SetBuildByBuildList: `{"_enable": true, "CanScrap": true}` | OnObjectiveCompleted:251 `M07_Objective_02a` |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M7:102` — enemy patrols for phase 1, Enemy Patrols | `Patrolm1`, `level11:423` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Бомбардировщик Радаа; `level11:437` / ИЛИ / Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level11:431` |
| `Mission_M7:130` — enemy patrols for phase 1, Enemy Patrols | `Patrol_Mothership_1-E`, `level11:389` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Бомбардировщик Радаа; `level11:482` / ИЛИ / Computer1: 1 отр. / 5 корп. × Бомбардировщик Радаа; `level11:491` |
| `Mission_M7:140` — Enemy Patrols, enemy patrols added for phase 3 | `Patrol_Mothership_3-E`, `level11:402` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level11:438` / ИЛИ / Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level11:414` |
| `Mission_M7:180` — Enemy Patrols, enemy patrols added for phase 3 | `Patrolm3`, `level11:442` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level11:379` / ИЛИ / Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level11:465` |
| `Mission_M7:217` — Enemy Patrols, enemy patrols added for phase 2 | `Patrolm2`, `level11:499` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Бомбардировщик Радаа; `level11:418` / ИЛИ / Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level11:488` |
| `Mission_M7:331` — Enemy Patrols, enemy patrols added for phase 2 | `Patrol_Mothership_2-E`, `level11:490` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Бомбардировщик Радаа; `level11:501` / ИЛИ / Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level11:391` |

### Объявление нового корпуса

Подключённой реплики FI_Unlock* в этом миссионном графе не найдено. Сюжетные упоминания ремонта/технологий не приравнены к исследованию.

## 3. Mission_M3 — Рейд на Гиббас

Определение: `2b18e34423a7cfc4687ca08f9d35789f:1`; карта `level3`; граф `Mission_M3` — `sharedassets3.assets:84`.

DefaultRU **1200**, FleetCap **30**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **1200**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M3_Default_1` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 1 отр. / 3 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | `d80cd38160365e84eab4364e56c0dcfb:3` |
| default_groups | `Group_M3_Default_2` | 2 отр. / 10 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 1 отр. / 3 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | `553947a44374a934b91d155c5f7edac3:3` |
| default_groups | `Group_M3_Default_3` | 1 отр. / 1 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `40f4605eb6475734eb8c4e22d43258c7:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level3:1031` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1044` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1053` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1062` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1069` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1082` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1088` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1159` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1173` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1176` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1182` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1188` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level3:1192` |

Baseline игрока (без других команд): **8 / 28 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level3:1202`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_HeavyCorvette`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M3:136` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase`, `level3:1186` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level3:1132` |
| `Mission_M3:154` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChasemid`, `level3:1080` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level3:1030` |
| `Mission_M3:182` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChaselrg`, `level3:1169` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level3:1085` |
| `Mission_M3:308` — spawn shipyards and waves, startup and dialogue | `Spawn_Shipyards`, `level3:1077` | нейтральная/None: 3 отр. / 3 корп. × Верфь Радаа; `level3:1077` |
| `Mission_M3:416` — This is what happens after the first of any of the four refineries are destroyed | `Spawn_Battlecruiser`, `level3:1042` | Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа; `level3:1042` |
| `Mission_M3:442` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase2lrg`, `level3:1191` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level3:1181` |
| `Mission_M3:462` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase2mid`, `level3:1033` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level3:1061` |
| `Mission_M3:510` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase2`, `level3:1130` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; `level3:1106` |
| `Mission_M3:512` — This is what happens after the first of any of the four refineries are destroyed | `Pat_PatrolRUCap`, `level3:1071` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1036` |
| `Mission_M3:532` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase3lrg`, `level3:1103` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level3:1179` |
| `Mission_M3:584` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase3`, `level3:1051` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level3:1043` |
| `Mission_M3:588` — This is what happens after the second refinery is destroyed | `Pat_PatrolFinalChase3mid`, `level3:1171` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level3:1154` |
| `Mission_M3:626` — This is what happens after the first of any of the four refineries are destroyed | `Pat_PatrolRUCap2`, `level3:1087` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level3:1149` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FB_Patrol2B_Enemy`, `level3:1035` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1032` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FB_Patrol2A_Enemy`, `level3:1153` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1109` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FB_Patrol3C_Enemy`, `level3:1133` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1127` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FA_Patrol3A_Enemy`, `level3:1099` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1166` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FD_Patrol1A_Enemies`, `level3:1068` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1058` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FB_Patrol3B_Enemy`, `level3:1050` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1046` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FD_Patrol1C_Enemy`, `level3:1120` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1121` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FC_Patrol4A_Ref`, `level3:1152` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level3:1178` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FA_Patrol2A_Ref`, `level3:1158` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level3:1060` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FC_Patrol2B_Ref`, `level3:1180` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level3:1177` |
| `Mission_M3/embed:41:M3_InitialPatrols:55` — group D | `Pat_FD_Patrol1A_Ref`, `level3:1168` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level3:1225` |
| `Mission_M3/embed:41:M3_InitialPatrols:65` — patrolling assault frigate | `Pat_MobilePatrolAD1`, `level3:1038` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level3:1115` |
| `Mission_M3/embed:41:M3_InitialPatrols:65` — patrolling assault frigate | `Pat_MobilePatrolDC2`, `level3:1175` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1040` |
| `Mission_M3/embed:41:M3_InitialPatrols:65` — patrolling assault frigate | `Pat_MobilePatrolDC1`, `level3:1064` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level3:1126` |
| `Mission_M3/embed:41:M3_InitialPatrols:65` — patrolling assault frigate | `Pat_MobilePatrolAD2`, `level3:1183` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; `level3:1097` |
| `Mission_M3/embed:41:M3_InitialPatrols:65` — patrolling assault frigate | `Pat_PatrolRUCap2`, `level3:1087` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level3:1149` |

### Объявление нового корпуса

**`FI_UnlockHeavyCorvette`**, `Mission_M3:432`; управляющие связи: **True**. после `M03_020_040_TS` (узел 293). DialogueLine `sharedassets3.assets:66`.

*EN — исходник Quest:*

> Our ongoing repairs to the Mothership has added ship build capabilities: we can now build Heavy Corvettes. Their armor is ideal against heavy ballistics from the gun platforms we have detected in this sector.

*RU — исходная локализация Quest:*

> В ходе ремонта Материнского корабля мы расширили его производственные возможности. Теперь можно строить тяжёлые корветы. Их броня хорошо защищает от тяжёлых снарядов орудийных платформ, обнаруженных в этом секторе.

## 4. Mission_M4 — Потерянный эсминец

Определение: `894aa6041375b8c4386950e1073d009c:1`; карта `level5`; граф `Mission_M4` — `sharedassets5.assets:45`.

DefaultRU **1200**, FleetCap **33**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **1200**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M4_Default_1` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`) | `bec2904360ec08d4fa45c7bb3b6351ec:3` |
| default_groups | `Group_M4_Default_2` | 3 отр. / 15 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 2 отр. / 6 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | `a1e683b41783ffd45a39f58aedcb1a1b:3` |
| default_groups | `Group_M4_Default_3` | 1 отр. / 5 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `f9f5bf70528e5cd49b415c5f9fdac2c1:3` |
| additional_groups | `Group_M4_Default_4` | 3 отр. / 3 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`) | `b9efd080a34e47447a8e2f0d395bf661:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level5:1800` |
| scene auto, команда 0 | `RAD Destroyer (Damaged)` | 1 отр. / 1 корп. × Повреждённый эсминец Радаа (`Ship_Rad_Destroyer Damaged`) | `level5:1930` |

Baseline игрока (без других команд): **15 / 45 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level5:1989`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_HeavyCorvette`, `Build_Kus_EngineerCorvette`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| `Mission_M4:474` | AddRU: `{"Amount to Add": 0, "Team ID": "Player1"}` | OnSimReady:384 |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M4:21` — spawn from HSG | `Patrol`, `level5:1937` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level5:2061` |
| `Mission_M4:21` — spawn from HSG | `Patrol2`, `level5:1941` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level5:1849` / ИЛИ / Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level5:1895` |
| `Mission_M4:25` — Destroyer on way to mothership, Set Elimiate Gate Objective | `HyperspaceGate`, `level5:1825` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level5:1825` |
| `Mission_M4:67` — Destroyer on way to mothership, Set Elimiate Gate Objective | `Group_HSGDefense`, `level5:1876` | Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level5:1876` |
| `Mission_M4:366` — Destroyer on way to mothership, Set Elimiate Gate Objective | `Patrol Final Wave`, `level5:1905` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 4 отр. / 20 корп. × Бомбардировщик Радаа; `level5:1821` |
| `Mission_M4:420` — Starting cutscene and objective | `PatrolStart`, `level5:1961` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level5:1906` |
| `Mission_M4:420` — Starting cutscene and objective | `EdgePatrol`, `level5:1934` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level5:1939` |
| `Mission_M4:422` — Start of mission | `RC3`, `level5:1960` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 2 корп. × Переработчик Радаа; `level5:1846` |
| `Mission_M4:422` — Start of mission | `RC2`, `level5:1896` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 2 корп. × Переработчик Радаа; `level5:1866` |
| `Mission_M4:422` — Start of mission | `RC1`, `level5:1857` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 2 корп. × Переработчик Радаа; `level5:1954` |
| `Mission_M4:494` — spawn from HSG | `Patrol`, `level5:1937` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level5:2061` |
| `Mission_M4:494` — spawn from HSG | `Patrol2`, `level5:1941` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level5:1849` / ИЛИ / Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level5:1895` |

### Объявление нового корпуса

**`FI_UnlockEngineerCraft`**, `Mission_M4:332`; управляющие связи: **True**. после `M04_020_070_TS` (узел 394). DialogueLine `sharedassets5.assets:16`.

*EN — исходник Quest:*

> Resources claimed from Gybbas allow us to build a new ship: the Engineer Craft, which has the ability to repair ships in their Strike Group. They are also key to capturing the Radaa Destroyer in this sector.

*RU — исходная локализация Quest:*

> Ресурсы, добытые в Гиббасе, позволили нам освоить новый корабль — инженерный корвет. Он способен ремонтировать корабли своей ударной группы. Эти корветы также понадобятся для захвата эсминца Радаа в этом секторе.

## 5. Mission_M5 — Верфь Хиигары

Определение: `68fed03dd3ebcff49bcb60c9565b658b:1`; карта `level7`; граф `Mission_M5` — `sharedassets7.assets:55`.

DefaultRU **3000**, FleetCap **33**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **3000**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M5_Default_1` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`); 2 отр. / 6 корп. × Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | `3d0e2236909e7a749830c18247549c25:3` |
| default_groups | `Group_M5_Default_2` | 4 отр. / 20 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | `5f305112fb261fb4ca2d7c3bfb6522cc:3` |
| default_groups | `Group_M5_Default_3` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `fd102af0aed08fc4d829751d7304f48d:3` |
| default_groups | `Group_M5_Default_4` | 4 отр. / 12 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`) | `8e0c2aeb380569a4abca871122a2fb60:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level7:1139` |
| scene auto, команда 2 | `Science Station` | 1 отр. / 1 корп. × Верфь хиигарян (`Ship_Hgn_Shipyard`) | `level7:1308` |

Baseline игрока (без других команд): **19 / 67 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level7:1367`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_EngineerCorvette`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_HeavyCorvette`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M5:24` — Waves, Patrol 1C | `Patrol1C-2-H`, `level7:1235` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1194` |
| `Mission_M5:24` — Waves, Patrol 1C | `Patrol1C-H`, `level7:1147` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level7:1177` |
| `Mission_M5:64` — Waves, Patrol 2B | `Patrol2B-H`, `level7:1184` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level7:1322` |
| `Mission_M5:70` — Patrol 1A, Waves | `Patrol1A-H`, `level7:1151` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1143` |
| `Mission_M5:137` — Waves, Patrol 2B | `Patrol2B`, `level7:1256` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level7:1243` |
| `Mission_M5:141` — Waves, Patrol 3B | `Patrol3B`, `level7:1160` | Патруль, один вариант: Computer1: 3 отр. / 3 корп. × Штурмовой фрегат Радаа; `level7:1329` |
| `Mission_M5:153` — Waves, Patrol 2A | `Patrol2A`, `level7:1353` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 1 отр. / 5 корп. × Лучевой истребитель Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level7:1284` |
| `Mission_M5:153` — Waves, Patrol 2A | `Patrol2A-2`, `level7:1358` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1161` |
| `Mission_M5:179` — Waves, Patrol 2C | `Patrol2C-2-H`, `level7:1267` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 1 отр. / 5 корп. × Лучевой истребитель Радаа; `level7:1283` |
| `Mission_M5:179` — Waves, Patrol 2C | `Patrol2C-H`, `level7:1179` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1299` |
| `Mission_M5:191` — Waves, Patrol 1D | `Patrol1D-H`, `level7:1137` | Патруль, один вариант: Computer1: 3 отр. / 15 корп. × Штурмовик Радаа; `level7:1146` |
| `Mission_M5:195` — Waves, Patrol 1C | `Patrol1C`, `level7:1280` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Бомбардировщик Радаа; `level7:1196` |
| `Mission_M5:195` — Waves, Patrol 1C | `Patrol1C-2`, `level7:1162` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level7:1350` |
| `Mission_M5:226` — Waves, Patrol 1B | `Patrol1B`, `level7:1250` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; `level7:1304` |
| `Mission_M5:232` — Patrol 2D, Waves | `Patrol2D-H`, `level7:1289` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1355` |
| `Mission_M5:232` — Patrol 2D, Waves | `Patrol2D-2-H`, `level7:1341` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 1 отр. / 5 корп. × Лучевой истребитель Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level7:1240` |
| `Mission_M5:276` — Patrol 3A, Waves | `Patrol3A-H`, `level7:1156` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level7:1213` |
| `Mission_M5:276` — Patrol 3A, Waves | `Patrol3A-2-H`, `level7:1248` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1302` |
| `Mission_M5:280` — Patrol 3A, Waves | `Patrol3A-2`, `level7:1281` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1315` |
| `Mission_M5:280` — Patrol 3A, Waves | `Patrol3A`, `level7:1318` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 3 отр. / 15 корп. × Бомбардировщик Радаа; `level7:1176` |
| `Mission_M5:348` — Waves, Patrol 2A | `Patrol2A-H`, `level7:1347` | Патруль, один вариант: Computer1: 3 отр. / 15 корп. × Лучевой истребитель Радаа; `level7:1279` |
| `Mission_M5:348` — Waves, Patrol 2A | `Patrol2A-2-H`, `level7:1170` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1278` |
| `Mission_M5:366` — Patrol 1A, Waves | `Patrol1A`, `level7:1316` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; `level7:1391` |
| `Mission_M5:386` — Waves, Patrol 1B | `Patrol1B-H`, `level7:1135` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Лучевой истребитель Радаа; `level7:1303` |
| `Mission_M5:434` — Patrol 2D, Waves | `Patrol2D`, `level7:1154` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; `level7:1166` |
| `Mission_M5:434` — Patrol 2D, Waves | `Patrol2D-2`, `level7:1175` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level7:1229` |
| `Mission_M5:442` — Waves, Patrol 3B | `Patrol3B-H`, `level7:1320` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 4 отр. / 20 корп. × Лучевой истребитель Радаа; `level7:1145` |
| `Mission_M5:496` — Waves, Patrol 1D | `Patrol1D`, `level7:1348` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level7:1300` |
| `Mission_M5:553` — Waves, Patrol 2C | `Patrol2C`, `level7:1276` | Патруль, один вариант: Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа; `level7:1187` |
| `Mission_M5:553` — Waves, Patrol 2C | `Patrol2C-2`, `level7:1257` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level7:1312` |

### Объявление нового корпуса

**`FI_UnlockMultiGunCorvette`**, `Mission_M5:56`; управляющие связи: **True**. после `M05_020_040_TS` (узел 448). DialogueLine `sharedassets7.assets:30`.

*EN — исходник Quest:*

> Our engineering team has added capability to our construction bays: Multi-Gun Corvettes. These are ideal for counter-attack against the Radaa's fast-moving threats to the shipyard.

*RU — исходная локализация Quest:*

> Наши инженеры расширили возможности сборочных цехов: теперь мы можем строить многопушечные корветы. Они отлично подходят для перехвата быстрых кораблей Радаа, угрожающих верфи.

## 6. Mission_M6 — Оружие

Определение: `c6a609b9e607c244fb916366c37ad701:1`; карта `level9`; граф `Mission_M6` — `sharedassets9.assets:65`.

DefaultRU **4000**, FleetCap **33**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **4000**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M6_Default_1` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 1 отр. / 3 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`); 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | `5541b527b5e108b468e6ee45c077f6f6:3` |
| default_groups | `Group_M6_Default_2` | 2 отр. / 10 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`); 2 отр. / 6 корп. × Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | `121c3b34fcf92214282f4091bf85866c:3` |
| default_groups | `Group__RCx2+Interceptors` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `11f203724a0ae63499a3284abb0c1568:3` |
| default_groups | `Group_M6_Default_4` | 2 отр. / 10 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 2 отр. / 6 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | `05703df08d72cea44853f152943093e5:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level9:835` |
| scene auto, команда 0 | `RAD Shield Emitter A` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level9:840` |
| scene auto, команда 0 | `RAD Shield Emitter D` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level9:842` |
| scene auto, команда 0 | `RAD Shield Emitter B` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level9:866` |
| scene auto, команда 1024 | `HSG1` | 1 отр. / 1 корп. × Гиперврата Радаа (`Ship_Rad_HyperSpaceGate`) | `level9:880` |
| scene auto, команда 1024 | `RAD Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level9:897` |
| scene auto, команда 1024 | `RAD Gun Platform` | 1 отр. / 1 корп. × Орудийная платформа (`Ship_Rad_GunPlatform`) | `level9:944` |
| scene auto, команда 0 | `RAD Shield Emitter C` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level9:960` |
| scene auto, команда 1024 | `RAD Tower` | 1 отр. / 1 корп. × Башня Радаа (`Ship_Rad_Tower`) | `level9:973` |

Baseline игрока (без других команд): **19 / 63 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level9:1000`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_EngineerCorvette`, `Build_Kus_HeavyCorvette`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_AssaultFrigate`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `05e430930eaaa1a4f9e30f7303e25c16:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| `Mission_M6:387` | DisableBuildSystem: `{"CanScrap": false}` | после `M06_080_070_TS` (узел 554) |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M6:94` — SPAWN ONCE, hard patrols around SEs | `Patrol2B-H`, `level9:904` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:887` |
| `Mission_M6:94` — SPAWN ONCE, hard patrols around SEs | `Patrol1C-H`, `level9:879` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level9:854` |
| `Mission_M6:94` — SPAWN ONCE, hard patrols around SEs | `Patrol1B-H`, `level9:917` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:952` |
| `Mission_M6:94` — SPAWN ONCE, hard patrols around SEs | `Patrol2C-H`, `level9:857` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Бомбардировщик Радаа; 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); `level9:885` |
| `Mission_M6:210` — harder patrols, PATROLS - CONTINUOUS SPAWN | `Patrol1D-H`, `level9:856` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level9:850` |
| `Mission_M6:210` — harder patrols, PATROLS - CONTINUOUS SPAWN | `Patrol3C-H`, `level9:832` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level9:937` |
| `Mission_M6:210` — harder patrols, PATROLS - CONTINUOUS SPAWN | `Patrol2D-H`, `level9:935` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:867` |
| `Mission_M6:210` — harder patrols, PATROLS - CONTINUOUS SPAWN | `Patrol3E-H`, `level9:855` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level9:892` |
| `Mission_M6:210` — harder patrols, PATROLS - CONTINUOUS SPAWN | `Patrol3B-H`, `level9:891` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level9:888` |
| `Mission_M6:210` — harder patrols, PATROLS - CONTINUOUS SPAWN | `Patrol1A-H`, `level9:987` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level9:957` |
| `Mission_M6:316` — send patrol to attack target | `Patrol_HSG1`, `level9:953` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level9:849` |
| `Mission_M6:449` — easier patrols, PATROLS - CONTINUOUS SPAWN | `Patrol1A`, `level9:966` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level9:1032` |
| `Mission_M6:449` — easier patrols, PATROLS - CONTINUOUS SPAWN | `Patrol3C`, `level9:976` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); `level9:890` |
| `Mission_M6:449` — easier patrols, PATROLS - CONTINUOUS SPAWN | `Patrol1D`, `level9:982` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); `level9:949` |
| `Mission_M6:449` — easier patrols, PATROLS - CONTINUOUS SPAWN | `Patrol2D`, `level9:841` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:852` |
| `Mission_M6:449` — easier patrols, PATROLS - CONTINUOUS SPAWN | `Patrol3E`, `level9:931` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Лазерный корвет Радаа; `level9:962` |
| `Mission_M6:449` — easier patrols, PATROLS - CONTINUOUS SPAWN | `Patrol3B`, `level9:845` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Лазерный корвет Радаа; `level9:972` |
| `Mission_M6:533` — SPAWN ONCE, normal patrols around SEs | `Patrol1B`, `level9:917` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:952` |
| `Mission_M6:533` — SPAWN ONCE, normal patrols around SEs | `Patrol2C`, `level9:934` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level9:869` |
| `Mission_M6:533` — SPAWN ONCE, normal patrols around SEs | `Patrol2B`, `level9:922` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:911` |
| `Mission_M6:533` — SPAWN ONCE, normal patrols around SEs | `Patrol1C`, `level9:936` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:876` |
| `Mission_M6:672` — win condition | `Shatter Station Group`, `level9:875` | Computer1: 1 отр. / 1 корп. × Shatter Station; `level9:875` |
| `Patrol_Setup_M6:21` — — | `Patrol1B`, `level9:917` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:952` |
| `Patrol_Setup_M6:23` — — | `Patrol1C`, `level9:936` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level9:876` |
| `Patrol_Setup_M6:25` — — | `Patrol1D`, `level9:982` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); `level9:949` |
| `Patrol_Setup_M6:27` — — | `Patrol1A`, `level9:966` | Патруль, один вариант: Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level9:1032` |

### Объявление нового корпуса

**`FI_UnlockAssaultFrigate`**, `Mission_M6:451`; управляющие связи: **True**. после `M06_020_050_TS` (узел 289). DialogueLine `sharedassets9.assets:30`.

*EN — исходник Quest:*

> With the technology transferred from the Shipyard, we can build a new ship: Assault Frigates. These heavy weapon craft are ideal for penetrating the Radaa defenses guarding the shield emitters.

*RU — исходная локализация Quest:*

> Технологии, полученные с верфи, позволили нам освоить новый тип кораблей — штурмовые фрегаты. Их тяжёлое вооружение отлично подходит для прорыва обороны Радаа, прикрывающей генераторы щита.

## 7. Mission_M9 — Система Тенхаузер

Определение: `b1100962db5bfd04d93dc41a7563ff7c:1`; карта `level15`; граф `Mission_M9_v2` — `sharedassets15.assets:60`.

DefaultRU **500**, FleetCap **36**, Carryover **False**, AdditionalRU **0**, MinimumCatchupValue **0**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M9_Default_1` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 1 отр. / 1 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | `debdb90bb26af7b458db6364e57a0f99:3` |
| default_groups | `Group_M9_Default_2` | 0 отрядов / 0 корпусов (пустой шаблон) | `1a4af95e6ce89aa4885c8f2580bda993:3` |
| default_groups | `Group__RCx2+Interceptors` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `11f203724a0ae63499a3284abb0c1568:3` |
| default_groups | `Group_M9_Default_4` | 0 отрядов / 0 корпусов (пустой шаблон) | `f8467411accda5a41a3eb844eeb643fc:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level15:463` |

Baseline игрока (без других команд): **8 / 24 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level15:632`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_EngineerCorvette`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_HeavyCorvette`, `Build_Kus_AssaultFrigate`, `Build_Kus_BarricadeFrigate`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `05e430930eaaa1a4f9e30f7303e25c16:1` |
| Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | 1/1 | 1700 | 40 | `Build_Kus_BarricadeFrigate`, `f45c8fa0d676a874c8d42ce2b90908fb:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| `Mission_M9_v2:205` | SetBuildByBuildList: `{"_enable": true, "CanScrap": true}` | после `M09_020_060_BN` (узел 587) |
| `Mission_M9_v2:313` | DisableBuildSystem: `{"CanScrap": false}` | OnSimReady:83 |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M9_v2:149` — HSG5 Spawner | `Patrol HSG5`, `level15:554` | Патруль, один вариант: Computer1: 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:543` / ИЛИ / Computer1: 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 2 корп. × Фрегат проникновения Радаа; `level15:588` |
| `Mission_M9_v2:239` — HSG1 Spawner | `Patrol HSG1 00`, `level15:565` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:590` |
| `Mission_M9_v2:309` — HSG2 Spawner | `Patrol HSG2`, `level15:469` | Патруль, один вариант: Computer1: 3 отр. / 15 корп. × Штурмовик Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:477` / ИЛИ / Computer1: 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:505` |
| `Mission_M9_v2:319` — M09_020 | `PlayerGroup5`, `level15:634` | игрок: 1 отр. / 1 корп. × Штурмовой фрегат; 1 отр. / 1 корп. × Инженерный корвет; 1 отр. / 1 корп. × Баррикадный фрегат; `level15:634` |
| `Mission_M9_v2:321` — spawn Radaa | `Group_Destroyer`, `level15:541` | Computer1: 1 отр. / 1 корп. × Эсминец Радаа; `level15:541` |
| `Mission_M9_v2:333` — HSG1 Spawner | `Patrol HSG1`, `level15:589` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level15:649` / ИЛИ / Computer1: 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level15:489` / ИЛИ / Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Эсминец Радаа; `level15:571` |
| `Mission_M9_v2:339` — HSG3 Spawner | `Patrol HSG3`, `level15:476` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:617` / ИЛИ / Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level15:496` / ИЛИ / Computer1: 3 отр. / 9 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:600` |
| `Mission_M9_v2:595` — spawn Radaa | `HSG5`, `level15:479` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level15:479` |
| `Mission_M9_v2:615` — spawn outpost | `Group_Bentusi`, `level15:558` | 2: 1 отр. / 1 корп. × Корабль бентуси; `level15:558` |
| `Mission_M9_v2:634` — HSG4 Spawner | `Patrol HSG4`, `level15:616` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Эсминец Радаа; `level15:580` / ИЛИ / Computer1: 3 отр. / 9 корп. × Корвет Радаа (исходный тип MissileCorvette); `level15:475` |
| `Mission_M9_v2:646` — HSG3 Spawner | `Patrol HSG3 00`, `level15:614` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level15:482` |
| `Mission_M9_v2:682` — spawn Radaa | `HSG0`, `level15:606` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level15:606` |
| `Mission_M9_v2:694` — spawn Radaa | `HSG1`, `level15:511` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level15:511` |
| `Mission_M9_v2:694` — spawn Radaa | `HSG3`, `level15:521` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level15:521` |
| `Mission_M9_v2:694` — spawn Radaa | `HSG2`, `level15:604` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level15:604` |
| `Mission_M9_v2:694` — spawn Radaa | `HSG4`, `level15:530` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level15:530` |

### Объявление нового корпуса

**`FI_UnlockBarricadeFrigate`**, `Mission_M9_v2:211`; управляющие связи: **True**. после `M09_030_040_KS` (узел 457). DialogueLine `sharedassets15.assets:21`.

*EN — исходник Quest:*

> With the technology the Bentusi provided, our construction bays can now build Barricade Frigates. When activated, these can provide shields for nearby ships. They can also be used to protect the Bentusi.

*RU — исходная локализация Quest:*

> Благодаря технологиям Бентуси наши сборочные цеха теперь могут выпускать баррикадные фрегаты. При активации они прикрывают щитом находящиеся рядом корабли. С их помощью можно защитить и самих Бентуси.

## 8. Mission_M10 — Добывающий комплекс Внешнего рифа

Определение: `5cd7702c05ff025469152b598cb0fda8:1`; карта `level17`; граф `Mission_M10` — `sharedassets17.assets:46`.

DefaultRU **3500**, FleetCap **36**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **3500**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M10_Default_1` | 2 отр. / 6 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`); 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 3 отр. / 3 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`) | `9f9dcfcc8d9ed9f4cb7940ef3f64c1fe:3` |
| default_groups | `Group_M10_Default_2` | 2 отр. / 2 корп. × Ионный фрегат (`Ship_Hgn_IonCannonFrigate`); 3 отр. / 9 корп. × Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | `03c619b88d64be6459a14165ec02e76d:3` |
| default_groups | `Group__RCx2` | 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `d70fd04b5f921ec4d90554aa58de5c3d:3` |
| default_groups | `Group_M10_Default_4` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`) | `a1e5dd6553b8e3e4785c2a4105f29d28:3` |
| default_groups | `Group_M10_Default_5` | 2 отр. / 10 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 1 отр. / 1 корп. × Ионный фрегат (`Ship_Hgn_IonCannonFrigate`); 2 отр. / 2 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | `1d8fd74fe51988d4781f6baefe8da0f1:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level17:1213` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (5)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1218` |
| scene auto, команда 1024 | `Group: Patrol Wave A` | 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`) | `level17:1219` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (2)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1222` |
| scene auto, команда 1024 | `Group: Patrol Wave D` | 1 отр. / 5 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`) | `level17:1223` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (4)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1235` |
| scene auto, команда 0 | `Mining Platform (active) B` | 1 отр. / 1 корп. × Добывающая платформа (`Ship_Hgn_MiningPlatform`) | `level17:1242` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (3)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1271` |
| scene auto, команда 1024 | `Group: Patrol Wave D` | 1 отр. / 5 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`) | `level17:1280` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1294` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (7)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1310` |
| scene auto, команда 1024 | `Group: Patrol Wave B` | 1 отр. / 5 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`) | `level17:1318` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (1)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1321` |
| scene auto, команда 0 | `Mining Platform (active)` | 1 отр. / 1 корп. × Добывающая платформа (`Ship_Hgn_MiningPlatform`) | `level17:1322` |
| scene auto, команда 0 | `Mining Platform (active) A` | 1 отр. / 1 корп. × Добывающая платформа (`Ship_Hgn_MiningPlatform`) | `level17:1327` |
| scene auto, команда 1024 | `Group: Spawn wave 3` | 2 отр. / 10 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 4 отр. / 4 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`) | `level17:1330` |
| scene auto, команда 1024 | `Group: Patrol Wave A` | 2 отр. / 10 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`) | `level17:1337` |
| scene auto, команда 1024 | `[CPU1] RAD Heavy Missile Platform (6)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level17:1342` |
| scene auto, команда 1024 | `Group: Patrol Wave B` | 1 отр. / 5 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`) | `level17:1389` |

Baseline игрока (без других команд): **25 / 53 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level17:1354`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_HeavyCorvette`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_EngineerCorvette`, `Build_Kus_AssaultFrigate`, `Build_Kus_IonCannonFrigate`, `Build_Kus_BarricadeFrigate`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `05e430930eaaa1a4f9e30f7303e25c16:1` |
| Ионный фрегат (`Ship_Hgn_IonCannonFrigate`) | 1/1 | 1800 | 40 | `Build_Kus_IonCannonFrigate`, `8203482b65ce37543af2d2668034b7d7:1` |
| Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | 1/1 | 1700 | 40 | `Build_Kus_BarricadeFrigate`, `f45c8fa0d676a874c8d42ce2b90908fb:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M10:30` — Platform B enemy spawns | `HyperspaceGateB`, `level17:1333` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level17:1333` |
| `Mission_M10:66` — Platform B enemy spawns | `HyperspaceGateA2`, `level17:1311` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level17:1311` |
| `Mission_M10:134` — Platform A enemy spawns | `HyperspaceGateA`, `level17:1320` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level17:1320` |
| `Mission_M10:327` — Platform A enemy spawns | `PlatformB_Patrol2`, `level17:1278` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level17:1331` |
| `Mission_M10:331` — responding wave to mothership, Platform B enemy spawns | `PlatformA_Patrol2`, `level17:1224` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level17:1263` |
| `Mission_M10:371` — Platform A enemy spawns | `HyperspaceGateB2`, `level17:1319` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level17:1319` |
| `Mission_M10:405` — Cutscene 2; Begin final platform | `Spawn Enemy Battle Cruiser`, `level17:1264` | Computer1: 1 отр. / 1 корп. × Стационарный линейный крейсер Радаа; `level17:1264` |
| `Mission_M10:488` — responding wave to mothership, Platform B enemy spawns | `PlatformA_Patrol3`, `level17:1238` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Лазерный корвет Радаа; 3 отр. / 15 корп. × Бомбардировщик Радаа; `level17:1343` |
| `Mission_M10:661` — Platform A enemy spawns | `PlatformB_Patrol3`, `level17:1341` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Лазерный корвет Радаа; 3 отр. / 15 корп. × Бомбардировщик Радаа; `level17:1266` |
| `Mission_M10:823` — Platform B enemy spawns | `PlatformB_Patrol`, `level17:1243` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level17:1289` |
| `Mission_M10:860` — Platform A enemy spawns | `PlatformA_Patrol`, `level17:1298` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 2 отр. / 2 корп. × Штурмовой фрегат Радаа; `level17:1269` |
| `Patrol_Setup_M10:17` — — | `Patrol Final Wave`, `level17:1296` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; `level17:1226` |

### Объявление нового корпуса

**`FI_UnlockIonFrigate`**, `Mission_M10:80`; управляющие связи: **True**. после `M10_020_080_KS` (узел 762). DialogueLine `sharedassets17.assets:22`.

*EN — исходник Quest:*

> The Bentusi also provided us the key components necessary to build a new ship class: Ion Frigates, which are ideal for long range attacks and cutting into the hulls of larger ships.

*RU — исходная локализация Quest:*

> Бентуси также передали нам ключевые компоненты для нового класса кораблей — ионных фрегатов. Они отлично подходят для дальнего боя и способны прожигать корпуса крупных кораблей.

## 9. Mission_M11 — Создатели оружия

Определение: `653d9688338bfb943b561c979612218e:1`; карта `level19`; граф `Mission_M11` — `sharedassets19.assets:41`.

DefaultRU **3500**, FleetCap **36**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **3500**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M11_Default_1` | 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 2 отр. / 6 корп. × Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`); 1 отр. / 1 корп. × Эсминец (`Ship_Hgn_Destroyer`) | `ff2bab2ad6e54f34c8a46c9bcd148073:3` |
| default_groups | `Group_M11_Default_2` | 1 отр. / 1 корп. × Ионный фрегат (`Ship_Hgn_IonCannonFrigate`); 2 отр. / 6 корп. × Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`); 1 отр. / 1 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | `180d5615a5b1a4e458a4b83e326faf24:3` |
| default_groups | `Group__RCx2+Interceptors` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `11f203724a0ae63499a3284abb0c1568:3` |
| default_groups | `Group_M11_Default_4` | 1 отр. / 3 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`); 2 отр. / 2 корп. × Ионный фрегат (`Ship_Hgn_IonCannonFrigate`); 2 отр. / 6 корп. × Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | `3c49e5aca3cc31e4f91cf09923797026:3` |
| default_groups | `Group_M11_Default_5` | 1 отр. / 3 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`); 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 1 отр. / 1 корп. × Ионный фрегат (`Ship_Hgn_IonCannonFrigate`); 1 отр. / 1 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | `5b86d14d441272a4c8f098a85105d0a5:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level19:1547` |

Baseline игрока (без других команд): **24 / 48 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level19:1698`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_HeavyCorvette`, `Build_Kus_EngineerCorvette`, `Build_Kus_BarricadeFrigate`, `Build_Kus_AssaultFrigate`, `Build_Kus_IonCannonFrigate`, `Build_Kus_Destroyer`, `Build_Kus_ResourceCollector`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | 1/1 | 1700 | 40 | `Build_Kus_BarricadeFrigate`, `f45c8fa0d676a874c8d42ce2b90908fb:1` |
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `05e430930eaaa1a4f9e30f7303e25c16:1` |
| Ионный фрегат (`Ship_Hgn_IonCannonFrigate`) | 1/1 | 1800 | 40 | `Build_Kus_IonCannonFrigate`, `8203482b65ce37543af2d2668034b7d7:1` |
| Эсминец (`Ship_Hgn_Destroyer`) | 1/1 | 2500 | 50 | `Build_Kus_Destroyer`, `7572241c9a1a5f047bd6278b52d4a818:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M11:74` — Final Patrols attack destroyer objective 3 | `FinalPatrolC`, `level19:1668` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 3 отр. / 15 корп. × Лучевой истребитель Радаа; `level19:1603` |
| `Mission_M11:119` — Correct Destroyer Detected - Actual Objective | `HyperspaceGate_B`, `level19:1672` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level19:1672` |
| `Mission_M11:187` — Mission Start Sequence | `DestroyerBPersonnelCraft`, `level19:1673` | нейтральная/None: 1 отр. / 1 корп. × Сдавшийся эсминец Радаа; `level19:1673` |
| `Mission_M11:285` — Mission Start Sequence | `Wave 1`, `level19:1703` | Computer1: 3 отр. / 15 корп. × Лучевой истребитель Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 10 корп. × Бомбардировщик Радаа; `level19:1703` |
| `Mission_M11:333` — Final Patrols attack destroyer objective 3 | `HyperspaceGate_C`, `level19:1671` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level19:1671` |
| `Mission_M11:335` — Final Patrols attack destroyer objective 3 | `FinalPatrolA`, `level19:1580` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Штурмовой фрегат Радаа; `level19:1614` |
| `Mission_M11:421` — Final Patrols attack destroyer objective 3 | `HyperspaceGate_D`, `level19:1568` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level19:1568` |
| `Mission_M11:445` — Spawn enemies from 1st Escape Hyperspace Gate, Correct Destroyer Detected - Actual Objective | `Patrol_RouteB`, `level19:1663` | Патруль, один вариант: Computer1: 1 отр. / 3 корп. × Лазерный корвет Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level19:1718` / ИЛИ / Computer1: 3 отр. / 15 корп. × Штурмовик Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level19:1590` |
| `Mission_M11:461` — Mission Start Sequence | `Wave 3`, `level19:1664` | Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; 3 отр. / 9 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; `level19:1664` |
| `Mission_M11:475` — Mission Start Sequence | `Wave 2`, `level19:1622` | Computer1: 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level19:1622` |
| `Mission_M11:493` — Final Patrols attack destroyer objective 3 | `HyperspaceGate_A`, `level19:1562` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level19:1562` |
| `Mission_M11:599` — Final Patrols attack destroyer objective 3 | `FinalPatrolD`, `level19:1652` | Патруль, один вариант: Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level19:1659` |

### Объявление нового корпуса

**`FI_UnlockDestroyer`**, `Mission_M11:72`; управляющие связи: **True**. после `M11_020_030_FI` (узел 343). DialogueLine `sharedassets19.assets:19`.

*EN — исходник Quest:*

> Our ship construction capabilities have been upgraded to build a new ship: Destroyers. These capital class ships have weapon systems most effective against squadrons of strike craft.

*RU — исходная локализация Quest:*

> Мы расширили возможности сборочных цехов и можем строить новый тип кораблей — эсминцы. Вооружение этих крупных боевых кораблей особенно эффективно против эскадрилий ударных кораблей.

## 10. Mission_M8 — Наступление на Гиббас

Определение: `a5358fed0221c06459236bb5e555ec41:1`; карта `level13`; граф `Mission_M8` — `sharedassets13.assets:33`.

DefaultRU **4000**, FleetCap **36**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **4000**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M8_Default_1` | 2 отр. / 2 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`); 1 отр. / 1 корп. × Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | `fe8c14e190d6eb041b03274ef8e421f8:3` |
| default_groups | `Group_M8_Default_2` | 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 1 отр. / 1 корп. × Эсминец (`Ship_Hgn_Destroyer`); 1 отр. / 1 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | `13e26a6040cd87442ac526e130f51af1:3` |
| default_groups | `Group_M8_Default_3` | 1 отр. / 1 корп. × Эсминец (`Ship_Hgn_Destroyer`); 3 отр. / 3 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `5e421938dd9d761479a8634cb3f9eed6:3` |
| default_groups | `Group_M8_Default_4` | 2 отр. / 2 корп. × Ионный фрегат (`Ship_Hgn_IonCannonFrigate`); 1 отр. / 1 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`); 1 отр. / 1 корп. × Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | `ee24675d0ba8bd44088f18f1803277e6:3` |
| default_groups | `Group_M8_Default_5` | 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 1 отр. / 1 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`); 1 отр. / 1 корп. × Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | `b70d93c980def08479e338ea8ecb63ca:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level13:1106` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1102` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1104` |
| scene auto, команда 1024 | `Group: ShipyardsC` | 1 отр. / 1 корп. × Верфь Радаа (`Ship_Rad_Shipyard`) | `level13:1105` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1123` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1126` |
| scene auto, команда 0 | `Group: SpawnFromShipyardAfter2RUFieldsCaptured` | 0 отрядов / 0 корпусов (пустой шаблон) | `level13:1128` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1129` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1139` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1149` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1161` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1175` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1180` |
| scene auto, команда 1024 | `Group: ShipyardsA` | 1 отр. / 1 корп. × Верфь Радаа (`Ship_Rad_Shipyard`) | `level13:1196` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1206` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1217` |
| scene auto, команда 0 | `Group: SpawnFromShipyardAfter1RUFieldCaptured` | 0 отрядов / 0 корпусов (пустой шаблон) | `level13:1218` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1222` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1231` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1246` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1254` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1258` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1259` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1262` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1267` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1283` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1284` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1285` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1286` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1287` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1293` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1300` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1301` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1303` |
| scene auto, команда 1024 | `Group: ShipyardsB` | 1 отр. / 1 корп. × Верфь Радаа (`Ship_Rad_Shipyard`) | `level13:1307` |
| scene auto, команда 1024 | `VGR Gun Platform` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level13:1308` |

Baseline игрока (без других команд): **20 / 20 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level13:1322`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_EngineerCorvette`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_HeavyCorvette`, `Build_Kus_AssaultFrigate`, `Build_Kus_IonCannonFrigate`, `Build_Kus_Destroyer`, `Build_Kus_ResourceCollector`, `Build_Kus_BarricadeFrigate`, `Build_Kus_BallisticDestroyer`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `05e430930eaaa1a4f9e30f7303e25c16:1` |
| Ионный фрегат (`Ship_Hgn_IonCannonFrigate`) | 1/1 | 1800 | 40 | `Build_Kus_IonCannonFrigate`, `8203482b65ce37543af2d2668034b7d7:1` |
| Эсминец (`Ship_Hgn_Destroyer`) | 1/1 | 2500 | 50 | `Build_Kus_Destroyer`, `7572241c9a1a5f047bd6278b52d4a818:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |
| Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | 1/1 | 1700 | 40 | `Build_Kus_BarricadeFrigate`, `f45c8fa0d676a874c8d42ce2b90908fb:1` |
| Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | 1/1 | 2700 | 50 | `Build_Kus_BallisticDestroyer`, `01e918c81218f344986dd720f2fc4f62:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M8:46` — Shipyards 1 & 2 destroyed Memos | `Patrol3Enemies-H`, `level13:1157` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 2 корп. × Эсминец Радаа; `level13:1263` |
| `Mission_M8:132` — Hyperspace gate spawns patrols in response to 1st Shipyard destruction | `HyperspaceGate1`, `level13:1227` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level13:1227` |
| `Mission_M8:216` — Detection Spheres sending reinforcements from shipyards | `PatrolShipBEnemies-H`, `level13:1269` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 10 корп. × Лучевой истребитель Радаа; 1 отр. / 3 корп. × Лазерный корвет Радаа; 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); `level13:1210` |
| `Mission_M8:220` — Shipyards 1 & 2 destroyed Memos | `Patrol4Enemies-H`, `level13:1110` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1189` |
| `Mission_M8:236` — Shipyards 1 & 2 destroyed Memos | `Patrol4enemies`, `level13:1179` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Эсминец Радаа; 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette); `level13:1230` |
| `Mission_M8:254` — Hyperspace gate spawns patrols in response to 1st Shipyard destruction | `HSGResponse1-H`, `level13:1170` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1146` |
| `Mission_M8:274` — Detection Spheres sending reinforcements from shipyards | `PatrolShipCEnemies-H`, `level13:1215` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level13:1297` |
| `Mission_M8:298` — Hyperspace gate spawns patrols in response to 2nd Shipyard destruction | `HSGResponse2-H`, `level13:1195` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1176` |
| `Mission_M8:306` — Detection Spheres sending reinforcements from shipyards | `PatrolShipAEnemies`, `level13:1103` | Патруль, один вариант: Computer1: 3 отр. / 9 корп. × Лазерный корвет Радаа; `level13:1178` |
| `Mission_M8:332` — Detection Spheres sending reinforcements from shipyards | `PatrolShipAEnemies-H`, `level13:1256` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1261` |
| `Mission_M8:358` — Hyperspace gate spawns patrols in response to 2nd Shipyard destruction | `HSGResponse2`, `level13:1098` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1253` |
| `Mission_M8:390` — Hyperspace gate spawns patrols in response to 1st Shipyard destruction | `HSGResponse1`, `level13:1127` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1117` |
| `Mission_M8:450` — Detection Spheres sending reinforcements from shipyards | `PatrolShipCEnemies`, `level13:1255` | Патруль, один вариант: Computer1: 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette); `level13:1221` |
| `Mission_M8:463` — Shipyards 1 & 2 destroyed Memos | `Patrol4enemies`, `level13:1179` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Эсминец Радаа; 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette); `level13:1230` |
| `Mission_M8:479` — Hyperspace gate spawns patrols in response to 2nd Shipyard destruction | `HyperspaceGate2`, `level13:1305` | Computer1: 1 отр. / 1 корп. × Гиперврата Радаа; `level13:1305` |
| `Mission_M8:503` — Shipyards 1 & 2 destroyed Memos | `Patrol3Enemies-H`, `level13:1157` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 2 отр. / 2 корп. × Эсминец Радаа; `level13:1263` |
| `Mission_M8:550` — Detection Spheres sending reinforcements from shipyards | `PatrolShipBEnemies`, `level13:1281` | Патруль, один вариант: Computer1: 5 отр. / 25 корп. × Лучевой истребитель Радаа; `level13:1248` |
| `Mission_M8:568` — Shipyards 1 & 2 destroyed Memos | `Patrol2enemies`, `level13:1169` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа; 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level13:1191` |
| `Mission_M8:591` — Shipyards 1 & 2 destroyed Memos | `Patrol3enemies`, `level13:1211` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 1 отр. / 1 корп. × Эсминец Радаа; `level13:1238` |
| `Mission_M8:601` — Shipyards 1 & 2 destroyed Memos | `Patrol2Enemies-H`, `level13:1228` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 2 корп. × Фрегат проникновения Радаа; `level13:1213` |
| `Mission_M8:621` — Shipyards 1 & 2 destroyed Memos | `Patrol3enemies`, `level13:1211` | Патруль, один вариант: Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа; 1 отр. / 1 корп. × Эсминец Радаа; `level13:1238` |
| `Mission_M8:627` — Shipyards 1 & 2 destroyed Memos | `Patrol4Enemies-H`, `level13:1110` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); 1 отр. / 1 корп. × Фрегат проникновения Радаа; `level13:1189` |
| `Mission_M8:631` — Shipyards 1 & 2 destroyed Memos | `Patrol2Enemies-H`, `level13:1228` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 2 корп. × Фрегат проникновения Радаа; `level13:1213` |
| `Mission_M8:669` — Shipyards 1 & 2 destroyed Memos | `Patrol2enemies`, `level13:1169` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа; 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level13:1191` |
| `Mission_M8:685` — Shipyards 1 & 2 destroyed Memos | `Patrol2enemies`, `level13:1169` | Патруль, один вариант: Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа; 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level13:1191` |
| `Patrol_Setup_M8:13` — Spawn Enemy Resource Collectors | `Patrol4B`, `level13:1306` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1240` |
| `Patrol_Setup_M8:13` — Spawn Enemy Resource Collectors | `Patrol4C`, `level13:1205` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1199` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol1enemies`, `level13:1299` | Патруль, один вариант: Computer1: 4 отр. / 4 корп. × Фрегат проникновения Радаа; `level13:1289` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol4A`, `level13:1173` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1204` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol3C`, `level13:1277` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1201` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol3B`, `level13:1229` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1233` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol2C`, `level13:1304` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1137` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol2B`, `level13:1190` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1207` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol2A`, `level13:1302` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1236` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol1B`, `level13:1141` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1242` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol3A`, `level13:1198` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1109` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol1C`, `level13:1119` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1111` |
| `Patrol_Setup_M8:17` — Spawn Enemy Resource Collectors | `Patrol1A`, `level13:1162` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Переработчик Радаа; `level13:1194` |

### Объявление нового корпуса

**`FI_UnlockBalisticDestroyer`**, `Mission_M8:88`; управляющие связи: **True**. после `M08_020_030_KS` (узел 186). DialogueLine `sharedassets13.assets:15`.

*EN — исходник Quest:*

> The Weapons Architects had ship plans we have put into use: we can now build Ballistic Destroyers, whose advanced Missile Barrage will be needed against the heavy Radaa fleet present in this sector.

*RU — исходная локализация Quest:*

> Среди данных создателей оружия нашлись чертежи, которые мы уже пустили в дело. Теперь мы можем строить баллистические эсминцы. Их мощный ракетный залп поможет нам против тяжёлых кораблей Радаа в этом секторе.

## 11. Mission_M13 — Возвращение на Хиигару

Определение: `dcb65b8cb311f7646b0d3c550ed5761f:1`; карта `level21`; граф `Mission_M13` — `sharedassets21.assets:78`.

DefaultRU **5000**, FleetCap **40**, Carryover **True**, AdditionalRU **600**, MinimumCatchupValue **5000**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| default_groups | `Group_M13_Default_1` | 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 1 отр. / 1 корп. × Тяжёлый крейсер (`Ship_Hgn_HeavyCruiser`); 2 отр. / 2 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`) | `b5903f0952362ef429a6b561421e2f8b:3` |
| default_groups | `Group_M13_Default_2` | 2 отр. / 2 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`); 1 отр. / 1 корп. × Эсминец (`Ship_Hgn_Destroyer`) | `10a6761a4e2dafc41ad9810dc297db15:3` |
| default_groups | `Group_M13_Default_3` | 1 отр. / 1 корп. × Эсминец (`Ship_Hgn_Destroyer`); 4 отр. / 4 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `b07942ad65fba57409ba4d3cc9eaccc7:3` |
| default_groups | `Group_M13_Default_4` | 2 отр. / 2 корп. × Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`); 1 отр. / 1 корп. × Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | `22b79907b3d36b84390e7301671e3736:3` |
| default_groups | `Group_M13_Default_5` | 2 отр. / 2 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`); 1 отр. / 1 корп. × Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | `299a58b4d4449af4498bdbba42db356b:3` |
| additional_groups | `Group_M13_Default_6` | 1 отр. / 1 корп. × Тяжёлый крейсер (`Ship_Hgn_HeavyCruiser`); 2 отр. / 2 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`); 1 отр. / 1 корп. × Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | `ca6cff4db5f6d054c9c04a31f32a3935:3` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level21:1101` |
| scene auto, команда 1024 | `Squadron Spawner (4)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1099` |
| scene auto, команда 0 | `ShieldGenOmega` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level21:1102` |
| scene auto, команда 0 | `ShieldGenDelta` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level21:1106` |
| scene auto, команда 1024 | `Squadron Spawner (6)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1107` |
| scene auto, команда 0 | `ShieldGenBeta` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level21:1108` |
| scene auto, команда 1024 | `WingC1` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1147` |
| scene auto, команда 1024 | `Squadron Spawner (9)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1148` |
| scene auto, команда 1024 | `WingB2` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1151` |
| scene auto, команда 1024 | `Squadron Spawner (6)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1157` |
| scene auto, команда 1024 | `WingB1` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1158` |
| scene auto, команда 0 | `ShieldGenAlpha` | 1 отр. / 1 корп. × Генератор щита Радаа (`Ship_Rad_Shield Emitter`) | `level21:1161` |
| scene auto, команда 1024 | `WingD2` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1162` |
| scene auto, команда 1024 | `Squadron Spawner (4)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1164` |
| scene auto, команда 1024 | `Squadron Spawner (5)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1174` |
| scene auto, команда 1024 | `Squadron Spawner (5)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1177` |
| scene auto, команда 1024 | `WingA2` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1184` |
| scene auto, команда 1024 | `Squadron Spawner (6)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1186` |
| scene auto, команда 1024 | `WingA1` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1201` |
| scene auto, команда 1024 | `WingD1` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1205` |
| scene auto, команда 1024 | `WingC2` | 1 отр. / 1 корп. × Крыло Shatter Station (`Ship_Rad_ShatterStation_SectionWing`) | `level21:1217` |
| scene auto, команда 1024 | `Squadron Spawner (4)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1258` |
| scene auto, команда 1024 | `Squadron Spawner (7)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1265` |
| scene auto, команда 1024 | `FINALTARGET` | 1 отр. / 1 корп. × Консоль Shatter Station (`Ship_Rad_ShatterStation_SectionConsole`) | `level21:1274` |
| scene auto, команда 1024 | `Squadron Spawner (4)` | 1 отр. / 1 корп. × Тяжёлая ракетная платформа Радаа (`Ship_Rad_HeavyMissilePlatform`) | `level21:1281` |

Baseline игрока (без других команд): **24 / 24 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level21:1293`; режим **Whitelist (1)**. Явный список: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_Multi-GunCorvette`, `Build_Kus_HeavyCorvette`, `Build_Kus_EngineerCorvette`, `Build_Kus_AssaultFrigate`, `Build_Kus_IonCannonFrigate`, `Build_Kus_Destroyer`, `Build_Kus_ResourceCollector`, `Build_Kus_HeavyCruiser`, `Build_Kus_BarricadeFrigate`, `Build_Kus_BallisticDestroyer`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `5b65cf980f6ac0840b25e77cb7fd962f:1` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `0d7bc5b32b089264db1adaa1b2126e3a:1` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `0fe69cb7a56059440b20b5f9b9adc2b0:1` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `54183a62c19e10241b0a3c27efdec8bb:1` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `f649bc48a54264b4abb2dd2f80bca332:1` |
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `05e430930eaaa1a4f9e30f7303e25c16:1` |
| Ионный фрегат (`Ship_Hgn_IonCannonFrigate`) | 1/1 | 1800 | 40 | `Build_Kus_IonCannonFrigate`, `8203482b65ce37543af2d2668034b7d7:1` |
| Эсминец (`Ship_Hgn_Destroyer`) | 1/1 | 2500 | 50 | `Build_Kus_Destroyer`, `7572241c9a1a5f047bd6278b52d4a818:1` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `371c36e5b9cdd5a45b72deef74c6cc30:1` |
| Тяжёлый крейсер (`Ship_Hgn_HeavyCruiser`) | 1/1 | 3000 | 70 | `Build_Kus_HeavyCruiser`, `8cb8310b601a0b342987cbc3e6d89916:1` |
| Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | 1/1 | 1700 | 40 | `Build_Kus_BarricadeFrigate`, `f45c8fa0d676a874c8d42ce2b90908fb:1` |
| Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | 1/1 | 2700 | 50 | `Build_Kus_BallisticDestroyer`, `01e918c81218f344986dd720f2fc4f62:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_M13:62` — Wing B Defense | `Patrol_WingB`, `level21:1155` | Патруль, один вариант: Computer1: 4 отр. / 4 корп. × Штурмовой фрегат Радаа; 2 отр. / 6 корп. × Лазерный корвет Радаа; `level21:1141` |
| `Mission_M13:347` — spawn hard version? | `PatrolAroundSStation-H`, `level21:1178` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 1 отр. / 5 корп. × Бомбардировщик Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level21:1244` / ИЛИ / Computer1: 1 отр. / 5 корп. × Штурмовик Радаа; 1 отр. / 3 корп. × Лазерный корвет Радаа; 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level21:1273` / ИЛИ / Computer1: 1 отр. / 3 корп. × Лазерный корвет Радаа; 2 отр. / 2 корп. × Эсминец Радаа; 1 отр. / 3 корп. × Корвет Радаа (исходный тип MissileCorvette); `level21:1251` |
| `Mission_M13:716` — Wing D Defense | `Patrol_WingD`, `level21:1135` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Эсминец Радаа; 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette); `level21:1097` |
| `Mission_M13:768` — Wing A Defense | `Patrol_WingA`, `level21:1216` | Патруль, один вариант: Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа; 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level21:1218` |
| `Mission_M13:796` — patrol around SStation spawner | `PatrolAroundSStation`, `level21:1254` | Патруль, один вариант: Computer1: 1 отр. / 1 корп. × Эсминец Радаа; 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette); `level21:1143` / ИЛИ / Computer1: 3 отр. / 3 корп. × Фрегат проникновения Радаа; `level21:1248` / ИЛИ / Computer1: 3 отр. / 3 корп. × Эсминец Радаа; `level21:1166` |
| `Mission_M13:937` — Wing C Defense | `Patrol_WingC`, `level21:1260` | Патруль, один вариант: Computer1: 3 отр. / 9 корп. × Лазерный корвет Радаа; 2 отр. / 2 корп. × Эсминец Радаа; `level21:1325` |

### Объявление нового корпуса

**`FI_UnlockHeavyCruiser`**, `Mission_M13:766`; управляющие связи: **True**. после `M13_020_210_KS` (узел 644). DialogueLine `sharedassets21.assets:27`.

*EN — исходник Quest:*

> From the wreckage of the Radaa shipyards we recovered technology to build a new ship: Heavy Cruisers have advanced weapon systems optimal for destroying the Shatter Station wings, once their shields are disabled.

*RU — исходная локализация Quest:*

> В обломках верфей Радаа мы нашли технологии, позволившие освоить тяжёлые крейсеры. Их мощное вооружение отлично подходит для уничтожения секций станции «Раскол», когда мы отключим их щиты.

## Отдельно: Mission_T1 — Обучение

Определение: `c77b2064d54d78e408ebc4c27fab4cc6:1`; карта `level23`; граф `Mission_T1` — `sharedassets23.assets:53`.

DefaultRU **5000**, FleetCap **30**, Carryover **False**, AdditionalRU **0**, MinimumCatchupValue **0**.

### DefaultGroups, AdditionalGroups и автоматические размещения

DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.

| Откуда | Группа | Состав: отряды / корпуса | Источник |
|---|---|---|---|
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level23:259` |

Baseline игрока (без других команд): **1 / 1 отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.

### Строительный список

BuildCommandController `level23:322`; режим **Whitelist (1)**. Явный список: `Build_Kus_Interceptor`.

| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |
|---|---:|---:|---:|---|
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `1ee9b427ef5b4614a925a2e7c1d0b29c:1` |

Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.

### Подключённые изменения доступности и выдачи RU

| Граф:узел | Действие и параметры | Управляющий контекст |
|---|---|---|
| `Mission_T1:782` | AddRU: `{"Amount to Add": 1000, "Team ID": "Player1"}` | после `T01_050_010_FI` (узел 91) |

### Дружеские подкрепления и противники, создаваемые сценарием

Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.

| Граф:узел / метка | Спавнер | Состав и команда |
|---|---|---|
| `Mission_T1:147` — waypoint move attack | `PatrolFinal`, `level23:318` | Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа; `level23:318` |
| `Mission_T1:163` — Select Ships | `PlaterSGA`, `level23:330` | игрок: 3 отр. / 15 корп. × Перехватчик; `level23:330` |
| `Mission_T1:187` — Command Palette Select | `PlayerSGB`, `level23:284` | игрок: 3 отр. / 15 корп. × Перехватчик; `level23:284` |
| `Mission_T1:453` — Attack | `EnemySpawn1`, `level23:271` | Computer1: 1 отр. / 5 корп. × Бомбардировщик Радаа; `level23:271` |
| `Mission_T1:718` — waypoint move attack | `PatrolGunPlatform`, `level23:260` | Computer1: 1 отр. / 1 корп. × Орудийная платформа; `level23:260` |

### Объявление нового корпуса

Подключённой реплики FI_Unlock* в этом миссионном графе не найдено. Сюжетные упоминания ремонта/технологий не приравнены к исследованию.

## Сводка подключённых объявлений и карта строительного открытия

| По порядку кампании | Объявление | Подключённый узел |
|---|---|---|
| Mission_M3 | `FI_UnlockHeavyCorvette` | `Mission_M3:432` |
| Mission_M4 | `FI_UnlockEngineerCraft` | `Mission_M4:332` |
| Mission_M5 | `FI_UnlockMultiGunCorvette` | `Mission_M5:56` |
| Mission_M6 | `FI_UnlockAssaultFrigate` | `Mission_M6:451` |
| Mission_M9 | `FI_UnlockBarricadeFrigate` | `Mission_M9_v2:211` |
| Mission_M10 | `FI_UnlockIonFrigate` | `Mission_M10:80` |
| Mission_M11 | `FI_UnlockDestroyer` | `Mission_M11:72` |
| Mission_M8 | `FI_UnlockBalisticDestroyer` | `Mission_M8:88` |
| Mission_M13 | `FI_UnlockHeavyCruiser` | `Mission_M13:766` |

Все девять объявлений имеют управляющие рёбра. Их содержимое — новые корпуса, инженерные работы, захваченные планы или передачи Бентуси. Для HWRM эти этапы можно отобразить через разрешения build/research, но это будет адаптация к механике HWRM, а не найденная исходная Research-очередь.

### Буквальные реплики, сопровождающие реальное восстановление M7/M9

**`M07_Objective_02a`**

*EN — исходник Quest:*

> Harvest 2000 total RU to restore construction sytems.

*RU — исходная локализация Quest:*

> Добудьте в общей сложности 2000 ед. ресурсов, чтобы восстановить кораблестроительные системы.

**`M07_030_050_KS`**

*EN — исходник Quest:*

> Lies or not, we must secure more resources to get the Mothership's construction bays back online.

*RU — исходная локализация Quest:*

> Лгут они или нет, нам нужно больше ресурсов, чтобы восстановить кораблестроительные отсеки Материнского корабля.

**`M07_040_010_TS`**

*EN — исходник Quest:*

> Ship build systems online. Fleet prepare to engage. 

*RU — исходная локализация Quest:*

> Кораблестроительные системы восстановлены. Флот, приготовиться к бою.

**`M09_020_060_BN`**

*EN — исходник Quest:*

> We are aware, and that is why we came Karan S'jet.  First, we have the technology to heal you.  Initiating transfer.

*RU — исходная локализация Quest:*

> Мы знаем о нём. Потому и пришли, Каран С’Джет. Прежде всего, у нас есть технология, способная тебя исцелить. Начинаем передачу.

**`M09_020_070_KS`**

*EN — исходник Quest:*

> Bentusi technology received. Construction bays are online and fully functional.

*RU — исходная локализация Quest:*

> Технология Бентуси получена. Производственные отсеки снова работают в полном объёме.

## Ограничения и воспроизводимость

В исходном аудите зафиксировано **642 ошибок чтения**; это не число потерянных миссий. В этой работе использованы прочитанные 12 MissionDefinition, 46 ShipDefinition, 30 BuildDefinition, MissionDatabase, доступные миссионные/патрульные графы, размещения и строки. Всего в таблицах разрешено **207 ссылок на подключённые цели SpawnEntity**; одна строка не означает уникальную волну.

Цели всех перечисленных подключённых SpawnEntity разрешены по SceneVariables и value-рёбрам, включая встроенные подграфы. Существование Patrol_Setup/GlobalAchievements-макросов учитывается, но команды Patrol не пересчитаны как новые корабли.

Источник данных — `local/quest-campaign` и `local/quest-audit`; ссылки `32hex:path_id` относятся к **Quest-файлам**, не к `resources.assets` Steam. Генератор — `tools/write_quest_progression.py`. Он читает существующую выгрузку и пишет только этот документ; игры, мод и Steam-файлы не изменяет.

Для проверки фактического начала миссии с переносом необходимы конкретное сохранение и сложность. Неиспользуемые шаблоны, disconnected AddRU/PlayDialogue и нейтральные объекты не объявлены бесплатным боевым флотом. Отдельное отсутствие Research-очереди — вывод по найденным структурам и графам, не утверждение о невозможности любой иной реализации в нечитаемых участках версии.
