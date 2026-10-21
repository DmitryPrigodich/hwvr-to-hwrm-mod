# Vast Reaches: сценарий кампании на русском и английском

Источник: предоставленные APK/OBB **1.1.0-16520**, без запуска игры. Это отдельная, более ранняя версия, а не дополнение к Steam-демке той же ревизии. В ней найдены 11 игровых миссий кампании, отдельное обучение, вступления и финальная сцена. Бонуса C1 в списке сцен этой сборки нет.

Ниже буквальные EN/RU исходной локализации, включая её ошибки. Состав флота, постройка и сюжетные открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md); сравнение ресурсов — в [QUEST_COMPARISON.md](QUEST_COMPARISON.md).

Порядок глав взят из MissionDatabase, он отличается от номеров внутренних M-файлов. Беседы сгруппированы по сценам диалога, а порядок реплик внутри связан управляющими рёбрами графа. **Независимые обработчики событий и развилки не образуют одну обязательную цепочку**: условия и ID узлов приведены рядом. Нумерация ключей используется для именования бесед, а не как доказательство очередности игры. Вступления упорядочены по времени клипов Timeline.

FI — разведка флота; TS — Тирра Собан; KS — Каран С’Джет; AR — Амма; GR — Гитан. Смысл HA зависит от сцены: во вступлении M1 это рассказчик, в репликах верфи — её главный инженер.

## Обучение. T1: Руководство / Tutorial

Определение `c77b2064d54d78e408ebc4c27fab4cc6:1`, карта `level23`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M1 - Hiigara Proving Grounds/M1_Animatic_Intro/M1_Animatic_Intro.unity`

*Клип начинается в 1.28 с.*

`M01_010_010_A_HA`

EN:

> After a long exile, we Hiigarans at last welcomed peace in our home.

RU:

> После долгого изгнания мы, хиигарцы, наконец-то обрели мир в нашем доме.

*Клип начинается в 7.60 с.*

`M01_010_020_A_HA`

EN:

> Our great Mothership, with Karan S'jet fused as its Commander, Navigator and living core, allowed our people to carve a fiery path from exile to home and freedom. Now the Mothership rests in orbit around Hiigara, a tribute to those times and the great generation that sacrificed everything to find and claim our Homeworld.

RU:

> Наш великий корабль-матка, в котором Каран С'джет стал его командиром, навигатором и живым ядром, позволил нашему народу проложить огненный путь от изгнания к дому и свободе. Сейчас Корабль-носитель находится на орбите Хиигары, это дань тем временам и великому поколению, которое пожертвовало всем, чтобы найти и завоевать наш Родной мир.

*Клип начинается в 30.07 с.*

`M01_010_030_A_HA`

EN:

> Though the Taiidani empire had fallen, the new Hiigarans were caught off guard by the short but deadly BeastWar. The Daiamid, the ruling council of the Hiigaran people, were painfully aware that they were alone in the Galaxy. So when the Radaa - interstellar traders with their own mysterious technology - approached with offers of an alliance and exchange, the Daiamid was very receptive.

RU:

> Хотя империя Тайидани пала, новые хиигарцы были застигнуты врасплох короткой, но смертоносной Звериной Войной. Дайамиды, правящий совет народа Хиигаран, с болью осознавали, что они одни в Галактике. Поэтому, когда Радаа — межзвездные торговцы со своими таинственными технологиями — обратились с предложениями союза и обмена, Дайамиды были очень восприимчивы.

*Клип начинается в 53.08 с.*

`M01_010_040_A_HA`

EN:

> The Radaa believed that the longer we were at peace, the more vulnerable we became. Their leader, Commander Amma, warned that former Taiidani bandit kingdoms were re-arming and a new Empire was a real possibility.  In exchange for permission to build and mine in the Hiigaran star system, Commander Amma offered to shepherd the Hiigaran Fleet through a new era of modernization and growth.

RU:

> Рада считала, что чем дольше мы живем в мире, тем более уязвимыми мы становимся. Их лидер, командующий Амма, предупредил, что бывшие бандитские королевства Тайидани перевооружаются и существует реальная возможность создания новой Империи. В обмен на разрешение на строительство и добычу полезных ископаемых в звездной системе Хиигаран командующий Амма предложил вести флот Хиигаран в новую эпоху модернизации и роста.

*Клип начинается в 79.07 с.*

`M01_010_050_A_HA`

EN:

> So we began to forge a new military force with our new allies.  We also pulled the original Mothership out of retirement and built her back up.  The Radaa were very interested in the Ship that had defeated the Taiidani Empire.

RU:

> Итак, мы начали создавать новую военную силу вместе с нашими новыми союзниками. Мы также вывели из эксплуатации оригинальный Mothership и восстановили его. Рада очень интересовалась Кораблём, победившим Империю Тайидани.

*Клип начинается в 93.98 с.*

`M01_010_060_A_HA`

EN:

> Karan S'jet retired years ago, but she was still the only being that had learned to control the Mothership by direct link to its Progenitor core. She agreed to return to the Mothership project but this time only as an instructor. She had earned her peace.

RU:

> Каран С'джет ушла на пенсию много лет назад, но она все еще была единственным существом, которое научилось управлять Кораблём-матерью посредством прямой связи с ядром его Прародителя. Она согласилась вернуться в проект Mothership, но на этот раз только в качестве инструктора. Она заслужила покой.

*Клип начинается в 110.72 с.*

`M01_010_070_A_HA`

EN:

> The role of Fleet Command fell to Tyrra Soban. A peerless military veteran, she had fought countless battles in the splintering remains of the Taiidani empire, and had broken up dozens of Raider groups.

RU:

> Роль командования флотом выпала на долю Тирры Собан. Бесподобный военный ветеран, она участвовала в бесчисленных битвах на развалинах империи Тайидани и разбила десятки групп рейдеров.

*Клип начинается в 122.95 с.*

`M01_010_080_A_HA`

EN:

> To take command of the Mothership and the Fleet, she underwent the same process that Karan S'jet had decades before. She was a trained warrior and that would make it clear to anyone that the Mothership was now a warship, pure and direct.Tyrra Soban was only the second of our people to become unbound.

RU:

> Чтобы принять на себя командование Кораблем-носителем и Флотом, она прошла тот же процесс, что и Каран С'джет несколько десятилетий назад. Она была обученным воином, и это дало бы понять любому, что «Корабль-носитель» теперь стал военным кораблем, чистым и прямым. Тирра Собан была лишь второй из наших людей, которая освободилась от уз.

### Задачи, подключённые к графу

Узлы: 89, 391, 503, 555.

`MT01_Objective_01`

EN:

> Destroy Target Ships while avoiding Gun Platform.

RU:

> Уничтожайте целевые корабли, избегая при этом артиллерийской платформы.

Узлы: 105, 193, 249, 427, 479, 701, 778.

`MT01_Objective_02`

EN:

> Complete each exercise of the training regimen.

RU:

> Выполняйте каждое упражнение тренировочного режима.

### T01_010

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #764`.

Узел `Mission_T1#259`.

`T01_010_010_TS`

EN:

> Command... on-line...

RU:

> Команда... онлайн...

Узел `Mission_T1#567`.

`T01_010_020_KS`

EN:

> It's ok, Fleet Command... Being fused with the Mothership takes getting used to.  Remember your training...flow with the ship, don't grasp at the data.  

RU:

> Все в порядке, командование флотом... К слиянию с Материнским кораблем нужно привыкнуть. Помните о своих тренировках... двигайтесь вместе с кораблем, не цепляйтесь за данные.

Узел `Mission_T1#405`.

`T01_010_030_TS`

EN:

> You're coming in clear, Karan.  But I can hear everything at the same time...it's amazing!

RU:

> Ты понимаешь, Каран. Но я слышу все одновременно... это потрясающе!

Узел `Mission_T1#409`.

`T01_010_040_KS`

EN:

> Fleet Intelligence will take you through some exercises now Commander.  But I'm here and you can call on me as well.  

RU:

> Разведка флота проведет вас через несколько учений, командир. Но я здесь, и ты тоже можешь позвонить мне.

### T01_020

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #181`.

Узел `Mission_T1#515`.

`T01_020_010_FI`

EN:

> Fleet Intelligence Officer on-line. My task is to collate information, analyze sensor data and provide objectives.  

RU:

> Офицер разведки флота на связи. Моя задача — сопоставить информацию, проанализировать данные датчиков и поставить цели.

Узел `Mission_T1#798`.

`T01_020_020_FI`

EN:

> First I will guide you through systems tests.  Open the Sensors Manager now.

RU:

> Сначала я проведу вас через системные тесты. Откройте диспетчер датчиков сейчас.

Узел `Mission_T1#231`.

`T01_020_030_FI`

EN:

> The Sensors Manager shows you a map of your local environment, including the heart of command operations, the Mothership.

RU:

> Менеджер датчиков показывает вам карту вашего местного окружения, включая центр командования — материнский корабль.

Узел `Mission_T1#728`.

`T01_020_040_FI`

EN:

> Current mission objectives are also displayed prominently in your sensors manager.

RU:

> Текущие цели миссии также отображаются на видном месте в вашем диспетчере датчиков.

Узел `Mission_T1#657`.

`T01_020_050_TS`

EN:

> Understood...attempting to refocus.

RU:

> Понятно... пытаюсь перефокусироваться.

Узел `Mission_T1#397`.

`T01_020_060_KS`

EN:

> Commander, let go.  Right now, self is your enemy.  

RU:

> Командир, отпусти. Прямо сейчас «я» — ваш враг.

### T01_030

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #653`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_T1#137`.

`T01_030_010_FI`

EN:

> Our next test is of your navigation systems, to help you gain tactical awareness around the Mothership.  First we will try moving around your environment. 

RU:

> Наше следующее испытание — ваши навигационные системы, которые помогут вам получить тактическую осведомленность о Материнском корабле. Сначала мы попробуем передвигаться по вашему окружению.

Узел `Mission_T1#135`.

`T01_030_013_FI`

EN:

> You can also zoom your view in and out.

RU:

> Вы также можете увеличивать и уменьшать масштаб изображения.

Узел `Mission_T1#585`.

`T01_030_020_FI`

EN:

> You can teleport your viewpoint and instantly move it anywhere within range.

RU:

> Вы можете телепортировать свою точку обзора и мгновенно переместить ее в любое место в пределах досягаемости.

Узел `Mission_T1#306`.

`T01_030_017_FI`

EN:

> You can move your view of the world using several methods.

RU:

> Изменить свой взгляд на мир можно несколькими способами.

Узел `Mission_T1#161`.

`T01_030_040_TS`

EN:

> This is stunning! I have spent years staring into tactical screens but never like this.

RU:

> Это потрясающе! Я провел годы, глядя на тактические экраны, но никогда не делал этого.

Узел `Mission_T1#278`.

`T01_030_050_KS`

EN:

> Remember when you merge with the sensor data you can see everything, everywhere.  You can make so many decisions, so quickly.  But you are not infinite, never forget that.

RU:

> Помните, что когда вы объединяете данные датчиков, вы можете видеть все и везде. Вы можете принять так много решений и так быстро. Но ты не бесконечен, никогда не забывай об этом.

### T01_040

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #547`; `OnDetectShip #383`; `OnWaveDestroyed (Enabled=True) #742`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_T1#561`.

`T01_040_010_FI`

EN:

> We will now focus on your fleet of ships and how to command them.  Start by surveying the ships you have available. They are placed into functional formations called Strike Groups.  

RU:

> Теперь мы сосредоточимся на вашем флоте кораблей и на том, как ими управлять. Начните с осмотра имеющихся у вас кораблей. Они объединены в функциональные формирования, называемые ударными группами.

Узел `Mission_T1#300`.

`T01_040_030_FI`

EN:

> You also have the ability to give commands to more than one Strike Group at a time.

RU:

> У вас также есть возможность отдавать команды более чем одной ударной группе одновременно.

Узел `Mission_T1#93`.

`T01_040_035_FI`

EN:

> You can also give Strike Groups attack orders.

RU:

> Вы также можете отдавать приказы ударным группам об атаке.

Узел `Mission_T1#792`.

`T01_040_050_FI`

EN:

> You are now facing simulated enemies, which will not fight back. Of course real enemies will.

RU:

> Теперь вы столкнулись с симулированными врагами, которые не будут сопротивляться. Конечно, настоящие враги будут.

Узел `Mission_T1#55`.

`T01_040_020_FI`

EN:

> You can give Strike Groups movement orders.

RU:

> Вы можете отдавать приказы о движении ударных групп.

Узел `Mission_T1#385`.

`T01_040_060_KS`

EN:

> That's it, Commander. You're getting it. 

RU:

> Вот и все, командир. Вы получаете это.

Узел `Mission_T1#535`.

`T01_040_070_TS`

EN:

> It's so direct, so immediate.

RU:

> Это так прямо, так непосредственно.

Узел `Mission_T1#525`.

`T01_040_080_KS`

EN:

> You are experiencing all the things only I have known. You and I now make a very exclusive pair.

RU:

> Вы испытываете все то, что знал только я. Мы с тобой теперь составляем очень эксклюзивную пару.

### T01_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #742`.

Узел `Mission_T1#91`.

`T01_050_010_FI`

EN:

> Tactical Pause allows you to stop the action so that you can plan your next moves, including spending Resources to build new ships. 

RU:

> Тактическая пауза позволяет вам остановить действие, чтобы вы могли спланировать свои следующие действия, в том числе потратить ресурсы на постройку новых кораблей.

Узел `Mission_T1#415`.

`T01_050_020_FI`

EN:

> You can also retire ships in your Strike Groups that you no longer need, and get some Resources returned to your reserves.

RU:

> Вы также можете вывести из эксплуатации корабли в своих ударных группах, которые вам больше не нужны, и вернуть часть ресурсов в свои резервы.

Узел `Mission_T1#221`.

`T01_050_040_KS`

EN:

> The ships are all yours now. Be careful with them, like they are a part of you.

RU:

> Корабли теперь все ваши. Будьте осторожны с ними, как будто они часть вас.

Узел `Mission_T1#549`.

`T01_050_050_TS`

EN:

> I have always felt that way.

RU:

> Я всегда так чувствовал.

Узел `Mission_T1#659`.

`T01_050_060_KS`

EN:

> Not like this. You will hear every loss now.  Be prepared for that.

RU:

> Не так. Теперь ты услышишь каждую потерю. Будьте к этому готовы.

### T01_060

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #573`; `OnObjectiveCompleted (Objective=30, MT01_Objective_01) #503`; `OnWaveDestroyed (Enabled=True) #742`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_T1#673`.

`T01_060_010_FI`

EN:

> You can also set up more advanced movement patterns for your Strike Groups, using waypoints.

RU:

> Вы также можете настроить более сложные схемы движения для своих ударных групп, используя путевые точки.

Узел `Mission_T1#770`.

`T01_060_020_FI`

EN:

> Use waypoints to navigate to attack those enemy ships while avoiding the gun platform.

RU:

> Используйте путевые точки для навигации и атаки вражеских кораблей, избегая при этом артиллерийской платформы.

Узел `Mission_T1#437`.

`T01_060_030_FI`

EN:

> This concludes our test of core systems.

RU:

> На этом мы завершаем тестирование основных систем.

### T01_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=30, MT01_Objective_01) #503`.

Узел `Mission_T1#360`.

`T01_070_010_KS`

EN:

> Well done, Commander. But now it's time to push your limits. I am sending you the coordinates for the Radaa meeting point. For this you are on your own. Hyperspace manipulation is for a singular mind.

RU:

> Молодец, командир. Но теперь пришло время расширить свои границы. Я посылаю вам координаты места встречи Рады. Для этого вы предоставлены сами себе. Манипулирование гиперпространством — удел исключительного ума.

Узел `Mission_T1#663`.

`T01_070_020_KS`

EN:

> You can do this.

RU:

> Вы можете сделать это.

Узел `Mission_T1#467`.

`T01_070_030_TS`

EN:

> It feels just like the simulation but I will not lie, Hyperspatial math is not my strongest suit.  

RU:

> Это похоже на симуляцию, но я не буду лгать: гиперпространственная математика — не моя сильная сторона.

Узел `Mission_T1#171`.

`T01_070_040_KS`

EN:

> Just keep control of the equations as you feed them to the Hyperspace Core and then... open the door.

RU:

> Просто продолжайте контролировать уравнения, передавая их в Гиперпространственное ядро, а затем... откройте дверь.

Узел `Mission_T1#439`.

`T01_070_050_TS`

EN:

> Roger that... Hyperspace engage on my mark. 

RU:

> Роджер, это... Гиперпространство вступает в бой по моей цели.

Узел `Mission_T1#545`.

`T01_070_060_TS`

EN:

> 3... 2... 1... mark.

RU:

> 3... 2... 1... отметка.

## 1. M1: Испытательный полигон Хиигара / Hiigara Proving Grounds

Определение `f43761a426e901e4897580ed0dc94979:1`, карта `level1`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

Общий пролог уже приведён перед обучением; повторно не воспроизводится.

### Задачи, подключённые к графу

Узлы: 60, 100, 118, 441, 469.

`M01_Objective_00`

EN:

> Harvest RU from asteroids to a total of 200.

RU:

> Соберите RU с астероидов в общей сложности до 200.

Узлы: 162, 435, 501.

`M01_Objective_00a`

EN:

> Use your RU to Build a Scout.

RU:

> Используйте свой RU, чтобы построить разведчика.

Узлы: 154, 326, 525.

`M01_Objective_00b`

EN:

> Locate the Radaa patrol using Scout Sensor Sweep Ability.

RU:

> Найдите патруль Радаа, используя способность «Разведчик-сенсор».

Узлы: 36, 52, 324.

`M01_Objective_01`

EN:

> Destroy the first Radaa patrol.

RU:

> Уничтожьте первый патруль Радаа.

Узлы: 74, 180, 519.

`M01_Objective_01b`

EN:

> Destroy the second Radaa patrol.

RU:

> Уничтожьте второй патруль Радаа.

Узлы: 104, 142, 595.

`M01_Objective_01c`

EN:

> Destroy the third Radaa patrol.

RU:

> Уничтожьте третий патруль Радаа.

Узлы: 94, 198, 206, 252, 397.

`M01_Objective_02`

EN:

> Defend the Mothership from the Radaa.

RU:

> Защитите корабль-носитель от Рады.

Узлы: 80, 236, 340.

`M01_Objective_02b`

EN:

> Destroy the Radaa Missile Frigates.

RU:

> Уничтожьте ракетные фрегаты Радаа.

### M01_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #453`.

Узел `Mission_M1#561`.

`M01_020_003_TS`

EN:

> Hyperspace jump... successful.

RU:

> Гиперпространственный прыжок... успешен.

Узел `Mission_M1#551`.

`M01_020_005_KS`

EN:

> I knew you could do it.

RU:

> Я знал, что ты сможешь это сделать.

Узел `Mission_M1#413`.

`M01_020_010_FI`

EN:

> We are early for our rendezvous with the Radaa.

RU:

> На встречу с Радой мы пришли рано.

Узел `Mission_M1#152`.

`M01_020_020_TS`

EN:

> Let's not put the time to waste.  Scanning for Resources in our vicinity.

RU:

> Давайте не будем тратить время попусту. Ищем ресурсы поблизости.

Узел `Mission_M1#26`.

`M01_020_030_FI`

EN:

> Acknowledged.  Command, this sector is rife with asteroids and rich dust clouds.

RU:

> Признано. Командир, этот сектор изобилует астероидами и богатыми пылевыми облаками.

Узел `Mission_M1#130`.

`M01_020_035_FI`

EN:

> One of your Strike Groups contains Resource Collectors which can be used for harvesting. Initiate at will.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M1#308`.

`M01_020_040_TS`

EN:

> Any objections, Commander Karan S'jet?

RU:

> Есть возражения, командир Каран С'джет?

Узел `Mission_M1#421`.

`M01_020_050_KS`

EN:

> Former Commander.  Your ship, your orders, Commander Tyrra Soban.

RU:

> Бывший командир. Ваш корабль, ваши приказы, командир Тирра Собан.

### M01_025

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=9, M01_Objective_00) #100`.

Узел `Mission_M1#300`.

`M01_025_010_FI`

EN:

> Necessary Resources secured.  Continuing to gather Resources is important for Mothership systems health, and keeps our construction bays capable of building more ships.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M1#563`.

`M01_025_020_FI`

EN:

> We now have the Resources to build a Scout unit so we can pinpoint the location of the Radaa.

RU:

> Теперь у нас есть ресурсы для создания отряда разведчиков, чтобы мы могли точно определить местонахождение Радаа.

### M01_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=17, M01_Objective_00a) #162`.

Узел `Mission_M1#547`.

`M01_030_010_GR`

EN:

> Greetings, Hiigaran Command, this is Radaa Admiral Giitan. Our Commander Amma relays her wishes for our long and fruitful partnership with the Hiigaran people.

RU:

> Приветствую вас, хиигарское командование, это адмирал Рада Гиитан. Наш командующий Амма желает нам долгого и плодотворного сотрудничества с народом Хиигаран.

Узел `Mission_M1#176`.

`M01_030_015_GR`

EN:

> And now that pleasantries are out of the way, let us begin. I live for a good battle.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M1#429`.

`M01_030_020_TS`

EN:

> As do I.

RU:

> Как и я.

Узел `Mission_M1#28`.

`M01_030_030_FI`

EN:

> Radaa craft signatures detected in this sector.

RU:

> В этом секторе обнаружены следы кораблей Радаа.

Узел `Mission_M1#653`.

`M01_030_040_GR`

EN:

> I thought it best for our skirmish to involve live fire.  I've found it's the only way to truly learn.  Are we agreed?  Good.

RU:

> Я подумал, что для нашей стычки лучше всего вести боевую стрельбу. Я обнаружил, что это единственный способ по-настоящему учиться. Мы согласны? Хороший.

Узел `Mission_M1#66`.

`M01_030_050_FI`

EN:

> To gain precise coordinates on the Radaa craft, have your Scout perform reconnaissance with a Sensor Sweep.

RU:

> Чтобы получить точные координаты корабля Радаа, попросите своего разведчика провести разведку с помощью сенсорного сканирования.

### M01_035

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=60, M01_Objective_00b) #525`.

Узел `Mission_M1#477`.

`M01_035_010_FI`

EN:

> The first Radaa skirmish group has been detected.

RU:

> Обнаружена первая боевая группа Радаа.

Узел `Mission_M1#240`.

`M01_035_020_KS`

EN:

> This is it, Fleet Command.  Take them on with one of your combat Strike Groups.

RU:

> Вот оно, командование флота. Сразитесь с ними с помощью одной из своих боевых ударных групп.

### M01_040

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=patrolC) #513`.

Узел `Mission_M1#433`.

`M01_040_010_FI`

EN:

> Second Radaa patrol signature detected.

RU:

> Обнаружена вторая подпись патруля Радаа.

Узел `Mission_M1#521`.

`M01_040_020_KS`

EN:

> Do you see their position in the Sensors Manager?

RU:

> Вы видите их положение в Менеджере датчиков?

Узел `Mission_M1#543`.

`M01_040_030_TS`

EN:

> I see it all.

RU:

> Я все это вижу.

### M01_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=patrolB) #48`.

Узел `Mission_M1#597`.

`M01_050_010_FI`

EN:

> Final Radaa skirmish initiated.

RU:

> Началась последняя стычка в Раде.

Узел `Mission_M1#188`.

`M01_050_020_KS`

EN:

> Intelligence reports say the Radaa utilize very high level technology, but I haven't seen anything remarkable yet.

RU:

> В отчетах разведки говорится, что Рада использует технологии очень высокого уровня, но я пока не видел ничего примечательного.

### M01_060

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=patrolA) #40`.

Узел `Mission_M1#489`.

`M01_060_010_AR`

EN:

> Hiigaran command, I am Amma, Commander of the Radaa Fleet. I am declaring Taiidani agreement TR-3 in effect.

RU:

> Хиигарский командующий, я Амма, командующий флотом Радаа. Я объявляю Тайданское соглашение ТР-3 вступившим в силу.

Узел `Mission_M1#346`.

`M01_060_020_TS`

EN:

> What? What agreement?

RU:

> Что? Какое соглашение?

Узел `Mission_M1#529`.

`M01_060_030_AR`

EN:

> In return for a considerable investment from us, the Taiidani Emperor agreed to share all technology related to a Hyperspace Core.

RU:

> В обмен на значительные инвестиции с нашей стороны Тайиданский император согласился поделиться всеми технологиями, связанными с гиперпространственным ядром.

Узел `Mission_M1#208`.

`M01_060_040_KS`

EN:

> We made no such agreement!

RU:

> Мы не заключали такого соглашения!

Узел `Mission_M1#146`.

`M01_060_050_AR`

EN:

> When the Taiidan Empire fell, you inherited the planet Hiigara and all legal agreements pertaining to it.

RU:

> Когда Империя Тайдан пала, вы унаследовали планету Хиигара и все юридические соглашения, относящиеся к ней.

Узел `Mission_M1#409`.

`M01_060_055_AR`

EN:

> You are bound by that agreement to relinquish your Hyperspace Core or face default. Thank you for your cooperation.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M1#294`.

`M01_060_060_FI`

EN:

> Radaa Frigates have jumped in near the Mothership.

RU:

> Фрегаты Радаа высадились возле Материнского корабля.

Узел `Mission_M1#242`.

`M01_060_070_KS`

EN:

> Scanning Radaa Frigates...They are a Beta class threat, the could do us great harm. They are not joking.

RU:

> Сканирование фрегатов Радаа... Они представляют угрозу класса Бета и могут причинить нам большой вред. Они не шутят.

Узел `Mission_M1#306`.

`M01_060_080_AR`

EN:

> Your governing body has not complied in the given time period and is in default.

RU:

> Ваш руководящий орган не выполнил обязательства в течение заданного периода времени и находится в состоянии дефолта.

Узел `Mission_M1#633`.

`M01_060_085_AR`

EN:

> Though we anticipated this result we wish to assure you we are only taking what is legally ours.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M1#539`.

`M01_060_085_GR`

EN:

> Time to cooperate and stand down.

RU:

> Время сотрудничать и отступать.

Узел `Mission_M1#224`.

`M01_060_090_TS`

EN:

> I've got your cooperation right here.  Fleet to battle positions!

RU:

> У меня есть ваше сотрудничество прямо здесь. Флот на боевые позиции!

### M01_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=26, M01_Objective_02b) #236`.

Узел `Mission_M1#507`.

`M01_070_010_FI`

EN:

> Radaa Frigates neutralized but the Mothership has sustained significant damage.  Additional Radaa units incoming.

RU:

> Фрегаты Радаа нейтрализованы, но корабль-носитель получил значительные повреждения. Прибывают дополнительные подразделения Радаа.

Узел `Mission_M1#393`.

`M01_070_020_KS`

EN:

> Tyrra, there's too many. I know the Mothership won't take much more of this. You have to jump us out of here.

RU:

> Тирра, их слишком много. Я знаю, что Материнский корабль не выдержит большего. Ты должен вытащить нас отсюда.

Узел `Mission_M1#601`.

`M01_070_030_TS`

EN:

> That is my decision Karan S'jet... but you are not wrong. We need an isolated location to regroup. Jumping the Mothership and fleet now.

RU:

> Это мое решение, Каран С'жет... но ты не ошибаешься. Нам нужно изолированное место, чтобы перегруппироваться. Прыгаем с корабля-носителя и флота прямо сейчас.

### M01_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=LossEvent) #298`.

Узел `Mission_M1#344`.

`M01_080_010_GR`

EN:

> The Skirmish is won.  Our victory, your loss.  You will need to do better.

RU:

> Схватка выиграна. Наша победа, твоя потеря. Вам нужно будет добиться большего.

### M01_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=LossEvent) #298`.

Узел `Mission_M1#276`.

`M01_090_010_FI`

EN:

> Catastrophic losses reported.  Hiigaran fleet has been eliminated.

RU:

> Сообщается о катастрофических потерях. Хиигаранский флот уничтожен.

### M01_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=LossEvent) #559`.

Узел `Mission_M1#381`.

`M01_100_010_FI`

EN:

> Mothership has sustained massive damages. I repeat: Mothership incapacitated, Radaa forces will capture it.

RU:

> Корабль-носитель понес огромные повреждения. Повторяю: корабль-носитель выведен из строя, силы Рада захватят его.

### M01_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #226`.

Узел `Mission_M1#178`.

`M01_110_010_FI`

EN:

> The Radaa Missile Frigates are capable of breaching the hull of the Mothership.

RU:

> Ракетные фрегаты Радаа способны пробить корпус корабля-матери.

### M01_120

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #591`.

Узел `Mission_M1#425`.

`M01_120_010_FI`

EN:

> Damage to the Mothership from the hull breach is substantial, our situation is urgent.

RU:

> Повреждения материнского корабля из-за пробоины в корпусе значительны, наша ситуация неотложная.

### M01_130

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #246`.

Узел `Mission_M1#613`.

`M01_130_010_FI`

EN:

> Mothership damage nearing critical levels.

RU:

> Повреждения корабля-носителя приближаются к критическому уровню.

Узел `Mission_M1#284`.

`M01_130_020_KS`

EN:

> They'll take the Mothership if we can't end this fast.

RU:

> Они захватят Материнский Корабль, если мы не сможем покончить с этим так быстро.

## 2. M7: Темная сторона Ангельской Луны / Dark Side of Angel Moon

Определение `66adb7078ddb522448ddc9de037c9d07:1`, карта `level11`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M7 - Dark Side of Angel Moon/M7_Animatic_Intro/M2_Animatic_Intro.unity`

*Клип начинается в 0.00 с.*

`M09_003_010_A_FI`

EN:

> We have successfully jumped to the Tenhauser System. Damage reports coming in.  What are your orders, Commander?

RU:

> Мы успешно перешли на систему Тенхаузера. Поступают отчеты о повреждениях. Каковы ваши приказы, командир?

*Клип начинается в 1.65 с.*

`M07_010_010_A_TS`

EN:

> Hyperspace jump complete. Here we can assess our damage and get our systems back online without endangering Hiigara.

RU:

> Гиперпространственный прыжок завершен. Здесь мы сможем оценить нанесенный ущерб и восстановить работу наших систем, не подвергая опасности Хиигару.

*Клип начинается в 6.65 с.*

`M09_003_020_A_KS`

EN:

> Tyrra!

RU:

> Тирра!

*Клип начинается в 7.33 с.*

`M09_003_030_A_FI`

EN:

> Command is unresponsive. Med teams to Command Pod.

RU:

> Командование не отвечает. Медицинские бригады в командную капсулу.

*Клип начинается в 9.53 с.*

`M07_010_020_A_KS`

EN:

> They were after the Mothership and the Progenitor Core all along.

RU:

> Они все время преследовали Корабль-носитель и Ядро Прародителя.

*Клип начинается в 10.90 с.*

`M09_003_040_A_KS`

EN:

> Tyrra...!

RU:

> Тирра...!

*Клип начинается в 11.83 с.*

`M09_003_050_A_FI`

EN:

> Med teams reporting negative life signs.

RU:

> Медицинские бригады сообщают об отрицательных признаках жизни.

*Клип начинается в 13.19 с.*

`M07_010_030_A_TS`

EN:

> Sands and sinners!  This is very bad.

RU:

*Нет строки в извлечённой таблице этой версии.*

*Клип начинается в 14.92 с.*

`M09_003_060_A_KS`

EN:

> What?

RU:

> Что?

*Клип начинается в 17.12 с.*

`M09_003_070_A_FI`

EN:

> ...Fleet Command Tyrra Soban... confirmed killed in action. Med teams report complete neural failure. The Radaa weapon overloaded the Commander's link to the mothership.

RU:

> ...Командующий флотом Тирра Собан... подтверждена гибель в бою. Медицинские бригады сообщают о полной нейронной недостаточности. Оружие Радаа перегрузило связь командира с базовым кораблем.

*Клип начинается в 17.24 с.*

`M07_010_040_A_KS`

EN:

> To put it mildly.

RU:

> Мягко говоря.

*Клип начинается в 20.18 с.*

`M07_010_050_A_TS`

EN:

> The Daiamid has grown complacent.  Peace has made all the Kiith-Sa's too trusting. They didn't see the Radaa for what they are.

RU:

> Дайамид стал самодовольным. Мир сделал всех киит-са слишком доверчивыми. Они не видели Раду такой, какая она есть.

*Клип начинается в 27.23 с.*

`M07_010_060_A_KS`

EN:

> From what I have read they are deal makers – no home planet and they often use ships they acquired from other peoples.  Compared to the Taiidan, they seemed harmless.  But recrimination won't change where we are now.

RU:

> Судя по тому, что я читал, они заключают сделки, у них нет родной планеты, и они часто используют корабли, приобретенные у других народов. По сравнению с Тайиданом они казались безобидными. Но взаимные обвинения не изменят того, где мы находимся сейчас.

*Клип начинается в 28.52 с.*

`M09_003_073_A_KS`

EN:

> She should have broken the link!

RU:

> Ей следовало сломать ссылку!

*Клип начинается в 31.42 с.*

`M09_003_075_A_FI`

EN:

> Commander Tyrra Soban's last command was to initiate emergency hyperspace.

RU:

> Последним приказом командира Тирры Собан было запустить аварийное гиперпространство.

*Клип начинается в 37.33 с.*

`M09_003_080_A_KS`

EN:

> Oh Tyrra... All that the Mothership can do… you were its heart.  And it cost you everything to save us.

RU:

> О, Тирра... Все, на что способен Материнский корабль... ты была его сердцем. И это стоило тебе всего, чтобы спасти нас.

*Клип начинается в 40.38 с.*

`M07_010_070_A_TS`

EN:

> Intel!  I need an enemy to strike.  What do we know about their leadership?

RU:

> Интел! Мне нужен враг, чтобы нанести удар. Что мы знаем об их лидерстве?

*Клип начинается в 44.77 с.*

`M07_010_080_A_FI`

EN:

> The Radaa Commander is Amma – she inherited the job from her father and she is known as a shrewd negotiator.

RU:

> Командующим Рады является Амма – она унаследовала эту должность от своего отца и известна как проницательный переговорщик.

*Клип начинается в 46.78 с.*

`M09_003_085_A_KS`

EN:

> Intel, report... fleet status?

RU:

> Разведка, доложи... состояние флота?

*Клип начинается в 50.09 с.*

`M09_003_090_A_FI`

EN:

> Unknown weapon has disabled the majority of the fleet.

RU:

> Неизвестное оружие вывело из строя большую часть флота.

*Клип начинается в 51.38 с.*

`M07_010_090_A_FI`

EN:

> Her son Giitan acts as her second in command, known for his ruthlessness.

RU:

> Ее сын Гитан действует как ее заместитель, известный своей безжалостностью.

*Клип начинается в 53.62 с.*

`M09_003_100_A_KS`

EN:

> Mothership status?

RU:

> Статус материнского корабля?

*Клип начинается в 55.77 с.*

`M09_003_110_A_FI`

EN:

> Damaged, AI systems maintaining ship basic operation.  Emergency teams are moving the Commander to Medbay Twelve.

RU:

> Повреждены системы искусственного интеллекта, поддерживающие базовую работу корабля. Бригады экстренной помощи перевозят командира в медицинский отсек двенадцать.

*Клип начинается в 57.98 с.*

`M07_010_100_A_KS`

EN:

> Before we lost contact with Hiigara, we were informed the Daiamid sent an emergency appeal to the Galactic Council to seek assistance. No word on how long it will take.  We need to buy the Homeworld time.

RU:

> Прежде чем мы потеряли связь с Хиигарой, нам сообщили, что Дайамид направил экстренный призыв в Галактический Совет с просьбой о помощи. Ни слова о том, сколько времени это займет. Нам нужно купить время Родного мира.

*Клип начинается в 64.10 с.*

`M09_003_120_A_KS`

EN:

> How long before the Radaa find us?

RU:

> Сколько времени пройдет, прежде чем Рада нас найдет?

*Клип начинается в 66.71 с.*

`M09_003_130_A_FI`

EN:

> Unknown. But it is highly probable that you are correct - they will be coming.

RU:

> Неизвестный. Но весьма вероятно, что вы правы – они придут.

*Клип начинается в 70.58 с.*

`M07_010_110_A_TS`

EN:

> The Hiigaran fleet is in no shape for battle.  Some of our fleet is out of commission, supposedly being "upgraded" by the Radaa, while others are scattered on maneuvers. It’s up to us.

RU:

> Хиигаранский флот не в состоянии сражаться. Часть нашего флота выведена из строя, якобы "модернизируется" Радой, а часть разбросана на маневрах. Это зависит от нас.

*Клип начинается в 71.87 с.*

`M09_003_140_A_KS`

EN:

> No time. Under the Kharak Emergency Protocols, I am assuming command of the Mothership.

RU:

> Нет времени. Согласно чрезвычайным протоколам Харака, я принимаю на себя командование кораблем-матерью.

*Клип начинается в 81.68 с.*

`M09_003_145_A_KS`

EN:

> Alert the med teams that I am on my way to the command pod. Tell them to access medical file, Karan-zero-zero-zero.

RU:

> Сообщите медицинским бригадам, что я направляюсь к командной капсуле. Скажите им, чтобы они получили доступ к медицинской карте, Каран-ноль-ноль-ноль.

*Клип начинается в 81.83 с.*

`M07_010_120_A_KS`

EN:

> Tyrra, I know the rage you are feeling.  I watched Kharak burn.  But emotion drained me when I first fought as the Mothership. Focus on staying calm.

RU:

> Тирра, я знаю, какую ярость ты чувствуешь. Я видел, как горел Харак. Но эмоции истощили меня, когда я впервые сражался в роли Корабля-матери. Сосредоточьтесь на том, чтобы сохранять спокойствие.

*Клип начинается в 90.31 с.*

`M09_003_150_A_FI`

EN:

> Confirmed, Commander Karan S'jet.

RU:

> Подтверждено, командир Каран С'джет.

*Клип начинается в 92.35 с.*

`M07_010_130_A_TS`

EN:

> No offense, Karan, but rarely does a Soban require war wisdom from a S'jet.

RU:

> Без обид, Каран, но Собан редко требует военной мудрости от С'джета.

*Клип начинается в 95.67 с.*

`M09_003_160_A_HA`

EN:

> When Tyrra Soban fell, no one but Karan S'jet could take her place as Fleet Command. This time, she did not hesitate.

RU:

> Когда Тирра Собан пала, никто, кроме Каран С'джета, не смог занять ее место на посту командующего флотом. На этот раз она не колебалась.

*Клип начинается в 99.11 с.*

`M07_010_140_A_FI`

EN:

> Radaan fighters on deep sensors.  We have incoming!

RU:

> Бойцы Радаана на глубинных сенсорах. У нас есть поступления!

*Клип начинается в 102.94 с.*

`M07_010_150_A_TS`

EN:

> Very well, let's see what this Mothership can do.

RU:

> Что ж, давайте посмотрим, на что способен этот корабль-матка.

### Задачи, подключённые к графу

Узлы: 54, 158, 223.

`M07_Objective_01a`

EN:

> Harvest 700 RU to bring Sensors back online.

RU:

> Соберите 700 RU, чтобы снова включить датчики.

Узлы: 44, 146, 186.

`M07_Objective_01b`

EN:

> Time until jump drive is recharged:

RU:

> Время до перезарядки прыжкового двигателя:

Узлы: 247, 385.

`M07_Objective_02`

EN:

> Defend the Mothership during structural repairs.

RU:

> Защитите материнский корабль во время структурного ремонта.

Узлы: 156, 221, 251.

`M07_Objective_02a`

EN:

> Harvest 2000 total RU to restore construction sytems.

RU:

> Соберите 2000 RU, чтобы восстановить строительные системы.

Узлы: 31, 349.

`M07_Objective_03`

EN:

> Defend the Mothership while jump drive spins up.

RU:

> Защитите материнский корабль, пока набирает обороты прыжковый двигатель.

### M07_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #194`.

Узел `Mission_M7#319`.

`M07_020_010_TS`

EN:

> All departments, status report!

RU:

> Всем отделам, отчет о состоянии!

Узел `Mission_M7#50`.

`M07_020_020_FI`

EN:

> Radaa forces are approaching.  They must have honed in on the core signature.

RU:

> Силы Рады приближаются. Должно быть, они отточили основную сигнатуру.

Узел `Mission_M7#283`.

`M07_020_050_KS`

EN:

> Construction facilities still offline. We will have to fight with the fleet we have. We have deployed all reserve ships.

RU:

> Строительные объекты пока не работают. Нам придется сражаться с тем флотом, который у нас есть. Мы развернули все резервные корабли.

Узел `Mission_M7#166`.

`M07_020_080_TS`

EN:

> Sensors are down. I'm nearly blind!

RU:

> Датчики не работают. Я почти ослеп!

Узел `Mission_M7#134`.

`M07_020_090_FI`

EN:

> To repair the Sensors Manager, we will need to collect more resources. 

RU:

> Чтобы починить Менеджер датчиков, нам нужно будет собрать больше ресурсов.

Узел `Mission_M7#48`.

`M07_020_030_KS`

EN:

> Resource reserves were wiped out when our supply bays were hit.  We will have to gather more.

RU:

> Запасы ресурсов были уничтожены, когда наши отсеки снабжения были атакованы. Нам придется собрать больше.

### M07_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=16, M07_Objective_01a) #158`.

Узел `Mission_M7#327`.

`M07_030_010_TS`

EN:

> Sensors back online. Comms back at full.

RU:

> Датчики снова в сети. Связь в полном объеме.

Узел `Mission_M7#154`.

`M07_030_020_FI`

EN:

> We are receiving a transmission from Admiral Giitan of the Radaa.

RU:

> Мы получаем сообщение от адмирала Гитана из Рады.

Узел `Mission_M7#86`.

`M07_030_030_GR`

EN:

> Hiigaran Mothership, you have attempted to flee with our property.  Do not underestimate our perseverance in claiming our assets.

RU:

> Хиигарский корабль-матка, вы попытались сбежать с нашим имуществом. Не стоит недооценивать нашу настойчивость в борьбе за наши активы.

Узел `Mission_M7#33`.

`M07_030_040_TS`

EN:

> This is a farce.  No warrior fights on technicalities and lies.

RU:

> Это фарс. Ни один воин не сражается на основе формальностей и лжи.

Узел `Mission_M7#281`.

`M07_030_050_KS`

EN:

> Lies or not, we must secure more resources to get the Mothership's construction bays back online.

RU:

> Ложь это или нет, но мы должны обеспечить больше ресурсов, чтобы вернуть в строй строительные отсеки Материнского корабля.

### M07_040

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=28, M07_Objective_02a) #251`.

Узел `Mission_M7#235`.

`M07_040_010_TS`

EN:

> Ship build systems online. Fleet prepare to engage. 

RU:

> Системы сборки кораблей онлайн. Флот готовится к бою.

Узел `Mission_M7#309`.

`M07_040_013_KS`

EN:

> Commander, should we be fighting right where the Radaa want us?

RU:

> Командующий, должны ли мы сражаться именно там, где нас хочет Рада?

Узел `Mission_M7#94`.

`M07_040_015_TS`

EN:

> An excellent point, Karan.  I concur.  Intel, how long will I need to spin up the Hyperspace Core?

RU:

> Отличный момент, Каран. Я согласен. Интел, сколько времени мне понадобится, чтобы раскрутить Гиперпространственное ядро?

Узел `Mission_M7#152`.

`M07_040_020_FI`

EN:

> Engineering reports they are still dealing with damaged conduits.

RU:

> Инженерные службы сообщают, что они все еще имеют дело с поврежденными трубопроводами.

Узел `Mission_M7#231`.

`M07_040_030_TS`

EN:

> First I am told we have to go and now I am told I can't leave!  

RU:

> Сначала мне сказали, что нам пора идти, а теперь говорят, что я не могу уйти!

Узел `Mission_M7#239`.

`M07_040_040_TS`

EN:

> Intel, make engineering aware that their time is paid for in lives.  All ships, hold the Radaa off until we are cleared to jump.

RU:

> Intel, дайте инженерам понять, что их время оплачивается жизнями. Всем кораблям, держите Раду подальше, пока нам не будет разрешено совершить прыжок.

### M07_050

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=12, M07_Objective_01b) #146`.

Узел `Mission_M7#190`.

`M07_050_010_FI`

EN:

> Hyperspace systems are primed and ready.

RU:

> Гиперпространственные системы заряжены и готовы.

Узел `Mission_M7#60`.

`M07_050_020_TS`

EN:

> Inputting coordinates to a safe harbor. Jumping... now.

RU:

> Ввод координат безопасной гавани. Прыгаю... сейчас.

### M07_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=InitialResourceGroupLost) #62`; `CustomEvent (name=InsufficientResourcesLossEvent) #229`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M7#321`.

`M07_100_010_FI`

EN:

> Fleet eliminated. Mothership repair incomplete. Escape pods activated.

RU:

> Флот ликвидирован. Ремонт корабля-носителя незавершен. Спасательные капсулы активированы.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #144`; `CustomEvent #307`; `CustomEvent #317`; `CustomEvent #381`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M7#377`.

`FI_MothershipAttacked_01`

EN:

> The Mothership is under attack.

RU:

> Корабль-носитель подвергся нападению.

Узел `Mission_M7#335`.

`FI_MothershipCriticalDamage_01`

EN:

> Mothership has sustained critical damage.

RU:

> Корабль-носитель получил критические повреждения.

Узел `Mission_M7#273`.

`FI_MothershipHeavyDamage_01`

EN:

> Mothership has taken heavy damage.

RU:

> Корабль-носитель получил серьезные повреждения.

Узел `Mission_M7#373`.

`FI_MothershipLost_01`

EN:

> Mothership damage is massive, life support systems unsustainable. All personnel to the escape pods.

RU:

> Повреждения корабля-носителя огромны, системы жизнеобеспечения неработоспособны. Весь персонал в спасательные капсулы.

## 3. M3: Рейд на Гиббас / The Gybbas Raid

Определение `2b18e34423a7cfc4687ca08f9d35789f:1`, карта `level3`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M3 - A New Offensive/M3_Animatic_Intro/M3_Animatic_Intro.unity`

*Клип начинается в 1.15 с.*

`M03_010_008_A_TS`

EN:

> Radaa forces repelled. Any word from the Galactic Council?

RU:

> Силы Рады отразили нападение. Есть новости от Галактического Совета?

*Клип начинается в 4.85 с.*

`M03_010_010_A_KS`

EN:

> They report that the Radaa claims may be legally valid, but any attempts to call for a cease fire are being blocked by the Radaa and the council members they have made deals with.  The Bentusi are abstaining!

RU:

> Совет сообщает, что юридические требования Рады могут быть обоснованными, а любые призывы прекратить их действия блокируются членами совета, с которыми Рада заключила соглашения. Бентуси воздерживаются!

*Клип начинается в 16.89 с.*

`M03_010_020_A_TS`

EN:

> Fine,  Hiigara stands alone...again.  And we are the tip of the spear.

RU:

> Ладно, Хиигара осталась одна... снова. И мы — острие копья.

*Клип начинается в 23.33 с.*

`M03_010_030_A_KS`

EN:

> Intelligence, how much damage did the Mothership sustain?

RU:

> Разведка, какой ущерб получил Материнский корабль?

*Клип начинается в 26.54 с.*

`M03_010_035_A_FI`

EN:

> Minimal damage to core systems. Older, non-critical systems breaking down under stress. Repairs nearly complete.

RU:

> Минимальный ущерб основным системам. Старые, некритичные системы выходят из строя под воздействием стресса. Ремонт почти завершен.

*Клип начинается в 34.39 с.*

`M03_010_040_A_TS`

EN:

> Good! I won't wait for the Radaa's next move that will just get us stuck in a defensive war I can't win. Time for the one thing the Radaa won't expect from us: we are going to attack.

RU:

> Хороший! Я не буду ждать следующего шага Рады – это просто заставит нас ввязаться в оборонительную войну, которую я не смогу выиграть. Пришло время для того, чего Рада от нас не ожидает: мы собираемся атаковать.

*Клип начинается в 47.18 с.*

`M03_010_050_A_KS`

EN:

> The size of our fleet pales in comparison to theirs. You're still learning to control the Mothership.

RU:

> Размер нашего флота меркнет по сравнению с их. Ты все еще учишься управлять Кораблём-матерью.

*Клип начинается в 52.59 с.*

`M03_010_060_A_TS`

EN:

> I may be new to the ship, but I'm not new to leading a fleet. What is the closest Radaa outpost?

RU:

> Возможно, я новичок на корабле, но я не новичок в управлении флотом. Какой ближайший аванпост Рада?

*Клип начинается в 58.35 с.*

`M03_010_070_A_FI`

EN:

> The Radaa have built a ship yard in high orbit above Gybbas on the outer edge of our system.

RU:

> Радаа построила верфь на высокой орбите над Гиббасом, на внешней границе нашей системы.

*Клип начинается в 63.80 с.*

`M03_010_080_A_TS`

EN:

> Hmm...an easy jump.

RU:

> Хм... легкий прыжок.

*Клип начинается в 65.97 с.*

`M03_010_090_A_KS`

EN:

> It's a bold move, I admit.

RU:

> Признаю, это смелый шаг.

*Клип начинается в 67.83 с.*

`M03_010_100_A_TS`

EN:

> I would never risk our people if it weren't the right move.

RU:

> Я бы никогда не стал рисковать нашими людьми, если бы это был неправильный шаг.

*Клип начинается в 71.30 с.*

`M03_010_110_A_FI`

EN:

> Repairs complete. Transferring coordinates for the Orbital Shipyard.

RU:

> Ремонт завершен. Передача координат Орбитальной Верфи.

### Задачи, подключённые к графу

Узлы: 142, 414, 498, 540.

`M03_Objective_01`

EN:

> Destroy a Radaa Mobile Refinery.

RU:

> Уничтожьте передвижной нефтеперерабатывающий завод Радаа.

Узлы: 144, 152, 158, 240, 295, 418, 530, 578.

`M03_Objective_02`

EN:

> Destroy a second Radaa Mobile Refinery.

RU:

> Уничтожьте второй мобильный нефтеперерабатывающий завод Радаа.

Узлы: 244, 302, 428, 492.

`M03_Objective_03`

EN:

> Return your strike groups to the Mothership.

RU:

> Верните свои ударные группы на корабль-носитель.

Узлы: 426, 598, 600.

`M03_Objective_DestroyA`

EN:

> Destroy the Radaa Refinery near RU Field A.

RU:

> Уничтожьте нефтеперерабатывающий завод Радаа возле РУ-поля А.

Узлы: 330, 398, 610.

`M03_Objective_DestroyB`

EN:

> Destroy the Radaa Refinery near RU Field B.

RU:

> Уничтожьте нефтеперерабатывающий завод Радаа возле РУ-поля B.

Узлы: 196, 271, 650.

`M03_Objective_DestroyC`

EN:

> Destroy the Radaa Refinery near RU Field C.

RU:

> Уничтожьте нефтеперерабатывающий завод Радаа возле РУ-поля C.

Узлы: 128, 140, 174.

`M03_Objective_DestroyD`

EN:

> Destroy the Radaa Refinery near RU Field D.

RU:

> Уничтожьте нефтеперерабатывающий завод Радаа возле RU Field D.

### M03_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #212`.

Узел `Mission_M3#574`.

`M03_020_010_TS`

EN:

> Hyperspace Jump successful, right outside enemy sensor range. Fleet, identify targets.

RU:

> Гиперпространственный прыжок успешен, за пределами зоны действия сенсоров противника. Флот, определите цели.

Узел `Mission_M3#514`.

`M03_020_020_FI`

EN:

> The Radaa strip asteroids in this sector, resulting in numerous resource fields. Radaa presence in each varies.

RU:

> Радаа уничтожает астероиды в этом секторе, в результате чего появляются многочисленные месторождения ресурсов. Присутствие Рады в каждом из них различается.

Узел `Mission_M3#472`.

`M03_020_030_KS`

EN:

> The key will be to take out one of the Radaa's Mobile Refineries without engaging their whole fleet.  It will not be easy.

RU:

> Ключевым моментом будет уничтожение одного из мобильных нефтеперерабатывающих заводов Рады, не задействуя при этом весь их флот. Это будет нелегко.

Узел `Mission_M3#293`.

`M03_020_040_TS`

EN:

> Then I will carefully choose the one with the best tactical potential. Or maybe I will choose two.

RU:

> Тогда я тщательно выберу того, у кого лучший тактический потенциал. Или, может быть, я выберу два.

### M03_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=24, M03_Objective_DestroyB) #398`; `OnObjectiveCompleted (Objective=28, M03_Objective_DestroyA) #426`; `OnObjectiveCompleted (Objective=3, M03_Objective_DestroyD) #140`; `OnObjectiveCompleted (Objective=50, M03_Objective_DestroyC) #650`.

Узел `Mission_M3#546`.

`M03_030_010_FI`

EN:

> Confirmed, Radaa Refinery eliminated.  The field is ours.

RU:

> Подтверждено, НПЗ Радаа ликвидирован. Поле наше.

Узел `Mission_M3#602`.

`M03_030_020_KS`

EN:

> The Radaa haven't committed their full fleet yet.

RU:

> Рада еще не задействовала весь свой флот.

Узел `Mission_M3#204`.

`M03_030_030_TS`

EN:

> I am keeping our movements variable.  If the Radaa guess wrong about our next objective, I will make them pay for it.  And they know it.

RU:

> Я сохраняю переменность наших движений. Если Рада ошибется в отношении нашей следующей цели, я заставлю их заплатить за это. И они это знают.

Узел `Mission_M3#486`.

`M03_030_040_KS`

EN:

> You are a dangerous opponent, Tyrra.

RU:

> Ты опасный противник, Тирра.

Узел `Mission_M3#304`.

`M03_030_050_TS`

EN:

> High praise from the woman who brought down the Taiidani Empire.

RU:

> Высокая похвала от женщины, которая разрушила Империю Тайидани.

Узел `Mission_M3#424`.

`M03_030_060_KS`

EN:

> I had a lot of help.

RU:

> Мне очень помогли.

Узел `Mission_M3#238`.

`M03_030_070_TS`

EN:

> And I have you. But I can feel our opponent getting tired of this dance. Whichever resource field I pick next, we will be facing many more Radaa forces.

RU:

> И у меня есть ты. Но я чувствую, что наш соперник устал от этого танца. Какое бы поле ресурсов я ни выбрал в следующий раз, нам придется столкнуться с гораздо большим количеством сил Рада.

### M03_040

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=24, M03_Objective_DestroyB) #398`; `OnObjectiveCompleted (Objective=28, M03_Objective_DestroyA) #426`; `OnObjectiveCompleted (Objective=3, M03_Objective_DestroyD) #140`; `OnObjectiveCompleted (Objective=50, M03_Objective_DestroyC) #650`.

Узел `Mission_M3#466`.

`M03_040_010_FI`

EN:

> Radaa Refinery neutralized.  Detecting numerous Radaa forces on intercept course.

RU:

> Нефтеперерабатывающий завод Радаа нейтрализован. Обнаружение многочисленных сил Рада на курсе перехвата.

Узел `Mission_M3#458`.

`M03_040_020_TS`

EN:

> I knew it.  All ships, pull back to the Mothership, now!

RU:

> Я знал это. Все корабли, немедленно отойдите к кораблю-матери!

Узел `Mission_M3#494`.

`M03_040_030_KS`

EN:

> Well played, Commander.

RU:

> Хорошая игра, коммандер.

### M03_060

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=13, M03_Objective_03) #244`.

Узел `Mission_M3#568`.

`M03_060_010_FI`

EN:

> Our fleet is in range of the Mothership.

RU:

> Наш флот в пределах досягаемости Материнского корабля.

Узел `Mission_M3#654`.

`M03_060_020_TS`

EN:

> Hyperspace Jump on my command. We have achieved our goal here.  The Radaa know we Hiigarans are ready to fight.

RU:

> Гиперпространственный прыжок по моей команде. Здесь мы достигли своей цели. Рада знает, что мы, хиигарцы, готовы сражаться.

### M03_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=NoResources) #456`.

Узел `Mission_M3#480`.

`M03_070_010_FI`

EN:

> Retreat! Critical loss of ships. Surviving ships retreat immediately.

RU:

> Отступление! Критическая потеря кораблей. Выжившие корабли немедленно отступают.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #283`; `CustomEvent #354`; `CustomEvent #436`; `OnSimReady #212`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M3#320`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M3#338`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M3#277`.

`FI_MothershipLost_05`

EN:

> Catastrophic damage to Mothership. All hands to the escape pods.

RU:

> Катастрофический ущерб Mothership. Все к спасательным капсулам.

Узел `Mission_M3#432`.

`FI_UnlockHeavyCorvette`

EN:

> Our ongoing repairs to the Mothership has added ship build capabilities: we can now build Heavy Corvettes. Their armor is ideal against heavy ballistics from the gun platforms we have detected in this sector.

RU:

> Наш текущий ремонт Материнского корабля расширил возможности постройки кораблей: теперь мы можем строить Тяжелые Корветы. Их броня идеальна против тяжелых баллистических снарядов артиллерийских платформ, которые мы обнаружили в этом секторе.

## 4. M4: Потерянный разрушитель / The Lost Destroyer

Определение `894aa6041375b8c4386950e1073d009c:1`, карта `level5`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M4 - A Key Asset/M4_Animatic_Intro/M4_Animatic_Intro.unity`

*Клип начинается в 1.05 с.*

`M04_010_010_A_FI`

EN:

> Commander, we are picking up a distress beacon.

RU:

> #REF!

*Клип начинается в 4.30 с.*

`M04_010_020_A_TS`

EN:

> Receiving... it's not one of ours.

RU:

> #REF!

*Клип начинается в 8.92 с.*

`M04_010_030_A_FI`

EN:

> Confirmed, it is from a Radaa Destroyer. It's signaling failing drives and life support...but weapon systems still functional.

RU:

*Нет строки в извлечённой таблице этой версии.*

*Клип начинается в 17.92 с.*

`M04_010_040_A_TS`

EN:

> Convenient. It could be a trap.

RU:

> Командир, мы ловим сигнал бедствия.

*Клип начинается в 21.48 с.*

`M04_010_050_A_KS`

EN:

> When I fought the Taiidani, captured ships were critical for understanding what we were up against.

RU:

> Получаю... это не наш.

*Клип начинается в 27.23 с.*

`M04_010_060_A_TS`

EN:

> So trap or not, it's a chance worth taking.

RU:

> Подтверждено, это от разрушителя Радаа. Это сигнализирует о выходе из строя двигателей и системы жизнеобеспечения... но системы вооружения все еще работают.

*Клип начинается в 30.87 с.*

`M04_010_070_A_KS`

EN:

> Knowledge is power.

RU:

> Удобный. Это может быть ловушка.

*Клип начинается в 32.72 с.*

`M04_010_080_A_TS`

EN:

> Spoken like a true S'jet. Fleet Intelligence, monitor the area for Radaa ships. We are going in.

RU:

> Когда я сражался с тайидани, захваченные корабли имели решающее значение для понимания того, с чем мы столкнулись.

### Задачи, подключённые к графу

Узлы: 257, 309, 502.

`M04_Objective_01`

EN:

> Locate the Radaa Destroyer.

RU:

> Найдите Разрушитель Радаа.

Узлы: 69, 165, 167, 273.

`M04_Objective_02`

EN:

> Destroy all hostiles around the Radaa Destroyer.

RU:

> Уничтожьте всех противников вокруг разрушителя Радаа.

Узлы: 340, 390.

`M04_Objective_03`

EN:

> Dock 3 Engineer Craft to the Radaa Destroyer.

RU:

> Док 3 Инженерного корабля к разрушителю Радаа.

Узлы: 63, 131, 179, 316, 324.

`M04_Objective_04`

EN:

> Defend the Radaa Destroyer while it is en route to the Mothership.

RU:

> Защитите разрушитель «Радаа», пока он направляется к кораблю-матери.

Узлы: 239, 281, 305, 406, 464.

`M04_Objective_05`

EN:

> (Optional) Destroy the Hyperspace Gate.

RU:

> (Необязательно) Уничтожьте Гиперпространственные врата.

### M04_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #384`.

Узел `Mission_M4#277`.

`M04_020_005_TS`

EN:

> Hyperspace jump complete.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M4#23`.

`M04_020_010_KS`

EN:

> These ships! They must have been a Hiigaran patrol.

RU:

> Эти корабли! Должно быть, это был хиигарский патруль.

Узел `Mission_M4#342`.

`M04_020_020_TS`

EN:

> Scan for threats.

RU:

> Сканируйте на наличие угроз.

Узел `Mission_M4#217`.

`M04_020_030_FI`

EN:

> All disabled. No signs of life.

RU:

> Все отключены. Никаких признаков жизни.

Узел `Mission_M4#336`.

`M04_020_040_KS`

EN:

> Just floating... lost souls without a mark on any ship. A Radaan Destroyer couldn't have just neutralized them like this.

RU:

> Просто плыву... потерянные души без отметки ни на одном корабле. Разрушитель Радаана не мог просто нейтрализовать их таким образом.

Узел `Mission_M4#75`.

`M04_020_050_TS`

EN:

> And yet here they are... Initiate search for what could have caused this.

RU:

> И все же они здесь... Начать поиск того, что могло стать причиной этого.

Узел `Mission_M4#61`.

`M04_020_060_FI`

EN:

> High concentrations of asteroid debris are interfering with scans. We are detecting multiple Radaa strike craft incoming.

RU:

> Высокая концентрация обломков астероидов мешает сканированию. Мы обнаруживаем приближающиеся несколько ударных кораблей Радаа.

Узел `Mission_M4#394`.

`M04_020_070_TS`

EN:

> They will never make this easy.

RU:

> Они никогда не сделают это легко.

### M04_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=27, M04_Objective_01) #257`.

Узел `Mission_M4#488`.

`M04_030_010_FI`

EN:

> Radaa Destroyer located. Enemy forces are en route to intercept.

RU:

> Разрушитель Радаа обнаружен. Вражеские силы идут на перехват.

Узел `Mission_M4#506`.

`M04_030_020_TS`

EN:

> Strike Groups, intercept the Radaa before they reach their target.

RU:

> Ударные группы, перехватите Раду до того, как она достигнет своей цели.

Узел `Mission_M4#33`.

`M04_030_030_KS`

EN:

> All this debris makes for a dangerous place to fight.

RU:

> Весь этот мусор делает место опасным для боя.

Узел `Mission_M4#227`.

`M04_030_040_TS`

EN:

> All ships, keep a close eye on sensors.

RU:

> Всем кораблям, внимательно следите за датчиками.

### M04_040

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=17, M04_Objective_02) #165`.

Узел `Mission_M4#57`.

`M04_040_010_FI`

EN:

> Radaa retrieval team eliminated.

RU:

> Спасательная группа Рада ликвидирована.

Узел `Mission_M4#137`.

`M04_040_020_KS`

EN:

> Too exposed out here. More Radaa will come before we can extract any intel.

RU:

> Здесь слишком открыто. Прежде чем мы сможем получить какую-либо информацию, придет еще Радаа.

Узел `Mission_M4#482`.

`M04_040_030_TS`

EN:

> So we haul the Destroyer back to the Mothership.

RU:

> Итак, мы тащим Разрушитель обратно на Корабль-носитель.

Узел `Mission_M4#496`.

`M04_040_040_FI`

EN:

> Transporting the Destroyer will require multiple Engineer Craft.

RU:

> Для транспортировки Разрушителя потребуется несколько инженерных судов.

### M04_050

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #508`.

Узел `Mission_M4#231`.

`M04_050_010_FI`

EN:

> All Engineer Craft are in place. Destroyer on course.

RU:

> Все инженерные корабли на месте. Разрушитель на курсе.

Узел `Mission_M4#470`.

`M04_050_020_KS`

EN:

> The Radaa will attempt to eradicate that Destroyer before letting us capture it.

RU:

> Рада попытается уничтожить этого Разрушителя, прежде чем позволить нам его захватить.

Узел `Mission_M4#237`.

`M04_050_030_TS`

EN:

> They are welcome to try.

RU:

> Они могут попробовать.

### M04_060

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #508`.

Узел `Mission_M4#41`.

`M04_060_010_FI`

EN:

> New signature detected.  Radaa Strike Craft emerging from Hyperspace Gate.

RU:

> Обнаружена новая подпись. Ударный корабль Радаа выходит из Гиперпространственных врат.

Узел `Mission_M4#233`.

`M04_060_020_TS`

EN:

> They really don't want us to get ahold of that Destroyer.

RU:

> Они действительно не хотят, чтобы мы завладели этим Разрушителем.

Узел `Mission_M4#55`.

`M04_060_030_KS`

EN:

> If we get the Destroyer to the Mothership, we can jump away with it. Or we can destroy the Hyperspace Gate to cripple the Radaa. Fleet Command, it's your call.

RU:

> Если мы доставим Разрушитель на Материнский корабль, мы сможем убежать вместе с ним. Или мы можем уничтожить Гиперпространственные Врата, чтобы нанести вред Раде. Командование флота, это ваше дело.

### M04_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=26, M04_Objective_05) #239`.

Узел `Mission_M4#450`.

`M04_070_010_FI`

EN:

> Hyperspace Gate neutralized.  Radaa forces in retreat.

RU:

> Гиперпространственные врата нейтрализованы. Силы Рады отступают.

Узел `Mission_M4#225`.

`M04_070_020_TS`

EN:

> And now, to the victor goes the prize.

RU:

> И вот победителю достается приз.

Узел `Mission_M4#376`.

`M04_070_030_FI`

EN:

> We have a lock on the Destroyer.  Hyperspace jump ready on your command.

RU:

> У нас есть замок на Разрушителе. Гиперпространственный прыжок готов по вашей команде.

### M04_080

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #458`.

Узел `Mission_M4#388`.

`M04_080_010_FI`

EN:

> The Destroyer is in range of the Mothership with Radaa forces in retreat. We are clear to jump on your command.

RU:

> Разрушитель находится в пределах досягаемости Материнского корабля, а силы Радаа отступают. Мы готовы прыгнуть по вашей команде.

### M04_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=YouLose1) #412`; `CustomEvent (name=YouLose2) #235`; `CustomEvent (name=YouLose3) #187`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M4#91`.

`M04_100_010_FI`

EN:

> Too many ships destroyed, we are out of options. Retreat, retreat.

RU:

> Слишком много кораблей уничтожено, у нас нет выбора. Отступить, отступить.

Узел `Mission_M4#442`.

`M04_100_020_FI`

EN:

> The Destroyer has taken critical damage, our objective is lost.

RU:

> Разрушитель получил критический урон, наша цель потеряна.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #259`; `CustomEvent #446`; `CustomEvent #468`; `OnSimReady #384`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M4#29`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M4#49`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M4#462`.

`FI_MothershipLost_03`

EN:

> We have lost the Mothership.

RU:

> Мы потеряли Материнский Корабль.

Узел `Mission_M4#332`.

`FI_UnlockEngineerCraft`

EN:

> Resources claimed from Gybbas allow us to build a new ship: the Engineer Craft, which has the ability to repair ships in their Strike Group. They are also key to capturing the Radaa Destroyer in this sector.

RU:

> Ресурсы, полученные от Гиббаса, позволяют нам построить новый корабль: «Инженерный корабль», способный ремонтировать корабли своей ударной группы. Они также играют ключевую роль в захвате Разрушителя Радаа в этом секторе.

## 5. M5: Верфь Хиигара / Hiigara Shipyard

Определение `68fed03dd3ebcff49bcb60c9565b658b:1`, карта `level7`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M5 - Turning the Tide/M5_Animatic_Intro/M5_Animatic_Intro.unity`

*Клип начинается в 1.03 с.*

`M05_010_010_A_TS`

EN:

> Chief Engineer Hauk, what is your analysis of the data we sent you on our captured Radaa Destroyer?

RU:

> Знание - сила.

*Клип начинается в 6.93 с.*

`M05_010_020_A_HA`

EN:

> It's been a challenge, Commander.  We saw very little consistency to their systems, but then we realized we were looking at a fusion of Taiidani, Bentus and even our own technology.  There are also some components we've never seen before.

RU:

> Говорю как настоящий С'джет. Разведка флота, следите за районом на предмет кораблей Радаа. Мы входим.

*Клип начинается в 19.08 с.*

`M05_010_030_A_KS`

EN:

> Did Radaa tech render all those ships inoperable?

RU:

*Нет строки в извлечённой таблице этой версии.*

*Клип начинается в 22.58 с.*

`M05_010_040_A_HA`

EN:

> Too early to say. My engineering team should have an educated guess very soon.

RU:

> Это был вызов, коммандер. Мы не увидели в их системах очень мало единообразия, но потом поняли, что перед нами слияние Тайидани, Бентуса и даже нашей собственной технологии. Есть также некоторые компоненты, которые мы никогда раньше не видели.

*Клип начинается в 26.18 с.*

`M05_010_050_A_TS`

EN:

> I can't afford guesses, Hauk.  I need an edge.  Something we can use right away.

RU:

> Неужели технологии Радаа вывели все эти корабли из строя?

*Клип начинается в 31.62 с.*

`M05_010_060_A_HA`

EN:

> Science is not something you can shoot, Commander.   I will have some--

RU:

> Слишком рано говорить. Моя команда инженеров очень скоро должна получить обоснованное предположение.

*Клип начинается в 35.80 с.*

`M05_010_070_A_FI`

EN:

> Another distress call, Fleet Command.  This time it's one of ours.  Hiigaran Orbital Shipyard Dalkaar is under siege.

RU:

> Я не могу позволить себе догадок, Хаук. Мне нужно преимущество. Что-то, что мы можем использовать прямо сейчас.

*Клип начинается в 44.22 с.*

`M05_010_075_A_KS`

EN:

> There are thousands of civilians on that station. Families.

RU:

> Наука – это не то, чем можно стрелять, коммандер. Я возьму немного...

*Клип начинается в 49.55 с.*

`M05_010_080_A_TS`

EN:

> Burning Hells! And if they take that Shipyard, Hiigara herself is wide open. No one is putting Hiigarans in chains again. Fleet, full alert and prepare for jump!

RU:

> Еще один сигнал бедствия, командование флотом. На этот раз это один из наших. Хиигаранская орбитальная верфь Далкаар находится в осаде.

### Задачи, подключённые к графу

Узлы: 262, 380, 498, 567.

`M05_Objective_01`

EN:

> Defend the Hiigara Shipyard.

RU:

> Защитите верфь Хиигара.

Узлы: 436, 504, 522, 557.

`M05_Objective_02`

EN:

> Defend the Mothership.

RU:

> Защитите материнский корабль.

Узлы: 133, unlinked_958633cf-027f-4e96-938d-349c52d9dfb8.

`M05_Objective_counter0`

EN:

> Waves of Radaa ships defeated: 0

RU:

> Побеждены корабли Волн Радаа: 0

Узлы: 82, 394.

`M05_Objective_counter1`

EN:

> Waves of Radaa ships defeated: 1

RU:

> Корабли Волн Рада побеждены: 1

Узлы: 54, 585.

`M05_Objective_counter10`

EN:

> Waves of Radaa ships defeated: 10

RU:

> Побеждены корабли Волн Радаа: 10

Узлы: 99, 609.

`M05_Objective_counter2`

EN:

> Waves of Radaa ships defeated: 2

RU:

> Побеждены корабли Волн Радаа: 2

Узлы: 68, 603.

`M05_Objective_counter3`

EN:

> Waves of Radaa ships defeated: 3

RU:

> Побеждены корабли Волн Радаа: 3

Узлы: 173, 661.

`M05_Objective_counter4`

EN:

> Waves of Radaa ships defeated: 4

RU:

> Побеждены корабли Волн Радаа: 4

Узлы: 356, 510.

`M05_Objective_counter5`

EN:

> Waves of Radaa ships defeated: 5

RU:

> Побеждены корабли Волн Радаа: 5

Узлы: 332, 388.

`M05_Objective_counter6`

EN:

> Waves of Radaa ships defeated: 6

RU:

> Побеждены корабли Волн Радаа: 6

Узлы: 66, 372.

`M05_Objective_counter7`

EN:

> Waves of Radaa ships defeated: 7

RU:

> Побеждены корабли Волн Радаа: 7

Узлы: 396, 402.

`M05_Objective_counter8`

EN:

> Waves of Radaa ships defeated: 8

RU:

> Побеждены корабли Волн Радаа: 8

Узлы: 143, 344.

`M05_Objective_counter9`

EN:

> Waves of Radaa ships defeated: 9

RU:

> Побеждены корабли Волн Радаа: 9

### M05_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #474`.

Узел `Mission_M5#286`.

`M05_020_010_FI`

EN:

> Hyperspace jump complete, the Shipyard is in range, and vulnerable.

RU:

> Гиперпространственный прыжок завершен, Верфь находится в пределах досягаемости и уязвима.

Узел `Mission_M5#490`.

`M05_020_020_HA`

EN:

> Fleet Command - our construction systems are down, defenses are badly reduced.  We won't survive another attack wave.

RU:

> Командование флотом – наши строительные системы вышли из строя, оборона сильно ослаблена. Мы не переживем еще одну волну нападения.

Узел `Mission_M5#316`.

`M05_020_030_FI`

EN:

> Radaa Strike Craft about to enter firing range.

RU:

> Ударный корабль Радаа собирается выйти на стрельбище.

Узел `Mission_M5#448`.

`M05_020_040_TS`

EN:

> We are going to make them regret threatening our people.

RU:

> Мы заставим их пожалеть об угрозах нашему народу.

### M05_030

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=wave1memos) #512`.

Узел `Mission_M5#573`.

`M05_030_010_HA`

EN:

> Fleet Command, you have a whole station cheering you on.  If you continue to provide defense, my team can focus on our analysis.

RU:

> Командование флота, вас поддерживает целая станция. Если вы продолжите обеспечивать защиту, моя команда сможет сосредоточиться на нашем анализе.

Узел `Mission_M5#565`.

`M05_030_020_TS`

EN:

> We each have our jobs to do, Chief Engineer.

RU:

> У каждого из нас есть своя работа, главный инженер.

Узел `Mission_M5#298`.

`M05_030_030_FI`

EN:

> Commander, there is an incoming Radaa transmission. It is broadcasting to Hiigara and all craft in orbit.

RU:

> Командир, идет входящее сообщение Радаа. Оно транслируется на Хиигару и все корабли на орбите.

Узел `Mission_M5#91`.

`M05_030_040_GR`

EN:

> Per our agreement, surrender the Mothership and its Hyperspace Core, or we will destroy the balance of your assets.

RU:

> Согласно нашему соглашению, сдайте материнский корабль и его гиперпространственное ядро, иначе мы уничтожим остаток ваших активов.

Узел `Mission_M5#446`.

`M05_030_050_TS`

EN:

> Our people are expendable to them, just negotiating points. And I'm not negotiating.

RU:

> Наши люди для них расходный материал, они просто обсуждают вопросы. И я не веду переговоров.

Узел `Mission_M5#216`.

`M05_030_060_FI`

EN:

> Additional enemy units are inbound.

RU:

> Приближаются дополнительные вражеские подразделения.

### M05_040

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=wave6memos) #308`.

Узел `Mission_M5#649`.

`M05_040_010_KS`

EN:

> You strike without reserve.

RU:

> Вы наносите удар без остатка.

Узел `Mission_M5#406`.

`M05_040_020_TS`

EN:

> What use will hesitation be If they take the shipyard. Our people...  My only son is on board.

RU:

> Какая польза от колебаний, если они захватят верфь. Наши люди... Мой единственный сын на борту.

Узел `Mission_M5#464`.

`M05_040_030_KS`

EN:

> Chief Engineer Hauk?  But isn't he...

RU:

> Главный инженер Хаук? Но разве он...

Узел `Mission_M5#149`.

`M05_040_040_TS`

EN:

> As a boy he found the ways of your people more familiar than the traditions of the Kiith he was born into. Do you have people close to you in the fleet?

RU:

> В детстве нравы вашего народа ему были более знакомы, чем традиции киита, в котором он родился. Есть ли у вас на флоте близкие вам люди?

Узел `Mission_M5#508`.

`M05_040_050_KS`

EN:

> S'jets may not be a warrior kiith but we go where we are needed.

RU:

> С'джетс, возможно, и не воинственный киит, но мы идем туда, где мы нужны.

Узел `Mission_M5#597`.

`M05_040_060_FI`

EN:

> Contact. Numerous Radaa Strike Craft detected.

RU:

> Контакт. Обнаружено множество ударных кораблей Радаа.

### M05_050

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=triggerCutscene) #268`.

Узел `Mission_M5#452`.

`M05_050_010_FI`

EN:

> Sensors are picking up a massive influx of Radaa ships.

RU:

> Сенсоры фиксируют массовый приток кораблей Радаа.

Узел `Mission_M5#42`.

`M05_050_020_KS`

EN:

> They are sending everything they have at us.

RU:

> Они посылают к нам все, что у них есть.

Узел `Mission_M5#440`.

`M05_050_030_TS`

EN:

> They will regret sending so many.

RU:

> Они пожалеют, что отправили так много людей.

### M05_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=winLevel) #218`.

Узел `Mission_M5#424`.

`M05_070_010_FI`

EN:

> No further Radaa signatures. Shipyard superstructure still intact, damages minimal.

RU:

> Больше никаких подписей в Раде. Надстройка верфи сохранилась целой, повреждения минимальны.

Узел `Mission_M5#516`.

`M05_070_020_KS`

EN:

> You did it. The shipyard is safe. Your son is...

RU:

> Ты сделал это. Верфь безопасна. Ваш сын...

Узел `Mission_M5#480`.

`M05_070_030_TS`

EN:

> ...not safe until all the Radaa are gone from this system. None of us are.

RU:

> ...небезопасно, пока вся Рада не уйдет из этой системы. Никто из нас не такой.

### M05_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=resourceLose) #185`.

Узел `Mission_M5#34`.

`M05_100_010_FI`

EN:

> Abort, abort. Unable to defend the Shipyard.

RU:

> Прервать, прервать. Невозможно защитить Верфь.

### M05_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=defendLoss) #306`.

Узел `Mission_M5#304`.

`M05_110_010_FI`

EN:

> The shipyard is damaged beyond repair. Surviving crew are heading for the escape pods.

RU:

> Верфь повреждена и не подлежит восстановлению. Выживший экипаж направляется к спасательным капсулам.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #139`; `CustomEvent #639`; `CustomEvent #657`; `OnSimReady #474`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M5#641`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M5#645`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M5#599`.

`FI_MothershipLost_06`

EN:

> All systems critically compromised. Abandon the Mothership.

RU:

> Все системы критически скомпрометированы. Покиньте материнский корабль.

Узел `Mission_M5#56`.

`FI_UnlockMultiGunCorvette`

EN:

> Our engineering team has added capability to our construction bays: Multi-Gun Corvettes. These are ideal for counter-attack against the Radaa's fast-moving threats to the shipyard.

RU:

> Наша команда инженеров расширила возможности наших строительных отсеков: многопушечные корветы. Они идеально подходят для контратаки против быстро распространяющихся угроз верфи со стороны Рады.

## 6. M6: Оружие / The Weapon

Определение `c6a609b9e607c244fb916366c37ad701:1`, карта `level9`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M6 - Shattered/M6_Animatic_Intro/M6_Animatic_Intro.unity`

*Клип начинается в 0.98 с.*

`M06_010_010_A_TS`

EN:

> Radaa expelled. Shipyard still in orbit, and Officer Hauk will board shortly with his engineering team and a report.

RU:

> Рада изгнана. Верфь все еще на орбите, и вскоре на борт поднимется офицер Хаук со своей инженерной командой и отчетом.

*Клип начинается в 8.58 с.*

`M06_010_020_A_KS`

EN:

> Tyrra, you are mastering the Mothership like you were born to it. Far faster than I did.

RU:

> Тирра, ты владеешь Кораблём-матерью так, как будто ты для него рождена. Гораздо быстрее, чем я.

*Клип начинается в 13.68 с.*

`M06_010_030_A_TS`

EN:

> I have something you didn't: a good advisor.

RU:

> У меня есть то, чего не было у тебя: хороший советчик.

*Клип начинается в 17.57 с.*

`M06_010_040_A_KS`

EN:

> You may not need me much longer.

RU:

> Возможно, я тебе больше не понадобится.

*Клип начинается в 20.37 с.*

`M06_010_050_A_TS`

EN:

> I wouldn't say that, but since there is no safe place to disembark the Hero of the Homeworld War, we are in this together for the duration. It's time to attack their command structure. What do we know of their base of operations?

RU:

> Я бы так не сказал, но поскольку нет безопасного места, где можно высадить Героя Войны Родного Мира, мы находимся в этом вместе на протяжении всего времени. Пришло время атаковать их командную структуру. Что мы знаем об их базе операций?

*Клип начинается в 33.20 с.*

`M06_010_100_A_FI`

EN:

> Their home base is mobile – they call it Radaa Tower – they often station it within one system to do business, then move on.

RU:

> Их базовая база мобильна — они называют ее Башней Рада — они часто размещают ее внутри одной системы, чтобы вести дела, а затем уходят дальше.

*Клип начинается в 41.16 с.*

`M06_010_110_A_KS`

EN:

> And now they're doing business with us.

RU:

> И теперь они имеют с нами дело.

*Клип начинается в 44.85 с.*

`M06_010_120_A_TS`

EN:

> The attack on the Orbital Shipyard was a misdirect. To keep us occupied while they established their main base.  Intel, find that Tower!

RU:

> Атака на орбитальную верфь была ошибочной. Чтобы держать нас занятыми, пока они создают свою главную базу. Интел, найди эту Башню!

*Клип начинается в 51.98 с.*

`M06_010_130_A_FI`

EN:

> Scanning...picking up a massive energy signature in Hiigara shadow. Indications are that it is Radaa Tower. Transferring coordinates.

RU:

> Сканирование... обнаружение мощного энергетического следа в тени Хиигары. Есть указания на то, что это башня Радаа. Передача координат.

*Клип начинается в 61.02 с.*

`M06_010_140_A_TS`

EN:

> That's it. Time to show that Hiigarans are not easy prey. Let's finish this.

RU:

> Вот и все. Пришло время показать, что хиигарцы — непростая добыча. Давай закончим это.

### Задачи, подключённые к графу

Узлы: 92, 128, 243, 283, 314, 320, 377, 413, 435, 485, 619.

`M06_Objective_01`

EN:

> Locate a shield emitter.

RU:

> Найдите излучатель щита.

Узлы: 253, 507, 537.

`M06_Objective_02`

EN:

> Dock an Engineer Craft to the shield emitter.

RU:

> Пристыкуйте инженерный корабль к излучателю щита.

Узлы: 76, 277, 345, 479, 497, 648, 696.

`M06_Objective_03counter`

EN:

> Disable shield emitters.

RU:

> Отключите излучатели щита.

Узлы: 328, 570, 734.

`M06_Objective_04`

EN:

> Attack the Radaa Tower.

RU:

> Атакуйте башню Радаа.

Узлы: 100, 363, 511, 704.

`M06_Objective_alphacapture`

EN:

> Disable shield emitter alpha.

RU:

> Отключите излучатель щита альфа.

Узлы: 86, 592, 646, 702.

`M06_Objective_betacapture`

EN:

> Disable shield emitter beta.

RU:

> Отключить бета-версию излучателя щита.

Узлы: 281, 407, 503, 816.

`M06_Objective_deltacapture`

EN:

> Disable shield emitter delta.

RU:

> Отключить дельту эмиттера щита.

Узлы: 58, 122, 332, 373.

`M06_Objective_omegacapture`

EN:

> Disable shield emitter omega.

RU:

> Отключите эмиттер щита Омега.

### M06_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #399`.

Узел `Mission_M6#353`.

`M06_020_010_FI`

EN:

> Radaa forces are swarming around the tower.

RU:

> Силы Рада толпятся вокруг башни.

Узел `Mission_M6#273`.

`M06_020_020_TS`

EN:

> They are a distraction. Our target is the tower.

RU:

> Они отвлекают. Наша цель — башня.

Узел `Mission_M6#580`.

`M06_020_023_AR`

EN:

> Hiigaran Mothership, Fleet Command.  We Radaa have been waiting patiently for you to turn over our property.

RU:

> Хиигаранский корабль-носитель, командование флотом. Мы, Рада, терпеливо ждали, пока вы передадите нашу собственность.

Узел `Mission_M6#174`.

`M06_020_025_TS`

EN:

> Ignore her  - we're not hear to talk.  Hauk, is that distortion around it a shield?

RU:

> Не обращайте на нее внимания – нам не слышно говорить. Хаук, это искажение вокруг него - щит?

Узел `Mission_M6#574`.

`M06_020_030_HA`

EN:

> It appears so.  They would need maybe... four Shield Emitters to generate one that large.

RU:

> Похоже на то. Им понадобится, возможно... четыре Щитовых Излучателя, чтобы создать такой большой.

Узел `Mission_M6#422`.

`M06_020_040_KS`

EN:

> I worked on that technology - something else they stole from us.  We won't get anywhere without taking down those shield emitters.

RU:

> Я работал над этой технологией, а они у нас украли еще кое-что. Мы никуда не доберемся, не уничтожив эти излучатели щитов.

Узел `Mission_M6#289`.

`M06_020_050_TS`

EN:

> Understood. Engineer Craft, prepare to deploy and find those Shield Emitters!

RU:

> Понял. Инженер Крафт, приготовьтесь развернуть и найти эти излучатели щита!

### M06_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=37, M06_Objective_01) #377`; `OnObjectiveCompleted (Objective=46, M06_Objective_01) #435`; `OnObjectiveCompleted (Objective=51, M06_Objective_01) #485`; `OnObjectiveCompleted (Objective=64, M06_Objective_01) #619`.

Узел `Mission_M6#38`.

`M06_030_010_FI`

EN:

> Shield Emitter located. Engineer Craft must dock to disable it.

RU:

> Обнаружен излучатель щита. Engineer Craft должен пристыковаться, чтобы отключить его.

### M06_040

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #489`.

Узел `Mission_M6#52`.

`M06_040_010_FI`

EN:

> Engineer Craft is disabling the Shield Emitter, but it is vulnerable to attack.

RU:

> Engineer Craft отключает излучатель щита, но он уязвим для атак.

### M06_050

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#96`.

`M06_050_010_FI`

EN:

> Shield Emitter disabled. Remaining Shield Emitters still active.

RU:

> Излучатель щита отключен. Остальные излучатели щита все еще активны.

### M06_060

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#56`.

`M06_060_010_FI`

EN:

> Shield Emitter disabled. Two remaining.

RU:

> Излучатель щита отключен. Осталось два.

Узел `Mission_M6#120`.

`M06_060_020_AR`

EN:

> This is your last opportunity to abide by your planet's standing agreement.  Your present actions make me fear that you are not listening.  But we can escalate our efforts to force you to surrender our assets.  The choice is yours.

RU:

> Это ваша последняя возможность соблюдать постоянное соглашение вашей планеты. Ваши нынешние действия заставляют меня опасаться, что вы не слушаете. Но мы можем активизировать наши усилия, чтобы заставить вас сдать наши активы. Выбор ваш.

Узел `Mission_M6#708`.

`M06_060_030_TS`

EN:

> Shut off the com channel and keep searching for those Shield Emitters.

RU:

> Отключите коммуникационный канал и продолжайте искать эти излучатели щита.

### M06_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#393`.

`M06_070_010_FI`

EN:

> Third Shield Emitter now disabled. Scan for the fourth.

RU:

> Третий излучатель щита теперь отключен. Сканируйте четвертый.

### M06_075

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #467`; `CustomEvent (name=WingB_Captured) #28`; `CustomEvent (name=WingC_Captured) #202`; `CustomEvent (name=WingD_Captured) #603`.

Узел `Mission_M6#62`.

`M06_075_010_FI`

EN:

> The last Shield Emitter has been disabled.

RU:

> Последний излучатель щита отключен.

Узел `Mission_M6#134`.

`M06_075_020_KS`

EN:

> Almost too easy.

RU:

> Почти слишком просто.

Узел `Mission_M6#576`.

`M06_075_030_TS`

EN:

> But now the Radaa Tower is wide open.  All ships, we have a new target.

RU:

> Но теперь Башня Рада широко открыта. Всем кораблям, у нас новая цель.

### M06_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #826`; `CustomEvent (name=TS_scream) #772`; `CustomEvent (name=winLevel) #110`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M6#690`.

`M06_080_010_FI`

EN:

> Unknown Radaa station has jumped in.

RU:

> Неизвестная станция Радаа подключилась.

Узел `Mission_M6#437`.

`M06_080_075_TS`

EN:

> --aaaaaaaaaaaauuughhh!!

RU:

> --ааааааааааа!!

Узел `Mission_M6#678`.

`M06_080_080_KS`

EN:

> Commander! Tyrra! What happened?

RU:

> Командир! Тирра! Что случилось?

Узел `Mission_M6#662`.

`M06_080_020_TS`

EN:

> It's massive. What is it?

RU:

> Это огромно. Что это такое?

Узел `Mission_M6#367`.

`M06_080_090_TS`

EN:

> Unclear... sensors... can't see... can't hear... attempting... attempting to...

RU:

> Неясно... датчики... не вижу... не слышу... пытаюсь... пытаюсь...

Узел `Mission_M6#652`.

`M06_080_030_FI`

EN:

> Analyzing.

RU:

> Анализируем.

Узел `Mission_M6#285`.

`M06_080_100_FI`

EN:

> Fleet incapacitated. Trying to reestablish contact.

RU:

> Флот выведен из строя. Пытаюсь восстановить контакт.

Узел `Mission_M6#523`.

`M06_080_040_TS`

EN:

> Weapon systems detected?

RU:

> Системы вооружения обнаружены?

Узел `Mission_M6#411`.

`M06_080_110_KS`

EN:

> Tyrra are you...?

RU:

> Тирра, ты...?

Узел `Mission_M6#229`.

`M06_080_043_KS`

EN:

> I don't like this. Spin up our core!

RU:

> Мне это не нравится. Раскрутите наше ядро!

Узел `Mission_M6#764`.

`M06_080_120_TS`

EN:

> Shaping coordinates for...  for jump to...  isolation point. They won't get this ship. Prepare... prepare...for...hy-

RU:

> Формирование координат для... перехода к... точке изоляции. Они не получат этот корабль. Готовься... готовься... к... х-

Узел `Mission_M6#267`.

`M06_080_045_TS`

EN:

> We've come this far, we can fight this. But prepping for jump in case your fear is warranted.

RU:

> Мы зашли так далеко, мы можем с этим бороться. Но готовьтесь к прыжку на случай, если ваш страх оправдан.

Узел `Mission_M6#130`.

`M06_080_130_FI`

EN:

> Emergency jump confirmed.

RU:

> Экстренный прыжок подтвержден.

Узел `Mission_M6#443`.

`M06_080_050_FI`

EN:

> Station appears to be powering up.

RU:

> Станция, кажется, включается.

Узел `Mission_M6#433`.

`M06_080_060_KS`

EN:

> They're targeting us!  We must hyperspace jump now!

RU:

> Они нацелены на нас! Мы должны совершить гиперпространственный прыжок прямо сейчас!

Узел `Mission_M6#554`.

`M06_080_070_TS`

EN:

> Analyzing weak points of Radaa Station. Targeting weapon...

RU:

> Анализ слабых мест станции Радаа. Прицельное оружие...

### M06_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #300`.

Узел `Mission_M6#426`.

`M06_100_010_FI`

EN:

> Resources depleted. Critical loss of Hiigaran ships. Full retreat unavoidable.

RU:

> Ресурсы исчерпаны. Критическая потеря хиигарских кораблей. Полное отступление неизбежно.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #784`; `CustomEvent #796`; `CustomEvent #806`; `OnSimReady #399`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M6#788`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M6#730`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M6#780`.

`FI_MothershipLost_07`

EN:

> Loss of structural integrity. Life support failing. Evacuate the Mothership at once.

RU:

> Потеря структурной целостности. Жизнеобеспечение не работает. Немедленно эвакуируйте корабль-носитель.

Узел `Mission_M6#451`.

`FI_UnlockAssaultFrigate`

EN:

> With the technology transferred from the Shipyard, we can build a new ship: Assault Frigates. These heavy weapon craft are ideal for penetrating the Radaa defenses guarding the shield emitters.

RU:

> Используя технологии, переданные с Верфи, мы сможем построить новый корабль: Штурмовые фрегаты. Эти корабли с тяжелым вооружением идеально подходят для прорыва обороны Радаа, охраняющей излучатели щитов.

## 7. M9: Система Тенхаузера / Tenhauser System

Определение `b1100962db5bfd04d93dc41a7563ff7c:1`, карта `level15`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Задачи, подключённые к графу

Узлы: 261, 567, 617.

`M09_Objective_00`

EN:

> Harvest RU for Mothership repairs.

RU:

> Соберите РУ для ремонта Mothership.

Узлы: 93, 459, 668.

`M09_Objective_01`

EN:

> Defend the Bentusi Exchange.

RU:

> Защитите биржу Бентуси.

Узлы: 171, 227, 241, 243, 257, 355, 415, 591.

`M09_Objective_02`

EN:

> Locate Radaa Hyperspace Gates.

RU:

> Найдите гиперпространственные врата Радаа.

Узлы: 30, 60, 75, 135, 221, 251, 273, 399, 514, 654.

`M09_Objective_02b`

EN:

> Locate the Radaa Shipyard.

RU:

> Найдите верфь Радаа.

Узлы: 71, 97, 179, 233, 373, 393, 425, 429, 433, 480, 504, 516, 684.

`M09_Objective_03`

EN:

> Destroy Radaa Hyperspace Gates.

RU:

> Уничтожьте гиперпространственные врата Радаа.

Узлы: 91, 553, unlinked_19b05fa8-b5a0-4787-9765-f49e408178a8.

`M09_Objective_Timer`

EN:

> Time until Bentusi warp out:

RU:

> Время до телепортации Бентуси:

### M09_005

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #83`.

Узел `Mission_M9_v2#89`.

`M09_005_010_KS`

EN:

> Life support calibrated. I am connected to all operant systems. Navigator embedded, I am... unbound.

RU:

> Система жизнеобеспечения откалибрована. Я подключен ко всем оперантным системам. Навигатор встроен, я... свободен.

Узел `Mission_M9_v2#435`.

`M09_005_020_FI`

EN:

> Repair progress at fifty percent. Additional resources needed to restore mothership to full functionality. Sensor systems at partial functionality.

RU:

> Прогресс ремонта на пятьдесят процентов. Дополнительные ресурсы необходимы для восстановления полной функциональности корабля-носителя. Сенсорные системы при частичной работоспособности.

Узел `Mission_M9_v2#506`.

`M09_005_030_KS`

EN:

> We used the last of our resources to save the ship.

RU:

> Мы использовали последние ресурсы, чтобы спасти корабль.

Узел `Mission_M9_v2#133`.

`M09_005_050_KS`

EN:

> I am detecting massive damage to structural integrity and internal systems. Construction facilities down.

RU:

> Я обнаруживаю массивные повреждения структурной целостности и внутренних систем. Строительные объекты вниз.

Узел `Mission_M9_v2#409`.

`M09_005_060_FI`

EN:

> Repair looks impossible without key components we do not have in our reserves.

RU:

> Ремонт выглядит невозможным без ключевых компонентов, которых у нас нет в наличии.

Узел `Mission_M9_v2#421`.

`M09_005_070_KS`

EN:

> Damage control. Cannibalize what you can, invent what you can't. I won't let this be hopeless. Tyrra, your sacrifice will have meaning.

RU:

> Ремонтно-восстановительные работы. Каннибализируйте то, что можете, изобретайте то, что не можете. Я не позволю этому быть безнадежным. Тирра, твоя жертва будет иметь смысл.

Узел `Mission_M9_v2#315`.

`M09_005_080_FI`

EN:

> Sensors detecting powerful anomalous signature. Can't lock it down. Also picking up potential Radaa ships on incoming vectors.

RU:

> Датчики обнаруживают мощную аномальную сигнатуру. Не могу запереть. Также выявляем потенциальные корабли Радаа на приближающихся направлениях.

Узел `Mission_M9_v2#589`.

`M09_005_090_KS`

EN:

> We have to get sensors back, at least.  We need those resources.

RU:

> По крайней мере, нам нужно вернуть датчики. Нам нужны эти ресурсы.

### M09_008

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

Узел `Mission_M9_v2#249`.

`M09_008_010_KS`

EN:

> Sensors back online. This is what I remember.

RU:

> Датчики снова в сети. Это то, что я помню.

Узел `Mission_M9_v2#664`.

`M09_008_020_FI`

EN:

> We have intercepted communication from Admiral Giitan.

RU:

> Мы перехватили сообщение адмирала Гитана.

Узел `Mission_M9_v2#48`.

`M09_008_030_GR`

EN:

> They can't hide from us, they can't fight us, Shatter Station hit its target. Bring me what's left of the Mothership! Bring me that Progenitor Core.

RU:

> Им не спрятаться от нас, им не сразиться с нами, Станция Разрушения поразила цель. Принесите мне то, что осталось от Корабля-матери! Принеси мне это Ядро Прародителя.

Узел `Mission_M9_v2#666`.

`M09_008_040_KS`

EN:

> Shatter Station. That's what left us broken. We're not ready to fight.

RU:

> Станция Разрушения. Вот что оставило нас сломленными. Мы не готовы драться.

Узел `Mission_M9_v2#331`.

`M09_008_050_FI`

EN:

> Signatures appearing now...

RU:

> Подписи появляются сейчас...

### M09_020

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

Узел `Mission_M9_v2#219`.

`M09_020_005_BN`

EN:

> We remember you, Karan S'jet, Seeker of The Home. You are now again what you will be. Unbound. And we welcome you to your place.

RU:

> Мы помним тебя, Каран С'джет, Искатель Дома. Теперь ты снова тот, кем будешь. Несвязанный. И мы приветствуем вас у вас.

Узел `Mission_M9_v2#267`.

`M09_020_010_KS`

EN:

> Thank you. But why are you here, now? At this point in spacetime?

RU:

> Спасибо. Но почему ты сейчас здесь? В этой точке пространства-времени?

Узел `Mission_M9_v2#229`.

`M09_020_020_BN`

EN:

> Hiigarans are worthy of our help. The Radaa are not.

RU:

> Хиигаранцы достойны нашей помощи. Рада – нет.

Узел `Mission_M9_v2#656`.

`M09_020_030_KS`

EN:

> You know of them?

RU:

> Вы знаете о них?

Узел `Mission_M9_v2#69`.

`M09_020_040_BN`

EN:

> We shape the galaxy on honorable exchange and the sharings of Knowledge. The Radaa trade flawed systems that prove useless in order to take what they desire. Thieves. Agents of Entropy.

RU:

> Мы формируем галактику на основе честного обмена и обмена Знаниями. Рада торгует порочными системами, которые оказываются бесполезными, чтобы получить то, что они желают. Воры. Агенты энтропии.

Узел `Mission_M9_v2#549`.

`M09_020_050_KS`

EN:

> Have you faced their weapon that can disable a fleet in one blast?  They call it Shatter Station.

RU:

> Вы сталкивались с их оружием, способным вывести из строя целый флот одним выстрелом? Они называют это Станцией Разрушения.

Узел `Mission_M9_v2#587`.

`M09_020_060_BN`

EN:

> We are aware, and that is why we came Karan S'jet.  First, we have the technology to heal you.  Initiating transfer.

RU:

> Мы в курсе, и именно поэтому мы пришли Каран С'жет. Во-первых, у нас есть технология, которая может вас исцелить. Инициируем передачу.

Узел `Mission_M9_v2#498`.

`M09_020_070_KS`

EN:

> Bentusi technology received. Construction bays are online and fully functional.

RU:

> Технология Бентуси получена. Строительные отсеки подключены к сети и полностью функциональны.

Узел `Mission_M9_v2#117`.

`M09_020_080_BN`

EN:

> We can hear the whispers of the technology the Radaa have stolen from us--

RU:

> Мы слышим слухи о технологиях, которые Рада украла у нас...

### M09_030

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

Узел `Mission_M9_v2#153`.

`M09_030_010_BN`

EN:

> The Radaa have come for you.

RU:

> Рада пришла за вами.

Узел `Mission_M9_v2#437`.

`M09_030_020_KS`

EN:

> They must have followed our core signature.

RU:

> Должно быть, они следовали нашей основной подписи.

Узел `Mission_M9_v2#54`.

`M09_030_030_BN`

EN:

> We are not willing to fight the stolen parts of Ourselves. The Radaa have made a wall in our sector by placing multiple hyperspace gates.

RU:

> Мы не готовы сражаться с украденными частями Нас самих. Рада воздвигла стену в нашем секторе, установив несколько гиперпространственных врат.

Узел `Mission_M9_v2#457`.

`M09_030_040_KS`

EN:

> All systems back online, we are prepared to fight. Then we hope you can tell us about their technology.

RU:

> Все системы снова в сети, мы готовы сражаться. Тогда мы надеемся, что вы расскажете нам об их технологии.

### M09_040

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

Узел `Mission_M9_v2#44`.

`M09_040_010_FI`

EN:

> Hyperspace gate destroyed. Locate remaining gates.

RU:

> Гиперпространственные врата уничтожены. Найдите оставшиеся ворота.

### M09_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

Узел `Mission_M9_v2#563`.

`M09_050_010_FI`

EN:

> Hyperspace gate eliminated. More gates remain.

RU:

> Гиперпространственные врата устранены. Осталось еще больше ворот.

### M09_060

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M9_v2#343`.

`M09_060_010_FI`

EN:

> Gate destruction confirmed. Scanning for more gates.

RU:

> Разрушение ворот подтверждено. Ищем больше ворот.

### M09_070

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True) #167`; `OnWaveDestroyed (Enabled=True) #349`; `OnWaveDestroyed (Enabled=True) #405`; `OnWaveDestroyed (Enabled=True) #482`; `OnWaveDestroyed (Enabled=True) #755`.

Узел `Mission_M9_v2#629`.

`M09_070_010_FI`

EN:

> Hyperspace gates neutralized. Sector clear.

RU:

> Гиперпространственные врата нейтрализованы. Сектор свободен.

### M09_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=winLevel) #585`.

Узел `Mission_M9_v2#337`.

`M09_080_010_BN`

EN:

> You kept your word, Karan S'jet of Hiigara.  What we understand of the devastating Radaa weapon we can share with you.

RU:

> Ты сдержал свое слово, Каран С'джет из Хиигары. Мы можем поделиться с вами тем, что мы знаем о разрушительном оружии Рады.

Узел `Mission_M9_v2#571`.

`M09_080_015_BN`

EN:

> It operates off a rare mineral found in the Outer Reef. You can also use this mineral to protect against it. We can provide specific details.

RU:

*Нет строки в извлечённой таблице этой версии.*

Узел `Mission_M9_v2#109`.

`M09_080_020_KS`

EN:

> Chief Engineer Hauk, prepare to receive data from the Bentusi.

RU:

> Главный инженер Хаук, приготовьтесь получить данные от «Бентузи».

Узел `Mission_M9_v2#163`.

`M09_080_030_BN`

EN:

> We do not wish to hear the Radaa again. The Galaxy will not be less for the loss of their Song. Use our knowledge to ensure it is silenced. Farewell.

RU:

> Мы не хотим снова слышать Раду. Галактика не станет меньше из-за потери их Песни. Используйте наши знания, чтобы заставить его замолчать. Прощание.

### M09_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=NormalLossEvent) #145`; `CustomEvent (name=NormalLossEvent) #658`.

Узел `Mission_M9_v2#253`.

`M09_090_010_FI`

EN:

> Too many ships destroyed, resource stores depleted. Retreat underway.  

RU:

> Слишком много кораблей уничтожено, запасы ресурсов истощены. Отступление идет.

### M09_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #443`.

Узел `Mission_M9_v2#291`.

`M09_100_010_FI`

EN:

> Bentusi ship taking substantial damage. We need to defend it.

RU:

> Корабль Бентуси получил значительные повреждения. Нам нужно защитить его.

### M09_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #147`.

Узел `Mission_M9_v2#490`.

`M09_110_010_FI`

EN:

> Bentusi ship will not be able to withstand attack for much longer.

RU:

> Корабль Бентуси не сможет долго противостоять атаке.

### M09_120

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=OutpostLossEvent) #525`.

Узел `Mission_M9_v2#155`.

`M09_120_010_FI`

EN:

> Bentusi ship critically damaged, hull integrity lost, repeat the Bentusi are lost.

RU:

> Корабль Бентуси критически поврежден, целостность корпуса потеряна, повторяю: Бентуси потеряны.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #36`; `CustomEvent #728`; `CustomEvent #757`; `OnObjectiveCompleted (Objective=71, M09_Objective_00) #567`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M9_v2#759`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M9_v2#771`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M9_v2#518`.

`FI_MothershipLost_05`

EN:

> Catastrophic damage to Mothership. All hands to the escape pods.

RU:

> Катастрофический ущерб Mothership. Все к спасательным капсулам.

Узел `Mission_M9_v2#211`.

`FI_UnlockBarricadeFrigate`

EN:

> With the technology the Bentusi provided, our construction bays can now build Barricade Frigates. When activated, these can provide shields for nearby ships. They can also be used to protect the Bentusi.

RU:

> Благодаря технологиям, предоставленным Бентуси, наши строительные отсеки теперь могут строить фрегаты-баррикады. При активации они могут обеспечить щиты для ближайших кораблей. Их также можно использовать для защиты Бентуси.

## 8. M10: Горнодобывающий комплекс на внешнем рифе / Outer Reef Mining Facility

Определение `5cd7702c05ff025469152b598cb0fda8:1`, карта `level17`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M10 - The Final Push/M10_Animatic_Intro/M10_Animatic_Intro.unity`

*Клип начинается в 0.72 с.*

`M10_010_010_A_KS`

EN:

> Fleet Command online. Assessing all systems.

RU:

> Командование флотом онлайн. Оценка всех систем.

*Клип начинается в 4.47 с.*

`M10_010_020_A_HA`

EN:

> The Bentusi’s information about the Radaa technology… this is exactly what we need to bring them down, just like they brought down our fleet… and my mother.

RU:

> Информация Бентуси о технологии Радаа… это именно то, что нам нужно, чтобы уничтожить их, точно так же, как они сбили наш флот… и мою мать.

*Клип начинается в 13.77 с.*

`M10_010_030_A_KS`

EN:

> Hauk.... Tyrra is the only reason we are still here to continue the fight...she sacrificed everything to save us... To save you.

RU:

> Хаук... Тирра - единственная причина, по которой мы все еще здесь, чтобы продолжать борьбу... она пожертвовала всем, чтобы спасти нас... Чтобы спасти тебя.

*Клип начинается в 24.19 с.*

`M10_010_033_A_HA`

EN:

> I know. She was better at tactics than she was as a mother, but she will walk with me always.

RU:

> Я знаю. Она была лучше в тактике, чем в роли матери, но она всегда будет идти со мной.

*Клип начинается в 31.03 с.*

`M10_010_035_A_KS`

EN:

> Akadeth Ferin.

RU:

> Акадет Ферин.

*Клип начинается в 32.57 с.*

`M10_010_037_A_HA`

EN:

> Akadeth Ferin.

RU:

> Акадет Ферин.

*Клип начинается в 35.58 с.*

`M10_010_040_A_HA`

EN:

> The Bentusi data shows a device we could construct to counter the Shatter Station weapon but we will need a substantial amount of a rare conductive silicon.

RU:

> Данные Бентуси показывают, что мы могли бы создать устройство для противодействия оружию Станции Разрушения, но нам понадобится значительное количество редкого проводящего кремния.

*Клип начинается в 43.38 с.*

`M10_010_050_A_FI`

EN:

> We have identified a supply in an old mining operation located at an outer reef asteroid field. Coordinates confirmed. There may be hostiles in the vicinity.

RU:

> Мы обнаружили запас на старом горнодобывающем предприятии, расположенном на внешнем рифовом астероидном поле. Координаты подтверждены. Поблизости могут быть враги.

*Клип начинается в 54.10 с.*

`M10_010_060_A_KS`

EN:

> Tyrra would not hesitate, and we will not waste this chance. Prepare for Hyperspace jump, on my command. And we will let them know that we are still brave.

RU:

> Тирра не станет колебаться, и мы не упустим этот шанс. Приготовьтесь к гиперпространственному прыжку по моей команде. И мы дадим им понять, что мы все еще храбры.

### Задачи, подключённые к графу

Узлы: 126, 179, 240, 295, 655, 746, 770.

`M10_Objective_01`

EN:

> Dock 3 Engineer Craft to the Mining Platform.

RU:

> Пристыковайте корабль инженера 3 к горнодобывающей платформе.

Узлы: 140, 144, 185, 557, 563, 809.

`M10_Objective_03`

EN:

> Dock 3 Engineer Craft to the Mining Platform.

RU:

> Пристыковайте корабль инженера 3 к горнодобывающей платформе.

Узлы: 299, 665.

`M10_Objective_05`

EN:

> Destroy enemy patrol protecting the final Mining Platform.

RU:

> Уничтожьте вражеский патруль, защищающий последнюю горнодобывающую платформу.

Узлы: 26, 68, 88, 102, 122, 321, 347, 707, 715.

`M10_Objective_07`

EN:

> Defend Mining Platform while Engineer Craft salvage Resonant Silicon.

RU:

> Защитите горнодобывающую платформу, пока инженер занимается сбором резонансного кремния.

### M10_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #114`.

Узел `Mission_M10#313`.

`M10_020_010_KS`

EN:

> Hyperspace jump successful. Scan for the silicon material.

RU:

> Гиперпространственный прыжок успешен. Сканируйте кремниевый материал.

Узел `Mission_M10#146`.

`M10_020_020_HA`

EN:

> I'm seeing multiple asteroid fields. There are several abandoned mining platforms that were placed to extract the silicon.

RU:

> Я вижу несколько полей астероидов. Есть несколько заброшенных горнодобывающих платформ, которые были размещены для добычи кремния.

Узел `Mission_M10#729`.

`M10_020_030_KS`

EN:

> Has the material been exhausted?

RU:

> Материал исчерпан?

Узел `Mission_M10#437`.

`M10_020_040_FI`

EN:

> Detecting Radaa strike craft around the Platforms and throughout this sector.

RU:

> Обнаружение ударных кораблей Радаа вокруг Платформ и во всем этом секторе.

Узел `Mission_M10#28`.

`M10_020_050_KS`

EN:

> Clearly not exhausted. And if the Radaa want it, we cannot let them have it. Calling up Strike Groups.

RU:

> Явно не исчерпан. И если Рада этого хочет, мы не можем позволить им это получить. Вызов ударных групп.

Узел `Mission_M10#512`.

`M10_020_060_FI`

EN:

> Radaa forces moving to secure the Mining Platforms.

RU:

> Силы Рада выдвигаются для обеспечения безопасности горнодобывающих платформ.

Узел `Mission_M10#619`.

`M10_020_070_HA`

EN:

> We need all the resonant silicon we can get our hands on.  Engineer Craft can recover the mineral from the platforms.  But they will need protection.   

RU:

> Нам нужен весь резонансный кремний, который мы сможем получить. Инженер Ремесло может добывать минерал с платформ. Но им понадобится защита.

Узел `Mission_M10#762`.

`M10_020_080_KS`

EN:

> So we will eliminate the Radaa and take the platforms, one by one.

RU:

> Итак, мы ликвидируем Раду и захватим платформы одну за другой.

### M10_030

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #215`; `CustomEvent #415`; `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M10#839`.

`M10_030_010_FI`

EN:

> First mining platform secured.  Engineer Craft mineral recovery well under way.

RU:

> Первая горнодобывающая платформа закреплена. Инженерное ремесло добыча полезных ископаемых идет полным ходом.

Узел `Mission_M10#277`.

`M10_030_020_KS`

EN:

> Now to the next platform.

RU:

> Теперь переходим к следующей платформе.

### M10_040

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #215`; `CustomEvent #415`; `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`; `OnObjectiveCompleted (Objective=8, M10_Objective_07) #102`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M10#670`.

`M10_040_010_FI`

EN:

> Next mining platform secured, silicon recovery has commenced. 

RU:

> Следующая майнинговая платформа обеспечена, началась добыча кремния.

Узел `Mission_M10#585`.

`M10_040_020_FI`

EN:

> There is a third platform, much more heavily guarded. Engaging it would be highly dangerous.

RU:

> Есть и третья платформа, гораздо более тщательно охраняемая. Вступать в бой с ним было бы очень опасно.

Узел `Mission_M10#175`.

`M10_040_030_KS`

EN:

> We need that silicon.  With the right Strike Groups, we can take them.

RU:

> Нам нужен этот кремний. Имея подходящие ударные группы, мы сможем их победить.

### M10_050

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`; `OnObjectiveCompleted (Objective=8, M10_Objective_07) #102`; `OnWaveDestroyed (Enabled=True) #448`.

Узел `Mission_M10#559`.

`M10_050_010_FI`

EN:

> Radaa forces around the last mining platform have been eliminated.  

RU:

> Силы Рада вокруг последней горнодобывающей платформы уничтожены.

### M10_060

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=10, M10_Objective_07) #122`; `OnObjectiveCompleted (Objective=8, M10_Objective_07) #102`; `OnWaveDestroyed (Enabled=True) #448`.

Узел `Mission_M10#279`.

`M10_060_010_FI`

EN:

> Contact! A Radaa Battlecruiser has jumped in. It has enough firepower to cripple our fleet.

RU:

> Контакт! Вмешался линейный крейсер Радаа. У него достаточно огневой мощи, чтобы нанести вред нашему флоту.

Узел `Mission_M10#611`.

`M10_060_020_KS`

EN:

> We can use the Mining Platform as a battering ram. Tyrra would like that.

RU:

> Мы можем использовать Горнодобывающую платформу как таран. Тирре бы этого хотелось.

Узел `Mission_M10#464`.

`M10_060_030_FI`

EN:

> Multiple Engineer Craft are needed to steer it into the Battlecruiser.

RU:

> Чтобы направить его в линейный крейсер, необходимо несколько инженерных кораблей.

### M10_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #446`.

Узел `Mission_M10#721`.

`M10_070_010_KS`

EN:

> The Engineer Craft are locked in.  

RU:

> Инженерный корабль заблокирован.

Узел `Mission_M10#678`.

`M10_070_020_FI`

EN:

> Mining platform is on course to collide with the Battlecruiser.

RU:

> Горнодобывающая платформа вот-вот столкнётся с линейным крейсером.

### M10_080

Обработчики, достигающие этих реплик по control-связям: `OnCheatEvent2 #369`; `OnDetectShip #567`.

Узел `Mission_M10#782`.

`M10_080_010_KS`

EN:

> We have impact!  

RU:

> У нас есть влияние!

Узел `Mission_M10#647`.

`M10_080_020_FI`

EN:

> Battlecruiser eliminated. Radaa forces are in retreat.

RU:

> Линейный крейсер ликвидирован. Силы Рады отступают.

### M10_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #565`; `CustomEvent #631`; `CustomEvent #727`; `CustomEvent (name=LossEvent) #530`; `OnCheatEvent3 #494`.

Узел `Mission_M10#389`.

`M10_100_010_FI`

EN:

> Critical ship loss, resources depleted. Fleet in full retreat.

RU:

> Критическая потеря корабля, ресурсы истощены. Флот в полном отступлении.

### M10_110

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=4, Objective_M10_00) #72`.

Узел `Mission_M10#60`.

`M10_110_010_FI`

EN:

> Radaa forces around this mining platform are in tight formation, which will block any attempt at docking.  Recommend securing the other platforms.  

RU:

> Силы Рада вокруг этой горнодобывающей платформы выстроены в плотный строй, который блокирует любую попытку стыковки. Рекомендую защитить другие платформы.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #46`; `CustomEvent #835`; `CustomEvent #852`; `OnSimReady #114`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M10#854`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M10#858`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M10#90`.

`FI_MothershipLost_06`

EN:

> All systems critically compromised. Abandon the Mothership.

RU:

> Все системы критически скомпрометированы. Покиньте материнский корабль.

Узел `Mission_M10#80`.

`FI_UnlockIonFrigate`

EN:

> The Bentusi also provided us the key components necessary to build a new ship class: Ion Frigates, which are ideal for long range attacks and cutting into the hulls of larger ships.

RU:

> «Бентузи» также предоставил нам ключевые компоненты, необходимые для создания нового класса кораблей: ионных фрегатов, которые идеально подходят для атак на большие расстояния и проникновения в корпуса более крупных кораблей.

## 9. M11: Архитекторы оружия / The Weapon Architects

Определение `653d9688338bfb943b561c979612218e:1`, карта `level19`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M11 - Intelligence/M11_Animatic_Intro/M11_Animatic_Intro.unity`

*Клип начинается в 0.65 с.*

`M11_010_010_A_FI`

EN:

> Our resource teams have extracted the resonant silicon from the mining platforms.

RU:

> Наши ресурсные группы извлекли резонансный кремний из горнодобывающих платформ.

*Клип начинается в 5.62 с.*

`M11_010_020_A_HA`

EN:

> Silicon yield from the platforms is higher than I expected, even without the third platform.  My team is commencing analysis.

RU:

> Выход кремния с платформ выше, чем я ожидал, даже без третьей платформы. Моя команда начинает анализ.

*Клип начинается в 13.83 с.*

`M11_010_030_A_KS`

EN:

> I've had a moment to review the Bentusi data, silicon alone will not be enough to counter their weapon.  What's your plan, Hauk?

RU:

> У меня была возможность просмотреть данные Бентуси: одного кремния будет недостаточно, чтобы противостоять их оружию. Какой у тебя план, Хаук?

*Клип начинается в 21.05 с.*

`M11_010_040_A_HA`

EN:

> We have a lot to work with, but without a Radaan weapons engineer to consult, we will need more time.

RU:

> Нам предстоит много работы, но без консультации с инженером-оружейником Радаана нам понадобится больше времени.

*Клип начинается в 25.62 с.*

`M11_010_050_A_KS`

EN:

> Time is the one thing we don't have. Intel, find us a consultant...fast.

RU:

> Время – это единственное, чего у нас нет. Интел, найди нам консультанта... быстро.

*Клип начинается в 30.72 с.*

`M11_010_060_A_FI`

EN:

> Accessing recon reports... cross referencing personnel codes from when the Radaa were consulting with Hiigaran Command... found it.  Radaa weapons architects identified on a Destroyer in the Hiigara System, Quadrant Omega.

RU:

> Получив доступ к отчетам разведки... перекрестные ссылки на коды личного состава, полученные во время консультаций Рады с хиигаранским командованием... нашли это. Разработчики оружия Радаа идентифицировали разрушитель в системе Хиигара, квадрант Омега.

*Клип начинается в 46.63 с.*

`M11_010_070_A_FI`

EN:

> Exact position and ship ID is unclear.

RU:

> Точное местоположение и идентификатор корабля неясны.

*Клип начинается в 49.48 с.*

`M11_010_080_A_KS`

EN:

> Won't be my first hunt for a dune snake, Intel.  Let's get close.

RU:

> Это не первая моя охота на дюнную змею, Интел. Давайте подойдем поближе.

*Клип начинается в 53.34 с.*

`M11_010_090_A_FI`

EN:

> Sending coordinates.

RU:

> Отправка координат.

*Клип начинается в 54.92 с.*

`M11_010_100_A_KS`

EN:

> Received.  Prepare for hyperspace on my mark.  Mark!

RU:

> Полученный. Приготовьтесь к гиперпространству по моему знаку. Отметка!

### Задачи, подключённые к графу

Узлы: 143, 287, 401.

`M11_Objective_01`

EN:

> Locate the ship containing the weapon architects.

RU:

> Найдите корабль, на котором находятся создатели оружия.

Узлы: 107, 135, 199, 367, 523, 575.

`M11_Objective_02`

EN:

> Destroy the Hyperspace Gate.

RU:

> Уничтожьте Гиперпространственные врата.

Узлы: 78, 299, 419.

`M11_Objective_03`

EN:

> Defend the Mothership until the Personnel Craft arrives.

RU:

> Защищайте материнский корабль, пока не прибудет кадровый корабль.

Узлы: 413, 453, 471.

`M11_Objective_03a`

EN:

> Dock 3 Engineer Craft to the Radaa Destroyer.

RU:

> Док 3 Инженерного корабля к разрушителю Радаа.

Узлы: 55, 309.

`M11_Objective_03b`

EN:

> Escort the Personnel Craft back to the Mothership.

RU:

> Сопроводите корабль персонала обратно на корабль-носитель.

### M11_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #497`.

Узел `Mission_M11#35`.

`M11_020_010_KS`

EN:

> Hyperspace jump successful. Confirm location of the ship holding the weapons architects.

RU:

> Гиперпространственный прыжок успешен. Подтвердите местонахождение корабля, на котором находятся разработчики оружия.

Узел `Mission_M11#123`.

`M11_020_020_FI`

EN:

> Unfortunately Commander, not possible. We were led to believe there was a single Radaa Destroyer, but we have detected three in this sector.

RU:

> К сожалению, командир, это невозможно. Нас заставили поверить, что существует один Разрушитель Радаа, но мы обнаружили в этом секторе три.

Узел `Mission_M11#343`.

`M11_020_030_FI`

EN:

> Recommend investigating each coordinate to scan for our target.

RU:

> Рекомендую исследовать каждую координату, чтобы найти нашу цель.

### M11_030

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #569`.

Узел `Mission_M11#191`.

`M11_030_010_FI`

EN:

> Scan reads negative. Targets not on board this ship. Proceed to next coordinate.

RU:

> Скан показывает отрицательный результат. Цели не на борту этого корабля. Перейдите к следующей координате.

### M11_040

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #43`.

Узел `Mission_M11#455`.

`M11_040_010_FI`

EN:

> Negative. Weapon architect designation not detected on this Destroyer. Continue the search.  

RU:

> Отрицательный. Обозначение разработчика оружия на этом эсминце не обнаружено. Продолжайте поиск.

### M11_050

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #535`.

Узел `Mission_M11#361`.

`M11_050_010_FI`

EN:

> Personnel scan confirms - the architects are passengers on this Destroyer.  

RU:

> Сканирование персонала подтверждает — архитекторы являются пассажирами этого Разрушителя.

Узел `Mission_M11#101`.

`M11_050_020_FI`

EN:

> Priority alert! The Destroyer has detected our presence and is fleeing to the nearest hyperspace gate.

RU:

> Приоритетное предупреждение! Разрушитель обнаружил наше присутствие и бежит к ближайшим вратам гиперпространства.

Узел `Mission_M11#203`.

`M11_050_030_KS`

EN:

> All ships! Destroy that gate before the Radaa use it to escape.

RU:

> Все корабли! Уничтожьте эти ворота, прежде чем Рада воспользуется ими, чтобы сбежать.

### M11_060

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=objective_2start) #525`.

Узел `Mission_M11#109`.

`M11_060_010_FI`

EN:

> Enemy units entering the system to defend the Destroyers.

RU:

> Вражеские подразделения входят в систему для защиты Разрушителей.

### M11_070

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=16, M11_Objective_02) #199`.

Узел `Mission_M11#479`.

`M11_070_010_FI`

EN:

> Hyperspace gate destroyed.

RU:

> Гиперпространственные врата уничтожены.

Узел `Mission_M11#543`.

`M11_070_020_KS`

EN:

> We've taken away their escape route.  Capture the Destroyer, and secure the personnel we came for.

RU:

> Мы лишили их пути отхода. Захватите Разрушитель и обеспечьте безопасность персонала, за которым мы пришли.

Узел `Mission_M11#183`.

`M11_070_030_FI`

EN:

> Engineer Craft are needed to latch on to the Destroyer and haul it back to the Mothership.

RU:

> Инженерные корабли необходимы, чтобы зацепиться за Разрушитель и доставить его обратно на материнский корабль.

### M11_080

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #397`.

Узел `Mission_M11#459`.

`M11_080_010_FI`

EN:

> Destroyer under tow. Warning, additional Radaa craft detected.

RU:

> Эсминец на буксире. Внимание, обнаружен еще один корабль Радаа.

Узел `Mission_M11#429`.

`M11_080_020_KS`

EN:

> They may want to eliminate the Destroyer before we complete the transfer. All ships, move to defend.

RU:

> Возможно, они захотят уничтожить Разрушителя до того, как мы завершим передачу. Все корабли, идите на защиту.

### M11_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #509`.

Узел `Mission_M11#441`.

`M11_090_010_FI`

EN:

> Heavy Radaa forces are jumping in and are now targeting the Mothership.

RU:

> Тяжелые силы Радаа вторгаются и теперь нацелены на Корабль-носитель.

Узел `Mission_M11#113`.

`M11_090_020_KS`

EN:

> We'll have to eliminate the Radaa to get the weapons architects onto the Mothership.

RU:

> Нам придется ликвидировать Раду, чтобы доставить разработчиков оружия на Материнский корабль.

### M11_100

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #527`.

Узел `Mission_M11#45`.

`M11_100_010_FI`

EN:

> Destroyer is in range of the Mothership.  Radaa threats are eliminated.

RU:

> Разрушитель находится в пределах досягаемости Материнского корабля. Угрозы Рады устранены.

Узел `Mission_M11#503`.

`M11_100_020_KS`

EN:

> Architects secured. Hyperspace jump on my mark.

RU:

> Архитекторы обеспечены. Гиперпространственный прыжок по моей цели.

### M11_150

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #37`.

Узел `Mission_M11#437`.

`M11_150_010_FI`

EN:

> Resources depleted. Ships destroyed. The Destroyer has evaded capture.

RU:

> Ресурсы исчерпаны. Корабли уничтожены. Разрушителю удалось избежать захвата.

### M11_160

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #583`.

Узел `Mission_M11#573`.

`M11_160_010_FI`

EN:

> Regroup! Targeted Destroyer has escaped through the Hyperspace Gate. Repeat: The Destroyer has escaped.

RU:

> Перегруппируйтесь! Целевой Разрушитель сбежал через Гиперпространственные Врата. Повторите: Разрушитель сбежал.

### M11_170

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #583`.

Узел `Mission_M11#593`.

`M11_170_010_FI`

EN:

> Destroyer with the Weapon Architects has been destroyed.  Our target is lost.  

RU:

> Разрушитель с Архитекторами оружия уничтожен. Наша цель потеряна.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #255`; `CustomEvent #273`; `CustomEvent #373`; `OnSimReady #497`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M11#241`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M11#239`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M11#545`.

`FI_MothershipLost_08`

EN:

> Complete systems failure. Mothership crew must abandon ship.

RU:

> Полный сбой системы. Экипаж материнского корабля должен покинуть корабль.

Узел `Mission_M11#72`.

`FI_UnlockDestroyer`

EN:

> Our ship construction capabilities have been upgraded to build a new ship: Destroyers. These capital class ships have weapon systems most effective against squadrons of strike craft.

RU:

> Наши возможности по строительству кораблей были улучшены для постройки нового корабля: Разрушителей. Эти корабли капитального класса имеют системы вооружения, наиболее эффективные против эскадрилий ударных кораблей.

## 10. M8: Гиббасское наступление / The Gybbas Offensive

Определение `a5358fed0221c06459236bb5e555ec41:1`, карта `level13`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M8 - Supply Lines/M8_Animatic_Intro/M8_Animatic_Intro.unity`

*Клип начинается в 0.93 с.*

`M08_010_010_A_KS`

EN:

> Weapons Architects secured. Mothership operational. Engineering, are we ready to face Shatter Station?

RU:

> Архитекторы оружия обеспечены. Материнский корабль в рабочем состоянии. Инженерное дело, мы готовы встретиться со Станцией Разрушения?

*Клип начинается в 8.30 с.*

`M08_010_030_A_HA`

EN:

> That makes no sense!  Explain again, slime-merchant, or so help me...

RU:

> Это бессмысленно! Объясни еще раз, торговец слизью, или так помоги мне...

*Клип начинается в 11.85 с.*

`M08_010_040_A_KS`

EN:

> Officer Hauk!

RU:

> Офицер Хаук!

*Клип начинается в 12.74 с.*

`M08_010_050_A_HA`

EN:

> Sorry...Command, we're running simulations, but our guest is not being as helpful as I had hoped. We need more time. I won't send you in without knowing I can protect you. I won't lose you too.

RU:

> Извините... Командование, мы запускаем симуляцию, но наш гость оказался не таким полезным, как я надеялся. Нам нужно больше времени. Я не отправлю тебя сюда, не зная, что смогу защитить тебя. Я не потеряю и тебя.

*Клип начинается в 25.55 с.*

`M08_010_060_A_KS`

EN:

> I'm sorry. It should have been me.

RU:

> Мне жаль. Это должен был быть я.

*Клип начинается в 31.33 с.*

`M08_010_070_A_FI`

EN:

> Reports show that the Radaa have returned to the Orbital Shipyards around Gybbas. They are building up a massive fleet.

RU:

> Отчеты показывают, что Рада вернулась на орбитальные верфи вокруг Гиббаса. Они создают огромный флот.

*Клип начинается в 38.08 с.*

`M08_010_080_A_KS`

EN:

> If we don't break up that fleet it won't matter if we stop Shatter Station.

RU:

> Если мы не разобьем этот флот, то не будет иметь значения, остановим ли мы Станцию ​​Раскола.

*Клип начинается в 41.87 с.*

`M08_010_090_A_FI`

EN:

> Our intelligence on the sector is excellent, and we now have the firepower to destroy that Shipyard if we can get close enough.

RU:

> Наша разведка в этом секторе превосходна, и теперь у нас есть огневая мощь, чтобы уничтожить эту верфь, если мы сможем подобраться достаточно близко.

*Клип начинается в 48.75 с.*

`M08_010_100_A_KS`

EN:

> Then that is the solution. Chief Engineer Hauk, you will get your time. We will pick up where you left off, Tyrra.

RU:

> Тогда это решение. Главный инженер Хаук, вы получите свое время. Мы продолжим с того места, на котором ты остановилась, Тирра.

### Задачи, подключённые к графу

Узлы: 256, 677.

`M08_Objective_01`

EN:

> Destroy a Radaa Shipyard.

RU:

> Уничтожьте верфь Радаа.

Узлы: 102, 661.

`M08_Objective_02`

EN:

> Destroy a second Radaa Shipyard.

RU:

> Уничтожьте вторую верфь Радаа.

Узлы: 154, 172, 176, 268, 653.

`M08_Objective_03`

EN:

> Destroy the final Radaa Shipyard.

RU:

> Уничтожьте последнюю верфь Радаа.

### M08_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #434`.

Узел `Mission_M8#346`.

`M08_020_010_KS`

EN:

> Hyperspace Jump successful. Gybbas orbit achieved.

RU:

> Гиперпространственный прыжок успешен. Орбита Гиббаса достигнута.

Узел `Mission_M8#110`.

`M08_020_020_FI`

EN:

> Picking up a massive Radaa defense fleet. Our capital ships will need a clear attack path to destroy the Shipyard.

RU:

> Собираем огромный оборонительный флот Радаа. Нашим крупным кораблям понадобится свободный путь атаки, чтобы уничтожить Верфь.

Узел `Mission_M8#186`.

`M08_020_030_KS`

EN:

> The Radaa were clearly preparing for another attack from Tyrra. We will not disappoint.

RU:

> Рада явно готовилась к новой атаке Тирры. Мы не разочаруем.

### M08_030

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardA) #330`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardB) #560`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardC) #284`.

Узел `Mission_M8#158`.

`M08_030_010_FI`

EN:

> Radaa Shipyard has been destroyed.  Fleet objectives met.

RU:

> Верфь Радаа разрушена. Цели флота достигнуты.

Узел `Mission_M8#336`.

`M08_030_020_KS`

EN:

> Tyrra would not stop here.  Do we have sufficient resources to take the second Shipyard?

RU:

> Тирра не собиралась здесь останавливаться. Хватит ли у нас ресурсов, чтобы захватить вторую Верфь?

Узел `Mission_M8#643`.

`M08_030_030_FI`

EN:

> Onboard systems report peak functionality.  But the other Radaa Shipyards are deploying heavy reinforcements.

RU:

> Бортовые системы сообщают о максимальной функциональности. Но другие верфи Радаа перебрасывают тяжелые подкрепления.

Узел `Mission_M8#70`.

`M08_030_040_KS`

EN:

> I have the solution for this equation. All ships, bring down that second shipyard.

RU:

> У меня есть решение этого уравнения. Всем кораблям, разрушьте вторую верфь.

### M08_040

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardA) #330`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardB) #560`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardC) #284`.

Узел `Mission_M8#461`.

`M08_040_010_FI`

EN:

> Second Shipyard neutralized.  Destroying the last Shipyard would negate their ability to reinforce their fleets in the Hiigara system.

RU:

> Вторая верфь нейтрализована. Уничтожение последней верфи лишило бы их возможности усилить свои флоты в системе Хиигара.

Узел `Mission_M8#270`.

`M08_040_020_KS`

EN:

> Fleet, status report.  Can we get this job done?

RU:

> Флот, отчет о состоянии. Сможем ли мы выполнить эту работу?

Узел `Mission_M8#657`.

`M08_040_030_FI`

EN:

> All ships and all systems report Green.  The word from fleet is "Aye!".

RU:

> Все корабли и все системы сообщают зеленый цвет. Слово от флота: «Да!».

Узел `Mission_M8#112`.

`M08_040_040_KS`

EN:

> Then let's not give them anymore time to build their fleet.  All gunners, set the third Radaa Shipyard as priority alpha.

RU:

> Тогда давайте не будем больше давать им времени на построение своего флота. Всем артиллеристам, установите третью верфь Радаа в качестве приоритетной альфы.

### M08_050

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardA) #330`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardB) #560`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=ShipyardC) #284`.

Узел `Mission_M8#538`.

`M08_050_010_FI`

EN:

> All Radaa Shipyards destroyed. Remaining Radaa forces are in disarray.

RU:

> Все верфи Радаа уничтожены. Оставшиеся силы Рады находятся в замешательстве.

Узел `Mission_M8#230`.

`M08_050_020_KS`

EN:

> Initiate a coms link through to our entire Fleet.

RU:

> Установить связь со всем нашим флотом.

Узел `Mission_M8#244`.

`M08_050_030_FI`

EN:

> Connected.

RU:

> Связанный.

Узел `Mission_M8#200`.

`M08_050_040_KS`

EN:

> This is Commander Karan S'jet on all coms. We have been pushed to the brink, but know this - Tyrra Soban never doubted our ability.

RU:

> По всем каналам связи говорит командир Каран С'джет. Мы оказались на грани, но знайте: Тирра Собан никогда не сомневалась в наших способностях.

Узел `Mission_M8#641`.

`M08_050_050_KS`

EN:

> Your victory today proves she was right. We will reclaim Hiigara. Command out.

RU:

> Ваша сегодняшняя победа доказывает, что она была права. Мы вернем Хиигару. Командуйте выходом.

### M08_060

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #248`.

Узел `Mission_M8#192`.

`M08_060_010_FI`

EN:

> Pull back! Materials and ships overextended. Retreat unavoidable.

RU:

> Отойди! Материалы и корабли перегружены. Отступление неизбежно.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #350`; `CustomEvent #444`; `CustomEvent #629`; `OnSimReady #434`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M8#518`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M8#637`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M8#410`.

`FI_MothershipLost_08`

EN:

> Complete systems failure. Mothership crew must abandon ship.

RU:

> Полный сбой системы. Экипаж материнского корабля должен покинуть корабль.

Узел `Mission_M8#88`.

`FI_UnlockBalisticDestroyer`

EN:

> The Weapons Architects had ship plans we have put into use: we can now build Ballistic Destroyers, whose advanced Missile Barrage will be needed against the heavy Radaa fleet present in this sector.

RU:

> У Архитекторов оружия были чертежи кораблей, которые мы использовали: теперь мы можем строить баллистические эсминцы, чей продвинутый ракетный залп понадобится против тяжелого флота Радаа, присутствующего в этом секторе.

## 11. M13: Вернуться в Хиигару / Return to Hiigara

Определение `dcb65b8cb311f7646b0d3c550ed5761f:1`, карта `level21`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).

### Вступление

`Assets/Hercules/Scenes/M13 - Return to Hiigara/M13_Animatic_Intro/M13_Animatic_Intro.unity`

*Клип начинается в 1.07 с.*

`M13_010_005_A_KS`

EN:

> All Radaa Shipyards eliminated. We've crippled their construction capacity.

RU:

> Все верфи Радаа ликвидированы. Мы подорвали их строительные мощности.

*Клип начинается в 6.00 с.*

`M13_010_010_A_KS`

EN:

> Mothership fully operational. Fleet intact. Engineering, was that enough time?

RU:

> Материнский корабль полностью работоспособен. Флот цел. Инженерное дело, было ли этого времени достаточно?

*Клип начинается в 12.13 с.*

`M13_010_020_A_HA`

EN:

> We have analyzed the plans and distributed the silicon across all our ships.

RU:

> Мы проанализировали планы и распределили кремний по всем нашим кораблям.

*Клип начинается в 15.42 с.*

`M13_010_030_A_KS`

EN:

> Is it enough to protect the fleet?

RU:

> Достаточно ли этого для защиты флота?

*Клип начинается в 17.19 с.*

`M13_010_040_A_HA`

EN:

> I've run hundreds of simulations. It has to work. It WILL work.

RU:

> Я провел сотни симуляций. Это должно сработать. Это будет работать.

*Клип начинается в 22.37 с.*

`M13_010_050_A_KS`

EN:

> Your mother would be proud.

RU:

> Твоя мать гордилась бы.

*Клип начинается в 25.42 с.*

`M13_010_060_A_FI`

EN:

> Shatter Station and Radaa Tower are still in orbit around Hiigara.  Amma has been broadcasting an ultimatum to the planet.

RU:

> Станция Разрушения и Башня Радаа все еще находятся на орбите Хиигары. Амма передала планете ультиматум.

*Клип начинается в 32.62 с.*

`M13_010_070_A_AR`

EN:

> Hiigaran Command, according to interstellar law, you are allowed a narrow window to make good on the binding agreement you inherited. That period has ended. I don't want to unleash Shatter Station on the surface of your homeworld... but I will if I must and make no mistake, I will use your own people to rebuild.

RU:

> Хиигаранское командование, согласно межзвездному закону, вам предоставлено узкое окно для выполнения обязывающего соглашения, которое вы унаследовали. Этот период закончился. Я не хочу запускать Станцию ​​Разрушения на поверхность вашего родного мира... но я это сделаю, и не ошибусь, я воспользуюсь вашими людьми для восстановления.

*Клип начинается в 53.38 с.*

`M13_010_090_A_HA`

EN:

> This is NOT going to go like you planned, Amma.

RU:

> Все пойдет НЕ так, как ты планировала, Амма.

*Клип начинается в 56.73 с.*

`M13_010_100_A_KS`

EN:

> Prepare the jump to Hiigara.  On.  My.  Mark.

RU:

> Подготовьте прыжок на Хиигару. На. Мой. Отметка.

### Финальная постановочная сцена

`Assets/Hercules/Scenes/M13 - Return to Hiigara/M13_Animatic_Outro/M13_Animatic_Outro.unity`

*Клип начинается в 2.03 с.*

`M14_010_010_A_HA`

EN:

> Karan S'jet, the first Unbound, gave up her well-earned peace to defend our Homeworld. The Hiigaran people owe a great debt of gratitude to Karan S'jet and my mother, Tyrra Soban, who laid down her life for Hiigara.

RU:

> Каран С'джет, первая Освобожденная, отказалась от заслуженного мира, чтобы защитить наш Родной мир. Народ Хиигары в большом долгу перед Караном С'джетом и моей матерью Тиррой Собан, которые отдали свою жизнь за Хиигару.

*Клип начинается в 19.03 с.*

`M14_010_020_A_HA`

EN:

> While we neutralized the Shatter Station, the mothership was damaged in the battle. It would have to be rebuilt and its technology evolved before we could use it again.

RU:

> Пока мы нейтрализовали станцию ​​«Раскол», материнский корабль был поврежден в бою. Его придется перестроить, а его технологии развить, прежде чем мы сможем использовать его снова.

*Клип начинается в 28.58 с.*

`M14_010_030_A_HA`

EN:

> My mother did not live to see the victory that she made possible. Karan S’Jet always spoke about how much she valued her time with Tyrra Soban.

RU:

> Моя мать не дожила до победы, которую она сделала возможной. Каран С’Джет всегда говорила о том, как сильно она ценит время, проведенное с Тиррой Собан.

*Клип начинается в 38.77 с.*

`M14_010_040_A_HA`

EN:

> Karan and Hiigaran Command also learned more about what was required to be Navigator and Commander of a Mothership.  Being one with the Core was not just an honor, it was a sacrifice. One that Karan S'jet chose to make until the end of her days.

RU:

> Каран и командование Хиигарана также узнали больше о том, кем должны быть навигаторы и командиры базового корабля. Быть единым целым с Ядром было не просто честью, это была жертва. Тот, который Каран С'джет решила создавать до конца своих дней.

### Задачи, подключённые к графу

Узлы: 236, 461, 552, 624.

`M13_Objective_02`

EN:

> Dock an Engineer Craft to a shield emitter.

RU:

> Пристыкуйте инженерный корабль к излучателю щита.

Узлы: 72, 640, 764.

`M13_Objective_03alpha`

EN:

> Disable shield emitter alpha.

RU:

> Отключите излучатель щита альфа.

Узлы: 323, 605, 927.

`M13_Objective_03beta`

EN:

> Disable shield emitter beta.

RU:

> Отключить бета-версию излучателя щита.

Узлы: 190, 281, 463, 538, 743, 756, 869.

`M13_Objective_03counter`

EN:

> Disable shield emitters.

RU:

> Отключите излучатели щита.

Узлы: 68, 829, 861.

`M13_Objective_03delta`

EN:

> Disable shield emitter delta.

RU:

> Отключить дельту эмиттера щита.

Узлы: 70, 636, 839.

`M13_Objective_03omega`

EN:

> Disable shield emitter omega.

RU:

> Отключите эмиттер щита Омега.

Узлы: 56, 234, 313, 361, 369, 714, 835, 837, 867, 935.

`M13_Objective_04counter`

EN:

> Destroy the wings of the Shatter Station.

RU:

> Уничтожьте крылья Станции Разрушения.

Узлы: 311, 853.

`M13_Objective_timer`

EN:

> Time until Shatter Station fires again:

RU:

> Время до повторного выстрела Станции Разрушения:

### M13_020

Обработчики, достигающие этих реплик по control-связям: `OnSimReady #303`.

Узел `Mission_M13#180`.

`M13_020_010_KS`

EN:

> The Radaa have been waiting for us.

RU:

> Рада нас ждала.

Узел `Mission_M13#548`.

`M13_020_020_HA`

EN:

> My team have prepared our defences.

RU:

> Моя команда подготовила нашу оборону.

Узел `Mission_M13#439`.

`M13_020_030_KS`

EN:

> This encounter will go differently.

RU:

> Эта встреча пройдет иначе.

Узел `Mission_M13#776`.

`M13_020_040_AR`

EN:

> Hiigaran Mothership. The Radaa are prepared to accept your surrender.

RU:

> Хиигаранский корабль-матка. Рада готова принять вашу капитуляцию.

Узел `Mission_M13#412`.

`M13_020_050_KS`

EN:

> Coms on lockdown. Do not respond.

RU:

> Комс на карантине. Не отвечайте.

Узел `Mission_M13#400`.

`M13_020_060_AR`

EN:

> Hiigaran Command, you ARE our property. Stand down your fleet.

RU:

> Хиигаранское командование, вы — наша собственность. Остановите свой флот.

Узел `Mission_M13#451`.

`M13_020_070_GR`

EN:

> Do not test us further!  If you continue to resist I will relish tearing the Progenitor Core from your smoking hull.

RU:

> Не испытывайте нас дальше! Если вы продолжите сопротивляться, мне будет приятно вырвать Ядро Прародителя из вашего дымящегося корпуса.

Узел `Mission_M13#739`.

`M13_020_080_AR`

EN:

> Very well. We have exhausted our efforts to enforce the law peacefully. Commander Giitan, proceed.

RU:

> Очень хорошо. Мы исчерпали свои усилия по обеспечению соблюдения закона мирным путем. Командир Гитан, продолжайте.

Узел `Mission_M13#674`.

`M13_020_090_GR`

EN:

> Of course, mother. Command confirmed. Engaging Shatter Station.

RU:

> Конечно, мама. Командование подтверждено. Захватывающая станция Разрушения.

Узел `Mission_M13#724`.

`M13_020_100_KS`

EN:

> Shatter pulse fired.  Fleet, status.

RU:

> Разрушительный импульс выстрелил. Флот, статус.

Узел `Mission_M13#98`.

`M13_020_110_FI`

EN:

> No damage reported. Our Fleet remains intact.

RU:

> О повреждениях не сообщается. Наш Флот остается нетронутым.

Узел `Mission_M13#774`.

`M13_020_120_KS`

EN:

> Mothership is fully functional. Chief Engineer Hauk, you and your team were successful. Congratulations!

RU:

> Mothership полностью функционален. Главный инженер Хаук, вы и ваша команда добились успеха. Поздравляем!

Узел `Mission_M13#528`.

`M13_020_130_HA`

EN:

> Let's not celebrate yet, Commander. To destroy Shatter Station we will need to disable *its* Shield Emitters.

RU:

> Давайте пока не будем праздновать, коммандер. Чтобы уничтожить Станцию ​​Раскола, нам нужно будет отключить *ее* излучатели щита.

Узел `Mission_M13#385`.

`M13_020_140_FI`

EN:

> The Radaa Tower has also activated internal shielding.

RU:

> Башня Рада также активировала внутреннюю защиту.

Узел `Mission_M13#556`.

`M13_020_150_KS`

EN:

> They are scrambling. Intel, can you intercept their coms?

RU:

> Они карабкаются. Интел, ты можешь перехватить их связь?

Узел `Mission_M13#520`.

`M13_020_160_FI`

EN:

> Intermittently.

RU:

> Периодически.

Узел `Mission_M13#36`.

`M13_020_170_GR`

EN:

> They must have counter-terminated the Shatter attack, we must re-calibrate!  How long until full recalibration?  How long--

RU:

> Должно быть, они отразили атаку Раскола, нам нужно провести повторную калибровку! Сколько времени осталось до полной рекалибровки? Сколько--

Узел `Mission_M13#722`.

`M13_020_180_HA`

EN:

> Command, that could work. We won't be able to change our settings to match. Unless we withdraw...

RU:

> Командование, это может сработать. Мы не сможем изменить наши настройки в соответствии с ними. Если мы не отступим...

Узел `Mission_M13#546`.

`M13_020_190_KS`

EN:

> No. This will end now. How long will it take them to re-calibrate the Shatter pulse?

RU:

> Нет. Сейчас это закончится. Сколько времени им понадобится, чтобы откалибровать импульс Раскола?

Узел `Mission_M13#611`.

`M13_020_200_HU`

EN:

> Unknown - we have some time, but no way to know exactly.

RU:

> Неизвестно – у нас есть время, но нет возможности узнать точно.

Узел `Mission_M13#644`.

`M13_020_210_KS`

EN:

> Then we had best strike quickly.

RU:

> Тогда нам лучше всего нанести быстрый удар.

### M13_040

Обработчики, достигающие этих реплик по control-связям: `OnSquadronCaptured #573`.

Узел `Mission_M13#905`.

`M13_040_010_FI`

EN:

> Docking complete. Engineer Craft will remain vulnerable until it disables the Emitter.

RU:

> Стыковка завершена. Инженерное судно останется уязвимым, пока не отключит излучатель.

### M13_050

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#46`.

`M13_050_010_FI`

EN:

> Emitter disabled. Wings on the Shatter Station now exposed.

RU:

> Излучатель отключен. Крылья Станции Разрушения теперь обнажены.

Узел `Mission_M13#391`.

`M13_050_020_KS`

EN:

> Concentrate fleet firepower on those wings.

RU:

> Сосредоточьте огневую мощь флота на этих крыльях.

### M13_060

Узел `Mission_M13#unlinked_138`.

`M13_060_010_FI`

EN:

> More Shield Emitters still active.  Track them down and disable them.

RU:

> Еще больше излучателей щита все еще активны. Отследите их и отключите.

*Изолированный узел без ID/control-подключения: наличие текста не подтверждает его произнесение в игре.*

### M13_070

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#387`.

`M13_070_010_FI`

EN:

> Shields still active. Additional Shield Emitters must be disabled. 

RU:

> Щиты все еще активны. Дополнительные излучатели щита должны быть отключены.

### M13_080

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#805`.

`M13_080_010_FI`

EN:

> One more Shield Emitter must be disabled.

RU:

> Необходимо отключить еще один излучатель щита.

### M13_090

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#365`.

`M13_090_010_FI`

EN:

> More wings of Shatter Station vulnerable to attack.

RU:

> Больше крыльев Станции Разрушения уязвимо для атак.

### M13_100

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#696`.

`M13_100_010_FI`

EN:

> Additional Shatter Station wings now exposed.

RU:

> Дополнительные крылья Станции Разрушения теперь открыты.

### M13_110

Обработчики, достигающие этих реплик по control-связям: `CustomEvent (name=WingA_Captured) #622`; `CustomEvent (name=WingB_Captured) #50`; `CustomEvent (name=WingC_Captured) #426`; `CustomEvent (name=WingD_Captured) #821`.

Узел `Mission_M13#232`.

`M13_110_010_FI`

EN:

> The final set of Shatter Station's wings can now be destroyed.

RU:

> Последний комплект крыльев Станции Разрушения теперь можно уничтожить.

### M13_120

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #222`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #240`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #264`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #879`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #124`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #140`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #246`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #919`.

Узел `Mission_M13#518`.

`M13_120_010_KS`

EN:

> Hauk, status update. How long until they re-calibrate Shatter Station?

RU:

> Хаук, обновление статуса. Как скоро они перекалибруют Станцию ​​Разрушения?

Узел `Mission_M13#238`.

`M13_120_020_HA`

EN:

> Unknown, every sim we run comes back with a different answer.

RU:

> Неизвестно, каждый симулятор, который мы запускаем, дает другой ответ.

Узел `Mission_M13#907`.

`M13_120_030_KS`

EN:

> Understood, I will do what I can to slow them down.

RU:

> Понятно, я сделаю все, что смогу, чтобы их замедлить.

### M13_130

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #222`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #240`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #264`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #879`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #124`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #140`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #246`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #919`.

Узел `Mission_M13#186`.

`M13_130_010_KS`

EN:

> Hauk... status!

RU:

> Хаук... статус!

Узел `Mission_M13#285`.

`M13_130_020_HA`

EN:

> If Shatter Station fires again, we have minimal defenses.

RU:

> Если Станция Разрушения снова выстрелит, у нас будет минимальная защита.

Узел `Mission_M13#833`.

`M13_130_030_KS`

EN:

> It'll be too late.  We will destroy those wings before they can fire again.

RU:

> Будет слишком поздно. Мы уничтожим эти крылья, прежде чем они смогут снова стрелять.

### M13_140

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #222`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #240`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #264`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA1) #879`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #124`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #140`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #246`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA2) #919`.

Узел `Mission_M13#416`.

`M13_140_010_AR`

EN:

> Hiigaran Command, last chance to surrender. You will not be able to counteract Shatter Station a second time. You will lose everything.

RU:

> Хиигарское командование, последний шанс сдаться. Вы не сможете противодействовать Станции Разрушения во второй раз. Вы потеряете все.

Узел `Mission_M13#118`.

`M13_140_020_KS`

EN:

> Amma should be thinking about what she will lose.

RU:

> Амме следует подумать о том, что она потеряет.

Узел `Mission_M13#593`.

`M13_140_030_HA`

EN:

> Command, she could be right.

RU:

> Командир, она может быть права.

Узел `Mission_M13#507`.

`M13_140_040_KS`

EN:

> Perhaps, but we can't leave that thing to wreak havoc our planet.  Have the fleet concentrate fire on the Shatter Station wings.

RU:

> Возможно, но мы не можем оставить эту штуку сеять хаос на нашей планете. Пусть флот сосредоточит огонь на крыльях станции Разрушения.

### M13_150

Обработчики, достигающие этих реплик по control-связям: `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #100`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #335`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #620`; `OnWaveDestroyed (Enabled=True, Wave Tag to Detect=WingA) #78`.

Узел `Mission_M13#250`.

`M13_150_010_FI`

EN:

> Damage to final set of wings cascading to Shatter Station Command Module.

RU:

> Повреждение последнего набора крыльев, каскадом падающего на командный модуль станции «Раскол».

Узел `Mission_M13#82`.

`M13_150_020_HA`

EN:

> That did it. Shatter Station can't possibly fire again.

RU:

> Это сделало это. Станция Разрушения не сможет снова стрелять.

Узел `Mission_M13#148`.

`M13_150_030_KS`

EN:

> What's happening to the Tower?

RU:

> Что происходит с Башней?

Узел `Mission_M13#770`.

`M13_150_040_FI`

EN:

> Critical failure of Shatter Station is chaining to their Tower. Destruction imminent.

RU:

> Критический провал Станции Разрушения приковал их к Башне. Разрушение неизбежно.

Узел `Mission_M13#841`.

`M13_150_050_KS`

EN:

> Now we stand down.  Victory in your name, Tyrra.

RU:

> Теперь мы отступаем. Победа во имя твое, Тирра.

### M13_200

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #453`.

Узел `Mission_M13#353`.

`M13_200_010_FI`

EN:

> Too many ships lost - resource reserves spent - Hiigara is lost!

RU:

> Слишком много кораблей потеряно – запасы ресурсов израсходованы – Хиигара потеряна!

### M13_210

Обработчики, достигающие этих реплик по control-связям: `OnObjectiveCompleted (Objective=86, M13_Objective_timer) #853`.

Узел `Mission_M13#512`.

`M13_210_010_FI`

EN:

> Readings from Shatter Station indicate it is powering up.

RU:

> Показания станции Shatter показывают, что она включается.

Узел `Mission_M13#585`.

`M13_210_020_HA`

EN:

> We didn't make it in time.

RU:

> Мы не успели вовремя.

Узел `Mission_M13#154`.

`M13_210_030_HA`

EN:

> Fleet Command, respond!  Karan!  Karan!  

RU:

> Командование флота, ответьте! Каран! Каран!

### M13_220

Обработчики, достигающие этих реплик по control-связям: `OnDetectShip #144`.

Узел `Mission_M13#128`.

`M13_220_010_FI`

EN:

> We cannot overcome the internal Radaa Tower shields. Recommend centering attacks on the immediate threat, Shatter Station.

RU:

> Мы не можем преодолеть внутренние щиты Башни Радаа. Рекомендую сосредоточить атаки на непосредственной угрозе — Станции Разрушения.

### Событийные и общие сообщения

Обработчики, достигающие этих реплик по control-связям: `CustomEvent #389`; `CustomEvent #52`; `CustomEvent #964`; `OnSimReady #303`.

*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*

Узел `Mission_M13#297`.

`FI_MothershipAttacked_03`

EN:

> Enemy has targeted Mothership.

RU:

> Враг нацелился на Mothership.

Узел `Mission_M13#373`.

`FI_MothershipHeavyDamage_03`

EN:

> Damage to Mothership is intensifying.

RU:

> Урон Материнскому кораблю усиливается.

Узел `Mission_M13#418`.

`FI_MothershipLost_03`

EN:

> We have lost the Mothership.

RU:

> Мы потеряли Материнский Корабль.

Узел `Mission_M13#766`.

`FI_UnlockHeavyCruiser`

EN:

> From the wreckage of the Radaa shipyards we recovered technology to build a new ship: Heavy Cruisers have advanced weapon systems optimal for destroying the Shatter Station wings, once their shields are disabled.

RU:

> Из обломков верфей Радаа мы извлекли технологию для постройки нового корабля: Тяжелые крейсеры оснащены передовыми системами вооружения, оптимальными для уничтожения крыльев станции Раскол, когда их щиты отключены.

## Полнота и ограничения

Включено **395 уникальных внутри глав реплик графов** и **125 реплик клипов вступлений/финала**. Повторяющиеся общие тревоги могут встречаться в нескольких главах. Покрытие всех найденных PlayDialogue проверено автоматически.

При чтении старой версии использована схема Steam с двумя проверенными отличиями: у MissionDatabase отсутствует массив демо-миссий, у ObjectiveStaticData — поле ModelScaleMultiplier. Разбор каждого сохранённого объекта требует полного совпадения длины, частичные чтения не принимаются. Все определения миссий, кораблей, задач и найденные сценарные графы прочитаны.

Не прочитано 642 объектов, преимущественно HUD/UI/VFX старой версии. В том числе 9 AbilityDefinition несовместимы с новой схемой; их параметры в этом отчёте не реконструированы. Это ограничение аудита способностей, а не отсутствие девяти способностей в Quest. Полный список — local/quest-audit/index.json.

Проверка относится к данным и связям скриптов. Видимость реплик, тайминги, бой и все условия полного прохождения запуском не проверены. Наличие вступления не означает готовый видеоролик для HWRM: исходник использует Timeline/Unity и внешний звук.

