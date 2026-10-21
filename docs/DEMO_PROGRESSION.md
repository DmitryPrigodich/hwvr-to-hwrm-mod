# Steam-демка: флот, постройка и сюжетные открытия

Этот документ относится **только к установленной Steam-демке**, проверенной по извлечённым данным 17 октября 2026 года. Он не описывает полную Quest-версию и не изменяет мод. Читаемые реплики и задачи на EN/RU — в [DEMO_SCENARIOS.md](DEMO_SCENARIOS.md).

## Важное различие: слот, отряд, физический корабль

Одна запись `GroupInitialization.Members` — **один отряд типа ShipType**, а не обязательно один физический корпус. `State.SpawnGroup` создаёт отряд для каждой записи; `State.SpawnSquadron` создаёт внутри него `ShipStaticData.SquadronCount` кораблей. Поэтому перенос «одна запись Members = один HWRM-корабль» уменьшает исходный флот.

Источники: `local/decompiled-demo/Hercules.Simulation/State.cs`, методы `SpawnSquadron` (около строки 1714, цикл на 1723) и `SpawnGroup` (около 1987); `local/campaign-audit/resources.assets.json`, соответствующий `Hercules.Designer.ShipDefinition`, `_staticData.<SquadronCount>k__BackingField`. Группа Strike Group может содержать несколько таких отрядов.

Начальный флот ниже — предписанный определением миссии плюс автоматические дружеские размещения сцены, **до свободной постройки игроком**. `LoadoutSpawner.BuildLoadout` добавляет `AdditionalGroups` сразу после DefaultGroups/перенесённых групп, а не после сюжетной реплики. У всех четырёх рассматриваемых определений `AllowCarryover=false`.

| Эпизод | RU | Отрядов/крупных единиц на старте | Физических корпусов | Разрешённых строительных типов |
|---|---:|---:|---:|---:|
| T1 | 5000 | 1 | 1 | 1 |
| M1 | 100 | 9 | 37 | 4 |
| M4 | 1200 | 15 | 45 | 6 |
| C1 | 5000 | 1 | 1 | 13 |

В C1 шесть DefaultGroups пусты; отряды игрока для боя не заданы жёстко. В T1 учебные группы выдаются позже. В M4 нейтральный повреждённый эсминец не посчитан частью стартового флота игрока.

### Размеры отрядов, влияющие на числа

| Тип | Корпусов в отряде | Точный источник |
|---|---:|---|
| Материнский корабль (`Ship_Hgn_Mothership`) | 1 | `resources.assets:6358` |
| Штурмовик Радаа (`Ship_Rad_AssaultCraft`) | 5 | `resources.assets:6366` |
| Перехватчик (`Ship_Kus_Interceptor`) | 5 | `resources.assets:6363` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 5 | `resources.assets:6362` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 3 | `resources.assets:6354` |
| Разведчик (`Ship_Kus_Scout`) | 3 | `resources.assets:6365` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 3 | `resources.assets:6359` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1 | `resources.assets:6353` |
| Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`) | 5 | `resources.assets:6377` |
| Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`) | 3 | `resources.assets:6378` |
| Бомбардировщик Радаа (`Ship_Rad_AttackBomber`) | 5 | `resources.assets:6367` |
| Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`) | 3 | `resources.assets:6379` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1 | `resources.assets:6360` |

## Как включается строительство

`BuildCommandController.Awake` применяет список сразу при загрузке сцены. В `BuildCommandList` режим **1 = Whitelist** разрешает только перечисленные команды, **0 = Blacklist** разрешает все недебажные команды, кроме перечисленных. `BuildCommandDatabase.SetUnlockModeAll` всегда блокирует `DebugOnly`; `BuildDefinition.IsUnlocked` читает этот флаг доступности. Это разрешение постройки, а не оплачиваемое исследование технологии.

В доступных графах T1/M1/M4 нет подключённого `SetBuildByBuildList` и нет цепочки покупки/завершения исследований. Их общий подграф `GeneralAchievements` — достижения. Сам класс `SetBuildByBuildList.cs` существует в коде, однако наличие класса ещё не доказывает его использование конкретной картой.

Цены ниже — за **отряд/slot**, не за один физический корпус. Время — `_duration` во время боя; `BuildDefinition.Duration` возвращает 1 секунду в Planning Phase. Множитель сложности/изменение времени симуляции здесь не пересчитывается.

## T1: старт и разрешённая постройка

Определение `Mission_T1_Demo` — `resources.assets:6316`; карта `level1`; RU=5000, FleetCap=30, Carryover=False.

| Источник старта | Группа | Состав | Ссылка |
|---|---|---|---|
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level1:259` |

Контроллер `level1:322`, режим **Whitelist**. Явно перечислено: `Build_Kus_Interceptor`.

| Разрешено построить | Отряд/корпусов | RU | Секунд в бою | BuildDefinition |
|---|---:|---:|---:|---|
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `resources.assets:6260` |

Уроки последовательно открывают управление интерфейсом. Это не новые исследованные корпуса: единственная разрешённая команда постройки весь эпизод — перехватчик. При тактической паузе после ожидания узла 575 срабатывает `AddRU`, узел **782: +1000 RU Player1**.

### Что добавляет сценарий

Таблица перечисляет подключённые SpawnEntity и их реальные цели. Числа — отряды и физические корпуса **за одно срабатывание**. PatrolManager выбирает один вариант и свободный маршрут; повторные таймеры могут давать дополнительные срабатывания. Порядок узлов в таблице по ID служит ссылкой, хронология — в читаемом сценарии.

| Узел графа / группа редактора | Переменная сцены | Что создаётся |
|---|---|---|
| `Mission_T1`:147 — waypoint move attack | `PatrolFinal` → `level1:318` | Радаа/Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrolc`; `level1:318` |
| `Mission_T1`:163 — Select Ships | `PlaterSGA` → `level1:330` | игрок: 3 отр. / 15 корп. × Перехватчик (`Ship_Kus_Interceptor`); теги `PlayerSGA`; `level1:330` |
| `Mission_T1`:187 — Command Palette Select | `PlayerSGB` → `level1:284` | игрок: 3 отр. / 15 корп. × Перехватчик (`Ship_Kus_Interceptor`); теги `PlayerSGB`; `level1:284` |
| `Mission_T1`:453 — Attack | `EnemySpawn1` → `level1:271` | Радаа/Computer1: 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrolA`; `level1:271` |
| `Mission_T1`:718 — waypoint move attack | `PatrolGunPlatform` → `level1:260` | Радаа/Computer1: 1 отр. / 1 корп. × Оружейная платформа (`Ship_Rad_GunPlatform`); теги `patrolG`; `level1:260` |

## M1: старт и разрешённая постройка

Определение `Mission_M1_Demo` — `resources.assets:6314`; карта `level4`; RU=100, FleetCap=30, Carryover=False.

| Источник старта | Группа | Состав | Ссылка |
|---|---|---|---|
| default_groups | `Group_M1_Default_1` | 3 отр. / 15 корп. × Перехватчик (`Ship_Kus_Interceptor`) | `resources.assets:7063` |
| default_groups | `Group_M1_Default_2` | 1 отр. / 5 корп. × Перехватчик (`Ship_Kus_Interceptor`); 3 отр. / 15 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | `resources.assets:7206` |
| default_groups | `Group__RCx1` | 1 отр. / 1 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `resources.assets:6850` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level4:408` |

Контроллер `level4:506`, режим **Whitelist**. Явно перечислено: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_ResourceCollector`.

| Разрешено построить | Отряд/корпусов | RU | Секунд в бою | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `resources.assets:6265` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `resources.assets:6260` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `resources.assets:6252` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `resources.assets:6264` |

Добыча до общей суммы 200 RU и постройка разведчика — последовательные цели `M01_Objective_00`, `_00a`. Сканирование — `_00b`. Контроллер уже разрешил постройку всех четырёх типов; достижение 200 RU не завершает отдельное исследование и не добавляет новый BuildDefinition.

### Что добавляет сценарий

Таблица перечисляет подключённые SpawnEntity и их реальные цели. Числа — отряды и физические корпуса **за одно срабатывание**. PatrolManager выбирает один вариант и свободный маршрут; повторные таймеры могут давать дополнительные срабатывания. Порядок узлов в таблице по ID служит ссылкой, хронология — в читаемом сценарии.

| Узел графа / группа редактора | Переменная сцены | Что создаётся |
|---|---|---|
| `Mission_M1`:120 — cutscene | `Pat_InfiltrationFrigPatrol2` → `level4:410` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `capture, capture3`; `level4:409` |
| `Mission_M1`:183 — spawn patrol A (3) | `Pat_Patrol1A` → `level4:493` | Один из вариантов патруля: Радаа/Computer1: 3 отр. / 15 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); теги `patrolA`; `level4:537` |
| `Mission_M1`:199 — spawn backup every 60 seconds | `Pat_Patrol1E` → `level4:476` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); теги `patrolE`; `level4:501` |
| `Mission_M1`:219 — Build Scout, added bc of beta (HERC-4467) | `Group1C` → `level4:468` | Радаа/Computer1: 1 отр. / 5 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); теги `patrolC`; `level4:468` |
| `Mission_M1`:267 — HSG spawns | `Pat_Patrol1D` → `level4:497` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrolD`; `level4:420` |
| `Mission_M1`:359 — Build Scout | `Spawn_Shipyards` → `level4:442` | нейтральная: 1 отр. / 1 корп. × Верфь Радаа (`Ship_Rad_Shipyard`); теги `Shipyards`; `level4:442` |
| `Mission_M1`:555 — cutscene | `Pat_InfiltrationFrigPatrol1` → `level4:487` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `capture, capture1`; `level4:432` |
| `Mission_M1`:607 — spawn scaries | `Frigate1` → `level4:469` | Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `level4:469` |
| `Mission_M1`:607 — spawn scaries | `Frigate2` → `level4:490` | Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `level4:490` |
| `Mission_M1`:607 — spawn scaries | `Frigate3` → `level4:467` | Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `level4:467` |
| `Mission_M1`:607 — spawn scaries | `Frigate4` → `level4:473` | Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `level4:473` |
| `Mission_M1`:607 — spawn scaries | `Group_EndShips` → `level4:412` | Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `EndShips`; `level4:412` |
| `Mission_M1`:611 — HSG spawns | `Spawn_HyperspaceGate` → `level4:446` | Радаа/Computer1: 1 отр. / 1 корп. × Гиперврата Радаа (`Ship_Rad_HyperSpaceGate`); теги `Carrier`; `level4:446` |
| `Mission_M1`:615 — spawn patrol B (2) | `Pat_Patrol1B` → `level4:426` | Один из вариантов патруля: Радаа/Computer1: 2 отр. / 10 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); теги `patrolB`; `level4:405` |
| `Mission_M1`:631 — cutscene | `Pat_InfiltrationFrigPatrol3` → `level4:479` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `capture, capture2`; `level4:461` |

## M4: старт и разрешённая постройка

Определение `Mission_M4_Demo` — `resources.assets:6315`; карта `level6`; RU=1200, FleetCap=33, Carryover=False.

| Источник старта | Группа | Состав | Ссылка |
|---|---|---|---|
| default_groups | `Group_M4_Default_1` | 2 отр. / 10 корп. × Перехватчик (`Ship_Kus_Interceptor`); 1 отр. / 3 корп. × Разведчик (`Ship_Kus_Scout`) | `resources.assets:7362` |
| default_groups | `Group_M4_Default_2` | 3 отр. / 15 корп. × Ударный бомбардировщик (`Ship_Kus_AttackBomber`); 2 отр. / 6 корп. × Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | `resources.assets:7606` |
| default_groups | `Group_M4_Default_3` | 1 отр. / 5 корп. × Перехватчик (`Ship_Kus_Interceptor`); 2 отр. / 2 корп. × Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | `resources.assets:7354` |
| additional_groups | `Group_M4_Default_4` | 3 отр. / 3 корп. × Инженерный корвет (`Ship_Hgn_EngineerCraft`) | `resources.assets:7353` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level6:1800` |

Контроллер `level6:1989`, режим **Whitelist**. Явно перечислено: `Build_Kus_Scout`, `Build_Kus_Interceptor`, `Build_Kus_AttackBomber`, `Build_Kus_HeavyCorvette`, `Build_Kus_EngineerCorvette`, `Build_Kus_ResourceCollector`.

| Разрешено построить | Отряд/корпусов | RU | Секунд в бою | BuildDefinition |
|---|---:|---:|---:|---|
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `resources.assets:6265` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `resources.assets:6260` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `resources.assets:6252` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `resources.assets:6258` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `resources.assets:6257` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `resources.assets:6264` |

**Три инженера уже входят в старт:** `Group_M4_Default_4` в AdditionalGroups. `FI_UnlockEngineerCraft` (узел 332) произносится после стартового разговора и патрульных появлений, но сам по себе не включает команду постройки: `Build_Kus_EngineerCorvette` разрешён контроллером при загрузке. Аналогично тяжёлый корвет доступен уже при загрузке M4; его отдельная строка открытия в этих трёх графах не подключена.

На карте также автоматически размещён **нейтральный повреждённый эсминец**, `level6:1930`, теги `DamagedDestroyer`, `Capturable`. После сцепления инженеров граф меняет его команду на Computer2, а не добавляет обычный свободно управляемый эсминец в стартовый флот игрока: узел 65 `SetEntityTeamId`.

### Что добавляет сценарий

Таблица перечисляет подключённые SpawnEntity и их реальные цели. Числа — отряды и физические корпуса **за одно срабатывание**. PatrolManager выбирает один вариант и свободный маршрут; повторные таймеры могут давать дополнительные срабатывания. Порядок узлов в таблице по ID служит ссылкой, хронология — в читаемом сценарии.

| Узел графа / группа редактора | Переменная сцены | Что создаётся |
|---|---|---|
| `Mission_M4`:21 — spawn from HSG | `Patrol` → `level6:1937` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrol`; `level6:2061` |
| `Mission_M4`:21 — spawn from HSG | `Patrol2` → `level6:1941` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrol2`; `level6:1849` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); теги `patrol2`; `level6:1895` |
| `Mission_M4`:25 — Destroyer on way to mothership, Set Elimiate Gate Objective | `HyperspaceGate` → `level6:1825` | Радаа/Computer1: 1 отр. / 1 корп. × Гиперврата Радаа (`Ship_Rad_HyperSpaceGate`); теги `Radaa_Hyperspacegate`; `level6:1825` |
| `Mission_M4`:67 — Destroyer on way to mothership, Set Elimiate Gate Objective | `Group_HSGDefense` → `level6:1876` | Радаа/Computer1: 2 отр. / 10 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `Radaa_Hyperspace`; `level6:1876` |
| `Mission_M4`:366 — Destroyer on way to mothership, Set Elimiate Gate Objective | `Patrol Final Wave` → `level6:1905` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 4 отр. / 20 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrol_final_wave`; `level6:1821` |
| `Mission_M4`:420 — Starting cutscene and objective | `PatrolStart` → `level6:1961` | Один из вариантов патруля: Радаа/Computer1: 2 отр. / 10 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrol_start`; `level6:1906` |
| `Mission_M4`:420 — Starting cutscene and objective | `EdgePatrol` → `level6:1934` | Один из вариантов патруля: Радаа/Computer1: 2 отр. / 10 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 10 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `level6:1939` |
| `Mission_M4`:422 — Start of mission | `RC2` → `level6:1896` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 2 корп. × Мобильный переработчик Радаа (`Ship_Rad_MobileRefinery`); теги `—`; `level6:1866` |
| `Mission_M4`:422 — Start of mission | `RC3` → `level6:1960` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 2 корп. × Мобильный переработчик Радаа (`Ship_Rad_MobileRefinery`); теги `—`; `level6:1846` |
| `Mission_M4`:422 — Start of mission | `RC1` → `level6:1857` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 2 отр. / 2 корп. × Мобильный переработчик Радаа (`Ship_Rad_MobileRefinery`); теги `—`; `level6:1954` |
| `Mission_M4`:494 — spawn from HSG | `Patrol` → `level6:1937` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrol`; `level6:2061` |
| `Mission_M4`:494 — spawn from HSG | `Patrol2` → `level6:1941` | Один из вариантов патруля: Радаа/Computer1: 1 отр. / 5 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 1 отр. / 5 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `patrol2`; `level6:1849` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); теги `patrol2`; `level6:1895` |

## C1: старт и разрешённая постройка

Определение `Mission_C1` — `resources.assets:6319`; карта `level9`; RU=5000, FleetCap=40, Carryover=False.

| Источник старта | Группа | Состав | Ссылка |
|---|---|---|---|
| default_groups | `Group_C3_Default_1` | Пустая группа: 0 отрядов, 0 корпусов | `resources.assets:7830` |
| default_groups | `Group_C3_Default_2` | Пустая группа: 0 отрядов, 0 корпусов | `resources.assets:7133` |
| default_groups | `Group_C3_Default_3` | Пустая группа: 0 отрядов, 0 корпусов | `resources.assets:7132` |
| default_groups | `Group_C3_Default_4` | Пустая группа: 0 отрядов, 0 корпусов | `resources.assets:7131` |
| default_groups | `Group_C3_Default_5` | Пустая группа: 0 отрядов, 0 корпусов | `resources.assets:7130` |
| default_groups | `Group_C3_Default_6` | Пустая группа: 0 отрядов, 0 корпусов | `resources.assets:7129` |
| scene auto | `Mothership` | 1 отр. / 1 корп. × Материнский корабль (`Ship_Hgn_Mothership`) | `level9:436` |

Контроллер `level9:508`, режим **Blacklist**. Явно перечислено: `Build_Kus_Carrier`, `Build_Kus_MobileRefinery`.

| Разрешено построить | Отряд/корпусов | RU | Секунд в бою | BuildDefinition |
|---|---:|---:|---:|---|
| Штурмовой фрегат (`Ship_Hgn_AssaultFrigate`) | 1/1 | 1600 | 35 | `Build_Kus_AssaultFrigate`, `resources.assets:6251` |
| Ударный бомбардировщик (`Ship_Kus_AttackBomber`) | 1/5 | 750 | 20 | `Build_Kus_AttackBomber`, `resources.assets:6252` |
| Баллистический эсминец (`Ship_Hgn_BallisticDestroyer`) | 1/1 | 2700 | 50 | `Build_Kus_BallisticDestroyer`, `resources.assets:6253` |
| Баррикадный фрегат (`Ship_Hgn_BarricadeFrigate`) | 1/1 | 1700 | 40 | `Build_Kus_BarricadeFrigate`, `resources.assets:6254` |
| Эсминец (`Ship_Hgn_Destroyer`) | 1/1 | 2500 | 50 | `Build_Kus_Destroyer`, `resources.assets:6256` |
| Инженерный корвет (`Ship_Hgn_EngineerCraft`) | 1/1 | 500 | 15 | `Build_Kus_EngineerCorvette`, `resources.assets:6257` |
| Тяжёлый корвет (`Ship_Hgn_HeavyCorvette`) | 1/3 | 800 | 25 | `Build_Kus_HeavyCorvette`, `resources.assets:6258` |
| Тяжёлый крейсер (`Ship_Hgn_HeavyCruiser`) | 1/1 | 3000 | 70 | `Build_Kus_HeavyCruiser`, `resources.assets:6259` |
| Перехватчик (`Ship_Kus_Interceptor`) | 1/5 | 500 | 20 | `Build_Kus_Interceptor`, `resources.assets:6260` |
| Ионный фрегат (`Ship_Hgn_IonCannonFrigate`) | 1/1 | 1800 | 40 | `Build_Kus_IonCannonFrigate`, `resources.assets:6261` |
| Многопушечный корвет (`Ship_Hgn_Multi-GunCorvette`) | 1/3 | 750 | 25 | `Build_Kus_Multi-GunCorvette`, `resources.assets:6263` |
| Сборщик ресурсов (`Ship_Hgn_ResourceCollector`) | 1/1 | 600 | 15 | `Build_Kus_ResourceCollector`, `resources.assets:6264` |
| Разведчик (`Ship_Kus_Scout`) | 1/3 | 200 | 12 | `Build_Kus_Scout`, `resources.assets:6265` |

**Это BLACKLIST.** `Build_Kus_Carrier` и `Build_Kus_MobileRefinery` не предлагаются к обычной постройке. Остальные 13 недебажных типов открыты с начала сцены; по мере волн отдельные новые типы контроллер не исследует и не открывает.

## Условия появления, которые легко перепутать

- **T1:** 163 создаёт StrikeGroupA, 187 — StrikeGroupB: каждая содержит 3 отряда перехватчиков, то есть 15 корпусов. Уничтожаемые учебные цели — реальные Radaa-типы в симуляции, но с учебными ограничениями/неуязвимостью; это не новый союзный флот.
- **M1:** после постройки разведчика узел 219 создаёт один отряд штурмовиков Радаа (5 корпусов), а узел 359 — нейтральную верфь Радаа. Затем последовательно идут patrolC → patrolB → patrolA. Предательство создаёт по одному ракетному/инфильтрационному фрегату узлами 555/120/631.
- **M1:** `CreateHealthEvent` 273 следит за тегом `capture` на пороге 99% и вызывает `spawnHSG`. Этот обработчик создаёт врата (611) и патруль D (267). Патруль E повторяется узлом 199/таймером 557 через 60 секунд; уничтожение группы с тегом `Carrier` останавливает таймер. Гиперврата имеют именно этот неожиданный тег.
- **M1:** финальная группа 607 создаёт ещё четыре отдельных missile-frigate spawner и EndShips. Это угроза для постановочного отхода, а не обязательные новые цели на уничтожение.
- **M4:** RC1/RC2/RC3 в узле 422 — три вражеских патруля; каждый содержит два переработчика Радаа и один фрегат. Это **6 вражеских переработчиков + 3 фрегата**, не выдача ресурсных кораблей игроку. Два своих сборщика уже содержатся в стартовом Group_M4_Default_3.
- **M4:** после сцепления трёх инженеров (OnSquadronCaptured 508) начинается буксировка. Гиперврата и охрана появляются узлами 25/67; финальная волна — 366. Патрули 21/494 также зависят от зон маршрута и повторной логики. Узел AddRU 474 содержит **0 RU**, денежной наградой его считать нельзя.

## C1: пул противников и волны

`level9:486`, ChallengeModeController: 20 WaveDefinition; 42 секунды до первой волны, 50 секунд между появлениями, отсчёт последующих волн — за 10 секунд. До уничтожения предыдущей волны контроллер не ждёт. В таблице — допустимые типы/составы групп, **не фиксированное количество врагов волны**. Количество повторений групп выбирается по бюджету мощности; одинаковые типы могут набираться несколько раз.

| Волна | WaveDefinition | Допустимые группы для набора |
|---:|---|---|
| 1 | `Wave_Test1`, `sharedassets9.assets:82` | Радаа/Computer1: 1 отр. / 5 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); теги `—`; `sharedassets9.assets:122` |
| 2 | `Wave_Test2`, `sharedassets9.assets:93` | Радаа/Computer1: 3 отр. / 15 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); теги `—`; `sharedassets9.assets:114` / ИЛИ / Радаа/Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:116` |
| 3 | `Wave_Test3`, `sharedassets9.assets:95` | Радаа/Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:116` / ИЛИ / Радаа/Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:112` / ИЛИ / Радаа/Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:104` |
| 4 | `Wave_Test4`, `sharedassets9.assets:96` | Радаа/Computer1: 3 отр. / 15 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:116` / ИЛИ / Радаа/Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:112` / ИЛИ / Радаа/Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:104` |
| 5 | `Wave_Test5`, `sharedassets9.assets:97` | Радаа/Computer1: 2 отр. / 10 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:112` / ИЛИ / Радаа/Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:104` / ИЛИ / Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 3 отр. / 15 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); теги `—`; `sharedassets9.assets:117` |
| 6 | `Wave_Test6`, `sharedassets9.assets:98` | Радаа/Computer1: 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 10 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:104` / ИЛИ / Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 3 отр. / 15 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); теги `—`; `sharedassets9.assets:117` |
| 7 | `Wave_Test7`, `sharedassets9.assets:99` | Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 3 отр. / 15 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); теги `—`; `sharedassets9.assets:117` / ИЛИ / Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 3 отр. / 9 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); теги `—`; `sharedassets9.assets:119` / ИЛИ / Радаа/Computer1: 3 отр. / 15 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); теги `—`; `sharedassets9.assets:105` |
| 8 | `Wave_Test8`, `sharedassets9.assets:100` | Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 3 отр. / 9 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); теги `—`; `sharedassets9.assets:119` / ИЛИ / Радаа/Computer1: 3 отр. / 15 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); теги `—`; `sharedassets9.assets:105` |
| 9 | `Wave_Test9`, `sharedassets9.assets:101` | Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 3 отр. / 15 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:118` / ИЛИ / Радаа/Computer1: 3 отр. / 9 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:108` |
| 10 | `Wave_Test10`, `sharedassets9.assets:83` | Радаа/Computer1: 2 отр. / 2 корп. × Штурмовой фрегат Радаа (`Ship_Rad_Frigate`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 3 отр. / 15 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:118` / ИЛИ / Радаа/Computer1: 3 отр. / 9 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:108` |
| 11 | `Wave_Test11`, `sharedassets9.assets:84` | Радаа/Computer1: 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); теги `—`; `sharedassets9.assets:107` |
| 12 | `Wave_Test12`, `sharedassets9.assets:85` | Радаа/Computer1: 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 4 отр. / 12 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); теги `—`; `sharedassets9.assets:107` / ИЛИ / Радаа/Computer1: 3 отр. / 15 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 3 отр. / 3 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); теги `—`; `sharedassets9.assets:123` |
| 13 | `Wave_Test13`, `sharedassets9.assets:86` | Радаа/Computer1: 3 отр. / 15 корп. × Штурмовик Радаа (`Ship_Rad_AssaultCraft`); 3 отр. / 3 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); теги `—`; `sharedassets9.assets:123` / ИЛИ / Радаа/Computer1: 4 отр. / 12 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 3 отр. / 3 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); теги `—`; `sharedassets9.assets:111` |
| 14 | `Wave_Test14`, `sharedassets9.assets:87` | Радаа/Computer1: 4 отр. / 12 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 3 отр. / 3 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); теги `—`; `sharedassets9.assets:111` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 4 отр. / 20 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:121` |
| 15 | `Wave_Test15`, `sharedassets9.assets:88` | Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 4 отр. / 20 корп. × Бомбардировщик Радаа (`Ship_Rad_AttackBomber`); теги `—`; `sharedassets9.assets:121` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:115` |
| 16 | `Wave_Test16`, `sharedassets9.assets:89` | Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:115` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); 3 отр. / 3 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:120` |
| 17 | `Wave_Test17`, `sharedassets9.assets:90` | Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 1 отр. / 1 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 6 корп. × Корвет Радаа (исходный тип MissileCorvette) (`Ship_Rad_MissileCorvette`); 3 отр. / 3 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:120` / ИЛИ / Радаа/Computer1: 3 отр. / 3 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 10 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); теги `—`; `sharedassets9.assets:109` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:106` |
| 18 | `Wave_Test18`, `sharedassets9.assets:91` | Радаа/Computer1: 3 отр. / 3 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 10 корп. × Лучевой истребитель Радаа (`Ship_Rad_LanceFighter`); теги `—`; `sharedassets9.assets:109` / ИЛИ / Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:106` / ИЛИ / Радаа/Computer1: 2 отр. / 2 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); теги `—`; `sharedassets9.assets:113` |
| 19 | `Wave_Test19`, `sharedassets9.assets:92` | Радаа/Computer1: 1 отр. / 1 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 6 корп. × Лазерный корвет Радаа (`Ship_Rad_LaserCorvette`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); 2 отр. / 2 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:106` / ИЛИ / Радаа/Computer1: 2 отр. / 2 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 2 отр. / 2 корп. × Эсминец Радаа (`Ship_Rad_Destroyer`); теги `—`; `sharedassets9.assets:113` |
| 20 | `Wave_Test20`, `sharedassets9.assets:94` | Радаа/Computer1: 3 отр. / 3 корп. × Линейный крейсер Радаа (`Ship_Rad_Battlecruiser`); 4 отр. / 4 корп. × Фрегат проникновения Радаа (`Ship_Rad_MissileFrigate`); теги `—`; `sharedassets9.assets:110` |

## Реплики об открытиях: что подключено, а что только лежит в таблицах

**Оплачиваемого дерева исследований в этих четырёх сценах не найдено.** В трёх миссионных графах корпуса доступны через списки сцены, задачи и интерфейсные ограничения. C1 с начала разрешает почти весь недебажный набор. Слова «technology», «engineering» и «can now build» в диалоге не означают автоматического существования отдельного исследования.

Ниже сохранены буквальные EN и RU. Из перечисленных объявлений в доступных трёх графах реально подключено только `FI_UnlockEngineerCraft`. Остальные строки присутствуют в Steam-демке как материал дальнейшей кампании; их карты/условия открытия по одним этим строкам не восстановлены.

### `FI_UnlockHeavyCorvette`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockHeavyCorvette`.

**Разведка флота** — `FI_UnlockHeavyCorvette`

*EN — исходный текст:*

> Our ongoing repairs to the Mothership has added ship build capabilities: we can now build Heavy Corvettes. Their armor is ideal against heavy ballistics from the gun platforms we have detected in this sector.

*RU — новый перевод:*

> В ходе ремонта Материнского корабля мы расширили его производственные возможности. Теперь можно строить тяжёлые корветы. Их броня хорошо защищает от тяжёлых снарядов орудийных платформ, обнаруженных в этом секторе.

### `FI_UnlockEngineerCraft`

Статус: **Mission_M4:332**. Источник текста: `Strings_Missions`, ключ `FI_UnlockEngineerCraft`.

**Разведка флота** — `FI_UnlockEngineerCraft`

*EN — исходный текст:*

> Resources claimed from Gybbas allow us to build a new ship: the Engineer Craft, which has the ability to repair ships in their Strike Group. They are also key to capturing the Radaa Destroyer in this sector.

*RU — новый перевод:*

> Ресурсы, добытые в Гиббасе, позволили нам освоить новый корабль — инженерный корвет. Он способен ремонтировать корабли своей ударной группы. Эти корветы также понадобятся для захвата эсминца Радаа в этом секторе.

### `FI_UnlockMultiGunCorvette`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockMultiGunCorvette`.

**Разведка флота** — `FI_UnlockMultiGunCorvette`

*EN — исходный текст:*

> Our engineering team has added capability to our construction bays: Multi-Gun Corvettes. These are ideal for counter-attack against the Radaa's fast-moving threats to the shipyard.

*RU — новый перевод:*

> Наши инженеры расширили возможности сборочных цехов: теперь мы можем строить многопушечные корветы. Они отлично подходят для перехвата быстрых кораблей Радаа, угрожающих верфи.

### `FI_UnlockAssaultFrigate`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockAssaultFrigate`.

**Разведка флота** — `FI_UnlockAssaultFrigate`

*EN — исходный текст:*

> With the technology transferred from the Shipyard, we can build a new ship: Assault Frigates. These heavy weapon craft are ideal for penetrating the Radaa defenses guarding the shield emitters.

*RU — новый перевод:*

> Технологии, полученные с верфи, позволили нам освоить новый тип кораблей — штурмовые фрегаты. Их тяжёлое вооружение отлично подходит для прорыва обороны Радаа, прикрывающей генераторы щита.

### `FI_UnlockBarricadeFrigate`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockBarricadeFrigate`.

**Разведка флота** — `FI_UnlockBarricadeFrigate`

*EN — исходный текст:*

> With the technology the Bentusi provided, our construction bays can now build Barricade Frigates. When activated, these can provide shields for nearby ships. They can also be used to protect the Bentusi.

*RU — новый перевод:*

> Благодаря технологиям Бентуси наши сборочные цеха теперь могут выпускать баррикадные фрегаты. При активации они прикрывают щитом находящиеся рядом корабли. С их помощью можно защитить и самих Бентуси.

### `FI_UnlockIonFrigate`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockIonFrigate`.

**Разведка флота** — `FI_UnlockIonFrigate`

*EN — исходный текст:*

> The Bentusi also provided us the key components necessary to build a new ship class: Ion Frigates, which are ideal for long range attacks and cutting into the hulls of larger ships.

*RU — новый перевод:*

> Бентуси также передали нам ключевые компоненты для нового класса кораблей — ионных фрегатов. Они отлично подходят для дальнего боя и способны прожигать корпуса крупных кораблей.

### `FI_UnlockDestroyer`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockDestroyer`.

**Разведка флота** — `FI_UnlockDestroyer`

*EN — исходный текст:*

> Our ship construction capabilities have been upgraded to build a new ship: Destroyers. These capital class ships have weapon systems most effective against squadrons of strike craft.

*RU — новый перевод:*

> Мы расширили возможности сборочных цехов и можем строить новый тип кораблей — эсминцы. Вооружение этих крупных боевых кораблей особенно эффективно против эскадрилий ударных кораблей.

### `FI_UnlockBalisticDestroyer`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockBalisticDestroyer`.

**Разведка флота** — `FI_UnlockBalisticDestroyer`

*EN — исходный текст:*

> The Weapons Architects had ship plans we have put into use: we can now build Ballistic Destroyers, whose advanced Missile Barrage will be needed against the heavy Radaa fleet present in this sector.

*RU — новый перевод:*

> Среди данных создателей оружия нашлись чертежи, которые мы уже пустили в дело. Теперь мы можем строить баллистические эсминцы. Их мощный ракетный залп поможет нам против тяжёлых кораблей Радаа в этом секторе.

### `FI_UnlockHeavyCruiser`

Статус: **Только строка в таблице; нет вызова в T1/M1/M4**. Источник текста: `Strings_Missions`, ключ `FI_UnlockHeavyCruiser`.

**Разведка флота** — `FI_UnlockHeavyCruiser`

*EN — исходный текст:*

> From the wreckage of the Radaa shipyards we recovered technology to build a new ship: Heavy Cruisers have advanced weapon systems optimal for destroying the Shatter Station wings, once their shields are disabled.

*RU — новый перевод:*

> В обломках верфей Радаа мы нашли технологии, позволившие освоить тяжёлые крейсеры. Их мощное вооружение отлично подходит для уничтожения секций станции «Раскол», когда мы отключим их щиты.

### Другие связанные реплики в доступных миссиях

Это сюжет/инструкции о ресурсах, строительстве и технологиях, а не дополнительные найденные исследования.

Подключение: `Mission_T1:91`.

**Разведка флота** — `T01_050_010_FI`

*EN — исходный текст:*

> Tactical Pause allows you to stop the action so that you can plan your next moves, including spending Resources to build new ships. 

*RU — новый перевод:*

> Тактическая пауза останавливает происходящее и позволяет спланировать дальнейшие действия, в том числе потратить ресурсы на постройку новых кораблей.

Подключение: `Mission_M1:231`.

**Разведка флота** — `M01_025_010_FI`

*EN — исходный текст:*

> Necessary Resources secured.  Continuing to gather Resources is important for Mothership systems health, and keeps our construction bays capable of building more ships.

*RU — новый перевод:*

> Необходимые ресурсы собраны. Продолжайте добычу: ресурсы нужны для поддержания систем Материнского корабля и работы его кораблестроительных отсеков.

Подключение: `Mission_M1:323`.

**Разведка флота** — `M01_025_020_FI`

*EN — исходный текст:*

> We now have the Resources to build a Scout unit so we can pinpoint the location of the Radaa.

*RU — новый перевод:*

> Теперь у нас достаточно ресурсов, чтобы построить разведчик и точно определить местоположение Радаа.

Подключение: `Mission_M1:429`.

**Каран С’Джет** — `M01_050_020_KS`

*EN — исходный текст:*

> Intelligence reports say the Radaa utilize very high level technology, but I haven't seen anything remarkable yet.

*RU — новый перевод:*

> По данным разведки, Радаа владеют весьма передовыми технологиями. Но пока я не увидела ничего особенного.

Подключение: `Mission_M1:60`.

**Амма Радаа** — `M01_060_030_AR`

*EN — исходный текст:*

> In return for a considerable investment from us, the Taiidani Emperor agreed to share all technology related to a Hyperspace Core.

*RU — новый перевод:*

> В обмен на наши значительные вложения таииданский император согласился передать нам все технологии, связанные с гиперпространственным ядром.

Подключение: `Mission_M4:496`.

**Разведка флота** — `M04_040_040_FI`

*EN — исходный текст:*

> Transporting the Destroyer will require multiple Engineer Craft.

*RU — новый перевод:*

> Для буксировки эсминца потребуется несколько инженерных корветов.

## Что не следует принимать за реальное подкрепление

В сценах есть шаблоны GroupSpawner/SquadronSpawner, у которых `_autoSpawn=0` и нет подключённого появления в найденных графах. Например, `level4:433` — большая дружеская тестовая ClusterInterceptors-группа; `level4:439` — отдельный сборщик. Они не добавлены в стартовый флот и не посчитаны подкреплениями только потому, что записи существуют в сцене. Аналогично текст нового корабля в Strings_Missions не добавляет его автоматически в строительство.

## Источники и границы

- `local/campaign/missions.json`: Mission_T1_Demo/M1_Demo/M4_Demo и Mission_C1; стартовые RU, DefaultGroups, AdditionalGroups, Carryover и FleetCap.
- `local/campaign/level1.json`, `level4.json`, `level6.json`, `level9.json`: сохранённые группы, сцены, переменные и размещения.
- `local/campaign-audit/level*.json` и `resources.assets.json`: исходные BuildCommandController, BuildDefinition, ShipDefinition и PatrolManager; точные source:path_id приведены рядом с записями.
- `local/campaign/Mission_{T1,M1,M4}-graph.json`: ID конкретных управляющих узлов появления и реплик.
- `local/decompiled-demo/Hercules/LoadoutSpawner.cs`: DefaultGroups/AdditionalGroups и назначение RU.
- `local/decompiled-demo/Hercules.Designer/{BuildCommandController,BuildCommandList,BuildCommandDatabase,BuildDefinition}.cs`: whitelist/blacklist, debug-флаги, цена и время.
- `local/decompiled-demo/Hercules.Designer.Mission/PatrolManager.cs` и `SpawnEntity.cs`: выбор состава/маршрута и запуск спавнеров.
- `local/decompiled-demo/Hercules.Designer/ChallengeModeController.cs`: волны и победа C1.

Это статический разбор извлечённых данных и декомпиляции, без запуска игры. Он фиксирует правила сцены, а не измеренное конкретное прохождение. Привязка строк дальнейших эпизодов к отсутствующим картам здесь не выдумывается; полная Quest-версия должна рассматриваться отдельным источником.
