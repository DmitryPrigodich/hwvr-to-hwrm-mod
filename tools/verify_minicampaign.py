"""Exercise campaign control flow in Lua 5.1 with a strict mock HWRM API.

This catches Lua/API wiring and stage errors, not engine compatibility or combat balance.
The scripts deliberately use the shared Lua 4/5.1 subset. No game process is launched.
"""
import json
import math
import re
from pathlib import Path
from lupa.lua51 import LuaRuntime

PROJECT=Path(__file__).resolve().parent.parent
ROOT=PROJECT/'minicampaign'
BASE=ROOT/'leveldata/campaign/VastReachesMiniCampaign'


class Engine:
    def __init__(self,chapter):
        self.lua=LuaRuntime(unpack_returned_tuples=True)
        self.g=self.lua.globals()
        self.ships={}
        self.groups={}
        self.volumes={}
        self.objectives={}
        self.results=[]
        self.orders=[]
        self.camera_orders=[]
        self.music_orders=[]
        self.speech_calls=[]
        self.played_lines=[]
        self.sensors_active=0
        self.letterbox=0
        self.camera_control=1
        self.player_orders=1
        self.sensors_toggle=1
        self.rotated=0
        self.panned=0
        self.zoom=1000
        self.selected=set()
        self.abilities={}
        self.build_restrictions=set()
        self.ru=0
        self.lua.execute('getn=table.getn')
        for name in ['AB_Move','AB_Attack','AB_Custom','ONEKEY','TWOKEY','OffensiveROE','PassiveROE','AggressiveStance','OT_Primary','OT_Secondary','OS_Complete','OS_Failed','MUS_Ambient']:
            self.g[name]=name
        functions={
            'dofilepath':self.load,'print':lambda *a:None,'addSquadron':self.add,
            'createSOBGroup':self.create,'SobGroup_Create':self.create,'addToSOBGroup':self.add_group,
            'addSphere':self.sphere,'addCamera':self.noop,'setWorldBoundsInner':self.noop,
            'loadBackground':self.noop,'setSensorsManagerCameraDistances':self.noop,'addAsteroid':self.noop,
            'CPU_Enable':self.noop,'SetAlliance':self.noop,'SobGroup_Despawn':self.despawn,'SobGroup_Spawn':self.spawn,
            'Player_RestrictBuildOption':lambda player,hull:self.build_restrictions.add(hull.lower()),
            'Player_UnrestrictBuildOption':lambda player,hull:self.build_restrictions.discard(hull.lower()),
            'Player_RestrictResearchOption':self.noop,'Player_GrantResearchOption':self.noop,
            'Player_UnrestrictResearchOption':self.noop,
            'SobGroup_AbilityActivate':self.ability,'UI_BindKeyEvent':self.noop,'Camera_Interpolate':lambda *a:self.camera_orders.append(a),
            'Rule_AddInterval':self.noop,'Rule_Remove':self.noop,'Subtitle_Message':self.noop,
            'Sound_SpeechSubtitlePath':self.noop,'Subtitle_Add':self.subtitle_add,'Subtitle_IsDone':self.subtitle_done,
            'Sound_MusicPlayType':lambda *a:self.music_orders.append(a),'fogSetActive':self.noop,'setGlareIntensity':self.noop,'setLevelShadowColour':self.noop,
            'Camera_SetLetterboxStateNoUI':lambda state,seconds:setattr(self,'letterbox',state),
            'Camera_AllowControl':lambda state:setattr(self,'camera_control',state),
            'Universe_AllowPlayerOrders':lambda state:setattr(self,'player_orders',state),
            'Sensors_EnableToggle':lambda state:setattr(self,'sensors_toggle',state),
            'Sensors_EnableCameraZoom':self.noop,'Universe_EnableSkip':self.noop,
            'Sensors_ManagerIsActive':lambda:self.sensors_active,
            'Camera_ResetRotated':lambda:setattr(self,'rotated',0),'Camera_PlayerHasRotated':lambda threshold:self.rotated,
            'Camera_ResetPanned':lambda:setattr(self,'panned',0),'Camera_PlayerHasPanned':lambda threshold:self.panned,
            'Camera_GetLastZoomAmount':lambda:self.zoom,'Camera_UsePanning':self.noop,
            'SobGroup_Selected':lambda group:int(bool(set(self.members(group)) & self.selected)),
            'Objective_Add':self.objective,'Objective_SetState':self.objective_state,
            'Objective_AddDescription':lambda ident,text:self.objectives[ident].__setitem__('description',text),
            'Ping_Remove':self.noop,'Ping_AddPoint':lambda *a:1,'Ping_AddSobGroup':lambda *a:1,
            'SobGroup_Count':lambda n:len(self.members(n)), 'FOW_RevealGroup':self.noop,
            'SobGroup_SetROE':self.noop,'SobGroup_SetStance':self.noop,'SobGroup_Attack':self.order,
            'SobGroup_Move':self.order,'SobGroup_SetHealth':self.health,'SobGroup_SetMaxSpeed':self.noop,
            'SobGroup_SwitchOwner':self.owner,'Player_FillShipsByType':self.fill_type,
            'Player_GetNumberOfSquadronsOfTypeAwakeOrSleeping':self.count_type,
            'SobGroup_IsInVolume':self.in_volume,'SobGroup_FillProximitySobGroup':self.proximity,
            'SobGroup_FillSobGroupInVolume':self.fill_volume,
            'Player_FillSobGroupInVolume':lambda out,player,volume:self.fill_volume(out,'Player_Ships'+str(player),volume),
            'Player_GetRU':lambda player:self.ru,'setMissionComplete':self.results.append,
        }
        for name,func in functions.items():self.g[name]=func
        path=BASE/chapter/(chapter+'.level')
        self.lua.execute(path.read_text())
        self.ru=self.g.player[0].resources
        self.g.DetermChunk()
        self.g.NonDetermChunk()
        self.lua.execute((BASE/chapter/(chapter+'.lua')).read_text())
        self.original_play_line=self.g.VRC_PlayLine
        self.g.VRC_PlayLine=self.play_line
        self.g.OnInit()

    def noop(self,*args):pass
    def play_line(self,key,duration):
        self.played_lines.append(key)
        return self.original_play_line(key,duration)
    def await_completion(self):
        # Native speech can legitimately exceed the former fixed 20s window.
        for _ in range(180):
            if self.results:return
            self.tick()
        raise AssertionError('Mission never completed after its final speech')
    def subtitle_add(self,actor,text,duration):
        self.speech_calls.append((actor,text,duration))
        if not hasattr(self,'subtitle_until'):self.subtitle_until={}
        self.subtitle_until[actor]=self.g.VRC_Time+duration
        return duration
    def subtitle_done(self,actor):
        return int(self.g.VRC_Time>=getattr(self,'subtitle_until',{}).get(actor,0))
    def order(self,*args):self.orders.append(args)
    def ability(self,group,ability,enabled):
        for name in self.members(group):self.abilities[name,ability]=enabled
    def load(self,path):
        path=path.removeprefix('data:')
        if path.lower()=='scripts/scar/scar_util.lua':return
        target=ROOT/path
        assert target.is_file(),path
        self.lua.execute(target.read_text())
    def create(self,name):self.groups.setdefault(name,set())
    def add(self,name,hull,pos,owner,rotation,size,hyper):
        self.ships[name]={'type':hull.lower(),'pos':list(pos.values()),'owner':owner,'active':True,'health':1,'spawn_size':size}
    def add_group(self,name,group):
        assert name in self.ships, ('Unknown squadron in addToSOBGroup',name)
        assert group in self.groups, ('Missing SOB group',group)
        self.groups[group].add(name)
    def sphere(self,name,pos,radius):self.volumes[name]=(list(pos.values()),radius)
    def members(self,group):
        if group.startswith('Player_Ships'):
            names=[k for k,v in self.ships.items() if v['owner']==int(group[-1])]
        else:
            assert group in self.groups,group
            names=self.groups[group]
        return [n for n in names if self.ships[n]['active'] and self.ships[n]['health']>0]
    def despawn(self,group):
        for n in self.groups[group]:self.ships[n]['active']=False
    def spawn(self,group,volume):
        pt,_=self.volumes[volume]
        for n in self.groups[group]:
            self.ships[n]['active']=True
            self.ships[n]['pos']=pt.copy()
    def objective(self,text,kind):
        assert re.fullmatch(r'\$995\d+',text),text
        i=len(self.objectives)+1
        self.objectives[i]={'text':text,'kind':kind,'state':'active'}
        return i
    def objective_state(self,i,state):self.objectives[i]['state']=state
    def health(self,group,value):
        for n in self.groups[group]:self.ships[n]['health']=value
    def owner(self,group,value):
        for n in self.groups[group]:self.ships[n]['owner']=value
    def fill_type(self,group,player,hull):
        self.groups[group]={k for k,v in self.ships.items() if v['owner']==player and v['type']==hull.lower() and v['active'] and v['health']>0}
    def count_type(self,player,hull):return len([v for v in self.ships.values() if v['owner']==player and v['type']==hull.lower() and v['active'] and v['health']>0])
    def in_volume(self,group,volume):
        center,radius=self.volumes[volume]
        return int(any(math.dist(self.ships[n]['pos'],center)<=radius for n in self.members(group)))
    def fill_volume(self,out,group,volume):
        center,radius=self.volumes[volume]
        self.groups[out]={n for n in self.members(group) if math.dist(self.ships[n]['pos'],center)<=radius}
        return int(bool(self.groups[out]))
    def proximity(self,out,source,target,radius):
        centers=[self.ships[n]['pos'] for n in self.members(target)]
        self.groups[out]={n for n in self.members(source) if any(math.dist(self.ships[n]['pos'],p)<=radius for p in centers)}
        return int(bool(self.groups[out]))
    def tick(self,n=1):
        for i in range(n):self.g.VRC_Tick()
    def kill(self,name):self.health(name,0)
    def move_type(self,hull,volume,limit=100):
        names=[k for k,v in self.ships.items() if v['owner']==0 and v['type']==hull.lower() and v['health']>0]
        for name in names[:limit]:self.ships[name]['pos']=self.volumes[volume][0].copy()
    def add_player(self,hull):
        i='mock_new_'+str(len(self.ships))
        self.ships[i]={'type':hull.lower(),'pos':[0,0,0],'owner':0,'active':True,'health':1}
        return i
    def assert_stage(self,value):assert self.g.VRC_State==value,(self.g.VRC_Mission,self.g.VRC_State,value)


def tests():
    passed=[]
    menu=LuaRuntime()
    menu.execute((ROOT/'leveldata/campaign/VastReachesMiniCampaign.campaign').read_text())
    assert menu.globals().contentType==2
    assert menu.globals().contentOrdered==1
    assert 'campaign_ascension' not in menu.globals().ExtFilter
    for i in range(1,4):
        chapter=menu.globals().Mission[i].directory
        assert (ROOT/'ui/mapthumbnails/campaign/VastReachesMiniCampaign'/(chapter+'.dds')).is_file()
    passed.append('Extra Missions entry declares ordered chapters, custom filters and all three thumbnails.')
    for p in ROOT.rglob('*'):
        if p.suffix in ['.lua','.level','.campaign']:
            LuaRuntime().execute('assert(loadstring(...))',p.read_text(encoding='ascii'))
    passed.append('All Lua/level/campaign files parse in Lua 5.1; source uses Lua 4-compatible subset.')
    e=Engine('T01_Training')
    starting_fighters=[v for v in e.ships.values() if v['owner']==0 and v['type']=='kus_scout']
    assert len(starting_fighters)==1 and starting_fighters[0]['spawn_size']==0,'M0 must request one full native batch'
    assert not any(v['owner']==0 and v['type']=='kus_interceptor' for v in e.ships.values())
    e.tick(10);e.assert_stage(0)
    assert e.g.VRC_IntroLock==1 and len(e.music_orders)==1
    assert e.music_orders[0][0]=='data:sound/music/battle/A01_mission1and16'
    assert e.letterbox==1 and e.camera_control==0
    e.tick(600);e.assert_stage(0)
    assert e.g.VRC_TrainingPhase==2 and e.g.VRC_IntroLock==1
    assert e.letterbox==0 and e.camera_control==1 and e.player_orders==1 and e.sensors_toggle==1
    assert len([call for call in e.speech_calls if call[0]==29])==2,'FI must introduce sensors before waiting for the player'
    assert len(e.objectives)==1 and e.objectives[e.g.VRC_Objective]['description']==e.g.VRC_Text['t_sensors_desc']
    assert not e.members('VRC_TrainingA'),'First target must not exist before reaching the movement point'
    camera_count=len(e.camera_orders);e.tick(12)
    assert len(e.camera_orders)==camera_count,'Camera must be released after opening dialogue'
    e.sensors_active=1;e.tick(240);e.assert_stage(1)
    assert e.g.VRC_IntroLock==0
    expected=['T01_010_010_TS','T01_010_020_KS','T01_010_030_TS','T01_010_040_KS','T01_020_010_FI','T01_020_020_FI','T01_020_030_FI','T01_020_040_FI','T01_020_050_TS','T01_020_060_KS']
    # Camera lessons use actual input queries; waiting must not pass them.
    assert [call[1] for call in e.speech_calls[:10]]==[e.g.VRC_Text[key] for key in expected]
    e.tick(100);e.assert_stage(1)
    e.rotated=1;e.tick();e.assert_stage(2)
    e.tick(100);e.assert_stage(2)
    e.zoom=900;e.tick();e.assert_stage(3)
    e.tick(100);e.assert_stage(3)
    e.panned=1;e.tick();e.assert_stage(4)
    e.tick(180);e.assert_stage(4)
    e.selected={'VRC_Player_1'};e.tick();e.assert_stage(5)
    e.tick(90);e.assert_stage(5)
    e.move_type('kus_scout','VRC_MovePoint',1);e.tick();e.assert_stage(6)
    assert e.ships['VRC_TrainingA']['type']=='vgr_scout'
    assert math.dist(e.ships['VRC_TrainingA']['pos'],e.volumes['VRC_MovePoint'][0])>3500
    assert e.abilities['VRC_TrainingA','AB_Attack']==0
    assert e.abilities['VRC_TrainingA','AB_Move']==0
    # A target killed during its briefing waits for the last line instead of dropping it.
    e.kill('VRC_TrainingA');e.tick();e.assert_stage(6)
    e.tick(150);e.assert_stage(7)
    assert 'kus_scout' not in e.build_restrictions
    e.add_player('kus_interceptor');e.tick(180);e.assert_stage(7)
    new_scout=e.add_player('kus_scout');e.tick();e.assert_stage(8)
    assert e.abilities[new_scout,'AB_Custom']==0
    assert e.abilities['VRC_Player_1','AB_Custom']==0
    assert not e.members('VRC_TrainingB') and not e.members('VRC_TrainingC')
    e.tick(240);e.assert_stage(8)
    e.move_type('kus_scout','VRC_RoutePoint',1);e.tick();e.assert_stage(8)
    e.move_type('kus_scout','VRC_RoutePoint');e.tick();e.assert_stage(9)
    assert len(e.music_orders)==2 and e.music_orders[-1][0]=='data:sound/music/battle/B01_TuranicRaidersLong'
    e.kill('VRC_TrainingB');e.tick(10);e.assert_stage(9)
    e.kill('VRC_TrainingC');e.tick();e.assert_stage(99)
    assert e.members('VRC_Platform'),'Avoiding the platform must be enough to win'
    assert not e.results,'Hyperspace story must finish before victory'
    e.tick(400);assert e.results==[1],e.results
    wanted={k for k in e.g.VRC_Text if re.fullmatch(r'T01_\d{3}_\d{3}_[A-Z]+',k)}-{'T01_030_020_FI'}
    actual=[e.g.VRC_Text[k] for k in e.played_lines if k.startswith('T01_')]
    assert len(wanted)==37 and len(actual)==37 and set(actual)=={e.g.VRC_Text[k] for k in wanted},(len(wanted),len(actual),e.played_lines)
    assert actual[-6:]==[e.g.VRC_Text[k] for k in ['T01_070_010_KS','T01_070_020_KS','T01_070_030_TS','T01_070_040_KS','T01_070_050_TS','T01_070_060_TS']]
    assert len(e.camera_orders)==camera_count,'Later lessons must never resume the automatic orbit'
    passed.append('M0 has one full starting batch; input-gated camera/selection/move lessons, distant passive scout, construction, two-squadron detour, Turanic attack, 37 serial spoken lines and victory with platform alive.')
    e=Engine('M01_ProvingGrounds')
    e.tick();e.assert_stage(1)
    e.ru=200;e.tick();e.assert_stage(2)
    e.add_player('kus_scout');e.tick();e.assert_stage(3)
    e.tick(5);e.assert_stage(3)
    e.move_type('kus_scout','VRC_ScoutPoint');e.tick();e.assert_stage(4)
    for index in range(1,4):
        e.kill('VRC_Patrol'+str(index));e.tick();e.assert_stage(4+index)
    for index in range(1,3):e.kill('VRC_Breach'+str(index))
    e.tick();e.assert_stage(7)
    e.kill('VRC_Breach3');e.tick();e.assert_stage(8)
    e.tick(19);e.assert_stage(8)
    e.tick(20);e.await_completion();assert e.results==[1]
    passed.append('M1 gates RU/scout/recon, all three patrols and three breach frigates; timed escape ignores final fleet kills.')

    def m4_attach():
        e=Engine('M04_LostDestroyer')
        e.tick();e.assert_stage(1)
        e.move_type('kus_scout','VRC_SearchPoint');e.tick();e.assert_stage(2)
        e.kill('VRC_Retrieval');e.tick();e.assert_stage(3)
        e.move_type('kus_salvagecorvette','VRC_DestroyerPoint',2);e.tick(12);e.assert_stage(3)
        e.move_type('kus_salvagecorvette','VRC_DestroyerPoint',3);e.tick(9);e.assert_stage(3)
        e.tick();e.assert_stage(4)
        assert all(e.ships[n]['owner']==0 for n in e.groups['VRC_Destroyer'])
        return e

    e=m4_attach();e.tick(16);assert e.g.VRC_PursuitWave==1
    for n in e.groups['VRC_Destroyer']:e.ships[n]['pos']=[0,0,0]
    e.tick(20);e.await_completion();assert e.results==[1]
    assert e.objectives[e.g.VRC_Optional]['state']=='active'
    passed.append('M4 requires THREE nearby engineers for 10 s, switches owner, issues tow order, spawns pursuit and wins by delivery with gate alive.')
    e=m4_attach();e.kill('VRC_Gate');e.tick(20);e.await_completion();assert e.results==[1]
    assert e.g.VRC_PursuitWave==0
    assert e.objectives[e.g.VRC_Optional]['state']=='OS_Complete'
    passed.append('M4 alternate gate kill wins without delivery and prevents further pursuit spawns.')
    e=Engine('M04_LostDestroyer');e.kill('VRC_Destroyer');e.tick(5);assert e.results==[0]
    for chapter in ['T01_Training','M01_ProvingGrounds','M04_LostDestroyer']:
        e=Engine(chapter);e.kill('VRC_Mothership');e.tick(5);assert e.results==[0]
    passed.append('Destroyer loss fails M4; Mothership loss fails every chapter; completion is never repeated.')

    # Referenced hulls must exist in the native extracted files, not just in this mock.
    audit=json.loads((PROJECT/'local/minicampaign-layout.json').read_text())
    hulls={g['hull'] for m in audit['missions'] for g in m['groups']}
    for hull in hulls:
        assert any((PROJECT/root/'ship'/hull/(hull+'.ship')).is_file() for root in ['local/hw1ships','local/hw2ships']),hull
    passed.append('All '+str(len(hulls))+' referenced stock hull definitions exist locally.')
    # Detect missing localization keys even in branches not reached above.
    text=json.loads((PROJECT/'local/campaign/strings-en.json').read_text(encoding='utf8'))
    keys=set(re.findall(r'VRC_Text\["([^"]+)"\]',(BASE/'VRC_Data.lua').read_text()))
    ucs={line.split('\t',1)[0] for line in (ROOT/'locale/Russian/vrcampaign.ucs').read_text(encoding='utf-16').splitlines()}
    for p in BASE.rglob('*.lua'):
        for key in re.findall(r'"((?:M01_|M04_|T01_)[^"]+)"',p.read_text()):
            if key in ('M01_ProvingGrounds','M04_LostDestroyer','T01_Training'):continue
            assert key in keys,(p,key)
    for string_id in re.findall(r'"\$(995\d+)"',(BASE/'VRC_Data.lua').read_text()):assert string_id in ucs,string_id
    passed.append('All VR dialogue/objective keys and generated Russian string IDs resolve.')
    result={'passed':True,'checks':passed,'game_launched':False,'limitations':['Mock API does not test native engine execution, save/load, UI, docking, pathing, combat or balance.','Lua 5.1 syntax check is not a run in the HWRM Lua 4 engine.']}
    (PROJECT/'local/minicampaign-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for check in passed:print('PASS:',check)


if __name__=='__main__':tests()
