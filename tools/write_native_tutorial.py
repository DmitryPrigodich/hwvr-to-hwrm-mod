"""Audit the installed HWRM tutorial as data, without running the game.

Lua tables are evaluated with pure data helpers only. OnInit and mission rules
are never called. Literal scheduling links distinguish reachable lessons from
old commented/unused sections, including the Remastered subsystem bypass.
"""
import collections
import html
import json
import re
from pathlib import Path
from lupa.lua51 import LuaRuntime, lua_type
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'local/hwrm-base'
OUT=ROOT/'docs/native-tutorial'
LOCAL=ROOT/'local/native-tutorial'
TITLES=['Камера, интерфейс и перемещение','Ресурсы, постройка, исследования и атака','Группы, бой, способности и захват']
EVENT_ORDER={
1:'''intelevent_SetupWorld intelevent_intro intelevent_intro_taskbar_active intelevent_intro_recall intelevent_intro_recall_active intelevent_intro_objectives intelevent_intro_active intelevent_introContinue intelevent_introContinue_active intelevent_selection intelevent_dragselection intelevent_dragselection_active intelevent_rotate dialogevent_rotated intelevent_zooming intelevent_zoomingChecked intelevent_panning intelevent_panned_little intelevent_focus intelevent_focus_active dialogevent_basics_end intelevent_sensors intelevent_sensors2 intelevent_ATI intelevent_sensors2_active intelevent_movement intelevent_movement_active intelevent_relativemove intelevent_relativemoveIssued intelevent_relativemove2 intelevent_movedisc intelevent_movediscdone intelevent_movedisc3D intelevent_movedisc3D_active intelevent_movedisc3D_shipSelected intelevent_movedisc3D_moveDiscActiveButLocked intelevent_movedisc3D_moveDiscActiveUnlocked intelevent_complete'''.split(),
2:'''intelevent_intro intelevent_harvest_active intelevent_researchmodule intelevent_researchmodule_buildactive intelevent_researchmodule_buildopened intelevent_building intelevent_researchselectedagainactive intelevent_researchmenu intelevent_techtree intelevent_unlockingtech intelevent_attacking intelevent_attackingReady intelevent_attackingReadyDrones intelevent_complete speechevent_bl'''.split(),
3:'''intelevent_controlgroups intelevent_controlgroups_active intelevent_group1 intelevent_focus intelevent_focus_active intelevent_attack intelevent_destroy_frigates intelevent_specialcommands intelevent_activatecloakingOpenSpecial intelevent_activatecloaking intelevent_uncloaking intelevent_capture intelevent_complete IntelEvent_Tactics IntelEvent_StikeGroups IntelEvent_StikeGroupsSelected IntelEvent_StikeGroupsStriked IntelEvent_Waypoints'''.split()}


def strip_comments(source):
    # Preserve quoted command strings and line numbers used by source links.
    token=re.compile(r'''('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|--\[\[.*?\]\]|--[^\n]*)''',re.S)
    return token.sub(lambda m:''.join('\n' if c=='\n' else ' ' for c in m[0]) if m[0].startswith('--') else m[0],source)


def strings(path):
    b=path.read_bytes()
    s=b.decode('utf-16') if b.startswith((b'\xff\xfe',b'\xfe\xff')) else b.decode('utf-8-sig',errors='strict')
    return {m[1]:m[2] for line in s.splitlines() if (m:=re.match(r'^(\d+)\s+(.+)$',line))}


def plain(value):
    if lua_type(value)=='table':
        keys=list(value.keys())
        if keys and all(isinstance(k,(int,float)) for k in keys):return [plain(value[k]) for k in sorted(keys)]
        return {str(k):plain(v) for k,v in value.items()}
    return value


def links(source):
    result=[]
    for call,name in re.findall(r'''\b(Rule_Add(?:Interval)?|Event_Start)\s*\(\s*["']([^"']+)["']''',source):
        result.append(('e:' if call=='Event_Start' else 'f:')+name)
    for name in re.findall(r'''UI_BindKeyEvent\s*\(\s*[^,]+,\s*["']([^"']+)["']''',source):result.append('f:'+name)
    return result


def main():
    OUT.mkdir(parents=True,exist_ok=True);LOCAL.mkdir(parents=True,exist_ok=True)
    reports=[];book=[]
    for n in [1,2,3]:
        code=f'm0{n}';path=BASE/f'leveldata/campaign/tutorial/{code}/{code}.lua';source=path.read_text();clean=strip_comments(source)
        lua=LuaRuntime(unpack_returned_tuples=True)
        lua.execute('''function dofilepath(...) end
function Universe_GameTime() return 0 end
Actor_FleetCommand="Actor_FleetCommand"
function HW2_SubTitleEvent(actor,text,time) return {kind="subtitle",actor=actor,text=text,time=time} end
function HW2_LocationCardEvent(text,time) return {kind="location",text=text,time=time} end
function HW2_Wait(time) return {kind="wait",time=time} end''')
        lua.execute(source) # define data/functions; never call OnInit/Rule_*.
        events=plain(lua.globals().Events);objectives=plain(lua.globals().objectives)
        marks=list(re.finditer(r'(?m)^function\s+(\w+)\s*\(|^Events\s*=|^Events\.(\w+)\s*=',clean))
        functions={};event_sources={}
        for i,m in enumerate(marks):
            body=clean[m.start():marks[i+1].start() if i+1<len(marks) else len(clean)]
            record={'source_line':source[:m.start()].count('\n')+1,'body':body,'links':links(body)}
            if m[1]:functions[m[1]]=record
            elif m[2]:event_sources[m[2]]=record
        reached=set();queue=['f:OnInit'];unknown=[]
        while queue:
            name=queue.pop(0)
            if name in reached:continue
            reached.add(name);kind,key=name.split(':',1)
            record=(functions if kind=='f' else event_sources).get(key)
            if not record:unknown.append(name);continue
            queue+=record['links']
            # Direct calls to locally defined helper functions, not engine APIs.
            queue+=['f:'+call for call in re.findall(r'\b(\w+)\s*\(',record['body']) if call in functions]
        active={key for key in events if 'e:'+key in reached}
        unused=set(events)-active
        en=strings(ROOT/f'local/english/leveldata/campaign/tutorial/{code}.dat')
        ru=strings(BASE/f'locale/russian/leveldata/campaign/tutorial/{code}.ucs')
        all_ids=set(re.findall(r'\$(\d+)',clean));missing={'en':sorted(all_ids-en.keys()),'ru':sorted(all_ids-ru.keys())}
        transcript=[]
        def walk(value,step):
            if isinstance(value,dict):
                if value.get('kind') in ('subtitle','location'):
                    ident=value['text'].lstrip('$');transcript.append({'event':event_name,'step':step,**value,'id':ident,'en':en.get(ident),'ru':ru.get(ident),'reachable':event_name in active})
                else:
                    for v in value.values():walk(v,step)
            elif isinstance(value,list):
                for v in value:walk(v,step)
        order=[e for e in EVENT_ORDER[n] if e in active]+[e for e in events if e in active and e not in EVENT_ORDER[n]]
        for event_name in order+[e for e in events if e not in active]:
            for step,value in enumerate(events[event_name],1):walk(value,step)
        assert all(t['en'] and t['ru'] for t in transcript if t['reachable']),(code,[t['id'] for t in transcript if t['reachable'] and (not t['en'] or not t['ru'])])
        # Actual stock preview and instructional image, not fabricated screenshots.
        art=OUT/'assets';art.mkdir(exist_ok=True)
        image_path=art/(code+'.png')
        Image.open(BASE/f'ui/mapthumbnails/campaign/tutorial/{code}.dds').save(image_path)
        level=(BASE/f'leveldata/campaign/tutorial/{code}/{code}.level').read_text()
        ships=re.findall(r'addSquadron\("([^"]+)",\s*"([^"]+)",\s*\{([^}]+)\},\s*(-?\d+)',level)
        record={'chapter':code,'title':TITLES[n-1],'source':str(path),'events_defined':len(events),'events_reachable':len(active),'unused_events':sorted(unused),'reachable_rules':sorted(x[2:] for x in reached if x.startswith('f:')),'unresolved_literal_links':unknown,'all_referenced_string_ids':sorted(all_ids,key=int),'missing_table_strings':missing,'objectives':objectives,'events':events,'functions':functions,'transcript':transcript,'ships':[{'name':a,'hull':b,'position':c,'owner':int(d)} for a,b,c,d in ships],'game_launched':False}
        reports.append(record)
        lines=[f'# HWRM: обучение {n} — {TITLES[n-1]}','',
               'Разбор именно файлов установленного Remastered. Родные RU/EN сохранены буквально; это не новый перевод Vast Reaches. Сценарии определены в Lua, но игра здесь не запускалась. «Достижимый» означает наличие цепочки вызовов от OnInit, а не обещание, что каждая условная реплика прозвучит за одно прохождение.','',
               f'![Родная миниатюра главы](<{image_path.as_posix()}>)','',
               '## Начальная сцена','', '| Имя группы | Корпус | Владелец в .level |','|---|---|---:|']
        for a,b,c,d in ships:lines.append(f'| `{a}` | `{b}` | {d} |')
        lines+=['','Эти записи не равны всему флоту урока: часть кораблей создаётся действиями SCAR позже. Размер штатной эскадрильи определяется движком.','',
                '## Родные задачи','', '| Ключ | RU | EN |','|---|---|---|']
        for key,obj in objectives.items():
            ident=obj['title'].lstrip('$');lines.append(f'| `{key}` / ${ident} | {ru.get(ident,"—")} | {en.get(ident,"—")} |')
        lines+=['','Наличие строки в таблице objectives не подтверждает, что активная ветка выдаёт её: старые упражнения могут быть обойдены.','',
                '## Действующие сцены: текст и действия','',
                'Порядок ниже отражает основную учебную цепочку. Элементы `_active` — ожидание действия/повторная инструкция; игрок может прервать часть объяснения выполнением нужного действия. Условия и исходные строки кода указаны под сценами.','']
        for event_name in order:
            ev=event_sources[event_name]
            lines+=['### '+event_name,'',f'[Исходный скрипт, строка {ev["source_line"]}](<{path.as_posix()}:{ev["source_line"]}>)','']
            relevant=[t for t in transcript if t['event']==event_name]
            if not relevant:lines+=['*Постановочная/управляющая сцена без реплики.*','']
            for t in relevant:
                lines += [f'**RU:** {t["ru"]}','','**EN:** '+t['en'],'',f'`$'+t['id']+f'`; шаг события {t["step"]}; параметр времени {t["time"]} с. Завершение речевого шага проверяется Subtitle_IsDone, это не замер длительности звука.','']
                audio=LOCAL/f'assets/audio/tut_0{n}/{t["id"]}.wav'
                if audio.is_file():lines+=['[Родная английская запись](<'+audio.as_posix()+'>)','']
            callers=[(k,v) for k,v in functions.items() if 'e:'+event_name in v['links'] and 'f:'+k in reached]
            if callers:lines+=['Запускают: '+', '.join(f'`{k}` (строка {v["source_line"]})' for k,v in callers)+'.','']
            actions=re.findall(r'''["']([^\n]*?(?:Camera_|UI_|EventPointer_|Ping_|addObjective|completeObjective|SobGroup_|Universe_|Sensors_|Rule_Add|setMissionComplete)[^\n]*?)["']\s*,''',ev['body'])
            # Preserve exact source commands in JSON; a short list here aids review.
            if actions:lines+=['<details><summary>Постановка, подсветка и действия этой сцены</summary>','','```lua',ev['body'].strip(),'```','','</details>','']
        lines+=['## Не включать автоматически','',
                f'Определено событий: {len(events)}, достижимо по буквальным ссылкам от OnInit: {len(active)}. Не подключены к этой цепочке: '+(', '.join('`'+e+'`' for e in sorted(unused)) or 'нет')+'.','',
                'Закомментированные куски исключены. Для M02 это особенно важно: ветка постройки Research-модуля в активной версии обойдена Rule_SkipHW2SubSystems; для M03 старый intelevent_3dmovement не подключён. JSON-аудит сохраняет все таблицы, функции, строки и найденные связи.','',
                '[Сопоставление с VR и рекомендации](../HWRM_NATIVE_TUTORIAL.md)','']
        target=OUT/(code.upper()+'.md');target.write_text('\n'.join(lines),encoding='utf8')
        book.append((n,record,target))
    Image.open(BASE/'ui/newui/tutorial/ati_shipexample.tga').save(OUT/'assets/ati-shipexample.png')
    Image.open(BASE/'ui/speechicons/fleetcommand0.tga').save(OUT/'assets/fleetcommand.png')
    sheet=Image.new('RGB',(960,260),'#101821');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for i in range(3):
        img=ImageOps.contain(Image.open(OUT/f'assets/m0{i+1}.png').convert('RGB'),(300,210))
        sheet.paste(img,(i*320+(320-img.width)//2,0));draw.text((i*320+15,222),f'{i+1}. '+['Камера и движение','Постройка и исследования','Бой и группы'][i],font=font,fill='white')
    sheet.save(OUT/'assets/overview.png')
    (LOCAL/'audit.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    summary=[{'chapter':r['chapter'],'events':r['events_defined'],'reachable_events':r['events_reachable'],'reachable_subtitles':sum(t['kind']=='subtitle' and t['reachable'] for t in r['transcript']),'unused_events':r['unused_events'],'unresolved_links':r['unresolved_literal_links']} for r in reports]
    (LOCAL/'verification.json').write_text(json.dumps({'game_launched':False,'chapters':summary},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    # Same source material in a lightweight offline reader with stock English voice.
    page=['<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Родное обучение HWRM</title>',
          '<style>body{background:#111923;color:#dce5ec;font:18px/1.6 system-ui;max-width:960px;margin:auto;padding:28px}a{color:#9dd5e1}h2{border-top:1px solid #465464;padding-top:24px}h3{color:#c4a871}article{padding:16px 0;border-bottom:1px solid #2a3949}p{margin:6px 0}details{font-size:15px;color:#aac0d0}audio{display:block;height:32px;margin:8px 0;max-width:100%}nav a{display:inline-block;padding:10px}img{max-width:100%}.note{border-left:3px solid #c4a871;padding:12px;background:#202b36}.key{font:12px monospace;color:#8398aa}</style>',
          '<h1>Родное обучение HWRM</h1><p>Источник — сценарии установленного Remastered, оригинальные русские/английские строки и английская озвучка. Это читатель сценария; игра не запускалась.</p><nav><a href="#m01">1. Камера и движение</a><a href="#m02">2. Экономика</a><a href="#m03">3. Бой и группы</a></nav>',
          '<p class="note">Показаны подключённые сцены. Повторные инструкции и раннее выполнение могут менять фактическое звучание. Старый урок Research-модуля в M02 обойдён активным скриптом; вырезанное перемещение M03 здесь не печатается.</p>']
    controls=0
    for r in reports:
        page+=['<section id="'+r['chapter']+'"><h2>'+r['chapter'].upper()+'. '+r['title']+'</h2><img src="assets/'+r['chapter']+'.png" alt="Родная миниатюра главы">']
        last=None
        for t in r['transcript']:
            if not t['reachable']:continue
            if t['event']!=last:page.append('<h3>'+html.escape(t['event'])+'</h3>');last=t['event']
            page+=['<article><p>'+html.escape(t['ru'])+'</p><details><summary>EN · $'+t['id']+'</summary><p>'+html.escape(t['en'])+'</p></details>']
            a=LOCAL/f'assets/audio/tut_{r["chapter"][1:]}/{t["id"]}.wav'
            if a.is_file():
                page.append('<audio controls preload="none" src="../../'+a.relative_to(ROOT).as_posix()+'"></audio>');controls+=1
            page.append('</article>')
        page.append('</section>')
    page.append('</html>');(OUT/'index.html').write_text('\n'.join(page),encoding='utf8')
    print('Offline reader audio controls:',controls)
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
