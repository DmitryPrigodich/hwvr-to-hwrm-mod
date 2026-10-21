"""Merge reviewed translations and prepare deterministic HWRM UCS bindings."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'campaign-export'


def main():
    en = json.loads((ROOT/'localization/source/campaign-en.json').read_text(encoding='utf8'))
    ru = {}
    for part in ('early', 'late', 'shared'):
        rows = json.loads((ROOT/f'localization/ru/{part}.json').read_text(encoding='utf8'))
        assert not (ru.keys() & rows.keys()), f'Duplicate keys in {part}'
        ru.update(rows)
    assert en.keys() == ru.keys(), (en.keys()-ru.keys(), ru.keys()-en.keys())
    for key, text in ru.items():
        assert text.strip() and text != en[key], key
        assert re.findall(r'\d+', text) == re.findall(r'\d+', en[key]), key
        assert re.findall(r'\{[^{}]+\}', text) == re.findall(r'\{[^{}]+\}', en[key]), key
    (ROOT/'localization/ru/campaign.json').write_text(json.dumps(ru, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    extras = {
        'export_campaign': ('Vast Reaches Campaign Demo', 'Vast Reaches Campaign Demo'),
        'export_choose': ('Choose chapter', 'Выбрать главу'),
        'export_description': ('Campaign preparation build: manual validation pending.', 'Подготовительная сборка кампании: предстоит совместная проверка.'),
    }
    texts = {key: (en[key], ru[key]) for key in en}
    texts.update(extras)
    manifest = {key: {'id': 9960000+i, 'en': pair[0], 'ru': pair[1]} for i, (key, pair) in enumerate(sorted(texts.items()))}
    (OUT/'manifests').mkdir(parents=True, exist_ok=True)
    (OUT/'manifests/localization.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    with (ROOT/'localization/campaign-en-ru.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer=csv.writer(f); writer.writerow(['key','EN_original','RU_reviewed'])
        writer.writerows((k,en[k],ru[k]) for k in en)
    for locale, column in [('English','en'),('Russian','ru')]:
        path=OUT/f'data/locale/{locale}/vre_campaign.ucs'; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('\n'.join(f'{v["id"]}\t{v[column].replace(chr(10)," ")}' for v in manifest.values())+'\n', encoding='utf-16')
    locale=OUT/'data/locale/localedat.lua'
    original=(ROOT/'local/hwrm-base/locale/localedat.lua').read_text()
    locale.write_text(original[:original.rfind('}')]+'    {name="vre_campaign.dat"},\n}\n',encoding='ascii')
    script=OUT/'data/scripts/VRE_Text.lua'; script.parent.mkdir(parents=True,exist_ok=True)
    script.write_text('-- Generated from reviewed EN/RU campaign text. Audio bindings: VRE_Dialogue.lua.\nVRE_Text = {}\nVRE_Duration = {}\n'+''.join(f'VRE_Text["{k}"] = "${v["id"]}"\n' for k,v in manifest.items())+'\nfunction VRE_PlayLine(key)\n    local duration = VRE_Duration[key] or 8\n    if VRE_AudioDuration and VRE_AudioDuration[key] then duration = VRE_AudioDuration[key] + 0.5 end\n    Subtitle_Message(VRE_Text[key] or key, duration)\nend\n',encoding='ascii')
    print(json.dumps({'reviewed_strings':len(ru),'ucs_strings':len(manifest),'range':[min(v['id'] for v in manifest.values()),max(v['id'] for v in manifest.values())]}))


if __name__=='__main__':main()
