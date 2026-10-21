"""Read the supplied APK/OBB, joining Unity split data inside this workspace."""
import json
import re
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

PROJECT=Path(__file__).resolve().parent.parent
INPUT=Path(r'G:\Games\HW_Games\Homeworld- Vast Reaches v16520+1.1.0-16520 -VRP')
GAME=PROJECT/'local/quest-content'
DATA=GAME/'HomeworldVastReachesDemo_Data'


def main():
    DATA.mkdir(parents=True,exist_ok=True)
    archives=[INPUT/'com.farbridge.vastreaches.apk',next((INPUT/'com.farbridge.vastreaches').glob('*.obb'))]
    grouped=defaultdict(list)
    zips=[zipfile.ZipFile(p) for p in archives]
    for zi,z in enumerate(zips):
        for item in z.infolist():
            name=item.filename
            if name.startswith('assets/bin/Data/'):
                relative=name.removeprefix('assets/bin/Data/')
                if relative.startswith(('Managed/','UnitySubsystems/')):continue
            elif name.startswith('assets/aa/') and name.endswith(('.bundle','.json','.xml')):
                relative='StreamingAssets/'+name.removeprefix('assets/')
            elif name.endswith('SoundbanksInfo.xml'):
                relative='StreamingAssets/'+name.removeprefix('assets/')
            else:continue
            if item.is_dir():continue
            match=re.search(r'\.split(\d+)$',relative)
            index=int(match[1]) if match else -1
            if match:relative=relative[:match.start()]
            target=(DATA/relative).resolve()
            assert target.is_relative_to(DATA.resolve()),relative
            grouped[relative].append((index,zi,item))
    report=[]
    for relative,parts in sorted(grouped.items()):
        parts.sort()
        numbers=[p[0] for p in parts]
        assert len(set(numbers))==len(numbers),(relative,numbers)
        if numbers!=[-1]:assert numbers==list(range(len(parts))),(relative,numbers)
        target=DATA/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        expected=sum(item.file_size for index,zi,item in parts)
        if not target.exists() or target.stat().st_size!=expected:
            with target.open('wb') as out:
                for index,zi,item in parts:
                    with zips[zi].open(item) as src:shutil.copyfileobj(src,out,1024*1024)
        report.append({'file':relative,'bytes':expected,'parts':len(parts)})
    for z in zips:z.close()
    (GAME/'unpack-index.json').write_text(json.dumps({'archives':[str(p) for p in archives],'files':report},indent=2)+'\n',encoding='utf8')
    print(json.dumps({'files':len(report),'bytes':sum(p['bytes'] for p in report),'directory':str(DATA)}))


if __name__=='__main__':main()
