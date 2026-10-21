"""Summarize the measured Quest/Steam resource comparison and story coverage."""
import collections
import json
from pathlib import Path
from UnityPy.enums import TextureFormat

ROOT=Path(__file__).resolve().parent.parent


def main():
    result=json.loads((ROOT/'local/quest-comparison.json').read_text())
    comp=result['comparison'];meshes=comp['meshes'];textures=comp['textures']
    same_size=sum(t['steam_size']==t['quest_size'] for t in textures)
    larger=[t for t in textures if t['quest_size'][0]>t['steam_size'][0] or t['quest_size'][1]>t['steam_size'][1]]
    smaller=[t for t in textures if t['quest_size'][0]<t['steam_size'][0] or t['quest_size'][1]<t['steam_size'][1]]
    steam=json.loads((ROOT/'local/campaign/missions.json').read_text())
    quest=json.loads((ROOT/'local/quest-campaign/missions.json').read_text())
    qs=json.loads((ROOT/'local/quest-campaign/summary.json').read_text())
    lines=['# Quest 1.1.0-16520 и Steam-демка: что совпало','',
           '**По геометрии общие модели совпали.** У предоставленного Quest-порта не найдено упрощённых версий среди 178 общих мешей кораблей, астероидов и связанного окружения. Во всех 178 совпали поверхность из треугольников и привязка UV. Разница рекламного ролика сама по себе не доказывает низкое качество исходных моделей.','',
           'Источник Quest: `G:\\Games\\HW_Games\\Homeworld- Vast Reaches v16520+1.1.0-16520 -VRP`, APK/OBB; внутренний PlayerSettings подтверждает `bundleVersion=1.1.0-16520`. Steam — установленная Windows-демка. Обе версии прочитаны как данные; APK и игры не запускались.','',
           '## Измеренное сравнение','',
           '| Показатель | Результат |','|---|---|',
           f'| Общие проверенные имена мешей | {len(meshes)} |',
           f'| Совпавшая геометрия треугольников | {sum(m["same_surface"] for m in meshes)} / {len(meshes)} |',
           f'| Совпавшие UV с привязкой к вершинам | {sum(m["same_uv"] for m in meshes)} / {len(meshes)} |',
           f'| Общие имена текстур в выборке | {len(textures)} |',
           f'| Одинаковые размеры текстур | {same_size} |',
           f'| Текстуры Quest больше по разрешению | {len(larger)} |',
           f'| Текстуры Quest меньше по разрешению | {len(smaller)} |','',
           'Геометрия сравнивается по координатам и поверхности, с точностью округления 10⁻⁶, независимо от порядка индексов/вершин. В выборке имеются LOD; они сравниваются с одноимёнными LOD, а не только по числу полигонов. Сравнение UV учитывает положение вершины, поэтому совпадение размеров атласа не подменяет проверку развёртки.','',
           '### Текстуры, у которых различается разрешение','',
           '| Текстура | Steam | Quest |','|---|---:|---:|']
    for t in larger+smaller:
        lines.append(f'| `{t["name"]}` | {t["steam_size"][0]}×{t["steam_size"][1]} | {t["quest_size"][0]}×{t["quest_size"][1]} |')
    formats=collections.Counter((t['steam_format'],t['quest_format']) for t in textures)
    lines+=['','### Хранение и внешний вид','',
            '| Steam | Quest | Общих текстур |','|---|---|---:|']
    for (a,b),count in sorted(formats.items()):lines.append(f'| {TextureFormat(a).name} | {TextureFormat(b).name} | {count} |')
    lines+=['',
            'Это разные способы GPU-сжатия. Декодированные цветовые атласы также не все побайтно идентичны: для 42 общих `_BC`-карт проверены уменьшенные образцы 64×64, отклонение RGB зависит от карты и достигает примерно 17,4 из 255 по RMS. Это проверка различий цвета/сжатия, а не оценка качества в игре. Нормальные карты в DXT5 и ASTC могут использовать разную упаковку каналов; большое поканальное отличие их сырых пикселей не означает испорченную геометрию.','',
            'По этим данным нет основания отвергать Quest-ресурсы как low-poly или повсеместно уменьшенные. У материнского корабля базовая карта в Quest даже 4096² против 2048² в Steam. Окончательный материал для HWRM всё равно требует адаптации шейдера, каналов и окраски. Совпадение поверхности/UV не является проверкой освещения, тангентов, всех материалов и качества рендера двух игр.','',
            '### Меши, дополнительно найденные в Quest','']
    for name in comp['quest_only_meshes']:lines.append('- `'+name+'`')
    lines+=['','Среди них — utility corvette, обломок корабля, дополнительные LOD носителя Радаа и меши щитов. Наличие меша не доказывает, что он строится игроком или имеет завершённую игровую роль. Среди проверенных имён отсутствующих в Quest общих моделей Steam не обнаружено.','',
            '## Кампания: дополнение существенное','',
            'Steam-демка действительно содержит карты обучения, M1, M4 и отдельного C1. В полной Quest-сборке есть **все 11 игровых карт основной кампании**, обучение и постановочные сцены. В её BuildSettings 37 сцен с учётом света, меню, вступлений и финала; это не 37 миссий. C1 здесь не включён.','',
            'Порядок кампании из MissionDatabase:','',
            '| Позиция | Внутренний код | EN / RU | Карта | Перенос флота |','|---:|---|---|---|---|']
    for m in quest:
        if m['category']!='_campaignMissions':continue
        lines.append(f'| {m["order"]} | {m["id"].removeprefix("Mission_")} | {m["title"]["en"]} / {m["title"]["ru"]} | `{m["scene_file"]}` | {"да" if m["carryover"] else "нет"} |')
    lines+=['',
            'У полной M4 разрешён перенос флота; у Mission_M4_Demo — нет и есть отдельно подготовленный демо-флот. Поэтому точные стартовые составы полной и демо-версии нельзя смешивать даже при одинаковой карте. Полная M7 после полигона и M9 после башни сбрасывают состав по своим правилам; остальные соответствующие главы могут учитывать уцелевший флот.','',
            'Все найденные сценарные графы, определения миссий, кораблей и задач прочитаны. Использована схема Steam с двумя строго проверенными отличиями старой версии: у MissionDatabase нет списка демо-миссий; у ObjectiveStaticData нет ModelScaleMultiplier. Для каждого принятого объекта требовалось полное чтение всех байтов. Остались несовместимые HUD/UI/VFX и 9 AbilityDefinition — они не считаются отсутствующими способностями.','',
            '## Что читать дальше','',
            '- [Полный сценарий Quest: EN и RU](QUEST_SCENARIOS.md).',
            '- [Quest: старт, выдачи, стройка и сюжетные технологии](QUEST_PROGRESSION.md).',
            '- [Steam-демка: сценарий EN/RU](DEMO_SCENARIOS.md) и [точные составы](DEMO_PROGRESSION.md).',
            '- [Принятое направление адаптации](DESIGN_DIRECTION.md).','',
            'Воспроизведение: `tools/unpack_quest_assets.py`, `audit_campaign.py --quest-v110`, `summarize_campaign.py --quest`, `compare_quest_steam.py`, `write_quest_scenarios.py`, `write_quest_progression.py`. Полные результаты геометрии/текстур — `local/quest-comparison.json`; описание распаковки — `local/quest-content/unpack-index.json`.','']
    (ROOT/'docs/QUEST_COMPARISON.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print('Wrote docs/QUEST_COMPARISON.md')


if __name__=='__main__':main()
