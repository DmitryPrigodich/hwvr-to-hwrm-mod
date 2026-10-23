"""Create only the user-facing release; working documents stay in the project."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from build_minicampaign import native_aliases

PROJECT=Path(__file__).resolve().parents[1]
PACKAGE=PROJECT/'local/VastReachesCampaignDemo-release'
IDENTITY='VastReachesCampaignDemo-release-v1'


def package(fleet_preview=False, research=False, cinematics=None):
    integration=PROJECT/'local/cinematic-update/integration.json'
    enabled=integration.exists() and json.loads(integration.read_text(encoding='utf8')).get('release_enabled') is True
    if cinematics is None:cinematics=enabled
    if cinematics and not enabled:
        raise RuntimeError('Cinematic release disabled after native menu regression; use isolated preparation until resolved.')
    if native_aliases(PROJECT/'local/VastReachesMiniCampaign.big')!=['data','locale']:
        raise RuntimeError('Unexpected primary BIG layout.')
    for language in ('English','Russian'):
        if native_aliases(PROJECT/f'local/{language}.big')!=['locale']:
            raise RuntimeError('Unexpected language BIG layout.')
    marker=PACKAGE/'package-id.txt'
    if PACKAGE.exists() and (not marker.is_file() or marker.read_text().strip()!=IDENTITY):
        raise RuntimeError('Unknown release directory')
    PACKAGE.mkdir(exist_ok=True);marker.write_text(IDENTITY+'\n',encoding='ascii')
    for path in [PROJECT/'local/VastReachesMiniCampaign.big',PROJECT/'start_campaign.ps1',PROJECT/'Vast Reaches Campaign Demo.cmd']:
        shutil.copy2(path,PACKAGE/path.name)
    for language in ('English','Russian'):
        shutil.copy2(PROJECT/f'local/{language}.big',PACKAGE/(language+'.big'))
    (PACKAGE/'README.txt').write_text('''Vast Reaches Campaign Demo

Запуск: двойной щелчок по Vast Reaches Campaign Demo.cmd.
В игре: Extra Missions → Vast Reaches Campaign Demo → первая глава.

Через официальный лаунчер: Mods → Remastered → выбрать Vast Reaches Campaign Demo
→ Launch. Галочки HW1/HW2 выключены, дополнительные аргументы не нужны.
В игре тот же путь: Extra Missions → Vast Reaches Campaign Demo.

Текущая тестовая последовательность: обучение → M1 → M4.
Полная кампания и её перенос флота ещё разрабатываются. Перенос флота между
этими тестовыми главами пока не подключён: каждая получает заданный состав.

В этой папке только игровой архив, запускатель и эта инструкция.
Сценарии, глоссарий, исходники, экспорт и отчёты находятся отдельно в рабочем проекте.
''',encoding='utf8')
    if fleet_preview:
        readme=PACKAGE/'README.txt'
        readme.write_text('''Vast Reaches Campaign Demo — объединённое обновление 20 октября 2026

Запускатель и мод в лаунчере называются Vast Reaches Campaign Demo.
В игре: Extra Missions → Новокушане и Новотаиидане — проба флота.
Выберите Новокушан или Новотаиидан. B — строительство, 1 — общий вид.
Даны 100000 RU и по одному юниту каждого проекта. Цели для стрельбы впереди.
Научных кораблей и исследований в этой пробе нет, проекты открыты сразу.

Статические проверки пройдены; игра автоматически не запускалась.
Это первый вариант отрядов/цен/лимитов, с исходным оружием и способностями.
Выпуск из станции использует пробные пути дока носителя и требует просмотра.
В том же моде сохранены главы HWVR: T1 → M1 → M4.
Полигоны новых рас доступны отдельным пунктом Extra Missions.
Исходники кампании, переводы и проектные документы сохраняются в проекте.
Предыдущий релиз сохранён в проекте local/fleet-preview/baseline-backup.

'''+readme.read_text(encoding='utf8'),encoding='utf8')
    if research:
        readme=PACKAGE/'README.txt'
        text=readme.read_text(encoding='utf8')
        text=text.replace('объединённое обновление 20 октября 2026','исследовательское обновление 21 октября 2026')
        text=text.replace('Научных кораблей и исследований в этой пробе нет, проекты открыты сразу.',
            'Новокушане: шесть научных модулей и инженерное дерево исследований.\n'
            'Для развития с нуля выберите «Новокушане — исследовательская проба».\n'
            'B — строительство, R — исследования (штатные клавиши Remastered).\n'
            'Полигоны показа флота сохраняются: у Новокушан технологии там выданы сразу.\n'
            'Новотаиидане пока остаются без исследований; их классовое дерево — следующий этап.')
        text += '\nЛокализация: русский и английский, отдельные названия и описания.\n'
        text += 'Обычный .cmd запускает русский. Для английского: start_campaign.ps1 -Language English\n'
        text += 'В лаунчере язык выбирается стандартным аргументом -locale Russian / -locale English.\n'
        text += '\nEnglish: launch start_campaign.ps1 -Language English.\n'
        text += 'Extra Missions > Novokushan and Neo-Taiidan — Fleet Preview > Novokushan — Research Trial.\n'
        text += 'B: construction; R: research. Plasma Weapons unlocks attack bombers and assault frigates;\n'
        text += 'Improved Plasma Bombs is a separate anti-subsystem ammunition upgrade for both.\n'
        readme.write_text(text,encoding='utf8')
    if cinematics:
        movies=PROJECT/'local/cinematic-update/release-movies'
        speech=PROJECT/'local/campaign-speech/integration.json'
        if speech.exists() and json.loads(speech.read_text(encoding='utf8')).get('enabled') is True:
            movies=PROJECT/'local/campaign-speech/release-movies'
        assert (movies/'vre-movies-id.txt').read_text().strip()=='VRC-rendered-campaign-movies-v1'
        shutil.copytree(movies,PACKAGE/'Movies',dirs_exist_ok=True)
        readme=PACKAGE/'README.txt'
        readme.write_text('''Обновление роликов, 21 октября 2026

Перед обучением показывается общий пролог, перед M4 — вступление этой миссии.
Исходные английские голоса, музыка и окружение; отдельные RU/EN-субтитры.
Ролики адаптированы для обычного экрана с фиксированной камерой, 1280×720.
Полная 3D-постановка финала ещё не восстановлена.
Воспроизведение и пропуск в HWRM требуют совместной проверки.

Movies содержит готовые игровые WebM. Установщик помещает их также в отдельную
собственную папку HomeworldRM/Data/Animatics/VastReaches — штатный путь видео.
Рабочих PNG/WEM/WAV и материалов подготовки в релизе нет.

'''+readme.read_text(encoding='utf8'),encoding='utf8')
        if speech.exists() and json.loads(speech.read_text(encoding='utf8')).get('enabled') is True:
            readme.write_text('''Штатная речь HWRM: отдельные PCM WAV и описания внутри BIG.
В роликах голос — отдельная дорожка Movie.filenameA, в миссиях — Subtitle_Add с портретом.
Прежние отдельные AddSpeechEvent не загружаются; WebM содержит музыку и окружение.
M0: The Beginning, возврат интерфейса после первого разговора, T01_020 и проверка сенсоров.
Остановка голоса при пропуске ещё требует проверки в движке; начинайте обучение заново.

'''+readme.read_text(encoding='utf8'),encoding='utf8')
    patch_config=PROJECT/'players-patch/integration.json'
    if patch_config.exists() and json.loads(patch_config.read_text(encoding='utf8')).get('enabled') is True:
        readme=PACKAGE/'README.txt'
        readme.write_text('''Основа Players Patch 2.3Test build 21, интеграция 23 октября 2026
Включён полный игровой состав 2.3Test. Общая основа — мультиплеерные параметры;
их подмены в одиночной игре нейтрализованы, используются MP-исследования.
Новокушане/Новотаиидане сохраняют свои отряды, стройку, науку и баланс эсминцев.
Их корабельные определения объединены с техническими изменениями патча.
Статическая проверка и CRC не заменяют проверку HWRM; новый нативный тест нужен.

Авторы основы: Players Patch team; 2.3Test — Fear/Novaras и участники проекта.
Карты сохраняют собственные авторские сведения.
https://steamcommunity.com/sharedfiles/filedetails/?id=1190476337
https://steamcommunity.com/sharedfiles/filedetails/?id=1413859511
https://github.com/Novaras/2.3-Test

'''+readme.read_text(encoding='utf8'),encoding='utf8')
    expected={'package-id.txt','VastReachesMiniCampaign.big','English.big','Russian.big','start_campaign.ps1','Vast Reaches Campaign Demo.cmd','README.txt','SHA256SUMS.txt'}
    if cinematics:expected.add('Movies')
    assert {p.name for p in PACKAGE.iterdir()}<=expected,'Unexpected files in release'
    manifest=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(PACKAGE).as_posix() for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt']
    (PACKAGE/'SHA256SUMS.txt').write_text('\n'.join(manifest)+'\n',encoding='utf8')
    archive=PACKAGE.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PACKAGE.rglob('*')):
            if p.is_file():z.write(p,PACKAGE.name+'/'+p.relative_to(PACKAGE).as_posix())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps({'folder':str(PACKAGE),'zip':str(archive),'files':sum(p.is_file() for p in PACKAGE.rglob('*')),'movies':sum(p.suffix=='.webm' for p in PACKAGE.rglob('*')),'zip_bytes':archive.stat().st_size},ensure_ascii=False))


if __name__=='__main__':
    from build_mod_layers import package as package_layers
    package_layers()
