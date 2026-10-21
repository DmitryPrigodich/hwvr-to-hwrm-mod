"""Build a separate, stock-hull HWRM campaign scaffold from the extracted demo."""
import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ROOT = PROJECT / "minicampaign"
SOURCE = PROJECT / "local/campaign"
CAMPAIGN = ROOT / "leveldata/campaign/VastReachesMiniCampaign"
MAP = {
    "Ship_Hgn_Mothership": "kus_mothership", "Ship_Kus_Scout": "kus_scout",
    "Ship_Kus_Interceptor": "kus_interceptor", "Ship_Kus_AttackBomber": "kus_attackbomber",
    "Ship_Hgn_HeavyCorvette": "kus_heavycorvette", "Ship_Hgn_EngineerCraft": "kus_salvagecorvette",
    "Ship_Hgn_ResourceCollector": "kus_resourcecollector", "Ship_Rad_AssaultCraft": "vgr_interceptor",
    "Ship_Rad_AttackBomber": "vgr_bomber", "Ship_Rad_LanceFighter": "vgr_lancefighter",
    "Ship_Rad_Frigate": "tai_assaultfrigate", "Ship_Rad_MissileFrigate": "vgr_heavymissilefrigate",
    "Ship_Rad_Destroyer": "tai_destroyer", "Ship_Rad_Destroyer Damaged": "tai_destroyer",
    "Ship_Rad_HyperSpaceGate": "vgr_hyperspace_platform", "Ship_Rad_Shipyard": "vgr_shipyard",
    "Ship_Rad_Battlecruiser": "vgr_battlecruiser", "Ship_Rad_MobileRefinery": "vgr_resourcecontroller",
    "Ship_Rad_GunPlatform": "vgr_weaponplatform_gun",
}
CUSTOM = {
    "campaign": ("Vast Reaches Campaign Demo", "Vast Reaches Campaign Demo"),
    "choose": ("Choose chapter", "Выбрать главу"),
    "training": ("M0. Tutorial", "M0. Обучение"),
    "proving": ("M1: Hiigara Proving Grounds", "M1: Испытательный полигон Хиигары"),
    "destroyer": ("M4: The Lost Destroyer", "M4: Потерянный эсминец"),
    "training_desc": ("Campaign prologue, first connection and fleet controls.", "Пролог кампании, первое подключение и управление флотом."),
    "proving_desc": ("Harvest, scout, three live-fire patrols, betrayal and escape.", "Добыча, разведка, три учебных боя, предательство и отход."),
    "destroyer_desc": ("Find the destroyer. Bring three salvage corvettes. Return it OR destroy the gate.", "Найдите эсминец. Подведите три абордажных корвета. Доставьте эсминец ИЛИ уничтожьте врата."),
    "prototype": ("Vast Reaches Campaign Demo. 1: Mothership; 2: current objective.", "Vast Reaches Campaign Demo. 1: Материнский корабль; 2: текущая цель."),
    "t_move": ("Move a light fighter squadron into the marked area (camera 2).", "Переместите отряд лёгких истребителей в отмеченную область (камера 2)."),
    "t_attack": ("Destroy the first target group.", "Уничтожьте первую группу целей."),
    "t_build": ("Build one additional light fighter squadron at the Mothership.", "Постройте ещё один отряд лёгких истребителей на Материнском корабле."),
    "t_final": ("Destroy the remaining training enemies.", "Уничтожьте оставшиеся учебные цели."),
    "t_done": ("Fleet controls exercise complete. Proceed to the proving grounds.", "Обучение управлению флотом завершено. Переходим к полигону."),
    "scan": ("Send a Scout to the marked patrol search area.", "Отправьте разведчик к отметке патруля."),
    "engineers": ("Keep THREE salvage corvettes within 1200 m of the destroyer for 10 seconds.", "Удерживайте ТРИ абордажных корвета в радиусе 1200 м от эсминца в течение 10 секунд."),
    "tow": ("Escort the destroyer to the Mothership, or destroy the hyperspace gate.", "Прикройте эсминец на пути к Материнскому кораблю или уничтожьте гиперврата."),
    "escape": ("Emergency jump charging: protect the Mothership for 20 seconds.", "Аварийный прыжок: защищайте материнский корабль ещё 20 секунд."),
    "win": ("Chapter complete.", "Глава завершена."),
    "loss": ("Mothership lost. Mission failed.", "Материнский корабль потерян. Задание провалено."),
}


def read(name):
    return json.loads((SOURCE / name).read_text(encoding="utf-8"))


def vector(p):
    return "{" + ",".join(f"{x:.3f}" for x in p) + "}"


def convert(p, origin):
    # Unity left-handed coordinates -> the X mirror used by the imported hulls.
    return [-(p[0]-origin[0])*100, (p[1]-origin[1])*100, (p[2]-origin[2])*100]


def prepare():
    CAMPAIGN.mkdir(parents=True, exist_ok=True)
    en, ru = read("strings-en.json"), read("strings-ru.json")
    texts = dict(CUSTOM)
    for table in ("Strings_Animatics", "Strings_Missions"):
        for key, english in en[table].items():
            if key.startswith(("M01_", "M04_", "T01_")):
                texts[key] = (english, ru[table].get(key) or english)
    reviewed=json.loads((PROJECT/'localization/ru/campaign.json').read_text(encoding='utf8'))
    for key in texts.keys() & reviewed.keys():texts[key]=(texts[key][0],reviewed[key])
    speakers={'FI':('Fleet Intelligence','Разведка флота'),'TS':('Tyrra Soban','Тирра Собан'),'KS':("Karan S’jet","Каран С’Джет"),'AR':('Amma','Амма'),'GR':('Giitan','Гиитан'),'HA':('Narrator','Рассказчик')}
    for key,value in list(texts.items()):
        speaker=speakers.get(key.rsplit('_',1)[-1])
        if speaker:texts[key]=tuple(speaker[i]+': '+value[i] for i in range(2))
    ids = {key: 9950000+i for i, key in enumerate(sorted(texts))}
    for lang, column in (("English", 0), ("Russian", 1)):
        path = ROOT / "locale" / lang / "vrcampaign.ucs"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(f"{ids[k]}\t{v[column].replace(chr(10), ' ')}" for k, v in sorted(texts.items()))+"\n", encoding="utf-16")
    locale = ROOT/'locale/localedat.lua'
    base_locale = (PROJECT/'local/hwrm-base/locale/localedat.lua').read_text()
    locale.write_text(base_locale[:base_locale.rfind('}')]+'    {name="vrcampaign.dat"},\n}\n',encoding='ascii')
    lines = ["-- Generated IDs. Reviewed Russian translation; literal original is in docs/*_RAW.md.", "VRC_Text = {}", "VRC_Duration = {}"]
    lines += [f'VRC_Text["{k}"] = "${v}"' for k,v in ids.items()]
    lines += [f'VRC_Duration["{k}"] = {max(8,min(40,len(texts[k][1])//15+3))}' for k in ids]
    all_builds = re.findall(r'ThingToBuild\s*=\s*"([^"]+)"', (PROJECT/"local/hwrm-base/scripts/races/kushan/scripts/def_build.lua").read_text())
    lines += ["VRC_AllBuilds = {" + ",".join(json.dumps(n) for n in all_builds) + "}"]
    all_research = set()
    for p in (PROJECT/"local/hwrm-base/scripts/races/kushan/scripts/research").glob("*.lua"):
        all_research.update(re.findall(r'\bName\s*=\s*"([^"]+)"',p.read_text()))
    lines += ["VRC_AllResearch = {" + ",".join(json.dumps(n) for n in sorted(all_research)) + "}"]
    (CAMPAIGN/"VRC_Data.lua").write_text("\n".join(lines)+"\n",encoding="ascii")
    campaign = ['displayName="'+f'${ids["campaign"]}'+'"', 'contentType=2', 'contentName="VastReachesMiniCampaign"', 'contentOrdered=1',
                f'contentChooseText="${ids["choose"]}"',f'contentThumbName="${ids["campaign"]}"', f'contentThumbDesc="${ids["proving_desc"]}"','contentSort=0.4', 'contentRules="SinglePlayer"', 'ExtFilter="campaign_vast_reaches,campaign_gbx"', 'Mission={}']
    audit = {"coordinate_transform": "HWRM = 100 * (mirrorX(UnityWorld - sceneMothershipWorld))", "ship_map": MAP, "missions": []}

    def make(scene, directory, title, groups, fleet, volumes, ru_amount):
        data = read(scene+".json")
        mother = next(x for x in data['placements'] if x['name']=="Mothership")
        origin = mother['world_position']
        folder = CAMPAIGN/directory
        folder.mkdir(exist_ok=True)
        lev = ['-- Generated from demo scene placements. Stock hulls and provisional economy.', 'function DetermChunk()']
        record = {"scene": scene,"directory":directory,"origin":origin,"groups":[],"resources":[]}
        positions = []

        def spawn(name, source_ship, pos, owner, collective=None, source_id=None, full_batch=False):
            hull=MAP[source_ship]
            pt=convert(pos,origin)
            positions.append(pt)
            # Zero uses the native buildBatch, rather than forcing one hull.
            size=0 if full_batch else 1
            lev.extend([f'    addSquadron("{name}","{hull}",{vector(pt)},{owner},{{0,0,0}},{size},0)', f'    createSOBGroup("{name}")', f'    addToSOBGroup("{name}","{name}")'])
            if collective:
                lev.append(f'    addToSOBGroup("{name}","{collective}")')
            record['groups'].append({"group":name,"collection":collective,"source_ship":source_ship,"hull":hull,"position":pt,"owner":owner,"source_path_id":source_id,"full_batch":full_batch})

        spawn("VRC_Mothership","Ship_Hgn_Mothership",origin,0,source_id=mother['path_id'])
        lev.append('    addSphere("VRC_Return",{0,0,0},1800)')
        for index,(ship,pos) in enumerate(fleet):
            spawn(f"VRC_Player_{index+1}",ship,pos,0,full_batch=directory=='T01_Training')
        hidden=[]
        for name,pid,owner,hidden_flag in groups:
            src=next(x for x in data['placements'] if x['path_id']==pid)
            members=src['members']
            if len(members)>1:
                lev.append(f'    createSOBGroup("{name}")')
            for i,m in enumerate(members):
                off=m.get('Offset',{})
                pt=[src['world_position'][j]+off.get(axis,0) for j,axis in enumerate(('x','y','z'))]
                spawn(name if len(members)==1 else name+"_"+str(i+1),m['ship_definition'],pt,owner,name if len(members)>1 else None,src['path_id'])
            if hidden_flag:
                hidden.append(name)
                lev.append(f'    addSphere("{name}_Spawn",{vector(convert(src["world_position"],origin))},500)')
        for name,pos,radius in volumes:
            pt=convert(pos,origin)
            positions.append(pt)
            lev.append(f'    addSphere("{name}",{vector(pt)},{radius})')
            lev.append(f'    addCamera("{name}_Camera",{vector(pt)},{vector([pt[0]+2500,pt[1]+1500,pt[2]-2500])})')
        for x in data['placements']:
            if not x['class_name'].endswith('PropSpawner') or not x['name'].startswith('Asteroid'):
                continue
            d=x['data']['_data']
            pt=convert(x['world_position'],origin)
            amount=max(300,d.get('ContainedRu',0))  # stock resource multiplier; exact VR balance is not portable
            multiplier=amount/18000  # native Asteroid_4.resource has resourceValue=18000
            lev.append(f'    addAsteroid("Asteroid_4",{vector(pt)},{multiplier:.8f},0,0,0,0)')
            positions.append(pt)
            record['resources'].append({"source_path_id":x['path_id'],"source_ru":d.get('ContainedRu'),"native_ru_multiplier":multiplier,"position":pt})
        lev += ['    addCamera("VRC_HomeCamera",{0,0,0},{3500,1800,-4000})']
        if directory=='T01_Training':
            # Eight gentle arcs keep the origin-centred Mothership in view.
            for i,eye in enumerate(((3500,1000,-3500),(4950,1000,0),(3500,1000,3500),(0,1000,4950),(-3500,1000,3500),(-4950,1000,0),(-3500,1000,-3500),(0,1000,-4950)),1):
                lev.append(f'    addCamera("VRC_IntroOrbit_{i}",{{0,0,0}},{vector(eye)})')
        half=[max(abs(p[j]) for p in positions)+5000 for j in range(3)]
        background='ez16' if directory=='T01_Training' else 'm01'
        environment=['    fogSetActive(0)','    setGlareIntensity(0.0)','    setLevelShadowColour(0,0,0,1)'] if directory=='T01_Training' else []
        lev += [f'    setWorldBoundsInner({{0,0,0}},{vector(half)})','end','function NonDetermChunk()',*environment,f'    loadBackground("{background}")','    setSensorsManagerCameraDistances(100,70000)','end',f'levelDesc="${ids[title]}"','maxPlayers=3','player={}',f'player[0]={{id=0,name="",resources={ru_amount},raceName="Kushan",startPos=0}}','player[1]={id=1,name="",resources=0,raceName="Vaygr",startPos=0}','player[2]={id=2,name="",resources=0,raceName="Vaygr",startPos=0}']
        (folder/(directory+'.level')).write_text('\n'.join(lev)+'\n',encoding='ascii')
        previews={'T01_Training':'Mission_T1','M01_ProvingGrounds':'Mission_M1','M04_LostDestroyer':'Mission_M4'}
        source=PROJECT/'campaign-export/assets/loading'/(previews[directory]+'.png')
        if source.is_file():
            from PIL import Image
            Image.open(source).convert('RGB').save(folder/(directory+'.dds'),pixel_format='DXT1')
            thumbnail=ROOT/'ui/mapthumbnails/campaign/VastReachesMiniCampaign'/(directory+'.dds')
            thumbnail.parent.mkdir(parents=True,exist_ok=True)
            Image.open(source).convert('RGB').save(thumbnail,pixel_format='DXT1')
            if directory=='M01_ProvingGrounds':
                Image.open(source).convert('RGB').save(ROOT/'leveldata/campaign/VastReachesMiniCampaign.dds',pixel_format='DXT1')
        focus_points=','.join(f'["{name}_Camera"]="{name}"' for name,pos,radius in volumes)
        config = [f'VRC_Hidden = {{'+','.join(json.dumps(n) for n in hidden)+'}',f'VRC_Mission = "{directory}"', 'VRC_FocusPoints={'+focus_points+'}']
        (folder/'VRC_Setup.lua').write_text('\n'.join(config)+'\n',encoding='ascii')
        number=len(audit['missions'])+1
        campaign.append(f'Mission[{number}]={{postload=function() end,directory="{directory}",level="{directory}.level",postlevel=function() postLevelComplete() end,displayName="${ids[title]}",description="${ids[title+"_desc"]}"}}')
        audit['missions'].append(record)

    make('level1','T01_Training','training',[
        ('VRC_TrainingA',271,1,1),('VRC_TrainingB',257,1,1),('VRC_TrainingC',318,1,1),('VRC_Platform',260,1,1)],
        [('Ship_Kus_Scout',[.02+i*4.5,0,-18.33]) for i in range(3)],
        [('VRC_MovePoint',[4.52,-10.4,42.88],1400),('VRC_TargetPoint',[-11.3,2.9,11.4],2000)],5000)
    # Actual LoadoutSpawner transforms (not the prefab's zero-position defaults).
    starts=[[-102.42908,-33.09749,-24.03379],[-116.33143,-33.09749,-26.27154],[-130.23378,-33.09749,-28.50929]]
    fleet=[]
    for gi,ships in enumerate([['Ship_Kus_Interceptor']*3,['Ship_Kus_AttackBomber']*3+['Ship_Kus_Interceptor'],['Ship_Hgn_ResourceCollector']]):
        for i,ship in enumerate(ships):fleet.append((ship,[starts[gi][0]+i*1.4,starts[gi][1],starts[gi][2]]))
    make('level4','M01_ProvingGrounds','proving',[
        ('VRC_Patrol1',468,1,1),('VRC_Patrol2',405,1,1),('VRC_Patrol3',537,1,1),
        ('VRC_Breach1',409,1,1),('VRC_Breach2',432,1,1),('VRC_Breach3',461,1,1),
        ('VRC_LateFrigate1',469,1,1),('VRC_LateFrigate2',490,1,1),('VRC_LateFrigate3',467,1,1),('VRC_LateFrigate4',473,1,1),('VRC_FinalFleet',412,1,1)],
        fleet,[('VRC_ScoutPoint',[-143.6,-51.43,-163.1],2200),('VRC_DefensePoint',[-95.32,-30.5,-51.7],3000)],100)
    starts=[[.39,.34,-18.34],[14.47129,.34,-18.34],[28.55258,.34,-18.34],[7.59631,.34,-30.77295]]
    fleet=[]
    for gi,ships in enumerate([['Ship_Kus_Scout']+['Ship_Kus_Interceptor']*2,['Ship_Kus_AttackBomber']*3+['Ship_Hgn_HeavyCorvette']*2,['Ship_Kus_Interceptor']+['Ship_Hgn_ResourceCollector']*2,['Ship_Hgn_EngineerCraft']*3]):
        for i,ship in enumerate(ships):fleet.append((ship,[starts[gi][0]+i*1.4,starts[gi][1],starts[gi][2]]))
    make('level6','M04_LostDestroyer','destroyer',[
        ('VRC_Destroyer',1930,2,0),('VRC_Gate',1825,1,1),('VRC_GateGuard',1876,1,1),
        ('VRC_Retrieval',1849,1,1),('VRC_Pursuit1',1906,1,1),('VRC_Pursuit2',1939,1,1),('VRC_Pursuit3',1821,1,1)],
        fleet,[('VRC_SearchPoint',[-12.42,32.35,125.6],4500),('VRC_DestroyerPoint',[-12.37,32.26,141.03],1200),('VRC_GatePoint',[44.368,47.03,60.063],2000)],1200)
    (ROOT/'leveldata/campaign/VastReachesMiniCampaign.campaign').write_text('\n'.join(campaign)+'\n',encoding='ascii')
    (PROJECT/'local/minicampaign-layout.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    integration=PROJECT/'local/cinematic-update/integration.json'
    if integration.exists() and json.loads(integration.read_text(encoding='utf8')).get('release_enabled') is True:
        from apply_campaign_movies import add_wrappers, bind_mini
        movies=json.loads((PROJECT/'campaign-export/cinematics/index.json').read_text(encoding='utf8'))['scenes']
        add_wrappers(ROOT,movies)
        bind_mini(ROOT)
    print('Prepared three campaign chapters and bilingual localization; Lua mission logic is maintained in minicampaign/.')


if __name__ == '__main__':
    prepare()
