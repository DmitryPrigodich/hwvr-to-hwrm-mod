"""Prepare an optional, reversible HWLauncher local-slot registration.

Default action only writes workspace/local. Install/restore are explicit actions;
neither action runs the launcher/game or calls Steam/Workshop.
"""
import argparse
import csv
import hashlib
import io
import json
import shutil
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
IDENTITY = 'VastReachesMiniCampaign-local-launcher-slot-v1'
TITLE = 'Vast Reaches Campaign Demo'
ARCHIVE = 'VastReachesMiniCampaign.big'
SLOT = Path('HomeworldRM/DataWorkshopMODs/Gearbox/BananaMothership')
DEFAULT_GAME = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld')
MENU_ARGUMENTS = '-locale Russian -fullscreen'
PAYLOAD_FILES = ('config.txt', 'preview.jpg', ARCHIVE, 'English.big', 'Russian.big')


def sha(path):
    path = Path(path)
    if not path.is_file():
        return None
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def config_values(path):
    result = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        text = line.strip()
        if not text or text.startswith('//'):
            continue
        if ':' in text:
            key, value = text.split(':', 1)
            if key.lower() == 'description':
                break
            result[key.lower()] = value.strip()
    return result


def check_workspace_output(path):
    path = path.resolve()
    if not path.is_relative_to((PROJECT / 'local').resolve()):
        raise RuntimeError('Registration output must remain inside this project/local.')
    if path.exists() and any(path.iterdir()):
        marker = path / 'registration-plan.json'
        if not marker.is_file() or load(marker).get('identity') != IDENTITY:
            raise RuntimeError('Unknown registration output directory; refusing to merge.')
    return path


def prepare(output):
    from PIL import Image, ImageDraw, ImageFont
    archive = PROJECT / 'local' / ARCHIVE
    if not archive.is_file():
        raise RuntimeError('Build the mini-campaign archive before preparing registration.')
    output.mkdir(parents=True, exist_ok=True)
    for language in ('English','Russian'):
        shutil.copy2(PROJECT/f'local/{language}.big',output/(language+'.big'))
    (output / 'config.txt').write_text(
        '// Optional local HWLauncher slot. Original BananaDLC.big is preserved.\n'
        f'Title: {TITLE}\nTags: HomeworldRM Campaign Local\n'
        f'GameType: HomeworldRM\nModType: MOD\nBigFilename: {ARCHIVE}\n'
        'WorkshopID: 0\nDescription:\n'
        'Local script prototype: training, Proving Grounds and Lost Destroyer.\n'
        'Mods > Remastered > select this mod > Launch. No campaign checkboxes needed.\n'
        'In game: Extra Missions > Vast Reaches Campaign Demo.\n'
        'Not published to Steam Workshop.\n', encoding='ascii')
    image = Image.new('RGB', (960, 540), '#091323')
    draw = ImageDraw.Draw(image)
    font_path = Path('C:/Windows/Fonts/arial.ttf')
    font = lambda size: ImageFont.truetype(str(font_path), size) if font_path.is_file() else ImageFont.load_default()
    draw.rectangle((58, 72, 902, 78), fill='#db8a42')
    draw.text((58, 113), 'VAST REACHES', font=font(60), fill='#eaf1fa')
    draw.text((60, 192), 'CAMPAIGN DEMO', font=font(34), fill='#db8a42')
    draw.text((60, 253), 'HOMEWORLD REMASTERED', font=font(24), fill='#a5b7cc')
    for x, label in [(60, 'T1  TRAINING'), (348, 'M1  PROVING GROUNDS'), (650, 'M4  LOST DESTROYER')]:
        draw.rectangle((x, 350, x + 248, 426), outline='#4d6580', width=2)
        draw.text((x + 13, 376), label, font=font(18), fill='#eaf1fa')
    draw.text((60, 476), 'LOCAL SCRIPT PROTOTYPE  /  NO WORKSHOP UPLOAD', font=font(18), fill='#a5b7cc')
    image.save(output / 'preview.jpg', quality=94)
    shutil.copy2(archive, output / ARCHIVE)
    (output / 'launcher-arguments.txt').write_text(MENU_ARGUMENTS + '\n', encoding='ascii')
    (output / 'launch_mod_menu.ps1').write_text(
        "param([string]$GameRoot='C:\\Program Files (x86)\\Steam\\steamapps\\common\\Homeworld',[switch]$PrintOnly)\n"
        "$ErrorActionPreference='Stop'\n"
        "$exe=Join-Path $GameRoot 'HWLauncher\\Launcher.exe'\n"
        "if (-not (Test-Path -LiteralPath $exe)) { throw 'Official HWLauncher not found.' }\n"
        f"$arguments='{MENU_ARGUMENTS}'\n"
        "if ($PrintOnly) { Write-Output ($exe+' '+$arguments); return }\n"
        "if (Get-Process -Name Launcher,HomeworldRM -ErrorAction SilentlyContinue) { throw 'Close the current launcher/game first.' }\n"
        "# Running this starter explicitly requests the interactive official mod menu.\n"
        "Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory (Split-Path $exe)\n",
        encoding='utf8')
    plan = dict(identity=IDENTITY, title=TITLE, target_relative=SLOT.as_posix(),
                menu_arguments=MENU_ARGUMENTS, files={name: sha(output / name) for name in PAYLOAD_FILES},
                source_archive=str(archive), source_archive_sha256=sha(archive),
                installation='Optional reversible replacement of the hardcoded local BananaMothership launcher slot.',
                preserved='BananaDLC.big is never changed. No Workshop upload, subscription or executable patch.')
    save(output / 'registration-plan.json', plan)
    return plan


def process_guard():
    result = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'], check=True, text=True, capture_output=True)
    for row in csv.reader(io.StringIO(result.stdout)):
        if row and row[0].lower() in ('launcher.exe', 'homeworldrm.exe'):
            raise RuntimeError('Close HWLauncher and HomeworldRM before changing the local slot.')


def target_slot(game):
    root = game.resolve()
    slot = (root / SLOT).resolve()
    if not slot.is_relative_to(root):
        raise RuntimeError('Resolved slot escapes the requested game directory.')
    if not (root / 'HWLauncher/Launcher.exe').is_file() or not (slot / 'BananaDLC.big').is_file():
        raise RuntimeError('Expected official launcher and BananaDLC.big were not found.')
    return slot


def checked_plan(output):
    plan = load(output / 'registration-plan.json')
    if plan['identity'] != IDENTITY or plan['target_relative'] != SLOT.as_posix():
        raise RuntimeError('Unknown registration plan.')
    if set(plan['files']) != set(PAYLOAD_FILES):
        raise RuntimeError('Registration file list changed.')
    if sha(PROJECT / 'local' / ARCHIVE) != plan['source_archive_sha256']:
        raise RuntimeError('The mini-campaign archive was rebuilt; run prepare again before installation.')
    for name, digest in plan['files'].items():
        if sha(output / name) != digest:
            raise RuntimeError(f'Prepared payload changed: {name}')
    expected = {'title': TITLE, 'gametype': 'HomeworldRM', 'modtype': 'MOD', 'bigfilename': ARCHIVE, 'workshopid': '0'}
    config = config_values(output / 'config.txt')
    if any(config.get(k) != value for k, value in expected.items()):
        raise RuntimeError('Prepared launcher config has unexpected values.')
    return plan


def check_state(state, slot, output):
    if state.get('identity') != IDENTITY or Path(state['target']).resolve() != slot:
        raise RuntimeError('Backup state belongs to a different registration target.')
    if sha(slot / 'BananaDLC.big') != state['banana_sha256']:
        raise RuntimeError('Original BananaDLC.big changed; refusing to proceed.')
    for name, info in state['files'].items():
        if name not in PAYLOAD_FILES:
            raise RuntimeError('Unknown file in backup state.')
        if info['before'] is not None and sha(output / 'backup' / name) != info['before']:
            raise RuntimeError(f'Backup missing or changed: {name}')
        if sha(slot / name) not in (info['before'], info['after'], info.get('previous', info['after'])):
            raise RuntimeError(f'Launcher slot contains outside edits: {name}')


def copy_atomic(source, destination):
    pending = destination.with_name(destination.name + '.vast-reaches-pending')
    shutil.copy2(source, pending)
    pending.replace(destination)


def install(output, game):
    plan = checked_plan(output)
    slot = target_slot(game)
    process_guard()
    state_file = output / 'slot-backup.json'
    if state_file.exists():
        state = load(state_file)
        check_state(state, slot, output)
        # Adopt only the two newly supplied locale files, preserving any
        # pre-existing bytes before extending the owned payload list.
        for name in PAYLOAD_FILES:
            if name not in state['files']:
                if name not in ('English.big','Russian.big'):
                    raise RuntimeError('Unexpected registration payload migration.')
                digest=sha(slot/name)
                if digest is not None:
                    backup=output/'backup'/name
                    if backup.exists():raise RuntimeError('Locale backup already exists.')
                    shutil.copy2(slot/name,backup)
                state['files'][name]=dict(before=digest,after=digest)
    else:
        original = config_values(slot / 'config.txt')
        if original.get('modtype', '').lower() != 'banana' or original.get('bigfilename') != 'BananaDLC.big':
            raise RuntimeError('Local slot is not the original Banana entry; refusing to replace it.')
        if (slot / ARCHIVE).exists():
            raise RuntimeError('Unknown mini-campaign archive already occupies the local slot.')
        backup = output / 'backup'
        backup.mkdir(exist_ok=True)
        state = dict(identity=IDENTITY, target=str(slot), banana_sha256=sha(slot / 'BananaDLC.big'), files={})
        for name in PAYLOAD_FILES:
            digest = sha(slot / name)
            if digest is not None:
                shutil.copy2(slot / name, backup / name)
            state['files'][name] = dict(before=digest, after=plan['files'][name])
    # Persist complete recovery information before the first target mutation.
    for name in PAYLOAD_FILES:
        state['files'][name]['previous'] = state['files'][name]['after']
        state['files'][name]['after'] = plan['files'][name]
    state['phase'] = 'installing'
    save(state_file, state)
    for name in PAYLOAD_FILES:
        copy_atomic(output / name, slot / name)
    check_state(state, slot, output)
    if any(sha(slot / name) != plan['files'][name] for name in PAYLOAD_FILES):
        raise RuntimeError('Installed payload hash mismatch.')
    state['phase'] = 'installed'
    save(state_file, state)
    return dict(status='installed', title=TITLE, folder=str(slot), banana_unchanged=True)


def restore(output, game):
    slot = target_slot(game)
    process_guard()
    state_file = output / 'slot-backup.json'
    state = load(state_file)
    check_state(state, slot, output)
    for name, info in state['files'].items():
        target = slot / name
        if info['before'] is None:
            if target.exists():
                target.unlink()  # One exact owned file, hash checked above; never recursive.
        elif sha(target) != info['before']:
            copy_atomic(output / 'backup' / name, target)
    if any(sha(slot / name) != info['before'] for name, info in state['files'].items()):
        raise RuntimeError('Restored slot hash mismatch.')
    if sha(slot / 'BananaDLC.big') != state['banana_sha256']:
        raise RuntimeError('Original Banana archive hash mismatch.')
    state['phase'] = 'restored'
    save(state_file, state)
    return dict(status='restored', folder=str(slot), banana_unchanged=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'verify', 'install', 'restore'), nargs='?', default='prepare')
    parser.add_argument('--output', type=Path, default=PROJECT / 'local/launcher-mod-registration')
    parser.add_argument('--game-root', type=Path, default=DEFAULT_GAME)
    args = parser.parse_args()
    output = check_workspace_output(args.output)
    if args.action == 'prepare':
        result = prepare(output)
    elif args.action == 'verify':
        result = dict(status='verified', **checked_plan(output))
    elif args.action == 'install':
        result = install(output, args.game_root)
    else:
        result = restore(output, args.game_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
