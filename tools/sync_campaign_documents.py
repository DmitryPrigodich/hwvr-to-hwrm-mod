"""Refresh current reading texts, preserve hand-written mission notes and RAW.

This updates project documents only. It never builds, installs or launches HWRM.
Use --check to verify the existing documents without regenerating anything.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from campaign_text_review import ROOT, REVIEW, review_label, review_notice

DOSSIERS = ['docs/missions/T01_Training.md', 'docs/missions/M01_ProvingGrounds.md']
SCRIPT_DOCS = ['docs/QUEST_SCENARIOS.md', 'docs/DEMO_SCENARIOS.md']
HEADER = re.compile(r'^\*\*[^\n]+\*\* — `([^`]+)`$', re.M)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocks(text):
    headers = list(HEADER.finditer(text))
    for i, match in enumerate(headers):
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        yield match[1], text[match.end():end]


def stamp(path, relative_link):
    text = path.read_text(encoding='utf8')
    text = re.sub(r'\n*<!-- translation-sync:start -->.*?<!-- translation-sync:end -->\n*', '\n\n', text, flags=re.S)
    heading, rest = text.split('\n', 1)
    text = heading + '\n\n<!-- translation-sync:start -->\n' + review_notice(relative_link) + '\n<!-- translation-sync:end -->\n\n' + rest.lstrip('\n')
    path.write_text(text, encoding='utf8')


def update_dossier(path, ru):
    text = path.read_text(encoding='utf8')
    text = re.sub(r'\n\n<!-- approved-line:[^>]+ -->\n\*[^\n]*\*', '', text)
    pattern = re.compile(r'(^\*\*[^\n]+\*\* — `([^`]+)`[\s\S]*?^\*\*RU, новый:\*\* )([^\n]+)', re.M)
    def replace(match):
        key = match[2]
        if key not in ru:
            return match[0]
        label = review_label(key, ru[key])
        note = '\n\n<!-- approved-line:'+key+' -->\n*'+label+'*' if label else ''
        return match[1] + ru[key] + note
    path.write_text(pattern.sub(replace, text), encoding='utf8')
    stamp(path, '../TRANSLATION_REVIEW.md')


def write_review(ru, en):
    lines = ['# Перевод: внесённые правки', '',
             'Обновлено ' + REVIEW['date_label'] + '. Ниже — текущие формулировки после замечаний Дмитрия. '
             'Это изменения текста; установка новой сборки учитывается отдельно в [состоянии кампании](CAMPAIGN_README.md).', '',
             'Название главы: **M0. Обучение / M0. Tutorial**. Внутренний ID `T01_Training` сохранён.', '']
    for key, row in REVIEW['lines'].items():
        lines += ['## ' + row['note'], '', '`'+key+'`', '', '**RU сейчас:** '+ru[key], '',
                  '*'+review_label(key, ru[key])+'*', '', '<details><summary>English original</summary>', '',
                  en[key], '', '</details>', '']
    lines += ['## Как обновляем дальше', '',
              'Редактируем соответствующую часть в `localization/ru/early.json`, `late.json` или `shared.json`; '
              '`campaign.json` — объединённый результат. Согласованные изменения отмечаем в `localization/reviewed_changes.json`.', '',
              'Синхронизация: `.venv\\Scripts\\python.exe -X utf8 tools/sync_campaign_documents.py`. '
              'Проверка без изменения файлов: та же команда с `--check`.', '',
              'Команда обновляет сценарии, HTML и текущие RU-блоки разборов миссий, сохраняя ручные заметки. '
              'RAW и буквальный EN не переписываются. Игра и установленные файлы мода не затрагиваются.', '']
    (ROOT/'docs/TRANSLATION_REVIEW.md').write_text('\n'.join(lines), encoding='utf8')


def check(ru):
    counts = {}
    for name in DOSSIERS:
        count = 0
        for key, block in blocks((ROOT/name).read_text(encoding='utf8')):
            match = re.search(r'^\*\*RU, новый:\*\* (.+)$', block, re.M)
            if match and key in ru:
                assert match[1] == ru[key], (name, key, 'stale translation')
                count += 1
        assert count, name
        counts[name] = count
    for name in SCRIPT_DOCS:
        text = (ROOT/name).read_text(encoding='utf8')
        if 'QUEST_' in name:
            entries=((m[1],m[2]) for m in re.finditer(r'^`([^`]+)`\n\nRU:\n\n((?:>[^\n]*(?:\n|$))+)',text,re.M))
        else:
            entries=((key,match[1]) for key,block in blocks(text)
                     if (match:=re.search(r'\*RU — новый перевод:\*\n\n((?:>[^\n]*(?:\n|$))+)',block)))
        count=0
        for key,quote in entries:
            if key not in ru:continue
            current='\n'.join(line[2:] for line in quote.rstrip('\n').splitlines())
            assert current==ru[key],(name,key,'stale translation')
            count+=1
        assert count,name
        for key in REVIEW['lines']:
            assert ru[key] in text, (name, key)
        counts[name] = count
    html = (ROOT/'campaign-export/index.html').read_text(encoding='utf8')
    import html as html_module
    count=0
    for article in re.findall(r'<article class="line">(.*?)</article>',html,re.S):
        key=re.search(r'<span class="key">([^<]+)</span>',article)[1]
        current=re.search(r'<p class="ru">(.*?)</p>',article,re.S)[1]
        current=html_module.unescape(current.replace('<br>','\n'))
        assert current==ru[key],('HTML',key,'stale translation')
        count+=1
    assert count
    counts['campaign-export/index.html']=count
    for key in REVIEW['lines']:
        assert html_module.escape(ru[key]) in html, key
    assert 'Внесена правка пользователя' in html
    assert 'M0. Обучение' in html
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    protected = [*sorted((ROOT/'localization/source').glob('*.json')),
                 *sorted((ROOT/'docs/archive/source-localization').glob('*_RAW.md'))]
    assert len([p for p in protected if p.name.endswith('_RAW.md')])==2
    before = {p: digest(p) for p in protected}
    if not args.check:
        for tool in ('prepare_campaign_localization.py', 'write_quest_scenarios.py', 'write_demo_scenarios.py', 'write_campaign_glossary.py'):
            subprocess.run([sys.executable, '-X', 'utf8', str(ROOT/'tools'/tool)], cwd=ROOT, check=True)
    ru = json.loads((ROOT/'localization/ru/campaign.json').read_text(encoding='utf8'))
    merged={}
    for part in ('early','late','shared'):
        rows=json.loads((ROOT/f'localization/ru/{part}.json').read_text(encoding='utf8'))
        assert not merged.keys() & rows.keys(),part
        merged.update(rows)
    assert merged==ru,'Merged campaign.json does not match the canonical RU parts; run synchronization.'
    en = json.loads((ROOT/'localization/source/campaign-en.json').read_text(encoding='utf8'))
    if not args.check:
        write_review(ru, en)
        for name in DOSSIERS:
            update_dossier(ROOT/name, ru)
        for name in SCRIPT_DOCS:
            stamp(ROOT/name, 'TRANSLATION_REVIEW.md')
        subprocess.run([sys.executable, '-X', 'utf8', str(ROOT/'tools/write_campaign_reader.py')], cwd=ROOT, check=True)
        stamp(ROOT/'docs/CAMPAIGN_READING_RU.md', 'TRANSLATION_REVIEW.md')
    result = {'status': 'passed', 'checked': check(ru), 'raw_and_literal_en_unchanged': all(digest(p)==value for p, value in before.items()),
              'reviewed_changes': len(REVIEW['lines']), 'game_files_modified': False}
    assert result['raw_and_literal_en_unchanged']
    output = ROOT/'local/documentation-cleanup-20261021/translation-verification.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
