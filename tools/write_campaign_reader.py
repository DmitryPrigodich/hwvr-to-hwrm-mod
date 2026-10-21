"""Reading edition from the audited graph order, with optional original voice cues."""
import html
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'campaign-export'


def main():
    text=json.loads((OUT/'manifests/localization.json').read_text(encoding='utf8'))
    dialogue={r['key']:r for r in json.loads((OUT/'manifests/dialogue.json').read_text(encoding='utf8'))}
    characters={c['id']:c for c in json.loads((OUT/'manifests/characters.json').read_text(encoding='utf8'))}
    previews=json.loads((OUT/'manifests/loading.json').read_text(encoding='utf8'))
    source=(ROOT/'docs/QUEST_SCENARIOS.md').read_text(encoding='utf8').splitlines()
    sections=[];current=None
    for line in source:
        if line.startswith('## '):
            if 'Полнота и ограничения' in line:break
            current={'title':line[3:],'items':[]};sections.append(current)
        elif current is not None:
            if line.startswith('### '):current['items'].append(('heading',line[4:]))
            elif line.startswith('*Есть независимые') or line.startswith('*Изолированный') or line.startswith('Общий пролог'):current['items'].append(('note',line.strip('*')))
            else:
                key=re.fullmatch(r'`([^`]+)`',line)
                if key and key[1] in text:current['items'].append(('line',key[1]))
    assert len(sections)==12
    en_ru=['# Vast Reaches: сценарий для чтения','',
        'Новый русский перевод, английский оригинал для сверки. Порядок: **пролог → обучение → M1 → M7 → M3 → M4 → M5 → M6 → M9 → M10 → M11 → M8 → M13 → эпилог**. Внутренние номера сохранены из игры.','',
        'Развилки и общие тревоги условны: напечатанные рядом строки не обязательно звучат подряд. Подробные условия, ID узлов и исходные ссылки — в [QUEST_SCENARIOS.md](QUEST_SCENARIOS.md); составы флота — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).','']
    title='Vast Reaches — сценарий'
    chunks=['<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title>',
    '<style>body{margin:0;background:#10151b;color:#e0e6e9;font:18px/1.6 system-ui,sans-serif}nav{position:fixed;inset:0 auto 0 0;width:230px;padding:24px;overflow:auto;background:#18212a;box-sizing:border-box}nav a{display:block;margin:12px 0;color:#a8d1d6;text-decoration:none;font-size:14px}main{max-width:900px;margin:0 auto 0 260px;padding:38px}h1,h2,h3{line-height:1.25;color:#fff}h2{padding-top:35px;border-top:1px solid #43515c}h3{color:#acced6;margin-top:38px}.line{position:relative;padding:15px 0;border-bottom:1px solid #28333e;min-height:50px}.head{width:64px;height:64px;object-fit:contain;float:left;margin:5px 16px 5px 0}.speaker{color:#d3bc94;font-size:15px}.ru{margin:6px 0 12px}.key{font:12px monospace;color:#8295a4}details{color:#91a8ba;font-size:15px;clear:both}summary{cursor:pointer}audio{height:32px;max-width:100%;width:350px;margin-top:8px}.cover{width:100%;height:auto;border-radius:4px}.note{padding:12px;border-left:3px solid #b08a4f;background:#29261f;font-size:15px}a{color:#9bd4df}@media(max-width:800px){nav{position:relative;width:auto}nav a{display:inline-block;margin:4px 10px 4px 0}main{margin:0;padding:20px}}</style><nav><strong>Vast Reaches</strong>']
    for i,section in enumerate(sections):chunks.append(f'<a href="#chapter{i}">{html.escape(section["title"].split(" / ")[0])}</a>')
    chunks+=['</nav><main><h1>'+title+'</h1><p>Новый русский перевод. EN раскрывается под репликой; аудио — исходная английская озвучка. Воспроизведение только по нажатию.</p><p class="note">Это сценарий для чтения и сверки. Условные ветви не составляют одну обязательную последовательность. Кнопки звука здесь не означают, что озвучка уже подключена в HWRM.</p>']
    count=0
    for i,section in enumerate(sections):
        en_ru+=['## '+section['title'],''];chunks.append(f'<section id="chapter{i}"><h2>{html.escape(section["title"])}</h2>')
        image=previews[i]['image']
        if image:chunks.append('<img class="cover" src="'+image['path']+'" alt="Исходное изображение главы">')
        for kind,value in section['items']:
            if kind=='heading':
                en_ru+=['### '+value,''];chunks.append('<h3>'+html.escape(value)+'</h3>')
            elif kind=='note':
                en_ru+=['*'+value+'*',''];chunks.append('<p class="note">'+html.escape(value)+'</p>')
            else:
                key=value;entry=text[key];line=dialogue.get(key);char=None
                if line and len(line['character_ids'])==1:char=characters[line['character_ids'][0]]
                speaker=char['ru'] if char else 'Задача'
                en_ru += [f'**{speaker}**', '', entry['ru'],'','<details><summary>EN · '+key+'</summary>','', '> '+entry['en'].replace('\n','\n> '),'','</details>','']
                chunks.append('<article class="line">')
                if char and char['portrait']:chunks.append('<img class="head" alt="" src="'+char['portrait']['path']+'">')
                chunks += ['<div class="speaker">'+html.escape(speaker)+'</div>','<p class="ru">'+html.escape(entry['ru']).replace('\n','<br>')+'</p>','<details><summary>EN · <span class="key">'+html.escape(key)+'</span></summary><p>'+html.escape(entry['en'])+'</p></details>']
                if line and line['english_audio']:chunks.append('<audio controls preload="none" src="'+line['english_audio']['wav']+'"></audio>')
                elif line:chunks.append('<div class="key">Звук для этой строки не найден в каталогах Quest/Steam.</div>')
                chunks.append('</article>');count+=1
        chunks.append('</section>')
    chunks.append('<footer><p>Источник: Quest 1.1.0-16520. Тексты обучения и миссий сверены со Steam. Перевод: localization/ru/campaign.json; привязки: manifests/dialogue.json. Обучение поставлено перед M1 по запросу Дмитрия.</p></footer></main></html>')
    (OUT/'index.html').write_text('\n'.join(chunks),encoding='utf8')
    (ROOT/'docs/CAMPAIGN_READING_RU.md').write_text('\n'.join(en_ru)+'\n',encoding='utf8')
    print(json.dumps({'chapters':len(sections),'text_entries':count,'html':str(OUT/'index.html')},ensure_ascii=False))


if __name__=='__main__':main()
