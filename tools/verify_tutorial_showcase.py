"""Check the handoff and exercise its installer only against a temporary fake game.

Never launches an executable or writes to the real Homeworld installation.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import uuid

from build_tutorial_showcase import PROJECT,WORK,RELEASE,ZIP,IDENTITY


def verify():
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    sums={name:digest for digest,name in (line.split('  ',1) for line in (RELEASE/'SHA256SUMS.txt').read_text().splitlines())}
    assert sums=={p.relative_to(RELEASE).as_posix():sha(p) for p in RELEASE.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'}
    setup=RELEASE/'Setup.ps1'
    def run(*args,success=True):
        proc=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(setup),*map(str,args)],capture_output=True,text=True)
        if success:assert proc.returncode==0,proc.stdout+proc.stderr
        else:assert proc.returncode!=0
        return proc
    run('-VerifyOnly')
    # Inherit workspace ACLs; mkdtemp's owner-only DACL breaks restricted tokens.
    temp=(WORK/('setup-smoke-'+uuid.uuid4().hex)).resolve()
    assert temp.is_relative_to(WORK.resolve())
    temp.mkdir()
    try:
        game=temp/'Homeworld';backup=temp/'backups'
        exe=game/'HomeworldRM/Bin/Release/HomeworldRM.exe';exe.parent.mkdir(parents=True);exe.write_bytes(b'Not executable; installer test only.')
        other=game/'HomeworldRM/DataWorkshopMODs/OtherMod/sentinel.txt';other.parent.mkdir(parents=True);other.write_text('preserve me')
        args=['-GameRoot',game,'-BackupRoot',backup]
        plan=json.loads(run(*args,'-PlanOnly').stdout)
        assert plan['Launch'] is False and 'VastReachesTutorial' in plan['Mod']
        assert plan['Arguments'][-5:]==['-windowed','-w','1600','-h','900']
        assert not Path(plan['Mod']).exists() and not backup.exists()
        plan_en=json.loads(run(*args,'-PlanOnly','-Language','English','-Fullscreen').stdout)
        assert 'English' in plan_en['Arguments'] and '-fullscreen' in plan_en['Arguments']
        run(*args)
        mod=Path(plan['Mod']);movies=Path(plan['Movies'])
        for source in (RELEASE/'payload').rglob('*'):
            if not source.is_file():continue
            relative=source.relative_to(RELEASE/'payload')
            target=movies/Path(*relative.parts[1:]) if relative.parts[0]=='Movies' else mod/relative
            assert sha(source)==sha(target),relative
        assert other.read_text()=='preserve me' and not backup.exists()
        # Launching the helper again with the same version must not move a package.
        before=(mod/'VastReachesTutorial.big').stat().st_mtime_ns
        run(*args)
        assert before==(mod/'VastReachesTutorial.big').stat().st_mtime_ns and not backup.exists()
        # Never adopt an unowned folder, even if it otherwise resembles this mod.
        marker=mod/'showcase-id.txt';marker.write_text('another owner\n')
        run(*args,success=False)
        assert marker.read_text()=='another owner\n' and not backup.exists()
        marker.write_text(IDENTITY+'\n')
        (mod/'config.txt').write_text('previous owned version\n')
        run(*args)
        copies=list(backup.iterdir());assert len(copies)==1
        assert (copies[0]/'Mod/config.txt').read_text()=='previous owned version\n'
        assert (copies[0]/'Movies/showcase-id.txt').is_file()
        assert sha(mod/'config.txt')==sha(RELEASE/'payload/config.txt')
        assert other.read_text()=='preserve me'
    finally:
        assert temp.is_relative_to(WORK.resolve())
        shutil.rmtree(temp)
    report={'status':'passed','checksums':len(sums),'powershell_5_1_verify_only':True,
            'install_into_fake_game':True,'same_version_idempotent':True,'unowned_folder_rejected':True,
            'owned_package_backed_up_outside_fake_game':True,'unrelated_mod_preserved':True,
            'ru_en_and_window_launch_plans':True,'real_game_installed':False,'game_launched':False,
            'zip_bytes':ZIP.stat().st_size,'zip_sha256':sha(ZIP)}
    (WORK/'handoff-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':verify()
