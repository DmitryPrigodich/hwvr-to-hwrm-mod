"""Package the frozen, verified layered source as an isolated M0 handoff ZIP.

No dependency updates, installation, game launch or main-release replacement.
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

from layer_runtime import PROJECT,configure,check_revision,BASE,RACES

IDENTITY='VRC-tutorial-showcase-v1'
WORK=PROJECT/'local/tutorial-showcase'
RELEASE=PROJECT/'local/VastReachesTutorial-release'
ZIP=PROJECT/'local/VastReaches-Tutorial-2026-10-24.zip'


def finalize():
    configure()
    import hwrm_common as common
    assert (RELEASE/'payload/showcase-id.txt').read_text().strip()==IDENTITY
    shutil.copy2(PROJECT/'distribution/tutorial/Setup.ps1',RELEASE/'Setup.ps1')
    build=json.loads((RELEASE/'BUILD.json').read_text(encoding='utf8'))
    build['packager_sha256']=common.sha(Path(__file__))
    build['setup_sha256']=common.sha(RELEASE/'Setup.ps1')
    common.save(RELEASE/'BUILD.json',build)
    sums={p.relative_to(RELEASE).as_posix():common.sha(p) for p in RELEASE.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'}
    (RELEASE/'SHA256SUMS.txt').write_text(''.join(digest+'  '+name+'\n' for name,digest in sorted(sums.items())),encoding='ascii')
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as archive:
        for path in sorted(RELEASE.rglob('*')):
            if path.is_file():archive.write(path,'VastReaches-Tutorial/'+path.relative_to(RELEASE).as_posix())
    with zipfile.ZipFile(ZIP) as archive:assert archive.testzip() is None
    build.update(zip=str(ZIP),zip_bytes=ZIP.stat().st_size,zip_sha256=common.sha(ZIP),release=str(RELEASE),checksums=len(sums))
    common.save(WORK/'release.json',build)
    print(json.dumps(build,ensure_ascii=False,indent=2))


def package():
    configure()
    import hwrm_common as common
    import hwrm_archive
    from lupa.lua51 import LuaRuntime
    revision=check_revision()
    manifest=json.loads((PROJECT/'local/mod-layers/source.json').read_text(encoding='utf8'))
    common.save(WORK/'input-source.json',manifest)
    verified=json.loads((PROJECT/'local/mod-layers/verification.json').read_text(encoding='utf8'))
    assert verified['status']=='passed' and verified['race_commit']==revision==manifest['race_commit']
    assert verified['mp_patch_commit']==manifest['mp_patch_commit']
    inherited=Path(manifest['source'])
    assert {n:common.sha(p) for n,p in common.index(inherited).items()}==manifest['files'],'Layered source changed; rebuild/verify it first.'
    source=common.build_directory('tutorial-showcase',PROJECT)/'source'
    if source.exists():
        assert source.resolve().is_relative_to(common.build_directory('tutorial-showcase',PROJECT).resolve())
        assert (source/'tutorial-showcase-id.txt').read_text().strip()==IDENTITY
        shutil.rmtree(source)
    shutil.copytree(inherited,source)
    (source/'tutorial-showcase-id.txt').write_text(IDENTITY+'\n',encoding='ascii')
    assert all(common.sha(source/name)==digest for name,digest in manifest['files'].items()),'Inputs changed during snapshot.'
    campaign=source/'leveldata/campaign/vastreachesminicampaign.campaign'
    text=campaign.read_text(encoding='ascii')
    text=re.sub(r'^Mission\[[23]\]=[^\n]*\n','',text,flags=re.M)
    text=text.replace('displayName="$9950146"','displayName="$9951200"').replace('contentThumbName="$9950146"','contentThumbName="$9951200"')
    text=text.replace('contentThumbDesc="$9950155"','contentThumbDesc="$9950164"')
    campaign.write_text(text,encoding='ascii',newline='\n')
    (source/'leveldata/campaign/vrcfleetpreview.campaign').unlink()
    shutil.copy2(source/'leveldata/campaign/vastreachesminicampaign/t01_training/t01_training.dds',source/'leveldata/campaign/vastreachesminicampaign.dds')
    for language,title in [('Russian','Vast Reaches: Обучение'),('English','Vast Reaches: Tutorial')]:
        folder=source/f'locale/{language}'
        ucs=folder/'vrcampaign.ucs'
        ucs.write_text(ucs.read_text(encoding='utf16')+'9951200\t'+title+'\n',encoding='utf16',newline='\r\n')
        for path in folder.glob('VRE_*.lua'):
            if path.name.lower()!='vre_prologue.lua':path.unlink()
        wrapper=folder/'VRE_Prologue.lua'
        data=wrapper.read_text(encoding='ascii')
        assert 'animatics/VastReaches/' in data
        wrapper.write_text(data.replace('animatics/VastReaches/','animatics/VastReachesTutorial/'),encoding='ascii',newline='\n')
    for path in (source/'sound/music/animatic/VRC').iterdir():
        if path.stem.lower()!='vre_prologue':path.unlink()
    # None of the race/base runtime or economic definitions may change here.
    for name,digest in manifest['files'].items():
        if name.startswith(('ship/','weapon/','subsystem/','scripts/races/','scripts/strike groups/','scripts/startingfleets/')) or name=='scripts/familylist.lua':
            assert common.sha(source/name)==digest,('Inherited definition changed',name)
    vm=LuaRuntime();vm.execute(campaign.read_text(encoding='ascii'))
    assert vm.globals().Mission[1].directory=='T01_Training' and vm.globals().Mission[2] is None
    assert 'VRE_Prologue.lua' in campaign.read_text(encoding='ascii')
    import verify_minicampaign as mini
    mini.ROOT=source;mini.BASE=source/'leveldata/campaign/VastReachesMiniCampaign'
    engine=mini.Engine('T01_Training');engine.tick(600)
    assert engine.g.VRC_TrainingPhase==2 and engine.camera_control==1
    engine.sensors_active=1;engine.tick(240);engine.assert_stage(1)
    assert len([v for v in engine.ships.values() if v['owner']==0 and v['type']=='kus_scout'])==1
    if RELEASE.exists():
        assert RELEASE.resolve().parent==(PROJECT/'local').resolve()
        assert (RELEASE/'payload/showcase-id.txt').read_text().strip()==IDENTITY
        shutil.rmtree(RELEASE)
    payload=RELEASE/'payload';payload.mkdir(parents=True)
    result=hwrm_archive.package_source(source,payload,'VastReachesTutorial.big','Vast Reaches Tutorial')
    logs=WORK/'package-logs';logs.mkdir(parents=True,exist_ok=True)
    for path in payload.glob('*.log'):shutil.move(str(path),str(logs/path.name))
    (payload/'showcase-id.txt').write_text(IDENTITY+'\n',encoding='ascii')
    (payload/'config.txt').write_text('Title: Vast Reaches Tutorial\nGameType: HomeworldRM\nModType: MOD\nBigFilename: VastReachesTutorial.big\n',encoding='ascii')
    for language in ('Russian','English'):
        target=payload/f'Movies/{language}/VRE_Prologue.webm';target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(PROJECT/f'local/campaign-speech/release-movies/{language}/VRE_Prologue.webm',target)
    (payload/'Movies/showcase-id.txt').write_text(IDENTITY+'\n',encoding='ascii')
    shutil.copy2(PROJECT/'distribution/tutorial/Setup.ps1',RELEASE/'Setup.ps1')
    for name,arguments in [('Play Tutorial.cmd','-Launch'),('Play Tutorial English.cmd','-Launch -Language English'),('Install only.cmd','')]:
        (RELEASE/name).write_text('@echo off\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Setup.ps1" '+arguments+'\r\nif errorlevel 1 pause\r\n',encoding='ascii',newline='')
    (RELEASE/'README.txt').write_text('''Vast Reaches — M0. Обучение / Tutorial

1. Распакуйте ZIP целиком в обычную папку.
2. Закройте Homeworld Remastered и его лаунчер.
3. Запустите Play Tutorial.cmd.
   Установка найдёт Steam-библиотеку; если не найдёт, попросит путь к папке Homeworld.
4. В игре: Extra Missions → Vast Reaches: Обучение → M0. Обучение.
   Сначала идёт пролог. Начните новую миссию, не загружайте старое сохранение.

Play Tutorial English.cmd выбирает английский. Install only.cmd только устанавливает.
Если установка сообщает Access denied, один раз запустите Install only.cmd от имени
администратора. Затем запускайте Play Tutorial.cmd обычным способом.
По умолчанию окно1600×900. Для полного экрана: powershell -ExecutionPolicy Bypass -File .\\Setup.ps1 -Launch -Fullscreen
Если автопоиск не нашёл игру: powershell -ExecutionPolicy Bypass -File .\\Setup.ps1 -GameRoot "D:\\SteamLibrary\\steamapps\\common\\Homeworld" -Launch

Требуется Steam Homeworld Remastered Collection. Python, Toolkit и отдельная
установка HWMP/Races не нужны: закреплённые слои уже собраны в одном игровом BIG.
Пакет ставится отдельно в HomeworldRM/DataWorkshopMODs/VastReachesTutorial и
HomeworldRM/Data/Animatics/VastReachesTutorial. Обычный мод/чужие моды не заменяются.
Прежняя версия только этого пакета сохраняется в %LOCALAPPDATA%/VastReachesTutorial/backups.
Для удаления при закрытой игре удалите только эти две папки VastReachesTutorial.

Для показа: пролог, Тирра/Каран/Разведка, сенсоры и камера, первый разведчик,
маршрут W через A/B вокруг платформы, учебный сброс, финальная атака и диалог.
Строительства нет; один отряд. Клавиши1/2 показывают Материнский корабль/цель.
Вход в3500м зону платформы возвращает отряд к началу попытки.

Это сборка для предварительного показа. Проверены состав/распаковка BIG,
сценарные проверки и контрольные суммы. Новая нативная проверка игры не выполнена.
Код: https://github.com/DmitryPrigodich/hwvr-to-hwrm-mod
''',encoding='utf-8-sig')
    build={'identity':IDENTITY,'date':'2026-10-24','chapter':'T01_Training','prologue':True,
           'race_commit':revision,'mp_patch_commit':manifest['mp_patch_commit'],'fix_revision':manifest['fix_revision'],
           'campaign_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),
           'archives':[{**row,'archive':'payload/'+Path(row['archive']).name} for row in result['archives']],
           'input_source_manifest_sha256':common.sha(WORK/'input-source.json'),
           'engine_tested':False,'installed':False,'game_launched':False}
    common.save(RELEASE/'BUILD.json',build)
    finalize()


if __name__=='__main__':
    if '--finalize' in sys.argv:finalize()
    else:package()
