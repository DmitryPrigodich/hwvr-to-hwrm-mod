# Vast Reaches: сценарий кампании на русском и английском

Источник: предоставленные APK/OBB **1.1.0-16520**, без запуска игры. Это отдельная, более ранняя версия, а не дополнение к Steam-демке той же ревизии. В ней найдены 11 игровых миссий кампании, отдельное обучение, вступления и финальная сцена. Бонуса C1 в списке сцен этой сборки нет.

Русский текст заново переведён с английского оригинала с учётом сюжета, говорящих и терминологии Homeworld. Рядом сохранён английский оригинал; плохая исходная русская локализация доступна отдельно в [QUEST_SCENARIOS_RAW.md](QUEST_SCENARIOS_RAW.md). Перевод не добавляет новых сюжетных событий, исследований или реплик. Состав флота, постройка и сюжетные открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md); сравнение ресурсов — в [QUEST_COMPARISON.md](QUEST_COMPARISON.md).

Порядок глав взят из MissionDatabase, он отличается от номеров внутренних M-файлов. Беседы сгруппированы по сценам диалога, а порядок реплик внутри связан управляющими рёбрами графа. **Независимые обработчики событий и развилки не образуют одну обязательную цепочку**: условия и ID узлов приведены рядом. Нумерация ключей используется для именования бесед, а не как доказательство очередности игры. Вступления упорядочены по времени клипов Timeline.

FI — разведка флота; TS — Тирра Собан; KS — Каран С’Джет; AR — Амма; GR — Гиитан. Смысл HA зависит от сцены: во вступлении M1 это рассказчик, в репликах верфи — её главный инженер.

## M0. Обучение / Tutorial

Определение `c77b2064d54d78e408ebc4c27fab4cc6:1`, карта `level23`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M1 - Hiigara Proving Grounds/M1_Animatic_Intro/M1_Animatic_Intro.unity`

*Клип начинается в 1.28 с.*

`M01_010_010_A_HA`

RU:

> После долгих лет изгнания мы, хиигаряне, наконец обрели мир на родной планете.

EN:

> After a long exile, we Hiigarans at last welcomed peace in our home.

*Клип начинается в 7.60 с.*

`M01_010_020_A_HA`

RU:

> Наш великий Материнский корабль, с которым Каран С’Джет слилась воедино, став его командиром, навигатором и живым ядром, позволил нашему народу проложить огненный путь из изгнания к дому и свободе. Теперь он покоится на орбите Хиигары — памятник той эпохе и великому поколению, пожертвовавшему всем, чтобы найти и вернуть наш родной мир.

EN:

> Our great Mothership, with Karan S'jet fused as its Commander, Navigator and living core, allowed our people to carve a fiery path from exile to home and freedom. Now the Mothership rests in orbit around Hiigara, a tribute to those times and the great generation that sacrificed everything to find and claim our Homeworld.

*Клип начинается в 30.07 с.*

`M01_010_030_A_HA`

RU:

> Таииданская империя пала, но хиигарян, едва вернувшихся домой, застала врасплох короткая и смертоносная война с Тварью. Дайамид, правящий совет Хиигары, болезненно осознавал, насколько хиигаряне одиноки в Галактике. Поэтому предложение Радаа — межзвёздных торговцев, владевших собственными загадочными технологиями, — заключить союз и наладить обмен встретило самый тёплый приём.

EN:

> Though the Taiidani empire had fallen, the new Hiigarans were caught off guard by the short but deadly BeastWar. The Daiamid, the ruling council of the Hiigaran people, were painfully aware that they were alone in the Galaxy. So when the Radaa - interstellar traders with their own mysterious technology - approached with offers of an alliance and exchange, the Daiamid was very receptive.

*Клип начинается в 53.08 с.*

`M01_010_040_A_HA`

RU:

> Радаа считали, что долгий мир делает нас всё уязвимее. Их предводительница, Коммандер Амма, предупреждала: осколки Таииданской империи, превратившиеся во владения военных вождей, снова вооружаются, и возникновение новой империи вполне возможно. В обмен на разрешение строить и добывать ресурсы в системе Хиигары Коммандер Амма предложила помочь нашему флоту вступить в новую эпоху развития и перевооружения.

EN:

> The Radaa believed that the longer we were at peace, the more vulnerable we became. Their leader, Commander Amma, warned that former Taiidani bandit kingdoms were re-arming and a new Empire was a real possibility.  In exchange for permission to build and mine in the Hiigaran star system, Commander Amma offered to shepherd the Hiigaran Fleet through a new era of modernization and growth.

*Клип начинается в 79.07 с.*

`M01_010_050_A_HA`

RU:

> Вместе с новыми союзниками мы начали создавать новую военную силу. Мы также вернули в строй и восстановили первый Материнский корабль. Радаа проявляли особый интерес к кораблю, сокрушившему Таииданскую империю.

EN:

> So we began to forge a new military force with our new allies.  We also pulled the original Mothership out of retirement and built her back up.  The Radaa were very interested in the Ship that had defeated the Taiidani Empire.

*Клип начинается в 93.98 с.*

`M01_010_060_A_HA`

RU:

> Каран С’Джет давно отошла от дел, но по-прежнему оставалась единственной, кто научился управлять Материнским кораблём через прямую связь с его ядром Предтеч. Она согласилась вернуться к работе над кораблём, но на этот раз лишь в качестве наставницы. Право на покой она заслужила.

EN:

> Karan S'jet retired years ago, but she was still the only being that had learned to control the Mothership by direct link to its Progenitor core. She agreed to return to the Mothership project but this time only as an instructor. She had earned her peace.

*Клип начинается в 110.72 с.*

`M01_010_070_A_HA`

RU:

> Роль Командующего Флотом переняла Тирра Собан. Закалённый в боях ветеран, она прошла через множество битв в разваливающейся Таииданской Империи и разгромила десятки банд рейдеров.

EN:

> The role of Fleet Command fell to Tyrra Soban. A peerless military veteran, she had fought countless battles in the splintering remains of the Taiidani empire, and had broken up dozens of Raider groups.

*Клип начинается в 122.95 с.*

`M01_010_080_A_HA`

RU:

> Чтобы принять командование Материнским кораблём и флотом, Тирра прошла ту же процедуру, что и Каран С’Джет за несколько десятилетий до неё. Она была опытным бойцом, и всем было понятно, что Материнский Корабль теперь — боевое судно без всяких оговорок. Тирра Собан стала второй Освобождённой среди нашего народа.

EN:

> To take command of the Mothership and the Fleet, she underwent the same process that Karan S'jet had decades before. She was a trained warrior and that would make it clear to anyone that the Mothership was now a warship, pure and direct.Tyrra Soban was only the second of our people to become unbound.

### Задачи, подключённые к графу

Узлы: 89, 391, 503, 555.

`MT01_Objective_01`

RU:

> Уничтожьте корабли-мишени, избегая орудийной платформы.

EN:

> Destroy Target Ships while avoiding Gun Platform.

Узлы: 105, 193, 249, 427, 479, 701, 778.

`MT01_Objective_02`

RU:

> Выполните все упражнения учебной программы.

EN:

> Complete each exercise of the training regimen.

### T01_010

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #764`.

Узел `Mission_T1#259`.

`T01_010_010_TS`

RU:

> Командование... на связи...

EN:

> Command... on-line...

Узел `Mission_T1#567`.

`T01_010_020_KS`

RU:

> Всё хорошо, Командование флота... К слиянию с Материнским кораблём нужно привыкнуть. Вспомни обучение... Доверься кораблю, не цепляйся за каждый поток данных.

EN:

> It's ok, Fleet Command... Being fused with the Mothership takes getting used to.  Remember your training...flow with the ship, don't grasp at the data.  

Узел `Mission_T1#405`.

`T01_010_030_TS`

RU:

> Тебя хорошо слышно, Каран. Но я слышу всё сразу... Невероятно!

EN:

> You're coming in clear, Karan.  But I can hear everything at the same time...it's amazing!

Узел `Mission_T1#409`.

`T01_010_040_KS`

RU:

> Сейчас Разведка флота проведёт с тобой несколько упражнений, командующая. Но я рядом — можешь обращаться и ко мне.

EN:

> Fleet Intelligence will take you through some exercises now Commander.  But I'm here and you can call on me as well.  

### T01_020

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #181`.

Узел `Mission_T1#515`.

`T01_020_010_FI`

RU:

> Офицер Разведки флота на связи. Моя задача — собирать информацию, анализировать данные сенсоров и ставить задачи.

EN:

> Fleet Intelligence Officer on-line. My task is to collate information, analyze sensor data and provide objectives.  

Узел `Mission_T1#798`.

`T01_020_020_FI`

RU:

> Для начала я проведу проверку систем. Откройте карту сенсоров.

EN:

> First I will guide you through systems tests.  Open the Sensors Manager now.

Узел `Mission_T1#231`.

`T01_020_030_FI`

RU:

> Карта сенсоров показывает окружающее пространство, включая центр управления операциями — Материнский корабль.

EN:

> The Sensors Manager shows you a map of your local environment, including the heart of command operations, the Mothership.

Узел `Mission_T1#728`.

`T01_020_040_FI`

RU:

> Текущие задачи миссии также отмечены на карте сенсоров.

EN:

> Current mission objectives are also displayed prominently in your sensors manager.

Узел `Mission_T1#657`.

`T01_020_050_TS`

RU:

> Понятно... Пытаюсь сосредоточиться.

EN:

> Understood...attempting to refocus.

Узел `Mission_T1#397`.

`T01_020_060_KS`

RU:

> Командующая, расслабься. Сейчас тебе мешает собственное «я».

EN:

> Commander, let go.  Right now, self is your enemy.  

### T01_030

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #653`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_T1#137`.

`T01_030_010_FI`

RU:

> Теперь проверим навигацию, чтобы вы освоились в пространстве вокруг Материнского корабля. Начнём с перемещения точки обзора.

EN:

> Our next test is of your navigation systems, to help you gain tactical awareness around the Mothership.  First we will try moving around your environment. 

Узел `Mission_T1#145`.

`T01_030_013_FI`

RU:

> Вы также можете приближать и отдалять изображение.

EN:

> You can also zoom your view in and out.

Узел `Mission_T1#585`.

`T01_030_020_FI`

RU:

> Вы можете телепортировать точку обзора, мгновенно перемещаясь в любое доступное место.

EN:

> You can teleport your viewpoint and instantly move it anywhere within range.

Узел `Mission_T1#306`.

`T01_030_017_FI`

RU:

> Перемещать точку обзора можно несколькими способами.

EN:

> You can move your view of the world using several methods.

Узел `Mission_T1#161`.

`T01_030_040_TS`

RU:

> Потрясающе! Столько лет я смотрела на тактические экраны, но такого ещё не видела.

EN:

> This is stunning! I have spent years staring into tactical screens but never like this.

Узел `Mission_T1#278`.

`T01_030_050_KS`

RU:

> Помни: слившись с потоками данных сенсоров, ты можешь видеть всё и везде. Принимать множество решений почти мгновенно. Но твои возможности не безграничны. Никогда об этом не забывай.

EN:

> Remember when you merge with the sensor data you can see everything, everywhere.  You can make so many decisions, so quickly.  But you are not infinite, never forget that.

### T01_040

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #547`; `OnDetectShip #383`; `OnWaveDestroyed (Enabled=True) #742`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_T1#561`.

`T01_040_010_FI`

RU:

> Теперь перейдём к вашему флоту и управлению им. Для начала осмотрите доступные корабли. Они объединены в боевые формирования — ударные группы.

EN:

> We will now focus on your fleet of ships and how to command them.  Start by surveying the ships you have available. They are placed into functional formations called Strike Groups.  

Узел `Mission_T1#300`.

`T01_040_030_FI`

RU:

> Вы также можете отдавать приказы нескольким ударным группам одновременно.

EN:

> You also have the ability to give commands to more than one Strike Group at a time.

Узел `Mission_T1#93`.

`T01_040_035_FI`

RU:

> Вы можете приказывать ударным группам атаковать.

EN:

> You can also give Strike Groups attack orders.

Узел `Mission_T1#792`.

`T01_040_050_FI`

RU:

> Сейчас перед вами учебные противники. Они не станут стрелять в ответ. Настоящий враг, разумеется, будет.

EN:

> You are now facing simulated enemies, which will not fight back. Of course real enemies will.

Узел `Mission_T1#55`.

`T01_040_020_FI`

RU:

> Вы можете отдавать ударным группам приказы о перемещении.

EN:

> You can give Strike Groups movement orders.

Узел `Mission_T1#385`.

`T01_040_060_KS`

RU:

> Вот так, командующая. Ты осваиваешься.

EN:

> That's it, Commander. You're getting it. 

Узел `Mission_T1#535`.

`T01_040_070_TS`

RU:

> Всё так непосредственно. Между мыслью и действием ничего нет.

EN:

> It's so direct, so immediate.

Узел `Mission_T1#525`.

`T01_040_080_KS`

RU:

> Ты ощущаешь то, что прежде знала только я. Теперь нас таких двое.

EN:

> You are experiencing all the things only I have known. You and I now make a very exclusive pair.

### T01_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #742`.

Узел `Mission_T1#91`.

`T01_050_010_FI`

RU:

> Тактическая пауза останавливает происходящее и позволяет спланировать дальнейшие действия, в том числе потратить ресурсы на постройку новых кораблей.

EN:

> Tactical Pause allows you to stop the action so that you can plan your next moves, including spending Resources to build new ships. 

Узел `Mission_T1#415`.

`T01_050_020_FI`

RU:

> Вы также можете списывать ненужные корабли из ударных групп, возвращая часть затраченных ресурсов.

EN:

> You can also retire ships in your Strike Groups that you no longer need, and get some Resources returned to your reserves.

Узел `Mission_T1#221`.

`T01_050_040_KS`

RU:

> Теперь все эти корабли — твои. Береги их, словно они часть тебя.

EN:

> The ships are all yours now. Be careful with them, like they are a part of you.

Узел `Mission_T1#549`.

`T01_050_050_TS`

RU:

> Я всегда так к ним относилась.

EN:

> I have always felt that way.

Узел `Mission_T1#659`.

`T01_050_060_KS`

RU:

> Теперь всё иначе. Ты будешь слышать каждую потерю. Будь к этому готова.

EN:

> Not like this. You will hear every loss now.  Be prepared for that.

### T01_060

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #573`; `OnObjectiveCompleted (Objective=30, MT01_Objective_01) #503`; `OnWaveDestroyed (Enabled=True) #742`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_T1#673`.

`T01_060_010_FI`

RU:

> С помощью путевых точек вы можете задавать ударным группам более сложные маршруты.

EN:

> You can also set up more advanced movement patterns for your Strike Groups, using waypoints.

Узел `Mission_T1#770`.

`T01_060_020_FI`

RU:

> Задайте маршрут через путевые точки, чтобы атаковать вражеские корабли, обойдя орудийную платформу.

EN:

> Use waypoints to navigate to attack those enemy ships while avoiding the gun platform.

Узел `Mission_T1#437`.

`T01_060_030_FI`

RU:

> Проверка основных систем завершена.

EN:

> This concludes our test of core systems.

### T01_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=30, MT01_Objective_01) #503`.

Узел `Mission_T1#360`.

`T01_070_010_KS`

RU:

> Хорошо, командующая. А теперь пора испытать твои возможности. Передаю координаты места встречи с Радаа. Здесь тебе придётся действовать самой: управлять гиперпространством должен один разум.

EN:

> Well done, Commander. But now it's time to push your limits. I am sending you the coordinates for the Radaa meeting point. For this you are on your own. Hyperspace manipulation is for a singular mind.

Узел `Mission_T1#663`.

`T01_070_020_KS`

RU:

> Ты справишься.

EN:

> You can do this.

Узел `Mission_T1#467`.

`T01_070_030_TS`

RU:

> Всё как на тренажёре. Но не стану врать: гиперпространственная математика никогда не была моей сильной стороной.

EN:

> It feels just like the simulation but I will not lie, Hyperspatial math is not my strongest suit.  

Узел `Mission_T1#171`.

`T01_070_040_KS`

RU:

> Просто удерживай уравнения под контролем, передавая их гиперпространственному ядру. А затем... открой дверь.

EN:

> Just keep control of the equations as you feed them to the Hyperspace Core and then... open the door.

Узел `Mission_T1#439`.

`T01_070_050_TS`

RU:

> Принято... Выход в гиперпространство по моей команде.

EN:

> Roger that... Hyperspace engage on my mark. 

Узел `Mission_T1#545`.

`T01_070_060_TS`

RU:

> 3... 2... 1... Пуск.

EN:

> 3... 2... 1... mark.

## 1. M1: Испытательный полигон Хиигары / Hiigara Proving Grounds

Определение `f43761a426e901e4897580ed0dc94979:1`, карта `level1`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

Общий пролог уже приведён перед обучением; повторно не воспроизводится.

### Задачи, подключённые к графу

Узлы: 60, 100, 118, 441, 469.

`M01_Objective_00`

RU:

> Добывайте ресурсы на астероидах, пока их запас не достигнет 200 ед.

EN:

> Harvest RU from asteroids to a total of 200.

Узлы: 162, 435, 501.

`M01_Objective_00a`

RU:

> Постройте разведчик на собранные ресурсы.

EN:

> Use your RU to Build a Scout.

Узлы: 154, 326, 525.

`M01_Objective_00b`

RU:

> Найдите патруль Радаа с помощью активного сканирования разведчика.

EN:

> Locate the Radaa patrol using Scout Sensor Sweep Ability.

Узлы: 36, 52, 324.

`M01_Objective_01`

RU:

> Уничтожьте первый патруль Радаа.

EN:

> Destroy the first Radaa patrol.

Узлы: 74, 180, 519.

`M01_Objective_01b`

RU:

> Уничтожьте второй патруль Радаа.

EN:

> Destroy the second Radaa patrol.

Узлы: 104, 142, 595.

`M01_Objective_01c`

RU:

> Уничтожьте третий патруль Радаа.

EN:

> Destroy the third Radaa patrol.

Узлы: 94, 198, 206, 252, 397.

`M01_Objective_02`

RU:

> Защитите Материнский корабль от Радаа.

EN:

> Defend the Mothership from the Radaa.

Узлы: 80, 236, 340.

`M01_Objective_02b`

RU:

> Уничтожьте ракетные фрегаты Радаа.

EN:

> Destroy the Radaa Missile Frigates.

### M01_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #453`.

Узел `Mission_M1#561`.

`M01_020_003_TS`

RU:

> Гиперпрыжок... выполнен успешно.

EN:

> Hyperspace jump... successful.

Узел `Mission_M1#551`.

`M01_020_005_KS`

RU:

> Я знала, что ты справишься.

EN:

> I knew you could do it.

Узел `Mission_M1#413`.

`M01_020_010_FI`

RU:

> Мы прибыли к месту встречи раньше Радаа.

EN:

> We are early for our rendezvous with the Radaa.

Узел `Mission_M1#152`.

`M01_020_020_TS`

RU:

> Не будем терять время. Сканирую окрестности в поисках ресурсов.

EN:

> Let's not put the time to waste.  Scanning for Resources in our vicinity.

Узел `Mission_M1#26`.

`M01_020_030_FI`

RU:

> Принято. Командование, в этом секторе множество астероидов и богатых ресурсами пылевых облаков.

EN:

> Acknowledged.  Command, this sector is rife with asteroids and rich dust clouds.

Узел `Mission_M1#130`.

`M01_020_035_FI`

RU:

> В одной из ваших ударных групп есть сборщики ресурсов. Можете отдавать приказ на добычу.

EN:

> One of your Strike Groups contains Resource Collectors which can be used for harvesting. Initiate at will.

Узел `Mission_M1#308`.

`M01_020_040_TS`

RU:

> Есть возражения, командующая Каран С’Джет?

EN:

> Any objections, Commander Karan S'jet?

Узел `Mission_M1#421`.

`M01_020_050_KS`

RU:

> Я уже не командую. Ваш корабль — ваши приказы, командующая Тирра Собан.

EN:

> Former Commander.  Your ship, your orders, Commander Tyrra Soban.

### M01_025

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=9, M01_Objective_00) #100`.

Узел `Mission_M1#300`.

`M01_025_010_FI`

RU:

> Необходимые ресурсы собраны. Продолжайте добычу: ресурсы нужны для поддержания систем Материнского корабля и работы его кораблестроительных отсеков.

EN:

> Necessary Resources secured.  Continuing to gather Resources is important for Mothership systems health, and keeps our construction bays capable of building more ships.

Узел `Mission_M1#563`.

`M01_025_020_FI`

RU:

> Теперь у нас достаточно ресурсов, чтобы построить разведчик и точно определить местоположение Радаа.

EN:

> We now have the Resources to build a Scout unit so we can pinpoint the location of the Radaa.

### M01_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=17, M01_Objective_00a) #162`.

Узел `Mission_M1#547`.

`M01_030_010_GR`

RU:

> Приветствую хиигарское командование. Говорит адмирал Гиитан Радаа. Наша Коммандер Амма передаёт свои пожелания долгого и плодотворного сотрудничества с народом Хиигары.

EN:

> Greetings, Hiigaran Command, this is Radaa Admiral Giitan. Our Commander Amma relays her wishes for our long and fruitful partnership with the Hiigaran people.

Узел `Mission_M1#176`.

`M01_030_015_GR`

RU:

> С любезностями покончено — приступим. Ничто не сравнится с хорошим боем.

EN:

> And now that pleasantries are out of the way, let us begin. I live for a good battle.

Узел `Mission_M1#429`.

`M01_030_020_TS`

RU:

> Здесь мы с вами согласны.

EN:

> As do I.

Узел `Mission_M1#28`.

`M01_030_030_FI`

RU:

> В секторе обнаружены сигнатуры кораблей Радаа.

EN:

> Radaa craft signatures detected in this sector.

Узел `Mission_M1#653`.

`M01_030_040_GR`

RU:

> Я решил, что для наших учений лучше использовать боевые снаряды. По моему опыту, только так и можно чему-то научиться. Вы согласны? Вот и прекрасно.

EN:

> I thought it best for our skirmish to involve live fire.  I've found it's the only way to truly learn.  Are we agreed?  Good.

Узел `Mission_M1#66`.

`M01_030_050_FI`

RU:

> Чтобы получить точные координаты кораблей Радаа, прикажите разведчику провести активное сканирование сенсорами.

EN:

> To gain precise coordinates on the Radaa craft, have your Scout perform reconnaissance with a Sensor Sweep.

### M01_035

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=60, M01_Objective_00b) #525`.

Узел `Mission_M1#477`.

`M01_035_010_FI`

RU:

> Первая учебная группа Радаа обнаружена.

EN:

> The first Radaa skirmish group has been detected.

Узел `Mission_M1#240`.

`M01_035_020_KS`

RU:

> Пора, Командование флота. Вступайте в бой одной из ваших ударных групп.

EN:

> This is it, Fleet Command.  Take them on with one of your combat Strike Groups.

### M01_040

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=patrolC) #513`.

Узел `Mission_M1#433`.

`M01_040_010_FI`

RU:

> Обнаружена сигнатура второго патруля Радаа.

EN:

> Second Radaa patrol signature detected.

Узел `Mission_M1#521`.

`M01_040_020_KS`

RU:

> Видишь их положение на карте сенсоров?

EN:

> Do you see their position in the Sensors Manager?

Узел `Mission_M1#543`.

`M01_040_030_TS`

RU:

> Я вижу всё.

EN:

> I see it all.

### M01_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=patrolB) #48`.

Узел `Mission_M1#597`.

`M01_050_010_FI`

RU:

> Начат последний учебный бой с Радаа.

EN:

> Final Radaa skirmish initiated.

Узел `Mission_M1#188`.

`M01_050_020_KS`

RU:

> По данным разведки, Радаа владеют весьма передовыми технологиями. Но пока я не увидела ничего особенного.

EN:

> Intelligence reports say the Radaa utilize very high level technology, but I haven't seen anything remarkable yet.

### M01_060

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=patrolA) #40`.

Узел `Mission_M1#489`.

`M01_060_010_AR`

RU:

> Хиигарское командование, я Амма, командующая флотом Радаа. Объявляю о вступлении в силу таииданского договора TR-3.

EN:

> Hiigaran command, I am Amma, Commander of the Radaa Fleet. I am declaring Taiidani agreement TR-3 in effect.

Узел `Mission_M1#346`.

`M01_060_020_TS`

RU:

> Что? Какого ещё договора?

EN:

> What? What agreement?

Узел `Mission_M1#529`.

`M01_060_030_AR`

RU:

> В обмен на наши значительные вложения таииданский император согласился передать нам все технологии, связанные с гиперпространственным ядром.

EN:

> In return for a considerable investment from us, the Taiidani Emperor agreed to share all technology related to a Hyperspace Core.

Узел `Mission_M1#208`.

`M01_060_040_KS`

RU:

> Мы не заключали такого договора!

EN:

> We made no such agreement!

Узел `Mission_M1#146`.

`M01_060_050_AR`

RU:

> После падения Таииданской империи вы унаследовали планету Хиигара вместе со всеми связанными с ней договорными обязательствами.

EN:

> When the Taiidan Empire fell, you inherited the planet Hiigara and all legal agreements pertaining to it.

Узел `Mission_M1#409`.

`M01_060_055_AR`

RU:

> По условиям договора вы обязаны передать нам гиперпространственное ядро. Иначе это будет признано неисполнением обязательств. Благодарю за содействие.

EN:

> You are bound by that agreement to relinquish your Hyperspace Core or face default. Thank you for your cooperation.

Узел `Mission_M1#294`.

`M01_060_060_FI`

RU:

> Фрегаты Радаа вышли из гиперпространства рядом с Материнским кораблём.

EN:

> Radaa Frigates have jumped in near the Mothership.

Узел `Mission_M1#242`.

`M01_060_070_KS`

RU:

> Сканирую фрегаты Радаа... Угроза класса «бета». Они способны причинить нам серьёзный ущерб. Это не блеф.

EN:

> Scanning Radaa Frigates...They are a Beta class threat, the could do us great harm. They are not joking.

Узел `Mission_M1#306`.

`M01_060_080_AR`

RU:

> Ваше правительство не выполнило требования в отведённый срок и тем самым нарушило договор.

EN:

> Your governing body has not complied in the given time period and is in default.

Узел `Mission_M1#633`.

`M01_060_085_AR`

RU:

> Мы предвидели такой исход, но заверяем вас: мы намерены забрать лишь то, что принадлежит нам по закону.

EN:

> Though we anticipated this result we wish to assure you we are only taking what is legally ours.

Узел `Mission_M1#539`.

`M01_060_085_GR`

RU:

> Пора проявить благоразумие. Прекратите сопротивление.

EN:

> Time to cooperate and stand down.

Узел `Mission_M1#224`.

`M01_060_090_TS`

RU:

> Вот вам наше содействие. Флот, к бою!

EN:

> I've got your cooperation right here.  Fleet to battle positions!

### M01_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=26, M01_Objective_02b) #236`.

Узел `Mission_M1#507`.

`M01_070_010_FI`

RU:

> Фрегаты Радаа нейтрализованы, но Материнский корабль получил серьёзные повреждения. Приближаются новые силы Радаа.

EN:

> Radaa Frigates neutralized but the Mothership has sustained significant damage.  Additional Radaa units incoming.

Узел `Mission_M1#393`.

`M01_070_020_KS`

RU:

> Тирра, их слишком много. Материнский корабль долго не продержится — я это знаю. Уводи нас отсюда прыжком.

EN:

> Tyrra, there's too many. I know the Mothership won't take much more of this. You have to jump us out of here.

Узел `Mission_M1#601`.

`M01_070_030_TS`

RU:

> Решать мне, Каран С’Джет... Но ты права. Нам нужно уединённое место для перегруппировки. Увожу Материнский корабль и флот в гиперпространство.

EN:

> That is my decision Karan S'jet... but you are not wrong. We need an isolated location to regroup. Jumping the Mothership and fleet now.

### M01_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=LossEvent) #298`.

Узел `Mission_M1#344`.

`M01_080_010_GR`

RU:

> Бой окончен. Мы победили, вы проиграли. В следующий раз постарайтесь лучше.

EN:

> The Skirmish is won.  Our victory, your loss.  You will need to do better.

### M01_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=LossEvent) #298`.

Узел `Mission_M1#276`.

`M01_090_010_FI`

RU:

> Катастрофические потери. Хиигарский флот уничтожен.

EN:

> Catastrophic losses reported.  Hiigaran fleet has been eliminated.

### M01_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=LossEvent) #559`.

Узел `Mission_M1#381`.

`M01_100_010_FI`

RU:

> Материнский корабль получил тяжелейшие повреждения. Повторяю: корабль выведен из строя. Радаа захватят его.

EN:

> Mothership has sustained massive damages. I repeat: Mothership incapacitated, Radaa forces will capture it.

### M01_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #226`.

Узел `Mission_M1#178`.

`M01_110_010_FI`

RU:

> Ракетные фрегаты Радаа способны пробить обшивку Материнского корабля.

EN:

> The Radaa Missile Frigates are capable of breaching the hull of the Mothership.

### M01_120

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #591`.

Узел `Mission_M1#425`.

`M01_120_010_FI`

RU:

> Пробоина в обшивке привела к тяжёлым повреждениям Материнского корабля. Требуются срочные меры.

EN:

> Damage to the Mothership from the hull breach is substantial, our situation is urgent.

### M01_130

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #246`.

Узел `Mission_M1#613`.

`M01_130_010_FI`

RU:

> Повреждения Материнского корабля приближаются к критическому уровню.

EN:

> Mothership damage nearing critical levels.

Узел `Mission_M1#284`.

`M01_130_020_KS`

RU:

> Если мы не покончим с этим немедленно, они захватят Материнский корабль.

EN:

> They'll take the Mothership if we can't end this fast.

## 2. M7: Тёмная сторона Ангельской Луны / Dark Side of Angel Moon

Определение `66adb7078ddb522448ddc9de037c9d07:1`, карта `level11`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M7 - Dark Side of Angel Moon/M7_Animatic_Intro/M2_Animatic_Intro.unity`

*Клип начинается в 1.65 с.*

`M07_010_010_A_TS`

RU:

> Гиперпрыжок завершён. Здесь мы сможем оценить повреждения и восстановить системы, не подвергая Хиигару опасности.

EN:

> Hyperspace jump complete. Here we can assess our damage and get our systems back online without endangering Hiigara.

*Клип начинается в 9.53 с.*

`M07_010_020_A_KS`

RU:

> Им с самого начала были нужны Материнский корабль и ядро Предтеч.

EN:

> They were after the Mothership and the Progenitor Core all along.

*Клип начинается в 13.19 с.*

`M07_010_030_A_TS`

RU:

> Проклятье! Дело дрянь.

EN:

> Sands and sinners!  This is very bad.

*Клип начинается в 17.24 с.*

`M07_010_040_A_KS`

RU:

> Мягко сказано.

EN:

> To put it mildly.

*Клип начинается в 20.18 с.*

`M07_010_050_A_TS`

RU:

> Дайамид утратил бдительность. Мир сделал глав киитов слишком доверчивыми. Они не разглядели, кто такие Радаа на самом деле.

EN:

> The Daiamid has grown complacent.  Peace has made all the Kiith-Sa's too trusting. They didn't see the Radaa for what they are.

*Клип начинается в 27.23 с.*

`M07_010_060_A_KS`

RU:

> Насколько я читала, они торговцы. Родной планеты у них нет, и они часто пользуются кораблями, приобретёнными у других народов. На фоне таиидан они казались безобидными. Но взаимные упрёки нам сейчас не помогут.

EN:

> From what I have read they are deal makers – no home planet and they often use ships they acquired from other peoples.  Compared to the Taiidan, they seemed harmless.  But recrimination won't change where we are now.

*Клип начинается в 40.38 с.*

`M07_010_070_A_TS`

RU:

> Разведка! Мне нужен противник, по которому можно ударить. Что мы знаем об их руководстве?

EN:

> Intel!  I need an enemy to strike.  What do we know about their leadership?

*Клип начинается в 44.77 с.*

`M07_010_080_A_FI`

RU:

> Флотом Радаа командует Амма. Она унаследовала пост от отца и известна как искусный переговорщик.

EN:

> The Radaa Commander is Amma – she inherited the job from her father and she is known as a shrewd negotiator.

*Клип начинается в 51.38 с.*

`M07_010_090_A_FI`

RU:

> Её заместитель — сын Гиитан, известный своей беспощадностью.

EN:

> Her son Giitan acts as her second in command, known for his ruthlessness.

*Клип начинается в 57.98 с.*

`M07_010_100_A_KS`

RU:

> До потери связи с Хиигарой нам сообщили, что Дайамид направил срочное обращение за помощью в Галактический совет. Когда будет ответ — неизвестно. Нам нужно выиграть время для родной планеты.

EN:

> Before we lost contact with Hiigara, we were informed the Daiamid sent an emergency appeal to the Galactic Council to seek assistance. No word on how long it will take.  We need to buy the Homeworld time.

*Клип начинается в 70.58 с.*

`M07_010_110_A_TS`

RU:

> Хиигарский флот не готов к бою. Часть кораблей выведена из строя — якобы проходит «модернизацию» у Радаа. Остальные разбросаны по учениям. Всё зависит от нас.

EN:

> The Hiigaran fleet is in no shape for battle.  Some of our fleet is out of commission, supposedly being "upgraded" by the Radaa, while others are scattered on maneuvers. It’s up to us.

*Клип начинается в 81.83 с.*

`M07_010_120_A_KS`

RU:

> Тирра, я понимаю твою ярость. Я видела, как горел Харак. Но когда я впервые сражалась, управляя Материнским кораблём, эмоции отнимали все силы. Постарайся сохранить спокойствие.

EN:

> Tyrra, I know the rage you are feeling.  I watched Kharak burn.  But emotion drained me when I first fought as the Mothership. Focus on staying calm.

*Клип начинается в 92.35 с.*

`M07_010_130_A_TS`

RU:

> Не обижайся, Каран, но Собанам редко нужны военные наставления С’Джет.

EN:

> No offense, Karan, but rarely does a Soban require war wisdom from a S'jet.

*Клип начинается в 99.11 с.*

`M07_010_140_A_FI`

RU:

> Дальние сенсоры обнаружили истребители Радаа. Противник приближается!

EN:

> Radaan fighters on deep sensors.  We have incoming!

*Клип начинается в 102.94 с.*

`M07_010_150_A_TS`

RU:

> Что ж, посмотрим, на что способен этот Материнский корабль.

EN:

> Very well, let's see what this Mothership can do.

### Задачи, подключённые к графу

Узлы: 54, 158, 223.

`M07_Objective_01a`

RU:

> Добудьте 700 ед. ресурсов, чтобы восстановить сенсоры.

EN:

> Harvest 700 RU to bring Sensors back online.

Узлы: 44, 146, 186.

`M07_Objective_01b`

RU:

> До перезарядки гипердвигателя осталось:

EN:

> Time until jump drive is recharged:

Узлы: 247, 385.

`M07_Objective_02`

RU:

> Защищайте Материнский корабль во время ремонта корпуса.

EN:

> Defend the Mothership during structural repairs.

Узлы: 156, 221, 251.

`M07_Objective_02a`

RU:

> Добудьте в общей сложности 2000 ед. ресурсов, чтобы восстановить кораблестроительные системы.

EN:

> Harvest 2000 total RU to restore construction sytems.

Узлы: 31, 349.

`M07_Objective_03`

RU:

> Защищайте Материнский корабль, пока запускается гипердвигатель.

EN:

> Defend the Mothership while jump drive spins up.

### M07_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #194`.

Узел `Mission_M7#319`.

`M07_020_010_TS`

RU:

> Всем службам доложить обстановку!

EN:

> All departments, status report!

Узел `Mission_M7#50`.

`M07_020_020_FI`

RU:

> Приближаются силы Радаа. Должно быть, они засекли сигнатуру ядра.

EN:

> Radaa forces are approaching.  They must have honed in on the core signature.

Узел `Mission_M7#283`.

`M07_020_050_KS`

RU:

> Кораблестроительные отсеки всё ещё не работают. Придётся сражаться тем флотом, что есть. Все резервные корабли уже введены в строй.

EN:

> Construction facilities still offline. We will have to fight with the fleet we have. We have deployed all reserve ships.

Узел `Mission_M7#166`.

`M07_020_080_TS`

RU:

> Сенсоры не работают. Я почти слепа!

EN:

> Sensors are down. I'm nearly blind!

Узел `Mission_M7#134`.

`M07_020_090_FI`

RU:

> Чтобы восстановить карту сенсоров, нам потребуется больше ресурсов.

EN:

> To repair the Sensors Manager, we will need to collect more resources. 

Узел `Mission_M7#48`.

`M07_020_030_KS`

RU:

> Наши запасы ресурсов погибли при попадании в грузовые отсеки. Придётся добывать новые.

EN:

> Resource reserves were wiped out when our supply bays were hit.  We will have to gather more.

### M07_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=16, M07_Objective_01a) #158`.

Узел `Mission_M7#327`.

`M07_030_010_TS`

RU:

> Сенсоры восстановлены. Связь работает в полном объёме.

EN:

> Sensors back online. Comms back at full.

Узел `Mission_M7#154`.

`M07_030_020_FI`

RU:

> Принимаем передачу адмирала Гиитана Радаа.

EN:

> We are receiving a transmission from Admiral Giitan of the Radaa.

Узел `Mission_M7#86`.

`M07_030_030_GR`

RU:

> Материнский корабль хиигарян, вы попытались скрыться с нашей собственностью. Не стоит недооценивать нашу настойчивость, когда речь идёт о возврате активов.

EN:

> Hiigaran Mothership, you have attempted to flee with our property.  Do not underestimate our perseverance in claiming our assets.

Узел `Mission_M7#33`.

`M07_030_040_TS`

RU:

> Это фарс. Настоящий воин не прикрывается ложью и юридическими уловками.

EN:

> This is a farce.  No warrior fights on technicalities and lies.

Узел `Mission_M7#281`.

`M07_030_050_KS`

RU:

> Лгут они или нет, нам нужно больше ресурсов, чтобы восстановить кораблестроительные отсеки Материнского корабля.

EN:

> Lies or not, we must secure more resources to get the Mothership's construction bays back online.

### M07_040

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=28, M07_Objective_02a) #251`.

Узел `Mission_M7#235`.

`M07_040_010_TS`

RU:

> Кораблестроительные системы восстановлены. Флот, приготовиться к бою.

EN:

> Ship build systems online. Fleet prepare to engage. 

Узел `Mission_M7#309`.

`M07_040_013_KS`

RU:

> Командующая, стоит ли принимать бой именно там, где этого хотят Радаа?

EN:

> Commander, should we be fighting right where the Radaa want us?

Узел `Mission_M7#94`.

`M07_040_015_TS`

RU:

> Верно подмечено, Каран. Согласна. Разведка, сколько времени потребуется на запуск гиперпространственного ядра?

EN:

> An excellent point, Karan.  I concur.  Intel, how long will I need to spin up the Hyperspace Core?

Узел `Mission_M7#152`.

`M07_040_020_FI`

RU:

> Инженеры сообщают, что ещё ремонтируют повреждённые энергомагистрали.

EN:

> Engineering reports they are still dealing with damaged conduits.

Узел `Mission_M7#231`.

`M07_040_030_TS`

RU:

> Сначала мне говорят, что нужно уходить, а теперь — что я не могу!

EN:

> First I am told we have to go and now I am told I can't leave!  

Узел `Mission_M7#239`.

`M07_040_040_TS`

RU:

> Разведка, напомните инженерам: за их время платят жизнями. Всем кораблям сдерживать Радаа, пока мы не сможем прыгнуть.

EN:

> Intel, make engineering aware that their time is paid for in lives.  All ships, hold the Radaa off until we are cleared to jump.

### M07_050

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=12, M07_Objective_01b) #146`.

Узел `Mission_M7#190`.

`M07_050_010_FI`

RU:

> Гиперпространственные системы готовы к работе.

EN:

> Hyperspace systems are primed and ready.

Узел `Mission_M7#60`.

`M07_050_020_TS`

RU:

> Ввожу координаты безопасного убежища. Прыжок... сейчас.

EN:

> Inputting coordinates to a safe harbor. Jumping... now.

### M07_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=InitialResourceGroupLost) #62`; `CustomEvent (name=InsufficientResourcesLossEvent) #229`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M7#321`.

`M07_100_010_FI`

RU:

> Флот уничтожен. Ремонт Материнского корабля не завершён. Спасательные капсулы приведены в действие.

EN:

> Fleet eliminated. Mothership repair incomplete. Escape pods activated.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #144`; `CustomEvent #307`; `CustomEvent #317`; `CustomEvent #381`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M7#377`.

`FI_MothershipAttacked_01`

RU:

> Материнский корабль под атакой.

EN:

> The Mothership is under attack.

Узел `Mission_M7#335`.

`FI_MothershipCriticalDamage_01`

RU:

> Материнский корабль получил критические повреждения.

EN:

> Mothership has sustained critical damage.

Узел `Mission_M7#273`.

`FI_MothershipHeavyDamage_01`

RU:

> Материнский корабль серьёзно повреждён.

EN:

> Mothership has taken heavy damage.

Узел `Mission_M7#373`.

`FI_MothershipLost_01`

RU:

> Материнский корабль тяжело повреждён. Системы жизнеобеспечения отказывают. Всему персоналу — к спасательным капсулам.

EN:

> Mothership damage is massive, life support systems unsustainable. All personnel to the escape pods.

## 3. M3: Рейд на Гиббас / The Gybbas Raid

Определение `2b18e34423a7cfc4687ca08f9d35789f:1`, карта `level3`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M3 - A New Offensive/M3_Animatic_Intro/M3_Animatic_Intro.unity`

*Клип начинается в 1.15 с.*

`M03_010_008_A_TS`

RU:

> Атака Радаа отбита. Есть вести от Галактического совета?

EN:

> Radaa forces repelled. Any word from the Galactic Council?

*Клип начинается в 4.85 с.*

`M03_010_010_A_KS`

RU:

> Сообщают, что претензии Радаа могут иметь законные основания. Но все попытки добиться прекращения огня блокируют сами Радаа и члены совета, с которыми они заключили сделки. Бентуси воздержались!

EN:

> They report that the Radaa claims may be legally valid, but any attempts to call for a cease fire are being blocked by the Radaa and the council members they have made deals with.  The Bentusi are abstaining!

*Клип начинается в 16.89 с.*

`M03_010_020_A_TS`

RU:

> Что ж, Хиигара снова одна... А мы — на острие удара.

EN:

> Fine,  Hiigara stands alone...again.  And we are the tip of the spear.

*Клип начинается в 23.33 с.*

`M03_010_030_A_KS`

RU:

> Разведка, насколько серьёзно повреждён Материнский корабль?

EN:

> Intelligence, how much damage did the Mothership sustain?

*Клип начинается в 26.54 с.*

`M03_010_035_A_FI`

RU:

> Основные системы почти не пострадали. От нагрузок отказывают старые, второстепенные системы. Ремонт близок к завершению.

EN:

> Minimal damage to core systems. Older, non-critical systems breaking down under stress. Repairs nearly complete.

*Клип начинается в 34.39 с.*

`M03_010_040_A_TS`

RU:

> Хорошо! Я не стану ждать следующего хода Радаа. Так мы лишь увязнем в оборонительной войне, которую мне не выиграть. Пора сделать то, чего они от нас не ждут: мы переходим в наступление.

EN:

> Good! I won't wait for the Radaa's next move that will just get us stuck in a defensive war I can't win. Time for the one thing the Radaa won't expect from us: we are going to attack.

*Клип начинается в 47.18 с.*

`M03_010_050_A_KS`

RU:

> Наш флот гораздо меньше их флота. И ты ещё только осваиваешь Материнский корабль.

EN:

> The size of our fleet pales in comparison to theirs. You're still learning to control the Mothership.

*Клип начинается в 52.59 с.*

`M03_010_060_A_TS`

RU:

> С кораблём я пока осваиваюсь, но флотом командую не впервые. Где ближайший форпост Радаа?

EN:

> I may be new to the ship, but I'm not new to leading a fleet. What is the closest Radaa outpost?

*Клип начинается в 58.35 с.*

`M03_010_070_A_FI`

RU:

> Радаа построили верфь на высокой орбите Гиббаса, у внешних границ нашей системы.

EN:

> The Radaa have built a ship yard in high orbit above Gybbas on the outer edge of our system.

*Клип начинается в 63.80 с.*

`M03_010_080_A_TS`

RU:

> Хм... Туда легко прыгнуть.

EN:

> Hmm...an easy jump.

*Клип начинается в 65.97 с.*

`M03_010_090_A_KS`

RU:

> Признаю, смелый ход.

EN:

> It's a bold move, I admit.

*Клип начинается в 67.83 с.*

`M03_010_100_A_TS`

RU:

> Я бы не рисковала нашими людьми, если бы не была уверена в своём решении.

EN:

> I would never risk our people if it weren't the right move.

*Клип начинается в 71.30 с.*

`M03_010_110_A_FI`

RU:

> Ремонт завершён. Передаю координаты орбитальной верфи.

EN:

> Repairs complete. Transferring coordinates for the Orbital Shipyard.

### Задачи, подключённые к графу

Узлы: 142, 414, 498, 540.

`M03_Objective_01`

RU:

> Уничтожьте мобильный переработчик Радаа.

EN:

> Destroy a Radaa Mobile Refinery.

Узлы: 144, 152, 158, 240, 295, 418, 530, 578.

`M03_Objective_02`

RU:

> Уничтожьте второй мобильный переработчик Радаа.

EN:

> Destroy a second Radaa Mobile Refinery.

Узлы: 244, 302, 428, 492.

`M03_Objective_03`

RU:

> Верните ударные группы к Материнскому кораблю.

EN:

> Return your strike groups to the Mothership.

Узлы: 426, 598, 600.

`M03_Objective_DestroyA`

RU:

> Уничтожьте переработчик Радаа у ресурсного поля A.

EN:

> Destroy the Radaa Refinery near RU Field A.

Узлы: 330, 398, 610.

`M03_Objective_DestroyB`

RU:

> Уничтожьте переработчик Радаа у ресурсного поля B.

EN:

> Destroy the Radaa Refinery near RU Field B.

Узлы: 196, 271, 650.

`M03_Objective_DestroyC`

RU:

> Уничтожьте переработчик Радаа у ресурсного поля C.

EN:

> Destroy the Radaa Refinery near RU Field C.

Узлы: 128, 140, 174.

`M03_Objective_DestroyD`

RU:

> Уничтожьте переработчик Радаа у ресурсного поля D.

EN:

> Destroy the Radaa Refinery near RU Field D.

### M03_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #212`.

Узел `Mission_M3#574`.

`M03_020_010_TS`

RU:

> Прыжок выполнен. Мы за пределами действия вражеских сенсоров. Флот, определить цели.

EN:

> Hyperspace Jump successful, right outside enemy sensor range. Fleet, identify targets.

Узел `Mission_M3#514`.

`M03_020_020_FI`

RU:

> Радаа интенсивно разрабатывают астероиды в этом секторе. Здесь несколько ресурсных полей, и силы их охраны различаются.

EN:

> The Radaa strip asteroids in this sector, resulting in numerous resource fields. Radaa presence in each varies.

Узел `Mission_M3#472`.

`M03_020_030_KS`

RU:

> Главное — уничтожить один из мобильных переработчиков, не вступая в бой со всем флотом Радаа. Это будет непросто.

EN:

> The key will be to take out one of the Radaa's Mobile Refineries without engaging their whole fleet.  It will not be easy.

Узел `Mission_M3#293`.

`M03_020_040_TS`

RU:

> Тогда я выберу тот, чьё положение даст нам наибольшее тактическое преимущество. А может, и два.

EN:

> Then I will carefully choose the one with the best tactical potential. Or maybe I will choose two.

### M03_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=24, M03_Objective_DestroyB) #398`; `OnObjectiveCompleted (Objective=28, M03_Objective_DestroyA) #426`; `OnObjectiveCompleted (Objective=3, M03_Objective_DestroyD) #140`; `OnObjectiveCompleted (Objective=50, M03_Objective_DestroyC) #650`.

Узел `Mission_M3#546`.

`M03_030_010_FI`

RU:

> Подтверждаю: переработчик Радаа уничтожен. Ресурсное поле наше.

EN:

> Confirmed, Radaa Refinery eliminated.  The field is ours.

Узел `Mission_M3#602`.

`M03_030_020_KS`

RU:

> Радаа ещё не ввели в бой весь флот.

EN:

> The Radaa haven't committed their full fleet yet.

Узел `Mission_M3#204`.

`M03_030_030_TS`

RU:

> Я не даю им предугадать наши манёвры. Если они ошибутся с нашей следующей целью, то дорого за это заплатят. И они это знают.

EN:

> I am keeping our movements variable.  If the Radaa guess wrong about our next objective, I will make them pay for it.  And they know it.

Узел `Mission_M3#486`.

`M03_030_040_KS`

RU:

> Ты опасный противник, Тирра.

EN:

> You are a dangerous opponent, Tyrra.

Узел `Mission_M3#304`.

`M03_030_050_TS`

RU:

> Высокая похвала от женщины, сокрушившей Таииданскую империю.

EN:

> High praise from the woman who brought down the Taiidani Empire.

Узел `Mission_M3#424`.

`M03_030_060_KS`

RU:

> Мне многие помогали.

EN:

> I had a lot of help.

Узел `Mission_M3#238`.

`M03_030_070_TS`

RU:

> А мне помогаешь ты. Но я чувствую: противник устал от этого танца. Какое бы ресурсное поле я ни выбрала следующим, сил Радаа там будет куда больше.

EN:

> And I have you. But I can feel our opponent getting tired of this dance. Whichever resource field I pick next, we will be facing many more Radaa forces.

### M03_040

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=24, M03_Objective_DestroyB) #398`; `OnObjectiveCompleted (Objective=28, M03_Objective_DestroyA) #426`; `OnObjectiveCompleted (Objective=3, M03_Objective_DestroyD) #140`; `OnObjectiveCompleted (Objective=50, M03_Objective_DestroyC) #650`.

Узел `Mission_M3#466`.

`M03_040_010_FI`

RU:

> Переработчик Радаа нейтрализован. Многочисленные силы противника идут на перехват.

EN:

> Radaa Refinery neutralized.  Detecting numerous Radaa forces on intercept course.

Узел `Mission_M3#458`.

`M03_040_020_TS`

RU:

> Так я и знала. Всем кораблям немедленно отходить к Материнскому кораблю!

EN:

> I knew it.  All ships, pull back to the Mothership, now!

Узел `Mission_M3#494`.

`M03_040_030_KS`

RU:

> Отлично сыграно, командующая.

EN:

> Well played, Commander.

### M03_060

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=13, M03_Objective_03) #244`.

Узел `Mission_M3#568`.

`M03_060_010_FI`

RU:

> Наш флот вошёл в зону действия Материнского корабля.

EN:

> Our fleet is in range of the Mothership.

Узел `Mission_M3#654`.

`M03_060_020_TS`

RU:

> Гиперпрыжок по моей команде. Мы выполнили задачу. Теперь Радаа знают: хиигаряне готовы сражаться.

EN:

> Hyperspace Jump on my command. We have achieved our goal here.  The Radaa know we Hiigarans are ready to fight.

### M03_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=NoResources) #456`.

Узел `Mission_M3#480`.

`M03_070_010_FI`

RU:

> Отступаем! Критические потери кораблей. Всем уцелевшим немедленно отходить.

EN:

> Retreat! Critical loss of ships. Surviving ships retreat immediately.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #283`; `CustomEvent #354`; `CustomEvent #436`; `OnSimReady #212`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M3#320`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M3#338`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M3#277`.

`FI_MothershipLost_05`

RU:

> Материнский корабль получил катастрофические повреждения. Всем — к спасательным капсулам.

EN:

> Catastrophic damage to Mothership. All hands to the escape pods.

Узел `Mission_M3#432`.

`FI_UnlockHeavyCorvette`

RU:

> В ходе ремонта Материнского корабля мы расширили его производственные возможности. Теперь можно строить тяжёлые корветы. Их броня хорошо защищает от тяжёлых снарядов орудийных платформ, обнаруженных в этом секторе.

EN:

> Our ongoing repairs to the Mothership has added ship build capabilities: we can now build Heavy Corvettes. Their armor is ideal against heavy ballistics from the gun platforms we have detected in this sector.

## 4. M4: Потерянный эсминец / The Lost Destroyer

Определение `894aa6041375b8c4386950e1073d009c:1`, карта `level5`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M4 - A Key Asset/M4_Animatic_Intro/M4_Animatic_Intro.unity`

*Клип начинается в 1.05 с.*

`M04_010_010_A_FI`

RU:

> Командующая, принимаем сигнал бедствия.

EN:

> Commander, we are picking up a distress beacon.

*Клип начинается в 4.30 с.*

`M04_010_020_A_TS`

RU:

> Принимаю... Это не наш корабль.

EN:

> Receiving... it's not one of ours.

*Клип начинается в 8.92 с.*

`M04_010_030_A_FI`

RU:

> Подтверждаю: сигнал с эсминца Радаа. Отказывают двигатели и системы жизнеобеспечения... Но вооружение ещё работает.

EN:

> Confirmed, it is from a Radaa Destroyer. It's signaling failing drives and life support...but weapon systems still functional.

*Клип начинается в 17.92 с.*

`M04_010_040_A_TS`

RU:

> Слишком удобно. Это может быть ловушка.

EN:

> Convenient. It could be a trap.

*Клип начинается в 21.48 с.*

`M04_010_050_A_KS`

RU:

> Когда я сражалась с таииданами, захваченные корабли были незаменимы: благодаря им мы понимали, с чем имеем дело.

EN:

> When I fought the Taiidani, captured ships were critical for understanding what we were up against.

*Клип начинается в 27.23 с.*

`M04_010_060_A_TS`

RU:

> Значит, ловушка это или нет — такой шанс стоит использовать.

EN:

> So trap or not, it's a chance worth taking.

*Клип начинается в 30.87 с.*

`M04_010_070_A_KS`

RU:

> Знание — сила.

EN:

> Knowledge is power.

*Клип начинается в 32.72 с.*

`M04_010_080_A_TS`

RU:

> Слова истинной С’Джет. Разведка флота, следите за кораблями Радаа в этом районе. Мы идём туда.

EN:

> Spoken like a true S'jet. Fleet Intelligence, monitor the area for Radaa ships. We are going in.

### Задачи, подключённые к графу

Узлы: 257, 309, 502.

`M04_Objective_01`

RU:

> Найдите эсминец Радаа.

EN:

> Locate the Radaa Destroyer.

Узлы: 69, 165, 167, 273.

`M04_Objective_02`

RU:

> Уничтожьте всех противников возле эсминца Радаа.

EN:

> Destroy all hostiles around the Radaa Destroyer.

Узлы: 340, 390.

`M04_Objective_03`

RU:

> Пристыкуйте к эсминцу Радаа 3 инженерных корвета.

EN:

> Dock 3 Engineer Craft to the Radaa Destroyer.

Узлы: 63, 131, 179, 316, 324.

`M04_Objective_04`

RU:

> Защищайте эсминец Радаа на пути к Материнскому кораблю.

EN:

> Defend the Radaa Destroyer while it is en route to the Mothership.

Узлы: 239, 281, 305, 406, 464.

`M04_Objective_05`

RU:

> (Необязательно) Уничтожьте гиперврата.

EN:

> (Optional) Destroy the Hyperspace Gate.

### M04_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #384`.

Узел `Mission_M4#277`.

`M04_020_005_TS`

RU:

> Гиперпрыжок завершён.

EN:

> Hyperspace jump complete.

Узел `Mission_M4#23`.

`M04_020_010_KS`

RU:

> Эти корабли! Похоже, это был хиигарский патруль.

EN:

> These ships! They must have been a Hiigaran patrol.

Узел `Mission_M4#342`.

`M04_020_020_TS`

RU:

> Сканировать пространство. Ищем угрозы.

EN:

> Scan for threats.

Узел `Mission_M4#217`.

`M04_020_030_FI`

RU:

> Все корабли выведены из строя. Признаков жизни нет.

EN:

> All disabled. No signs of life.

Узел `Mission_M4#336`.

`M04_020_040_KS`

RU:

> Просто дрейфуют... Потерянные души, и ни следа повреждений на кораблях. Один эсминец Радаа не мог вывести их из строя вот так.

EN:

> Just floating... lost souls without a mark on any ship. A Radaan Destroyer couldn't have just neutralized them like this.

Узел `Mission_M4#75`.

`M04_020_050_TS`

RU:

> И всё же мы видим результат... Начать поиск того, что могло это сделать.

EN:

> And yet here they are... Initiate search for what could have caused this.

Узел `Mission_M4#61`.

`M04_020_060_FI`

RU:

> Плотное поле астероидных обломков мешает сканированию. Обнаружены приближающиеся ударные корабли Радаа.

EN:

> High concentrations of asteroid debris are interfering with scans. We are detecting multiple Radaa strike craft incoming.

Узел `Mission_M4#394`.

`M04_020_070_TS`

RU:

> Ничего-то они нам не упрощают.

EN:

> They will never make this easy.

### M04_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=27, M04_Objective_01) #257`.

Узел `Mission_M4#488`.

`M04_030_010_FI`

RU:

> Эсминец Радаа обнаружен. Силы противника идут на перехват.

EN:

> Radaa Destroyer located. Enemy forces are en route to intercept.

Узел `Mission_M4#506`.

`M04_030_020_TS`

RU:

> Ударным группам перехватить Радаа, прежде чем они доберутся до своей цели.

EN:

> Strike Groups, intercept the Radaa before they reach their target.

Узел `Mission_M4#33`.

`M04_030_030_KS`

RU:

> Среди этих обломков опасно вести бой.

EN:

> All this debris makes for a dangerous place to fight.

Узел `Mission_M4#227`.

`M04_030_040_TS`

RU:

> Всем кораблям внимательно следить за сенсорами.

EN:

> All ships, keep a close eye on sensors.

### M04_040

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=17, M04_Objective_02) #165`.

Узел `Mission_M4#57`.

`M04_040_010_FI`

RU:

> Эвакуационная группа Радаа уничтожена.

EN:

> Radaa retrieval team eliminated.

Узел `Mission_M4#137`.

`M04_040_020_KS`

RU:

> Здесь мы слишком уязвимы. Новые силы Радаа прибудут раньше, чем мы успеем получить хоть какие-то сведения.

EN:

> Too exposed out here. More Radaa will come before we can extract any intel.

Узел `Mission_M4#482`.

`M04_040_030_TS`

RU:

> Тогда отбуксируем эсминец к Материнскому кораблю.

EN:

> So we haul the Destroyer back to the Mothership.

Узел `Mission_M4#496`.

`M04_040_040_FI`

RU:

> Для буксировки эсминца потребуется несколько инженерных корветов.

EN:

> Transporting the Destroyer will require multiple Engineer Craft.

### M04_050

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #508`.

Узел `Mission_M4#231`.

`M04_050_010_FI`

RU:

> Все инженерные корветы закреплены. Эсминец следует заданным курсом.

EN:

> All Engineer Craft are in place. Destroyer on course.

Узел `Mission_M4#470`.

`M04_050_020_KS`

RU:

> Радаа скорее уничтожат эсминец, чем позволят нам его захватить.

EN:

> The Radaa will attempt to eradicate that Destroyer before letting us capture it.

Узел `Mission_M4#237`.

`M04_050_030_TS`

RU:

> Пусть попробуют.

EN:

> They are welcome to try.

### M04_060

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #508`.

Узел `Mission_M4#41`.

`M04_060_010_FI`

RU:

> Обнаружена новая сигнатура. Из гиперврат выходят ударные корабли Радаа.

EN:

> New signature detected.  Radaa Strike Craft emerging from Hyperspace Gate.

Узел `Mission_M4#233`.

`M04_060_020_TS`

RU:

> Они очень не хотят, чтобы этот эсминец попал к нам.

EN:

> They really don't want us to get ahold of that Destroyer.

Узел `Mission_M4#55`.

`M04_060_030_KS`

RU:

> Если доведём эсминец до Материнского корабля, то сможем уйти прыжком вместе с ним. Или уничтожим гиперврата, чтобы лишить Радаа подкреплений. Командование флота, решать вам.

EN:

> If we get the Destroyer to the Mothership, we can jump away with it. Or we can destroy the Hyperspace Gate to cripple the Radaa. Fleet Command, it's your call.

### M04_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=26, M04_Objective_05) #239`.

Узел `Mission_M4#450`.

`M04_070_010_FI`

RU:

> Гиперврата нейтрализованы. Силы Радаа отступают.

EN:

> Hyperspace Gate neutralized.  Radaa forces in retreat.

Узел `Mission_M4#225`.

`M04_070_020_TS`

RU:

> А теперь победитель забирает добычу.

EN:

> And now, to the victor goes the prize.

Узел `Mission_M4#376`.

`M04_070_030_FI`

RU:

> Эсминец под нашим контролем. Готовы к гиперпрыжку по вашей команде.

EN:

> We have a lock on the Destroyer.  Hyperspace jump ready on your command.

### M04_080

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #458`.

Узел `Mission_M4#388`.

`M04_080_010_FI`

RU:

> Эсминец вошёл в зону действия Материнского корабля. Радаа отступают. Готовы к прыжку по вашей команде.

EN:

> The Destroyer is in range of the Mothership with Radaa forces in retreat. We are clear to jump on your command.

### M04_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=YouLose1) #412`; `CustomEvent (name=YouLose2) #235`; `CustomEvent (name=YouLose3) #187`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M4#91`.

`M04_100_010_FI`

RU:

> Потеряно слишком много кораблей. Других вариантов нет. Отступаем, отступаем.

EN:

> Too many ships destroyed, we are out of options. Retreat, retreat.

Узел `Mission_M4#442`.

`M04_100_020_FI`

RU:

> Эсминец получил критические повреждения. Задание провалено.

EN:

> The Destroyer has taken critical damage, our objective is lost.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #259`; `CustomEvent #446`; `CustomEvent #468`; `OnSimReady #384`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M4#29`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M4#49`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M4#462`.

`FI_MothershipLost_03`

RU:

> Материнский корабль потерян.

EN:

> We have lost the Mothership.

Узел `Mission_M4#332`.

`FI_UnlockEngineerCraft`

RU:

> Ресурсы, добытые в Гиббасе, позволили нам освоить новый корабль — инженерный корвет. Он способен ремонтировать корабли своей ударной группы. Эти корветы также понадобятся для захвата эсминца Радаа в этом секторе.

EN:

> Resources claimed from Gybbas allow us to build a new ship: the Engineer Craft, which has the ability to repair ships in their Strike Group. They are also key to capturing the Radaa Destroyer in this sector.

## 5. M5: Верфь Хиигары / Hiigara Shipyard

Определение `68fed03dd3ebcff49bcb60c9565b658b:1`, карта `level7`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M5 - Turning the Tide/M5_Animatic_Intro/M5_Animatic_Intro.unity`

*Клип начинается в 1.03 с.*

`M05_010_010_A_TS`

RU:

> Главный инженер Хаук, что показал анализ данных с захваченного эсминца Радаа?

EN:

> Chief Engineer Hauk, what is your analysis of the data we sent you on our captured Radaa Destroyer?

*Клип начинается в 6.93 с.*

`M05_010_020_A_HA`

RU:

> Пришлось поломать голову, командующая. Их системы казались совершенно разнородными. Потом мы поняли, что перед нами смесь таииданских технологий, технологий Бентуси и даже наших собственных. Есть и компоненты, которых мы никогда раньше не видели.

EN:

> It's been a challenge, Commander.  We saw very little consistency to their systems, but then we realized we were looking at a fusion of Taiidani, Bentus and even our own technology.  There are also some components we've never seen before.

*Клип начинается в 19.08 с.*

`M05_010_030_A_KS`

RU:

> Именно технологии Радаа вывели из строя все те корабли?

EN:

> Did Radaa tech render all those ships inoperable?

*Клип начинается в 22.58 с.*

`M05_010_040_A_HA`

RU:

> Пока рано утверждать. Скоро моя инженерная группа сможет дать обоснованный ответ.

EN:

> Too early to say. My engineering team should have an educated guess very soon.

*Клип начинается в 26.18 с.*

`M05_010_050_A_TS`

RU:

> Мне не нужны догадки, Хаук. Мне нужно преимущество. То, что мы сможем использовать прямо сейчас.

EN:

> I can't afford guesses, Hauk.  I need an edge.  Something we can use right away.

*Клип начинается в 31.62 с.*

`M05_010_060_A_HA`

RU:

> Научную проблему выстрелом не решить, командующая. Скоро у меня будут...

EN:

> Science is not something you can shoot, Commander.   I will have some--

*Клип начинается в 35.80 с.*

`M05_010_070_A_FI`

RU:

> Ещё один сигнал бедствия, Командование флота. На этот раз наш. Хиигарская орбитальная верфь Далкаар осаждена.

EN:

> Another distress call, Fleet Command.  This time it's one of ours.  Hiigaran Orbital Shipyard Dalkaar is under siege.

*Клип начинается в 44.22 с.*

`M05_010_075_A_KS`

RU:

> На станции тысячи гражданских. Целые семьи.

EN:

> There are thousands of civilians on that station. Families.

*Клип начинается в 49.55 с.*

`M05_010_080_A_TS`

RU:

> Проклятье! Если они захватят верфь, Хиигара останется беззащитной. Никто больше не закуёт хиигарян в цепи. Флот, полная боевая готовность! Приготовиться к прыжку!

EN:

> Burning Hells! And if they take that Shipyard, Hiigara herself is wide open. No one is putting Hiigarans in chains again. Fleet, full alert and prepare for jump!

### Задачи, подключённые к графу

Узлы: 262, 380, 498, 567.

`M05_Objective_01`

RU:

> Защитите верфь Хиигары.

EN:

> Defend the Hiigara Shipyard.

Узлы: 436, 504, 522, 557.

`M05_Objective_02`

RU:

> Защитите Материнский корабль.

EN:

> Defend the Mothership.

Узлы: 133, unlinked_958633cf-027f-4e96-938d-349c52d9dfb8.

`M05_Objective_counter0`

RU:

> Отбито атак Радаа: 0

EN:

> Waves of Radaa ships defeated: 0

Узлы: 82, 394.

`M05_Objective_counter1`

RU:

> Отбито атак Радаа: 1

EN:

> Waves of Radaa ships defeated: 1

Узлы: 54, 585.

`M05_Objective_counter10`

RU:

> Отбито атак Радаа: 10

EN:

> Waves of Radaa ships defeated: 10

Узлы: 99, 609.

`M05_Objective_counter2`

RU:

> Отбито атак Радаа: 2

EN:

> Waves of Radaa ships defeated: 2

Узлы: 68, 603.

`M05_Objective_counter3`

RU:

> Отбито атак Радаа: 3

EN:

> Waves of Radaa ships defeated: 3

Узлы: 173, 661.

`M05_Objective_counter4`

RU:

> Отбито атак Радаа: 4

EN:

> Waves of Radaa ships defeated: 4

Узлы: 356, 510.

`M05_Objective_counter5`

RU:

> Отбито атак Радаа: 5

EN:

> Waves of Radaa ships defeated: 5

Узлы: 332, 388.

`M05_Objective_counter6`

RU:

> Отбито атак Радаа: 6

EN:

> Waves of Radaa ships defeated: 6

Узлы: 66, 372.

`M05_Objective_counter7`

RU:

> Отбито атак Радаа: 7

EN:

> Waves of Radaa ships defeated: 7

Узлы: 396, 402.

`M05_Objective_counter8`

RU:

> Отбито атак Радаа: 8

EN:

> Waves of Radaa ships defeated: 8

Узлы: 143, 344.

`M05_Objective_counter9`

RU:

> Отбито атак Радаа: 9

EN:

> Waves of Radaa ships defeated: 9

### M05_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #474`.

Узел `Mission_M5#286`.

`M05_020_010_FI`

RU:

> Гиперпрыжок завершён. Верфь в пределах досягаемости. Она уязвима.

EN:

> Hyperspace jump complete, the Shipyard is in range, and vulnerable.

Узел `Mission_M5#490`.

`M05_020_020_HA`

RU:

> Командование флота, наши строительные системы не работают, оборона сильно ослаблена. Ещё одной атаки нам не выдержать.

EN:

> Fleet Command - our construction systems are down, defenses are badly reduced.  We won't survive another attack wave.

Узел `Mission_M5#316`.

`M05_020_030_FI`

RU:

> Ударные корабли Радаа скоро войдут в зону огня.

EN:

> Radaa Strike Craft about to enter firing range.

Узел `Mission_M5#448`.

`M05_020_040_TS`

RU:

> Они пожалеют, что посмели угрожать нашим людям.

EN:

> We are going to make them regret threatening our people.

### M05_030

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=wave1memos) #512`.

Узел `Mission_M5#573`.

`M05_030_010_HA`

RU:

> Командование флота, за вас болеет вся станция. Пока вы держите оборону, моя группа сможет сосредоточиться на анализе.

EN:

> Fleet Command, you have a whole station cheering you on.  If you continue to provide defense, my team can focus on our analysis.

Узел `Mission_M5#565`.

`M05_030_020_TS`

RU:

> У каждого своя работа, главный инженер.

EN:

> We each have our jobs to do, Chief Engineer.

Узел `Mission_M5#298`.

`M05_030_030_FI`

RU:

> Командующая, входящая передача Радаа. Её транслируют на Хиигару и всем кораблям на орбите.

EN:

> Commander, there is an incoming Radaa transmission. It is broadcasting to Hiigara and all craft in orbit.

Узел `Mission_M5#91`.

`M05_030_040_GR`

RU:

> Согласно нашему договору, передайте нам Материнский корабль и его гиперпространственное ядро. В противном случае мы уничтожим всё остальное ваше имущество.

EN:

> Per our agreement, surrender the Mothership and its Hyperspace Core, or we will destroy the balance of your assets.

Узел `Mission_M5#446`.

`M05_030_050_TS`

RU:

> Для них наши люди — разменная монета. А я торговаться не собираюсь.

EN:

> Our people are expendable to them, just negotiating points. And I'm not negotiating.

Узел `Mission_M5#216`.

`M05_030_060_FI`

RU:

> Приближаются новые силы противника.

EN:

> Additional enemy units are inbound.

### M05_040

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=wave6memos) #308`.

Узел `Mission_M5#649`.

`M05_040_010_KS`

RU:

> Ты идёшь в бой без колебаний.

EN:

> You strike without reserve.

Узел `Mission_M5#406`.

`M05_040_020_TS`

RU:

> Что толку колебаться, если они захватят верфь? Наши люди... Там мой единственный сын.

EN:

> What use will hesitation be If they take the shipyard. Our people...  My only son is on board.

Узел `Mission_M5#464`.

`M05_040_030_KS`

RU:

> Главный инженер Хаук? Но разве он не...

EN:

> Chief Engineer Hauk?  But isn't he...

Узел `Mission_M5#149`.

`M05_040_040_TS`

RU:

> Ещё мальчиком он почувствовал, что обычаи твоего киита ему ближе традиций того, в котором он родился. А у тебя есть близкие во флоте?

EN:

> As a boy he found the ways of your people more familiar than the traditions of the Kiith he was born into. Do you have people close to you in the fleet?

Узел `Mission_M5#508`.

`M05_040_050_KS`

RU:

> Пусть С’Джет и не воинский киит, но мы идём туда, где нужны.

EN:

> S'jets may not be a warrior kiith but we go where we are needed.

Узел `Mission_M5#597`.

`M05_040_060_FI`

RU:

> Контакт. Обнаружены многочисленные ударные корабли Радаа.

EN:

> Contact. Numerous Radaa Strike Craft detected.

### M05_050

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=triggerCutscene) #268`.

Узел `Mission_M5#452`.

`M05_050_010_FI`

RU:

> Сенсоры фиксируют массовое прибытие кораблей Радаа.

EN:

> Sensors are picking up a massive influx of Radaa ships.

Узел `Mission_M5#42`.

`M05_050_020_KS`

RU:

> Они бросают против нас всё, что у них есть.

EN:

> They are sending everything they have at us.

Узел `Mission_M5#440`.

`M05_050_030_TS`

RU:

> Пожалеют, что прислали так много.

EN:

> They will regret sending so many.

### M05_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=winLevel) #218`.

Узел `Mission_M5#424`.

`M05_070_010_FI`

RU:

> Сигнатур Радаа больше нет. Несущие конструкции верфи целы, повреждения минимальны.

EN:

> No further Radaa signatures. Shipyard superstructure still intact, damages minimal.

Узел `Mission_M5#516`.

`M05_070_020_KS`

RU:

> Ты справилась. Верфь в безопасности. Твой сын...

EN:

> You did it. The shipyard is safe. Your son is...

Узел `Mission_M5#480`.

`M05_070_030_TS`

RU:

> ...не будет в безопасности, пока в системе остаются Радаа. Как и все мы.

EN:

> ...not safe until all the Radaa are gone from this system. None of us are.

### M05_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=resourceLose) #185`.

Узел `Mission_M5#34`.

`M05_100_010_FI`

RU:

> Прекратить операцию! Защитить верфь невозможно.

EN:

> Abort, abort. Unable to defend the Shipyard.

### M05_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=defendLoss) #306`.

Узел `Mission_M5#304`.

`M05_110_010_FI`

RU:

> Верфь не подлежит восстановлению. Уцелевший экипаж направляется к спасательным капсулам.

EN:

> The shipyard is damaged beyond repair. Surviving crew are heading for the escape pods.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #139`; `CustomEvent #639`; `CustomEvent #657`; `OnSimReady #474`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M5#641`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M5#645`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M5#599`.

`FI_MothershipLost_06`

RU:

> Все системы в критическом состоянии. Покинуть Материнский корабль.

EN:

> All systems critically compromised. Abandon the Mothership.

Узел `Mission_M5#56`.

`FI_UnlockMultiGunCorvette`

RU:

> Наши инженеры расширили возможности сборочных цехов: теперь мы можем строить многопушечные корветы. Они отлично подходят для перехвата быстрых кораблей Радаа, угрожающих верфи.

EN:

> Our engineering team has added capability to our construction bays: Multi-Gun Corvettes. These are ideal for counter-attack against the Radaa's fast-moving threats to the shipyard.

## 6. M6: Оружие / The Weapon

Определение `c6a609b9e607c244fb916366c37ad701:1`, карта `level9`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M6 - Shattered/M6_Animatic_Intro/M6_Animatic_Intro.unity`

*Клип начинается в 0.98 с.*

`M06_010_010_A_TS`

RU:

> Радаа отброшены. Верфь уцелела, и скоро главный инженер Хаук поднимется на борт со своей группой и докладом.

EN:

> Radaa expelled. Shipyard still in orbit, and Officer Hauk will board shortly with his engineering team and a report.

*Клип начинается в 8.58 с.*

`M06_010_020_A_KS`

RU:

> Тирра, ты осваиваешь Материнский корабль так, словно родилась для этого. Гораздо быстрее, чем я.

EN:

> Tyrra, you are mastering the Mothership like you were born to it. Far faster than I did.

*Клип начинается в 13.68 с.*

`M06_010_030_A_TS`

RU:

> У меня есть то, чего не было у тебя: хорошая наставница.

EN:

> I have something you didn't: a good advisor.

*Клип начинается в 17.57 с.*

`M06_010_040_A_KS`

RU:

> Возможно, скоро я тебе больше не понадоблюсь.

EN:

> You may not need me much longer.

*Клип начинается в 20.37 с.*

`M06_010_050_A_TS`

RU:

> Я бы так не сказала. Да и высадить героиню войны за родной мир пока негде — безопасного места нет. Так что до конца этой истории мы вместе. Пора ударить по их командованию. Что известно об их оперативной базе?

EN:

> I wouldn't say that, but since there is no safe place to disembark the Hero of the Homeworld War, we are in this together for the duration. It's time to attack their command structure. What do we know of their base of operations?

*Клип начинается в 33.20 с.*

`M06_010_100_A_FI`

RU:

> Их главная база мобильна. Они называют её Башней Радаа. Обычно размещают в какой-нибудь системе на время своих дел, а затем перемещаются дальше.

EN:

> Their home base is mobile – they call it Radaa Tower – they often station it within one system to do business, then move on.

*Клип начинается в 41.16 с.*

`M06_010_110_A_KS`

RU:

> А теперь ведут дела с нами.

EN:

> And now they're doing business with us.

*Клип начинается в 44.85 с.*

`M06_010_120_A_TS`

RU:

> Нападение на орбитальную верфь было отвлекающим манёвром. Они связывали нас боем, пока развёртывали главную базу. Разведка, найдите эту башню!

EN:

> The attack on the Orbital Shipyard was a misdirect. To keep us occupied while they established their main base.  Intel, find that Tower!

*Клип начинается в 51.98 с.*

`M06_010_130_A_FI`

RU:

> Сканирую... В тени Хиигары обнаружен мощный источник энергии. По всем признакам — Башня Радаа. Передаю координаты.

EN:

> Scanning...picking up a massive energy signature in Hiigara shadow. Indications are that it is Radaa Tower. Transferring coordinates.

*Клип начинается в 61.02 с.*

`M06_010_140_A_TS`

RU:

> Вот и всё. Пора показать, что хиигаряне — нелёгкая добыча. Покончим с этим.

EN:

> That's it. Time to show that Hiigarans are not easy prey. Let's finish this.

### Задачи, подключённые к графу

Узлы: 92, 128, 243, 283, 314, 320, 377, 413, 435, 485, 619.

`M06_Objective_01`

RU:

> Найдите генератор щита.

EN:

> Locate a shield emitter.

Узлы: 253, 507, 537.

`M06_Objective_02`

RU:

> Пристыкуйте инженерный корвет к генератору щита.

EN:

> Dock an Engineer Craft to the shield emitter.

Узлы: 76, 277, 345, 479, 497, 648, 696.

`M06_Objective_03counter`

RU:

> Отключите генераторы щита.

EN:

> Disable shield emitters.

Узлы: 328, 570, 734.

`M06_Objective_04`

RU:

> Атакуйте Башню Радаа.

EN:

> Attack the Radaa Tower.

Узлы: 100, 363, 511, 704.

`M06_Objective_alphacapture`

RU:

> Отключите генератор щита «Альфа».

EN:

> Disable shield emitter alpha.

Узлы: 86, 592, 646, 702.

`M06_Objective_betacapture`

RU:

> Отключите генератор щита «Бета».

EN:

> Disable shield emitter beta.

Узлы: 281, 407, 503, 816.

`M06_Objective_deltacapture`

RU:

> Отключите генератор щита «Дельта».

EN:

> Disable shield emitter delta.

Узлы: 58, 122, 332, 373.

`M06_Objective_omegacapture`

RU:

> Отключите генератор щита «Омега».

EN:

> Disable shield emitter omega.

### M06_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #399`.

Узел `Mission_M6#353`.

`M06_020_010_FI`

RU:

> Вокруг башни сосредоточены многочисленные силы Радаа.

EN:

> Radaa forces are swarming around the tower.

Узел `Mission_M6#273`.

`M06_020_020_TS`

RU:

> Они пытаются нас отвлечь. Наша цель — башня.

EN:

> They are a distraction. Our target is the tower.

Узел `Mission_M6#580`.

`M06_020_023_AR`

RU:

> Материнский корабль хиигарян, Командование флота. Мы, Радаа, терпеливо ждём, когда вы вернёте нашу собственность.

EN:

> Hiigaran Mothership, Fleet Command.  We Radaa have been waiting patiently for you to turn over our property.

Узел `Mission_M6#174`.

`M06_020_025_TS`

RU:

> Не обращайте на неё внимания: мы пришли не разговаривать. Хаук, это искажение вокруг башни — щит?

EN:

> Ignore her  - we're not hear to talk.  Hauk, is that distortion around it a shield?

Узел `Mission_M6#574`.

`M06_020_030_HA`

RU:

> Похоже на то. Для щита такого размера им потребуется... пожалуй, четыре генератора.

EN:

> It appears so.  They would need maybe... four Shield Emitters to generate one that large.

Узел `Mission_M6#422`.

`M06_020_040_KS`

RU:

> Я работала над этой технологией. Ещё одна их кража. Пока не выведем из строя генераторы щита, нам не пробиться.

EN:

> I worked on that technology - something else they stole from us.  We won't get anywhere without taking down those shield emitters.

Узел `Mission_M6#289`.

`M06_020_050_TS`

RU:

> Понятно. Инженерным корветам приготовиться к развёртыванию. Найдите генераторы щита!

EN:

> Understood. Engineer Craft, prepare to deploy and find those Shield Emitters!

### M06_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=37, M06_Objective_01) #377`; `OnObjectiveCompleted (Objective=46, M06_Objective_01) #435`; `OnObjectiveCompleted (Objective=51, M06_Objective_01) #485`; `OnObjectiveCompleted (Objective=64, M06_Objective_01) #619`.

Узел `Mission_M6#38`.

`M06_030_010_FI`

RU:

> Генератор щита обнаружен. Чтобы отключить его, нужно пристыковать инженерный корвет.

EN:

> Shield Emitter located. Engineer Craft must dock to disable it.

### M06_040

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #489`.

Узел `Mission_M6#52`.

`M06_040_010_FI`

RU:

> Инженерный корвет отключает генератор щита. Во время работы он уязвим для атак.

EN:

> Engineer Craft is disabling the Shield Emitter, but it is vulnerable to attack.

### M06_050

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#96`.

`M06_050_010_FI`

RU:

> Генератор щита отключён. Остальные продолжают работать.

EN:

> Shield Emitter disabled. Remaining Shield Emitters still active.

### M06_060

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#56`.

`M06_060_010_FI`

RU:

> Генератор щита отключён. Осталось два.

EN:

> Shield Emitter disabled. Two remaining.

Узел `Mission_M6#120`.

`M06_060_020_AR`

RU:

> Это ваш последний шанс выполнить договор, обязательный для вашей планеты. Судя по вашим действиям, вы не желаете слушать. Но мы можем усилить давление, чтобы заставить вас вернуть наши активы. Выбор за вами.

EN:

> This is your last opportunity to abide by your planet's standing agreement.  Your present actions make me fear that you are not listening.  But we can escalate our efforts to force you to surrender our assets.  The choice is yours.

Узел `Mission_M6#708`.

`M06_060_030_TS`

RU:

> Отключить канал связи. Продолжайте искать генераторы щита.

EN:

> Shut off the com channel and keep searching for those Shield Emitters.

### M06_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#393`.

`M06_070_010_FI`

RU:

> Третий генератор щита отключён. Продолжайте поиск четвёртого.

EN:

> Third Shield Emitter now disabled. Scan for the fourth.

### M06_075

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#62`.

`M06_075_010_FI`

RU:

> Последний генератор щита отключён.

EN:

> The last Shield Emitter has been disabled.

Узел `Mission_M6#134`.

`M06_075_020_KS`

RU:

> Даже слишком легко.

EN:

> Almost too easy.

Узел `Mission_M6#576`.

`M06_075_030_TS`

RU:

> Зато теперь Башня Радаа беззащитна. Всем кораблям: новая цель.

EN:

> But now the Radaa Tower is wide open.  All ships, we have a new target.

### M06_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #826`; `CustomEvent (name=TS_scream) #772`; `CustomEvent (name=winLevel) #110`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M6#690`.

`M06_080_010_FI`

RU:

> Из гиперпространства вышла неизвестная станция Радаа.

EN:

> Unknown Radaa station has jumped in.

Узел `Mission_M6#437`.

`M06_080_075_TS`

RU:

> А-а-а-а-а-а-а-а-а!..

EN:

> --aaaaaaaaaaaauuughhh!!

Узел `Mission_M6#678`.

`M06_080_080_KS`

RU:

> Командующая! Тирра! Что случилось?

EN:

> Commander! Tyrra! What happened?

Узел `Mission_M6#662`.

`M06_080_020_TS`

RU:

> Какая огромная. Что это?

EN:

> It's massive. What is it?

Узел `Mission_M6#367`.

`M06_080_090_TS`

RU:

> Не понимаю... сенсоры... не вижу... не слышу... пытаюсь... пытаюсь...

EN:

> Unclear... sensors... can't see... can't hear... attempting... attempting to...

Узел `Mission_M6#652`.

`M06_080_030_FI`

RU:

> Анализируем.

EN:

> Analyzing.

Узел `Mission_M6#285`.

`M06_080_100_FI`

RU:

> Флот выведен из строя. Пытаемся восстановить связь.

EN:

> Fleet incapacitated. Trying to reestablish contact.

Узел `Mission_M6#523`.

`M06_080_040_TS`

RU:

> Вооружение обнаружено?

EN:

> Weapon systems detected?

Узел `Mission_M6#411`.

`M06_080_110_KS`

RU:

> Тирра, ты?..

EN:

> Tyrra are you...?

Узел `Mission_M6#229`.

`M06_080_043_KS`

RU:

> Мне это не нравится. Запускайте ядро!

EN:

> I don't like this. Spin up our core!

Узел `Mission_M6#764`.

`M06_080_120_TS`

RU:

> Рассчитываю... координаты... прыжка... в укромное место. Корабль им не достанется. Приготовиться... приготовиться... к... гипер...

EN:

> Shaping coordinates for...  for jump to...  isolation point. They won't get this ship. Prepare... prepare...for...hy-

Узел `Mission_M6#267`.

`M06_080_045_TS`

RU:

> Мы зашли так далеко — справимся и с этим. Но подготовьте прыжок на случай, если твои опасения оправдаются.

EN:

> We've come this far, we can fight this. But prepping for jump in case your fear is warranted.

Узел `Mission_M6#130`.

`M06_080_130_FI`

RU:

> Аварийный прыжок подтверждён.

EN:

> Emergency jump confirmed.

Узел `Mission_M6#443`.

`M06_080_050_FI`

RU:

> Похоже, станция накапливает энергию.

EN:

> Station appears to be powering up.

Узел `Mission_M6#433`.

`M06_080_060_KS`

RU:

> Они целятся в нас! Нужно немедленно прыгать!

EN:

> They're targeting us!  We must hyperspace jump now!

Узел `Mission_M6#554`.

`M06_080_070_TS`

RU:

> Ищу уязвимые места станции Радаа. Навожу орудие...

EN:

> Analyzing weak points of Radaa Station. Targeting weapon...

### M06_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #300`.

Узел `Mission_M6#426`.

`M06_100_010_FI`

RU:

> Ресурсы исчерпаны. Критические потери хиигарских кораблей. Общее отступление неизбежно.

EN:

> Resources depleted. Critical loss of Hiigaran ships. Full retreat unavoidable.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #784`; `CustomEvent #796`; `CustomEvent #806`; `OnSimReady #399`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M6#788`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M6#730`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M6#780`.

`FI_MothershipLost_07`

RU:

> Корпус разрушается. Системы жизнеобеспечения отказывают. Немедленно эвакуировать Материнский корабль.

EN:

> Loss of structural integrity. Life support failing. Evacuate the Mothership at once.

Узел `Mission_M6#451`.

`FI_UnlockAssaultFrigate`

RU:

> Технологии, полученные с верфи, позволили нам освоить новый тип кораблей — штурмовые фрегаты. Их тяжёлое вооружение отлично подходит для прорыва обороны Радаа, прикрывающей генераторы щита.

EN:

> With the technology transferred from the Shipyard, we can build a new ship: Assault Frigates. These heavy weapon craft are ideal for penetrating the Radaa defenses guarding the shield emitters.

## 7. M9: Система Тенхаузер / Tenhauser System

Определение `b1100962db5bfd04d93dc41a7563ff7c:1`, карта `level15`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M7 - Dark Side of Angel Moon/M7_Animatic_Intro/M7_Animatic_Intro.unity`

*Клип начинается в 0.00 с.*

`M09_003_010_A_FI`

RU:

> Переход в систему Тенхаузер завершён. Поступают сведения о повреждениях. Ваши приказы, командующая?

EN:

> We have successfully jumped to the Tenhauser System. Damage reports coming in.  What are your orders, Commander?

*Клип начинается в 6.65 с.*

`M09_003_020_A_KS`

RU:

> Тирра!

EN:

> Tyrra!

*Клип начинается в 7.33 с.*

`M09_003_030_A_FI`

RU:

> Командование не отвечает. Медицинским бригадам — в командную капсулу.

EN:

> Command is unresponsive. Med teams to Command Pod.

*Клип начинается в 10.90 с.*

`M09_003_040_A_KS`

RU:

> Тирра…!

EN:

> Tyrra...!

*Клип начинается в 11.83 с.*

`M09_003_050_A_FI`

RU:

> По докладу медиков, признаков жизни нет.

EN:

> Med teams reporting negative life signs.

*Клип начинается в 14.92 с.*

`M09_003_060_A_KS`

RU:

> Что?

EN:

> What?

*Клип начинается в 17.12 с.*

`M09_003_070_A_FI`

RU:

> …Гибель командующей флотом Тирры Собан в бою подтверждена. Медики сообщают о полном отказе нервной системы. Оружие Радаа вызвало перегрузку нейросвязи командующей с Материнским кораблём.

EN:

> ...Fleet Command Tyrra Soban... confirmed killed in action. Med teams report complete neural failure. The Radaa weapon overloaded the Commander's link to the mothership.

*Клип начинается в 28.52 с.*

`M09_003_073_A_KS`

RU:

> Она должна была разорвать связь!

EN:

> She should have broken the link!

*Клип начинается в 31.42 с.*

`M09_003_075_A_FI`

RU:

> Последним приказом командующей Тирры Собан был экстренный гиперпереход.

EN:

> Commander Tyrra Soban's last command was to initiate emergency hyperspace.

*Клип начинается в 37.33 с.*

`M09_003_080_A_KS`

RU:

> Тирра… При всех возможностях Материнского корабля… его сердцем была ты. И ты отдала всё, чтобы нас спасти.

EN:

> Oh Tyrra... All that the Mothership can do… you were its heart.  And it cost you everything to save us.

*Клип начинается в 46.78 с.*

`M09_003_085_A_KS`

RU:

> Разведка, доклад… состояние флота?

EN:

> Intel, report... fleet status?

*Клип начинается в 50.09 с.*

`M09_003_090_A_FI`

RU:

> Неизвестное оружие вывело из строя большую часть флота.

EN:

> Unknown weapon has disabled the majority of the fleet.

*Клип начинается в 53.62 с.*

`M09_003_100_A_KS`

RU:

> Состояние Материнского корабля?

EN:

> Mothership status?

*Клип начинается в 55.77 с.*

`M09_003_110_A_FI`

RU:

> Повреждён. Искусственный интеллект поддерживает основные системы. Аварийные бригады переносят командующую в медицинский отсек номер двенадцать.

EN:

> Damaged, AI systems maintaining ship basic operation.  Emergency teams are moving the Commander to Medbay Twelve.

*Клип начинается в 64.10 с.*

`M09_003_120_A_KS`

RU:

> Как скоро Радаа нас найдут?

EN:

> How long before the Radaa find us?

*Клип начинается в 66.71 с.*

`M09_003_130_A_FI`

RU:

> Неизвестно. Но вы, скорее всего, правы: они придут за нами.

EN:

> Unknown. But it is highly probable that you are correct - they will be coming.

*Клип начинается в 71.87 с.*

`M09_003_140_A_KS`

RU:

> Времени нет. В соответствии с чрезвычайными протоколами Кхарака я принимаю командование Материнским кораблём.

EN:

> No time. Under the Kharak Emergency Protocols, I am assuming command of the Mothership.

*Клип начинается в 81.68 с.*

`M09_003_145_A_KS`

RU:

> Передайте медикам: я иду в командную капсулу. Пусть откроют медицинское досье «Каран-ноль-ноль-ноль».

EN:

> Alert the med teams that I am on my way to the command pod. Tell them to access medical file, Karan-zero-zero-zero.

*Клип начинается в 90.31 с.*

`M09_003_150_A_FI`

RU:

> Принято, командующая Каран С’Джет.

EN:

> Confirmed, Commander Karan S'jet.

*Клип начинается в 95.67 с.*

`M09_003_160_A_HA`

RU:

> После гибели Тирры Собан только Каран С’Джет могла занять её место во главе флота. На этот раз она не колебалась.

EN:

> When Tyrra Soban fell, no one but Karan S'jet could take her place as Fleet Command. This time, she did not hesitate.

### Задачи, подключённые к графу

Узлы: 261, 567, 617.

`M09_Objective_00`

RU:

> Добудьте ресурсы для ремонта Материнского корабля.

EN:

> Harvest RU for Mothership repairs.

Узлы: 93, 459, 668.

`M09_Objective_01`

RU:

> Защитите торговый корабль Бентуси.

EN:

> Defend the Bentusi Exchange.

Узлы: 171, 227, 241, 243, 257, 355, 415, 591.

`M09_Objective_02`

RU:

> Найдите гиперпространственные врата Радаа.

EN:

> Locate Radaa Hyperspace Gates.

Узлы: 30, 60, 75, 135, 221, 251, 273, 399, 514, 654.

`M09_Objective_02b`

RU:

> Найдите верфь Радаа.

EN:

> Locate the Radaa Shipyard.

Узлы: 71, 97, 179, 233, 373, 393, 425, 429, 433, 480, 504, 516, 684.

`M09_Objective_03`

RU:

> Уничтожьте гиперпространственные врата Радаа.

EN:

> Destroy Radaa Hyperspace Gates.

Узлы: 91, 553, unlinked_19b05fa8-b5a0-4787-9765-f49e408178a8.

`M09_Objective_Timer`

RU:

> До гиперперехода Бентуси:

EN:

> Time until Bentusi warp out:

### M09_005

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #83`.

Узел `Mission_M9_v2#89`.

`M09_005_010_KS`

RU:

> Система жизнеобеспечения настроена. Я подключена ко всем действующим системам. Навигатор интегрирован. Я… Освобождённая.

EN:

> Life support calibrated. I am connected to all operant systems. Navigator embedded, I am... unbound.

Узел `Mission_M9_v2#435`.

`M09_005_020_FI`

RU:

> Ремонт завершён на пятьдесят процентов. Для полного восстановления Материнского корабля нужны дополнительные ресурсы. Сенсоры работают лишь частично.

EN:

> Repair progress at fifty percent. Additional resources needed to restore mothership to full functionality. Sensor systems at partial functionality.

Узел `Mission_M9_v2#506`.

`M09_005_030_KS`

RU:

> Мы потратили последние ресурсы, чтобы спасти корабль.

EN:

> We used the last of our resources to save the ship.

Узел `Mission_M9_v2#133`.

`M09_005_050_KS`

RU:

> Обнаружены тяжёлые повреждения корпуса и внутренних систем. Производственные мощности не работают.

EN:

> I am detecting massive damage to structural integrity and internal systems. Construction facilities down.

Узел `Mission_M9_v2#409`.

`M09_005_060_FI`

RU:

> Для ремонта нужны ключевые компоненты, которых у нас нет. Без них восстановление, похоже, невозможно.

EN:

> Repair looks impossible without key components we do not have in our reserves.

Узел `Mission_M9_v2#421`.

`M09_005_070_KS`

RU:

> Аварийным командам: снимайте детали отовсюду, где можно. Чего не найдёте — изобретайте. Я не позволю нам потерять надежду. Тирра, твоя жертва не будет напрасной.

EN:

> Damage control. Cannibalize what you can, invent what you can't. I won't let this be hopeless. Tyrra, your sacrifice will have meaning.

Узел `Mission_M9_v2#315`.

`M09_005_080_FI`

RU:

> Сенсоры обнаружили мощный аномальный сигнал. Источник определить не удаётся. Также фиксируем приближающиеся корабли, предположительно Радаа.

EN:

> Sensors detecting powerful anomalous signature. Can't lock it down. Also picking up potential Radaa ships on incoming vectors.

Узел `Mission_M9_v2#589`.

`M09_005_090_KS`

RU:

> Нужно восстановить хотя бы сенсоры. Нам необходимы эти ресурсы.

EN:

> We have to get sensors back, at least.  We need those resources.

### M09_008

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

Узел `Mission_M9_v2#249`.

`M09_008_010_KS`

RU:

> Сенсоры снова работают. Это чувство я помню.

EN:

> Sensors back online. This is what I remember.

Узел `Mission_M9_v2#664`.

`M09_008_020_FI`

RU:

> Мы перехватили сообщение адмирала Гиитана.

EN:

> We have intercepted communication from Admiral Giitan.

Узел `Mission_M9_v2#48`.

`M09_008_030_GR`

RU:

> Им от нас не спрятаться и не отбиться. Станция «Раскол» поразила цель. Доставьте мне останки Материнского корабля! И это ядро Предтеч!

EN:

> They can't hide from us, they can't fight us, Shatter Station hit its target. Bring me what's left of the Mothership! Bring me that Progenitor Core.

Узел `Mission_M9_v2#666`.

`M09_008_040_KS`

RU:

> Станция «Раскол». Вот что нас покалечило. Мы ещё не готовы к бою.

EN:

> Shatter Station. That's what left us broken. We're not ready to fight.

Узел `Mission_M9_v2#331`.

`M09_008_050_FI`

RU:

> Появляются новые сигналы…

EN:

> Signatures appearing now...

### M09_020

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

Узел `Mission_M9_v2#219`.

`M09_020_005_BN`

RU:

> Мы помним тебя, Каран С’Джет, Искательница Дома. Ты вновь стала той, кем тебе суждено быть. Освобождённой. Мы приветствуем тебя среди нас.

EN:

> We remember you, Karan S'jet, Seeker of The Home. You are now again what you will be. Unbound. And we welcome you to your place.

Узел `Mission_M9_v2#267`.

`M09_020_010_KS`

RU:

> Спасибо. Но почему вы здесь именно сейчас? В этой точке пространства и времени?

EN:

> Thank you. But why are you here, now? At this point in spacetime?

Узел `Mission_M9_v2#229`.

`M09_020_020_BN`

RU:

> Хиигаряне достойны нашей помощи. Радаа — нет.

EN:

> Hiigarans are worthy of our help. The Radaa are not.

Узел `Mission_M9_v2#656`.

`M09_020_030_KS`

RU:

> Вы знаете о них?

EN:

> You know of them?

Узел `Mission_M9_v2#69`.

`M09_020_040_BN`

RU:

> Мы созидаем галактику честным обменом и передачей Знания. Радаа торгуют ущербными системами, которые оказываются бесполезны, и так забирают всё, чего пожелают. Воры. Служители Энтропии.

EN:

> We shape the galaxy on honorable exchange and the sharings of Knowledge. The Radaa trade flawed systems that prove useless in order to take what they desire. Thieves. Agents of Entropy.

Узел `Mission_M9_v2#549`.

`M09_020_050_KS`

RU:

> Вы сталкивались с их оружием, способным одним выстрелом вывести из строя целый флот? Они называют его станцией «Раскол».

EN:

> Have you faced their weapon that can disable a fleet in one blast?  They call it Shatter Station.

Узел `Mission_M9_v2#587`.

`M09_020_060_BN`

RU:

> Мы знаем о нём. Потому и пришли, Каран С’Джет. Прежде всего, у нас есть технология, способная тебя исцелить. Начинаем передачу.

EN:

> We are aware, and that is why we came Karan S'jet.  First, we have the technology to heal you.  Initiating transfer.

Узел `Mission_M9_v2#498`.

`M09_020_070_KS`

RU:

> Технология Бентуси получена. Производственные отсеки снова работают в полном объёме.

EN:

> Bentusi technology received. Construction bays are online and fully functional.

Узел `Mission_M9_v2#117`.

`M09_020_080_BN`

RU:

> Мы слышим шёпот технологий, которые Радаа похитили у нас…

EN:

> We can hear the whispers of the technology the Radaa have stolen from us--

### M09_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

Узел `Mission_M9_v2#153`.

`M09_030_010_BN`

RU:

> Радаа пришли за вами.

EN:

> The Radaa have come for you.

Узел `Mission_M9_v2#437`.

`M09_030_020_KS`

RU:

> Должно быть, выследили нас по сигналу ядра.

EN:

> They must have followed our core signature.

Узел `Mission_M9_v2#54`.

`M09_030_030_BN`

RU:

> Мы не желаем сражаться с похищенными частицами Нас самих. Радаа перегородили наш сектор, разместив в нём несколько гиперпространственных врат.

EN:

> We are not willing to fight the stolen parts of Ourselves. The Radaa have made a wall in our sector by placing multiple hyperspace gates.

Узел `Mission_M9_v2#457`.

`M09_030_040_KS`

RU:

> Все системы восстановлены. Мы готовы сражаться. А после надеемся услышать от вас об их технологиях.

EN:

> All systems back online, we are prepared to fight. Then we hope you can tell us about their technology.

### M09_040

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

Узел `Mission_M9_v2#44`.

`M09_040_010_FI`

RU:

> Гиперпространственные врата уничтожены. Найдите остальные.

EN:

> Hyperspace gate destroyed. Locate remaining gates.

### M09_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

Узел `Mission_M9_v2#563`.

`M09_050_010_FI`

RU:

> Гиперпространственные врата уничтожены. В секторе есть и другие.

EN:

> Hyperspace gate eliminated. More gates remain.

### M09_060

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M9_v2#451`.

`M09_060_010_FI`

RU:

> Уничтожение врат подтверждено. Ищем остальные.

EN:

> Gate destruction confirmed. Scanning for more gates.

### M09_070

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

Узел `Mission_M9_v2#629`.

`M09_070_010_FI`

RU:

> Гиперпространственные врата уничтожены. Сектор чист.

EN:

> Hyperspace gates neutralized. Sector clear.

### M09_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=winLevel) #585`.

Узел `Mission_M9_v2#337`.

`M09_080_010_BN`

RU:

> Ты сдержала слово, Каран С’Джет с Хиигары. Теперь мы поделимся тем, что знаем о разрушительном оружии Радаа.

EN:

> You kept your word, Karan S'jet of Hiigara.  What we understand of the devastating Radaa weapon we can share with you.

Узел `Mission_M9_v2#571`.

`M09_080_015_BN`

RU:

> Оно работает на редком минерале, который встречается во Внешнем рифе. Этот же минерал может защитить вас от оружия. Мы предоставим необходимые сведения.

EN:

> It operates off a rare mineral found in the Outer Reef. You can also use this mineral to protect against it. We can provide specific details.

Узел `Mission_M9_v2#109`.

`M09_080_020_KS`

RU:

> Главный инженер Хаук, приготовьтесь принять данные от Бентуси.

EN:

> Chief Engineer Hauk, prepare to receive data from the Bentusi.

Узел `Mission_M9_v2#163`.

`M09_080_030_BN`

RU:

> Мы больше не желаем слышать Радаа. Галактика ничего не потеряет, если их Песнь умолкнет. Воспользуйтесь нашим знанием и заставьте её смолкнуть. Прощайте.

EN:

> We do not wish to hear the Radaa again. The Galaxy will not be less for the loss of their Song. Use our knowledge to ensure it is silenced. Farewell.

### M09_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=NormalLossEvent) #145`; `CustomEvent (name=NormalLossEvent) #658`.

Узел `Mission_M9_v2#253`.

`M09_090_010_FI`

RU:

> Слишком много кораблей потеряно. Запасы ресурсов исчерпаны. Начинаем отступление.

EN:

> Too many ships destroyed, resource stores depleted. Retreat underway.  

### M09_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #443`.

Узел `Mission_M9_v2#291`.

`M09_100_010_FI`

RU:

> Корабль Бентуси получает тяжёлые повреждения. Нужно его защитить.

EN:

> Bentusi ship taking substantial damage. We need to defend it.

### M09_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #147`.

Узел `Mission_M9_v2#490`.

`M09_110_010_FI`

RU:

> Корабль Бентуси больше не выдержит длительного обстрела.

EN:

> Bentusi ship will not be able to withstand attack for much longer.

### M09_120

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=OutpostLossEvent) #525`.

Узел `Mission_M9_v2#155`.

`M09_120_010_FI`

RU:

> Корабль Бентуси получил критические повреждения. Корпус разрушен. Повторяю: Бентуси погибли.

EN:

> Bentusi ship critically damaged, hull integrity lost, repeat the Bentusi are lost.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #36`; `CustomEvent #728`; `CustomEvent #757`; `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M9_v2#759`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M9_v2#771`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M9_v2#518`.

`FI_MothershipLost_05`

RU:

> Материнский корабль получил катастрофические повреждения. Всем — к спасательным капсулам.

EN:

> Catastrophic damage to Mothership. All hands to the escape pods.

Узел `Mission_M9_v2#211`.

`FI_UnlockBarricadeFrigate`

RU:

> Благодаря технологиям Бентуси наши сборочные цеха теперь могут выпускать баррикадные фрегаты. При активации они прикрывают щитом находящиеся рядом корабли. С их помощью можно защитить и самих Бентуси.

EN:

> With the technology the Bentusi provided, our construction bays can now build Barricade Frigates. When activated, these can provide shields for nearby ships. They can also be used to protect the Bentusi.

## 8. M10: Добывающий комплекс Внешнего рифа / Outer Reef Mining Facility

Определение `5cd7702c05ff025469152b598cb0fda8:1`, карта `level17`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M10 - The Final Push/M10_Animatic_Intro/M10_Animatic_Intro.unity`

*Клип начинается в 0.72 с.*

`M10_010_010_A_KS`

RU:

> Командование флота на связи. Проверяю все системы.

EN:

> Fleet Command online. Assessing all systems.

*Клип начинается в 4.47 с.*

`M10_010_020_A_HA`

RU:

> Сведения Бентуси о технологиях Радаа… Именно с их помощью мы сможем сокрушить врага. Так же, как они сокрушили наш флот… и мою мать.

EN:

> The Bentusi’s information about the Radaa technology… this is exactly what we need to bring them down, just like they brought down our fleet… and my mother.

*Клип начинается в 13.77 с.*

`M10_010_030_A_KS`

RU:

> Хаук… Только благодаря Тирре мы ещё живы и можем продолжать борьбу. Она пожертвовала всем, чтобы спасти нас… Чтобы спасти тебя.

EN:

> Hauk.... Tyrra is the only reason we are still here to continue the fight...she sacrificed everything to save us... To save you.

*Клип начинается в 24.19 с.*

`M10_010_033_A_HA`

RU:

> Я знаю. Тактиком она была лучше, чем матерью. Но она навсегда останется со мной.

EN:

> I know. She was better at tactics than she was as a mother, but she will walk with me always.

*Клип начинается в 31.03 с.*

`M10_010_035_A_KS`

RU:

> Акадет Ферин.

EN:

> Akadeth Ferin.

*Клип начинается в 32.57 с.*

`M10_010_037_A_HA`

RU:

> Акадет Ферин.

EN:

> Akadeth Ferin.

*Клип начинается в 35.58 с.*

`M10_010_040_A_HA`

RU:

> В данных Бентуси есть схема устройства, способного защитить нас от оружия станции «Раскол». Но для его создания понадобится много редкой разновидности проводящего кремния.

EN:

> The Bentusi data shows a device we could construct to counter the Shatter Station weapon but we will need a substantial amount of a rare conductive silicon.

*Клип начинается в 43.38 с.*

`M10_010_050_A_FI`

RU:

> Мы обнаружили запасы на старом добывающем комплексе в астероидном поле Внешнего рифа. Координаты подтверждены. Поблизости могут быть вражеские силы.

EN:

> We have identified a supply in an old mining operation located at an outer reef asteroid field. Coordinates confirmed. There may be hostiles in the vicinity.

*Клип начинается в 54.10 с.*

`M10_010_060_A_KS`

RU:

> Тирра бы не колебалась. И мы не упустим этот шанс. Приготовиться к гиперпереходу по моей команде. Пусть знают: мы всё ещё умеем быть смелыми.

EN:

> Tyrra would not hesitate, and we will not waste this chance. Prepare for Hyperspace jump, on my command. And we will let them know that we are still brave.

### Задачи, подключённые к графу

Узлы: 126, 179, 240, 295, 655, 746, 770.

`M10_Objective_01`

RU:

> Пристыкуйте 3 инженерных корвета к добывающей платформе.

EN:

> Dock 3 Engineer Craft to the Mining Platform.

Узлы: 140, 144, 185, 557, 563, 809.

`M10_Objective_03`

RU:

> Пристыкуйте 3 инженерных корвета к добывающей платформе.

EN:

> Dock 3 Engineer Craft to the Mining Platform.

Узлы: 299, 665.

`M10_Objective_05`

RU:

> Уничтожьте вражеский патруль, охраняющий последнюю добывающую платформу.

EN:

> Destroy enemy patrol protecting the final Mining Platform.

Узлы: 26, 68, 88, 102, 122, 321, 347, 707, 715.

`M10_Objective_07`

RU:

> Защищайте добывающую платформу, пока инженерные корветы извлекают резонансный кремний.

EN:

> Defend Mining Platform while Engineer Craft salvage Resonant Silicon.

### M10_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #114`.

Узел `Mission_M10#313`.

`M10_020_010_KS`

RU:

> Гиперпереход завершён. Начать поиск кремния.

EN:

> Hyperspace jump successful. Scan for the silicon material.

Узел `Mission_M10#146`.

`M10_020_020_HA`

RU:

> Вижу несколько астероидных полей. Здесь есть заброшенные платформы, установленные для добычи кремния.

EN:

> I'm seeing multiple asteroid fields. There are several abandoned mining platforms that were placed to extract the silicon.

Узел `Mission_M10#729`.

`M10_020_030_KS`

RU:

> Запасы уже исчерпаны?

EN:

> Has the material been exhausted?

Узел `Mission_M10#437`.

`M10_020_040_FI`

RU:

> Обнаружены малые корабли Радаа у платформ и по всему сектору.

EN:

> Detecting Radaa strike craft around the Platforms and throughout this sector.

Узел `Mission_M10#28`.

`M10_020_050_KS`

RU:

> Явно не исчерпаны. И если кремний нужен Радаа, им он не достанется. Вызываю ударные группы.

EN:

> Clearly not exhausted. And if the Radaa want it, we cannot let them have it. Calling up Strike Groups.

Узел `Mission_M10#512`.

`M10_020_060_FI`

RU:

> Силы Радаа выдвигаются к добывающим платформам, чтобы взять их под контроль.

EN:

> Radaa forces moving to secure the Mining Platforms.

Узел `Mission_M10#619`.

`M10_020_070_HA`

RU:

> Нам нужен весь резонансный кремний, какой только удастся собрать. Инженерные корветы могут извлечь его с платформ. Но им понадобится защита.

EN:

> We need all the resonant silicon we can get our hands on.  Engineer Craft can recover the mineral from the platforms.  But they will need protection.   

Узел `Mission_M10#762`.

`M10_020_080_KS`

RU:

> Значит, уничтожим Радаа и займём платформы. Одну за другой.

EN:

> So we will eliminate the Radaa and take the platforms, one by one.

### M10_030

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #215`; `CustomEvent #415`; `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M10#839`.

`M10_030_010_FI`

RU:

> Первая добывающая платформа под нашим контролем. Инженерные корветы уже извлекают минерал.

EN:

> First mining platform secured.  Engineer Craft mineral recovery well under way.

Узел `Mission_M10#277`.

`M10_030_020_KS`

RU:

> Теперь к следующей платформе.

EN:

> Now to the next platform.

### M10_040

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #215`; `CustomEvent #415`; `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`; `OnObjectiveCompleted (Objective=8, M10_Objective_07) #102`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M10#670`.

`M10_040_010_FI`

RU:

> Следующая добывающая платформа захвачена. Извлечение кремния начато.

EN:

> Next mining platform secured, silicon recovery has commenced. 

Узел `Mission_M10#585`.

`M10_040_020_FI`

RU:

> Есть третья платформа, но её охрана гораздо сильнее. Атаковать её крайне опасно.

EN:

> There is a third platform, much more heavily guarded. Engaging it would be highly dangerous.

Узел `Mission_M10#175`.

`M10_040_030_KS`

RU:

> Нам нужен этот кремний. Подберём ударные группы — и справимся.

EN:

> We need that silicon.  With the right Strike Groups, we can take them.

### M10_050

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`; `OnObjectiveCompleted (Objective=8, M10_Objective_07) #102`; `OnWaveDestroyed (Enabled=True) #448`.

Узел `Mission_M10#559`.

`M10_050_010_FI`

RU:

> Силы Радаа у последней добывающей платформы уничтожены.

EN:

> Radaa forces around the last mining platform have been eliminated.  

### M10_060

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`; `OnObjectiveCompleted (Objective=8, M10_Objective_07) #102`; `OnWaveDestroyed (Enabled=True) #448`.

Узел `Mission_M10#279`.

`M10_060_010_FI`

RU:

> Контакт! Из гиперпространства вышел линейный крейсер Радаа. Его огневой мощи хватит, чтобы разгромить наш флот.

EN:

> Contact! A Radaa Battlecruiser has jumped in. It has enough firepower to cripple our fleet.

Узел `Mission_M10#611`.

`M10_060_020_KS`

RU:

> Мы можем таранить его добывающей платформой. Тирре бы понравилось.

EN:

> We can use the Mining Platform as a battering ram. Tyrra would like that.

Узел `Mission_M10#464`.

`M10_060_030_FI`

RU:

> Чтобы направить платформу на линейный крейсер, потребуется несколько инженерных корветов.

EN:

> Multiple Engineer Craft are needed to steer it into the Battlecruiser.

### M10_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #446`.

Узел `Mission_M10#721`.

`M10_070_010_KS`

RU:

> Инженерные корветы закрепились на платформе.

EN:

> The Engineer Craft are locked in.  

Узел `Mission_M10#678`.

`M10_070_020_FI`

RU:

> Добывающая платформа идёт на столкновение с линейным крейсером.

EN:

> Mining platform is on course to collide with the Battlecruiser.

### M10_080

Обработчики, достигающие этих реплик по control-связям: `OnCheatEvent2 #369`; `OnDetectShip #567`.

Узел `Mission_M10#782`.

`M10_080_010_KS`

RU:

> Есть попадание!

EN:

> We have impact!  

Узел `Mission_M10#647`.

`M10_080_020_FI`

RU:

> Линейный крейсер уничтожен. Силы Радаа отступают.

EN:

> Battlecruiser eliminated. Radaa forces are in retreat.

### M10_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #565`; `CustomEvent #631`; `CustomEvent #727`; `CustomEvent (name=LossEvent) #530`; `OnCheatEvent3 #494`.

Узел `Mission_M10#389`.

`M10_100_010_FI`

RU:

> Критические потери кораблей, ресурсы исчерпаны. Флот отступает по всем направлениям.

EN:

> Critical ship loss, resources depleted. Fleet in full retreat.

### M10_110

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=4, Objective_M10_00) #72`.

Узел `Mission_M10#60`.

`M10_110_010_FI`

RU:

> Силы Радаа у этой добывающей платформы держатся плотным строем и не дадут нам пристыковаться. Рекомендуем занять другие платформы.

EN:

> Radaa forces around this mining platform are in tight formation, which will block any attempt at docking.  Recommend securing the other platforms.  

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #46`; `CustomEvent #835`; `CustomEvent #852`; `OnSimReady #114`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M10#854`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M10#858`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M10#90`.

`FI_MothershipLost_06`

RU:

> Все системы в критическом состоянии. Покинуть Материнский корабль.

EN:

> All systems critically compromised. Abandon the Mothership.

Узел `Mission_M10#80`.

`FI_UnlockIonFrigate`

RU:

> Бентуси также передали нам ключевые компоненты для нового класса кораблей — ионных фрегатов. Они отлично подходят для дальнего боя и способны прожигать корпуса крупных кораблей.

EN:

> The Bentusi also provided us the key components necessary to build a new ship class: Ion Frigates, which are ideal for long range attacks and cutting into the hulls of larger ships.

## 9. M11: Создатели оружия / The Weapon Architects

Определение `653d9688338bfb943b561c979612218e:1`, карта `level19`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M11 - Intelligence/M11_Animatic_Intro/M11_Animatic_Intro.unity`

*Клип начинается в 0.65 с.*

`M11_010_010_A_FI`

RU:

> Наши команды извлекли резонансный кремний с добывающих платформ.

EN:

> Our resource teams have extracted the resonant silicon from the mining platforms.

*Клип начинается в 5.62 с.*

`M11_010_020_A_HA`

RU:

> Кремния оказалось больше, чем я ожидал, даже без третьей платформы. Моя команда приступает к анализу.

EN:

> Silicon yield from the platforms is higher than I expected, even without the third platform.  My team is commencing analysis.

*Клип начинается в 13.83 с.*

`M11_010_030_A_KS`

RU:

> Я успела изучить данные Бентуси. Одного кремния недостаточно, чтобы противостоять их оружию. Каков ваш план, Хаук?

EN:

> I've had a moment to review the Bentusi data, silicon alone will not be enough to counter their weapon.  What's your plan, Hauk?

*Клип начинается в 21.05 с.*

`M11_010_040_A_HA`

RU:

> Материала для работы хватает, но без консультации инженера-оружейника Радаа нам понадобится больше времени.

EN:

> We have a lot to work with, but without a Radaan weapons engineer to consult, we will need more time.

*Клип начинается в 25.62 с.*

`M11_010_050_A_KS`

RU:

> А вот времени у нас нет. Разведка, найдите нам консультанта. Быстро.

EN:

> Time is the one thing we don't have. Intel, find us a consultant...fast.

*Клип начинается в 30.72 с.*

`M11_010_060_A_FI`

RU:

> Изучаем разведдонесения… Сверяем сведения о персонале за период сотрудничества Радаа с хиигарским командованием… Есть. Создатели оружия Радаа находятся на эсминце в системе Хиигары, в квадранте Омега.

EN:

> Accessing recon reports... cross referencing personnel codes from when the Radaa were consulting with Hiigaran Command... found it.  Radaa weapons architects identified on a Destroyer in the Hiigara System, Quadrant Omega.

*Клип начинается в 46.63 с.*

`M11_010_070_A_FI`

RU:

> Точные координаты и идентификатор корабля неизвестны.

EN:

> Exact position and ship ID is unclear.

*Клип начинается в 49.48 с.*

`M11_010_080_A_KS`

RU:

> Не впервой мне охотиться на дюнную змею, Разведка. Подберёмся поближе.

EN:

> Won't be my first hunt for a dune snake, Intel.  Let's get close.

*Клип начинается в 53.34 с.*

`M11_010_090_A_FI`

RU:

> Передаём координаты.

EN:

> Sending coordinates.

*Клип начинается в 54.92 с.*

`M11_010_100_A_KS`

RU:

> Приняты. Приготовиться к гиперпереходу по моей команде. Переход!

EN:

> Received.  Prepare for hyperspace on my mark.  Mark!

### Задачи, подключённые к графу

Узлы: 143, 287, 401.

`M11_Objective_01`

RU:

> Найдите корабль с создателями оружия на борту.

EN:

> Locate the ship containing the weapon architects.

Узлы: 107, 135, 199, 367, 523, 575.

`M11_Objective_02`

RU:

> Уничтожьте гиперпространственные врата.

EN:

> Destroy the Hyperspace Gate.

Узлы: 78, 299, 419.

`M11_Objective_03`

RU:

> Защищайте Материнский корабль до прибытия транспорта с пленными.

EN:

> Defend the Mothership until the Personnel Craft arrives.

Узлы: 413, 453, 471.

`M11_Objective_03a`

RU:

> Пристыкуйте 3 инженерных корвета к эсминцу Радаа.

EN:

> Dock 3 Engineer Craft to the Radaa Destroyer.

Узлы: 55, 309.

`M11_Objective_03b`

RU:

> Сопроводите транспорт с пленными к Материнскому кораблю.

EN:

> Escort the Personnel Craft back to the Mothership.

### M11_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #497`.

Узел `Mission_M11#35`.

`M11_020_010_KS`

RU:

> Гиперпереход завершён. Подтвердите местоположение корабля с создателями оружия на борту.

EN:

> Hyperspace jump successful. Confirm location of the ship holding the weapons architects.

Узел `Mission_M11#123`.

`M11_020_020_FI`

RU:

> К сожалению, это невозможно, командующая. Мы ожидали встретить один эсминец Радаа, но обнаружили в секторе три.

EN:

> Unfortunately Commander, not possible. We were led to believe there was a single Radaa Destroyer, but we have detected three in this sector.

Узел `Mission_M11#343`.

`M11_020_030_FI`

RU:

> Рекомендуем проверить каждую точку и просканировать корабли, чтобы найти цель.

EN:

> Recommend investigating each coordinate to scan for our target.

### M11_030

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #569`.

Узел `Mission_M11#191`.

`M11_030_010_FI`

RU:

> Результат сканирования отрицательный. Нужных нам людей на этом корабле нет. Следуйте к следующей точке.

EN:

> Scan reads negative. Targets not on board this ship. Proceed to next coordinate.

### M11_040

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #43`.

Узел `Mission_M11#455`.

`M11_040_010_FI`

RU:

> Отрицательно. Создателей оружия на этом эсминце не обнаружено. Продолжайте поиски.

EN:

> Negative. Weapon architect designation not detected on this Destroyer. Continue the search.  

### M11_050

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #535`.

Узел `Mission_M11#361`.

`M11_050_010_FI`

RU:

> Сканирование персонала подтвердило: создатели оружия находятся на этом эсминце.

EN:

> Personnel scan confirms - the architects are passengers on this Destroyer.  

Узел `Mission_M11#101`.

`M11_050_020_FI`

RU:

> Срочное предупреждение! Эсминец обнаружил нас и уходит к ближайшим гиперпространственным вратам.

EN:

> Priority alert! The Destroyer has detected our presence and is fleeing to the nearest hyperspace gate.

Узел `Mission_M11#203`.

`M11_050_030_KS`

RU:

> Всем кораблям! Уничтожить врата, пока Радаа не успели уйти.

EN:

> All ships! Destroy that gate before the Radaa use it to escape.

### M11_060

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=objective_2start) #525`.

Узел `Mission_M11#109`.

`M11_060_010_FI`

RU:

> В систему прибывают вражеские силы для защиты эсминцев.

EN:

> Enemy units entering the system to defend the Destroyers.

### M11_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=16, M11_Objective_02) #199`.

Узел `Mission_M11#479`.

`M11_070_010_FI`

RU:

> Гиперпространственные врата уничтожены.

EN:

> Hyperspace gate destroyed.

Узел `Mission_M11#543`.

`M11_070_020_KS`

RU:

> Путь к отступлению отрезан. Захватите эсминец и возьмите под стражу тех, за кем мы пришли.

EN:

> We've taken away their escape route.  Capture the Destroyer, and secure the personnel we came for.

Узел `Mission_M11#183`.

`M11_070_030_FI`

RU:

> Инженерные корветы должны закрепиться на эсминце и отбуксировать его к Материнскому кораблю.

EN:

> Engineer Craft are needed to latch on to the Destroyer and haul it back to the Mothership.

### M11_080

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #397`.

Узел `Mission_M11#459`.

`M11_080_010_FI`

RU:

> Эсминец взят на буксир. Внимание: обнаружены новые корабли Радаа.

EN:

> Destroyer under tow. Warning, additional Radaa craft detected.

Узел `Mission_M11#429`.

`M11_080_020_KS`

RU:

> Они могут попытаться уничтожить эсминец, прежде чем мы завершим передачу пленных. Всем кораблям — прикрыть его.

EN:

> They may want to eliminate the Destroyer before we complete the transfer. All ships, move to defend.

### M11_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #509`.

Узел `Mission_M11#441`.

`M11_090_010_FI`

RU:

> Из гиперпространства выходят крупные силы Радаа. Их цель — Материнский корабль.

EN:

> Heavy Radaa forces are jumping in and are now targeting the Mothership.

Узел `Mission_M11#113`.

`M11_090_020_KS`

RU:

> Придётся уничтожить Радаа, прежде чем мы сможем перевести создателей оружия на Материнский корабль.

EN:

> We'll have to eliminate the Radaa to get the weapons architects onto the Mothership.

### M11_100

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #527`.

Узел `Mission_M11#45`.

`M11_100_010_FI`

RU:

> Эсминец приблизился к Материнскому кораблю. Силы Радаа уничтожены.

EN:

> Destroyer is in range of the Mothership.  Radaa threats are eliminated.

Узел `Mission_M11#503`.

`M11_100_020_KS`

RU:

> Создатели оружия у нас. Гиперпереход по моей команде.

EN:

> Architects secured. Hyperspace jump on my mark.

### M11_150

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #37`.

Узел `Mission_M11#437`.

`M11_150_010_FI`

RU:

> Ресурсы исчерпаны. Корабли уничтожены. Эсминец избежал захвата.

EN:

> Resources depleted. Ships destroyed. The Destroyer has evaded capture.

### M11_160

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #583`.

Узел `Mission_M11#573`.

`M11_160_010_FI`

RU:

> Перегруппироваться! Эсминец-цель ушёл через гиперпространственные врата. Повторяю: эсминец ушёл.

EN:

> Regroup! Targeted Destroyer has escaped through the Hyperspace Gate. Repeat: The Destroyer has escaped.

### M11_170

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #583`.

Узел `Mission_M11#593`.

`M11_170_010_FI`

RU:

> Эсминец с создателями оружия уничтожен. Мы потеряли цель.

EN:

> Destroyer with the Weapon Architects has been destroyed.  Our target is lost.  

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #255`; `CustomEvent #273`; `CustomEvent #373`; `OnSimReady #497`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M11#241`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M11#239`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M11#545`.

`FI_MothershipLost_08`

RU:

> Полный отказ систем. Экипажу Материнского корабля — покинуть корабль.

EN:

> Complete systems failure. Mothership crew must abandon ship.

Узел `Mission_M11#72`.

`FI_UnlockDestroyer`

RU:

> Мы расширили возможности сборочных цехов и можем строить новый тип кораблей — эсминцы. Вооружение этих крупных боевых кораблей особенно эффективно против эскадрилий ударных кораблей.

EN:

> Our ship construction capabilities have been upgraded to build a new ship: Destroyers. These capital class ships have weapon systems most effective against squadrons of strike craft.

## 10. M8: Наступление на Гиббас / The Gybbas Offensive

Определение `a5358fed0221c06459236bb5e555ec41:1`, карта `level13`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M8 - Supply Lines/M8_Animatic_Intro/M8_Animatic_Intro.unity`

*Клип начинается в 0.93 с.*

`M08_010_010_A_KS`

RU:

> Создатели оружия у нас. Материнский корабль в строю. Инженерная служба, мы готовы противостоять станции «Раскол»?

EN:

> Weapons Architects secured. Mothership operational. Engineering, are we ready to face Shatter Station?

*Клип начинается в 8.30 с.*

`M08_010_030_A_HA`

RU:

> Да это же бессмыслица! Объясняй ещё раз, скользкий торгаш, не то я…

EN:

> That makes no sense!  Explain again, slime-merchant, or so help me...

*Клип начинается в 11.85 с.*

`M08_010_040_A_KS`

RU:

> Офицер Хаук!

EN:

> Officer Hauk!

*Клип начинается в 12.74 с.*

`M08_010_050_A_HA`

RU:

> Простите… Командование, мы проводим моделирование, но наш гость помогает не так охотно, как я надеялся. Нужно ещё время. Я не отправлю вас туда, пока не буду уверен, что смогу защитить. Я не потеряю ещё и вас.

EN:

> Sorry...Command, we're running simulations, but our guest is not being as helpful as I had hoped. We need more time. I won't send you in without knowing I can protect you. I won't lose you too.

*Клип начинается в 25.55 с.*

`M08_010_060_A_KS`

RU:

> Прости. На её месте должна была быть я.

EN:

> I'm sorry. It should have been me.

*Клип начинается в 31.33 с.*

`M08_010_070_A_FI`

RU:

> По нашим данным, Радаа вернулись на орбитальные верфи Гиббаса. Они собирают огромный флот.

EN:

> Reports show that the Radaa have returned to the Orbital Shipyards around Gybbas. They are building up a massive fleet.

*Клип начинается в 38.08 с.*

`M08_010_080_A_KS`

RU:

> Если мы не разгромим этот флот, даже уничтожение станции «Раскол» нас не спасёт.

EN:

> If we don't break up that fleet it won't matter if we stop Shatter Station.

*Клип начинается в 41.87 с.*

`M08_010_090_A_FI`

RU:

> У нас подробные разведданные по этому сектору. Теперь нам хватит огневой мощи, чтобы уничтожить верфь, если удастся подобраться достаточно близко.

EN:

> Our intelligence on the sector is excellent, and we now have the firepower to destroy that Shipyard if we can get close enough.

*Клип начинается в 48.75 с.*

`M08_010_100_A_KS`

RU:

> Значит, так и поступим. Главный инженер Хаук, у вас будет время. Мы продолжим твоё дело, Тирра.

EN:

> Then that is the solution. Chief Engineer Hauk, you will get your time. We will pick up where you left off, Tyrra.

### Задачи, подключённые к графу

Узлы: 256, 677.

`M08_Objective_01`

RU:

> Уничтожьте верфь Радаа.

EN:

> Destroy a Radaa Shipyard.

Узлы: 102, 661.

`M08_Objective_02`

RU:

> Уничтожьте вторую верфь Радаа.

EN:

> Destroy a second Radaa Shipyard.

Узлы: 154, 172, 176, 268, 653.

`M08_Objective_03`

RU:

> Уничтожьте последнюю верфь Радаа.

EN:

> Destroy the final Radaa Shipyard.

### M08_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #434`.

Узел `Mission_M8#346`.

`M08_020_010_KS`

RU:

> Гиперпереход завершён. Мы на орбите Гиббаса.

EN:

> Hyperspace Jump successful. Gybbas orbit achieved.

Узел `Mission_M8#110`.

`M08_020_020_FI`

RU:

> Обнаружен крупный оборонительный флот Радаа. Чтобы уничтожить верфь, нашим крупным кораблям понадобится свободный путь для атаки.

EN:

> Picking up a massive Radaa defense fleet. Our capital ships will need a clear attack path to destroy the Shipyard.

Узел `Mission_M8#186`.

`M08_020_030_KS`

RU:

> Радаа явно ждали нового удара Тирры. Не будем их разочаровывать.

EN:

> The Radaa were clearly preparing for another attack from Tyrra. We will not disappoint.

### M08_030

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardA) #330`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardB) #560`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardC) #284`.

Узел `Mission_M8#158`.

`M08_030_010_FI`

RU:

> Верфь Радаа уничтожена. Задачи флота выполнены.

EN:

> Radaa Shipyard has been destroyed.  Fleet objectives met.

Узел `Mission_M8#336`.

`M08_030_020_KS`

RU:

> Тирра бы на этом не остановилась. У нас хватит ресурсов, чтобы уничтожить вторую верфь?

EN:

> Tyrra would not stop here.  Do we have sufficient resources to take the second Shipyard?

Узел `Mission_M8#643`.

`M08_030_030_FI`

RU:

> По данным бортовых систем, все корабли полностью боеспособны. Но с других верфей Радаа уже выдвигаются крупные подкрепления.

EN:

> Onboard systems report peak functionality.  But the other Radaa Shipyards are deploying heavy reinforcements.

Узел `Mission_M8#70`.

`M08_030_040_KS`

RU:

> Я нашла решение. Всем кораблям: уничтожить вторую верфь.

EN:

> I have the solution for this equation. All ships, bring down that second shipyard.

### M08_040

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardA) #330`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardB) #560`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardC) #284`.

Узел `Mission_M8#461`.

`M08_040_010_FI`

RU:

> Вторая верфь уничтожена. Уничтожив последнюю, мы лишим Радаа возможности пополнять флот в системе Хиигары.

EN:

> Second Shipyard neutralized.  Destroying the last Shipyard would negate their ability to reinforce their fleets in the Hiigara system.

Узел `Mission_M8#270`.

`M08_040_020_KS`

RU:

> Флот, доложить обстановку. Мы сможем довести дело до конца?

EN:

> Fleet, status report.  Can we get this job done?

Узел `Mission_M8#657`.

`M08_040_030_FI`

RU:

> Все корабли и системы в норме. Ответ флота: «Так точно!»

EN:

> All ships and all systems report Green.  The word from fleet is "Aye!".

Узел `Mission_M8#112`.

`M08_040_040_KS`

RU:

> Тогда не дадим им больше времени на постройку кораблей. Всем орудийным расчётам: третья верфь Радаа — цель высшего приоритета.

EN:

> Then let's not give them anymore time to build their fleet.  All gunners, set the third Radaa Shipyard as priority alpha.

### M08_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardA) #330`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardB) #560`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardC) #284`.

Узел `Mission_M8#538`.

`M08_050_010_FI`

RU:

> Все верфи Радаа уничтожены. Оставшиеся силы противника дезорганизованы.

EN:

> All Radaa Shipyards destroyed. Remaining Radaa forces are in disarray.

Узел `Mission_M8#230`.

`M08_050_020_KS`

RU:

> Откройте канал связи со всем флотом.

EN:

> Initiate a coms link through to our entire Fleet.

Узел `Mission_M8#244`.

`M08_050_030_FI`

RU:

> Связь установлена.

EN:

> Connected.

Узел `Mission_M8#200`.

`M08_050_040_KS`

RU:

> Всем постам. Говорит командующая Каран С’Джет. Нас загнали на край гибели, но знайте: Тирра Собан ни на мгновение не сомневалась в нас.

EN:

> This is Commander Karan S'jet on all coms. We have been pushed to the brink, but know this - Tyrra Soban never doubted our ability.

Узел `Mission_M8#641`.

`M08_050_050_KS`

RU:

> Сегодняшняя победа доказала, что она была права. Мы вернём Хиигару. Командование, конец связи.

EN:

> Your victory today proves she was right. We will reclaim Hiigara. Command out.

### M08_060

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #248`.

Узел `Mission_M8#192`.

`M08_060_010_FI`

RU:

> Отходим! Ресурсы на исходе, флот истощён. Отступление неизбежно.

EN:

> Pull back! Materials and ships overextended. Retreat unavoidable.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #350`; `CustomEvent #444`; `CustomEvent #629`; `OnSimReady #434`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M8#518`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M8#637`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M8#410`.

`FI_MothershipLost_08`

RU:

> Полный отказ систем. Экипажу Материнского корабля — покинуть корабль.

EN:

> Complete systems failure. Mothership crew must abandon ship.

Узел `Mission_M8#88`.

`FI_UnlockBalisticDestroyer`

RU:

> Среди данных создателей оружия нашлись чертежи, которые мы уже пустили в дело. Теперь мы можем строить баллистические эсминцы. Их мощный ракетный залп поможет нам против тяжёлых кораблей Радаа в этом секторе.

EN:

> The Weapons Architects had ship plans we have put into use: we can now build Ballistic Destroyers, whose advanced Missile Barrage will be needed against the heavy Radaa fleet present in this sector.

## 11. M13: Возвращение на Хиигару / Return to Hiigara

Определение `dcb65b8cb311f7646b0d3c550ed5761f:1`, карта `level21`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M13 - Return to Hiigara/M13_Animatic_Intro/M13_Animatic_Intro.unity`

*Клип начинается в 1.07 с.*

`M13_010_005_A_KS`

RU:

> Все верфи Радаа уничтожены. Их кораблестроительная отрасль парализована.

EN:

> All Radaa Shipyards eliminated. We've crippled their construction capacity.

*Клип начинается в 6.00 с.*

`M13_010_010_A_KS`

RU:

> Материнский корабль полностью боеспособен. Флот в строю. Инженерная служба, времени хватило?

EN:

> Mothership fully operational. Fleet intact. Engineering, was that enough time?

*Клип начинается в 12.13 с.*

`M13_010_020_A_HA`

RU:

> Мы изучили схемы и распределили кремний по всем кораблям.

EN:

> We have analyzed the plans and distributed the silicon across all our ships.

*Клип начинается в 15.42 с.*

`M13_010_030_A_KS`

RU:

> Этого достаточно, чтобы защитить флот?

EN:

> Is it enough to protect the fleet?

*Клип начинается в 17.19 с.*

`M13_010_040_A_HA`

RU:

> Я провёл сотни симуляций. Это должно сработать. Это сработает.

EN:

> I've run hundreds of simulations. It has to work. It WILL work.

*Клип начинается в 22.37 с.*

`M13_010_050_A_KS`

RU:

> Твоя мать гордилась бы тобой.

EN:

> Your mother would be proud.

*Клип начинается в 25.42 с.*

`M13_010_060_A_FI`

RU:

> Станция «Раскол» и Башня Радаа всё ещё на орбите Хиигары. Амма передаёт ультиматум планете.

EN:

> Shatter Station and Radaa Tower are still in orbit around Hiigara.  Amma has been broadcasting an ultimatum to the planet.

*Клип начинается в 32.62 с.*

`M13_010_070_A_AR`

RU:

> Хиигарское командование, межзвёздное право предоставляет вам ограниченный срок на исполнение обязательств по унаследованному вами договору. Этот срок истёк. Я не хочу обрушивать мощь станции «Раскол» на вашу родную планету… но сделаю это, если потребуется. И не сомневайтесь: восстанавливать её будут ваши же люди.

EN:

> Hiigaran Command, according to interstellar law, you are allowed a narrow window to make good on the binding agreement you inherited. That period has ended. I don't want to unleash Shatter Station on the surface of your homeworld... but I will if I must and make no mistake, I will use your own people to rebuild.

*Клип начинается в 53.38 с.*

`M13_010_090_A_HA`

RU:

> Амма, всё пойдёт совсем не по твоему плану.

EN:

> This is NOT going to go like you planned, Amma.

*Клип начинается в 56.73 с.*

`M13_010_100_A_KS`

RU:

> Приготовиться к переходу к Хиигаре. По. Моей. Команде.

EN:

> Prepare the jump to Hiigara.  On.  My.  Mark.

### Финальная постановочная сцена

`Assets/Hercules/Scenes/M13 - Return to Hiigara/M13_Animatic_Outro/M13_Animatic_Outro.unity`

*Клип начинается в 2.03 с.*

`M14_010_010_A_HA`

RU:

> Каран С’Джет, первая Освобождённая, отказалась от заслуженного покоя, чтобы защитить наш родной мир. Хиигаряне в неоплатном долгу перед Каран С’Джет и моей матерью, Тиррой Собан, отдавшей жизнь за Хиигару.

EN:

> Karan S'jet, the first Unbound, gave up her well-earned peace to defend our Homeworld. The Hiigaran people owe a great debt of gratitude to Karan S'jet and my mother, Tyrra Soban, who laid down her life for Hiigara.

*Клип начинается в 19.03 с.*

`M14_010_020_A_HA`

RU:

> Мы обезвредили станцию «Раскол», но Материнский корабль пострадал в бою. Прежде чем он смог бы вернуться в строй, требовалось восстановить его и усовершенствовать технологии.

EN:

> While we neutralized the Shatter Station, the mothership was damaged in the battle. It would have to be rebuilt and its technology evolved before we could use it again.

*Клип начинается в 28.58 с.*

`M14_010_030_A_HA`

RU:

> Моя мать не дожила до победы, которую сделала возможной. Каран С’Джет всегда говорила, как дорожила временем, проведённым с Тиррой Собан.

EN:

> My mother did not live to see the victory that she made possible. Karan S’Jet always spoke about how much she valued her time with Tyrra Soban.

*Клип начинается в 38.77 с.*

`M14_010_040_A_HA`

RU:

> Каран и хиигарское командование также многое узнали о том, что значит быть навигатором и командующим Материнского корабля. Единение с ядром было не только честью, но и жертвой. Жертвой, которую Каран С’Джет решила приносить до конца своих дней.

EN:

> Karan and Hiigaran Command also learned more about what was required to be Navigator and Commander of a Mothership.  Being one with the Core was not just an honor, it was a sacrifice. One that Karan S'jet chose to make until the end of her days.

### Задачи, подключённые к графу

Узлы: 236, 461, 552, 624.

`M13_Objective_02`

RU:

> Пристыкуйте инженерный корвет к щитовому излучателю.

EN:

> Dock an Engineer Craft to a shield emitter.

Узлы: 72, 640, 764.

`M13_Objective_03alpha`

RU:

> Отключите щитовой излучатель «Альфа».

EN:

> Disable shield emitter alpha.

Узлы: 323, 605, 927.

`M13_Objective_03beta`

RU:

> Отключите щитовой излучатель «Бета».

EN:

> Disable shield emitter beta.

Узлы: 190, 281, 463, 538, 743, 756, 869.

`M13_Objective_03counter`

RU:

> Отключите щитовые излучатели.

EN:

> Disable shield emitters.

Узлы: 68, 829, 861.

`M13_Objective_03delta`

RU:

> Отключите щитовой излучатель «Дельта».

EN:

> Disable shield emitter delta.

Узлы: 70, 636, 839.

`M13_Objective_03omega`

RU:

> Отключите щитовой излучатель «Омега».

EN:

> Disable shield emitter omega.

Узлы: 56, 234, 313, 361, 369, 714, 835, 837, 867, 935.

`M13_Objective_04counter`

RU:

> Уничтожьте секции станции «Раскол».

EN:

> Destroy the wings of the Shatter Station.

Узлы: 311, 853.

`M13_Objective_timer`

RU:

> До следующего выстрела станции «Раскол»:

EN:

> Time until Shatter Station fires again:

### M13_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #303`.

Узел `Mission_M13#180`.

`M13_020_010_KS`

RU:

> Радаа нас ждали.

EN:

> The Radaa have been waiting for us.

Узел `Mission_M13#548`.

`M13_020_020_HA`

RU:

> Моя команда подготовила защиту.

EN:

> My team have prepared our defences.

Узел `Mission_M13#439`.

`M13_020_030_KS`

RU:

> На этот раз всё будет иначе.

EN:

> This encounter will go differently.

Узел `Mission_M13#776`.

`M13_020_040_AR`

RU:

> Хиигарский Материнский корабль. Радаа готовы принять вашу капитуляцию.

EN:

> Hiigaran Mothership. The Radaa are prepared to accept your surrender.

Узел `Mission_M13#412`.

`M13_020_050_KS`

RU:

> Закрыть все каналы связи. Не отвечать.

EN:

> Coms on lockdown. Do not respond.

Узел `Mission_M13#400`.

`M13_020_060_AR`

RU:

> Хиигарское командование, вы — наша собственность. Отзовите флот.

EN:

> Hiigaran Command, you ARE our property. Stand down your fleet.

Узел `Mission_M13#451`.

`M13_020_070_GR`

RU:

> Не испытывайте наше терпение! Продолжите сопротивляться — и я с удовольствием вырву ядро Предтеч из вашего дымящегося корпуса.

EN:

> Do not test us further!  If you continue to resist I will relish tearing the Progenitor Core from your smoking hull.

Узел `Mission_M13#739`.

`M13_020_080_AR`

RU:

> Что ж. Мы исчерпали все возможности добиться исполнения закона мирным путём. Командир Гиитан, приступайте.

EN:

> Very well. We have exhausted our efforts to enforce the law peacefully. Commander Giitan, proceed.

Узел `Mission_M13#674`.

`M13_020_090_GR`

RU:

> Разумеется, мать. Приказ принят. Активирую станцию «Раскол».

EN:

> Of course, mother. Command confirmed. Engaging Shatter Station.

Узел `Mission_M13#724`.

`M13_020_100_KS`

RU:

> Станция «Раскол» выпустила импульс. Флот, доложить состояние.

EN:

> Shatter pulse fired.  Fleet, status.

Узел `Mission_M13#98`.

`M13_020_110_FI`

RU:

> Повреждений нет. Наш флот не пострадал.

EN:

> No damage reported. Our Fleet remains intact.

Узел `Mission_M13#774`.

`M13_020_120_KS`

RU:

> Материнский корабль полностью исправен. Главный инженер Хаук, вы и ваша команда справились. Поздравляю!

EN:

> Mothership is fully functional. Chief Engineer Hauk, you and your team were successful. Congratulations!

Узел `Mission_M13#528`.

`M13_020_130_HA`

RU:

> Рано праздновать, командующая. Чтобы уничтожить станцию «Раскол», нам придётся отключить её щитовые излучатели.

EN:

> Let's not celebrate yet, Commander. To destroy Shatter Station we will need to disable *its* Shield Emitters.

Узел `Mission_M13#385`.

`M13_020_140_FI`

RU:

> Башня Радаа также активировала внутреннюю защиту.

EN:

> The Radaa Tower has also activated internal shielding.

Узел `Mission_M13#556`.

`M13_020_150_KS`

RU:

> Они в панике. Разведка, можете перехватить их переговоры?

EN:

> They are scrambling. Intel, can you intercept their coms?

Узел `Mission_M13#520`.

`M13_020_160_FI`

RU:

> Лишь отдельные фрагменты.

EN:

> Intermittently.

Узел `Mission_M13#36`.

`M13_020_170_GR`

RU:

> Они нейтрализовали импульс «Раскола»! Нужна перекалибровка! Сколько времени она займёт? Сколько…

EN:

> They must have counter-terminated the Shatter attack, we must re-calibrate!  How long until full recalibration?  How long--

Узел `Mission_M13#722`.

`M13_020_180_HA`

RU:

> Командование, это может сработать. Мы не успеем подстроить нашу защиту. Разве что отступим…

EN:

> Command, that could work. We won't be able to change our settings to match. Unless we withdraw...

Узел `Mission_M13#546`.

`M13_020_190_KS`

RU:

> Нет. Всё закончится здесь и сейчас. Сколько времени им понадобится, чтобы перекалибровать импульс «Раскола»?

EN:

> No. This will end now. How long will it take them to re-calibrate the Shatter pulse?

Узел `Mission_M13#611`.

`M13_020_200_HU`

RU:

> Неизвестно. Какое-то время у нас есть, но сколько именно — мы не знаем.

EN:

> Unknown - we have some time, but no way to know exactly.

Узел `Mission_M13#644`.

`M13_020_210_KS`

RU:

> Значит, нужно действовать быстро.

EN:

> Then we had best strike quickly.

### M13_040

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #573`.

Узел `Mission_M13#905`.

`M13_040_010_FI`

RU:

> Стыковка завершена. Инженерный корвет будет уязвим, пока не отключит излучатель.

EN:

> Docking complete. Engineer Craft will remain vulnerable until it disables the Emitter.

### M13_050

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#46`.

`M13_050_010_FI`

RU:

> Излучатель отключён. Часть секций станции «Раскол» лишилась защиты.

EN:

> Emitter disabled. Wings on the Shatter Station now exposed.

Узел `Mission_M13#391`.

`M13_050_020_KS`

RU:

> Сосредоточить огонь флота на этих секциях.

EN:

> Concentrate fleet firepower on those wings.

### M13_060

Узел `Mission_M13#unlinked_138`.

`M13_060_010_FI`

RU:

> Остальные щитовые излучатели всё ещё работают. Найдите и отключите их.

EN:

> More Shield Emitters still active.  Track them down and disable them.

*Изолированный узел без ID/control-подключения: наличие текста не подтверждает его произнесение в игре.*

### M13_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#387`.

`M13_070_010_FI`

RU:

> Щиты всё ещё активны. Нужно отключить и другие щитовые излучатели.

EN:

> Shields still active. Additional Shield Emitters must be disabled. 

### M13_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#805`.

`M13_080_010_FI`

RU:

> Осталось отключить ещё один щитовой излучатель.

EN:

> One more Shield Emitter must be disabled.

### M13_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#365`.

`M13_090_010_FI`

RU:

> Новые секции станции «Раскол» открыты для атаки.

EN:

> More wings of Shatter Station vulnerable to attack.

### M13_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#696`.

`M13_100_010_FI`

RU:

> Ещё часть секций станции «Раскол» лишилась защиты.

EN:

> Additional Shatter Station wings now exposed.

### M13_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#232`.

`M13_110_010_FI`

RU:

> Последняя группа секций станции «Раскол» теперь уязвима.

EN:

> The final set of Shatter Station's wings can now be destroyed.

### M13_120

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #222`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #240`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #264`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #879`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #124`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #140`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #246`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #919`.

Узел `Mission_M13#518`.

`M13_120_010_KS`

RU:

> Хаук, доложите. Сколько осталось до завершения перекалибровки станции «Раскол»?

EN:

> Hauk, status update. How long until they re-calibrate Shatter Station?

Узел `Mission_M13#238`.

`M13_120_020_HA`

RU:

> Неизвестно. Каждая симуляция даёт другой результат.

EN:

> Unknown, every sim we run comes back with a different answer.

Узел `Mission_M13#907`.

`M13_120_030_KS`

RU:

> Понятно. Постараюсь их задержать.

EN:

> Understood, I will do what I can to slow them down.

### M13_130

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #222`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #240`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #264`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #879`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #124`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #140`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #246`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #919`.

Узел `Mission_M13#186`.

`M13_130_010_KS`

RU:

> Хаук… Докладывайте!

EN:

> Hauk... status!

Узел `Mission_M13#285`.

`M13_130_020_HA`

RU:

> Если станция «Раскол» выстрелит снова, наша защита почти не поможет.

EN:

> If Shatter Station fires again, we have minimal defenses.

Узел `Mission_M13#833`.

`M13_130_030_KS`

RU:

> Они не успеют. Мы уничтожим секции до следующего выстрела.

EN:

> It'll be too late.  We will destroy those wings before they can fire again.

### M13_140

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #222`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #240`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #264`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #879`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #124`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #140`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #246`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #919`.

Узел `Mission_M13#416`.

`M13_140_010_AR`

RU:

> Хиигарское командование, это последний шанс сдаться. Второй удар станции «Раскол» вы отразить не сможете. Вы потеряете всё.

EN:

> Hiigaran Command, last chance to surrender. You will not be able to counteract Shatter Station a second time. You will lose everything.

Узел `Mission_M13#118`.

`M13_140_020_KS`

RU:

> Амме стоило бы подумать о собственных потерях.

EN:

> Amma should be thinking about what she will lose.

Узел `Mission_M13#593`.

`M13_140_030_HA`

RU:

> Командование, возможно, она права.

EN:

> Command, she could be right.

Узел `Mission_M13#507`.

`M13_140_040_KS`

RU:

> Возможно. Но мы не можем оставить эту махину уничтожать нашу планету. Прикажите флоту сосредоточить огонь на секциях станции «Раскол».

EN:

> Perhaps, but we can't leave that thing to wreak havoc our planet.  Have the fleet concentrate fire on the Shatter Station wings.

### M13_150

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #100`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #335`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #620`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #78`.

Узел `Mission_M13#250`.

`M13_150_010_FI`

RU:

> Повреждения последней группы секций вызвали цепной отказ в командном модуле станции «Раскол».

EN:

> Damage to final set of wings cascading to Shatter Station Command Module.

Узел `Mission_M13#82`.

`M13_150_020_HA`

RU:

> Получилось. Станция «Раскол» больше не сможет выстрелить.

EN:

> That did it. Shatter Station can't possibly fire again.

Узел `Mission_M13#148`.

`M13_150_030_KS`

RU:

> Что происходит с Башней?

EN:

> What's happening to the Tower?

Узел `Mission_M13#770`.

`M13_150_040_FI`

RU:

> Цепная реакция после критического отказа станции «Раскол» перекинулась на Башню. Разрушение неизбежно.

EN:

> Critical failure of Shatter Station is chaining to their Tower. Destruction imminent.

Узел `Mission_M13#841`.

`M13_150_050_KS`

RU:

> Теперь можно отозвать флот. Эта победа — в твою честь, Тирра.

EN:

> Now we stand down.  Victory in your name, Tyrra.

### M13_200

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #453`.

Узел `Mission_M13#353`.

`M13_200_010_FI`

RU:

> Слишком много кораблей потеряно, ресурсы исчерпаны. Хиигара потеряна!

EN:

> Too many ships lost - resource reserves spent - Hiigara is lost!

### M13_210

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=86, M13_Objective_timer) #853`.

Узел `Mission_M13#512`.

`M13_210_010_FI`

RU:

> По показаниям сенсоров, станция «Раскол» накапливает энергию.

EN:

> Readings from Shatter Station indicate it is powering up.

Узел `Mission_M13#585`.

`M13_210_020_HA`

RU:

> Мы не успели.

EN:

> We didn't make it in time.

Узел `Mission_M13#154`.

`M13_210_030_HA`

RU:

> Командование флота, ответьте! Каран! Каран!

EN:

> Fleet Command, respond!  Karan!  Karan!  

### M13_220

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #144`.

Узел `Mission_M13#128`.

`M13_220_010_FI`

RU:

> Мы не можем пробить внутреннюю защиту Башни Радаа. Рекомендуем сосредоточить огонь на непосредственной угрозе — станции «Раскол».

EN:

> We cannot overcome the internal Radaa Tower shields. Recommend centering attacks on the immediate threat, Shatter Station.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #389`; `CustomEvent #52`; `CustomEvent #964`; `OnSimReady #303`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M13#297`.

`FI_MothershipAttacked_03`

RU:

> Противник атакует Материнский корабль.

EN:

> Enemy has targeted Mothership.

Узел `Mission_M13#373`.

`FI_MothershipHeavyDamage_03`

RU:

> Материнский корабль получает всё новые повреждения.

EN:

> Damage to Mothership is intensifying.

Узел `Mission_M13#418`.

`FI_MothershipLost_03`

RU:

> Материнский корабль потерян.

EN:

> We have lost the Mothership.

Узел `Mission_M13#766`.

`FI_UnlockHeavyCruiser`

RU:

> В обломках верфей Радаа мы нашли технологии, позволившие освоить тяжёлые крейсеры. Их мощное вооружение отлично подходит для уничтожения секций станции «Раскол», когда мы отключим их щиты.

EN:

> From the wreckage of the Radaa shipyards we recovered technology to build a new ship: Heavy Cruisers have advanced weapon systems optimal for destroying the Shatter Station wings, once their shields are disabled.

## Полнота и ограничения

Включено **395 уникальных внутри глав реплик графов** и **125 реплик клипов вступлений/финала**. Повторяющиеся общие тревоги могут встречаться в нескольких главах. Покрытие всех найденных PlayDialogue проверено автоматически.

При чтении старой версии использована схема Steam с двумя проверенными отличиями: у MissionDatabase отсутствует массив демо-миссий, у ObjectiveStaticData — поле ModelScaleMultiplier. Разбор каждого сохранённого объекта требует полного совпадения длины, частичные чтения не принимаются. Все определения миссий, кораблей, задач и найденные сценарные графы прочитаны.

Не прочитано 642 объектов, преимущественно HUD/UI/VFX старой версии. В том числе 9 AbilityDefinition несовместимы с новой схемой; их параметры в этом отчёте не реконструированы. Это ограничение аудита способностей, а не отсутствие девяти способностей в Quest. Полный список — local/quest-audit/index.json.

Проверка относится к данным и связям скриптов. Видимость реплик, тайминги, бой и все условия полного прохождения запуском не проверены. Наличие вступления не означает готовый видеоролик для HWRM: исходник использует Timeline/Unity и внешний звук.

