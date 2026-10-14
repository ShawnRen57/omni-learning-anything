"""Filesystem course state. Host agents own research, approval and scheduling."""
import hashlib
import json
import os
import re
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp=path.with_name(path.name+f'.{os.getpid()}.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temp.replace(path)


def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def today(root):
    return datetime.now(ZoneInfo(read(root/'config.json')['timezone'])).date().isoformat()


@contextmanager
def lock(root):
    path=Path(root)/'.omni-learning-anything.lock'
    try: path.mkdir()
    except FileExistsError: raise RuntimeError('Project busy. If a process crashed, confirm it stopped before removing .omni-learning-anything.lock.')
    try: yield
    finally: path.rmdir()


def validate_plan(plan):
    days=plan.get('days',[])
    if not plan.get('topic') or not days or [d.get('day') for d in days]!=list(range(1,len(days)+1)) or any(not d.get('topic') for d in days):
        raise ValueError('Plan needs a topic and consecutive days starting at 1.')


def validate_config(config):
    ZoneInfo(config['timezone'])
    if 'daily_minutes' in config and (type(config['daily_minutes']) is not int or config['daily_minutes']<1):
        raise ValueError('daily_minutes must be a positive integer.')
    if 'time' in config and not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d',str(config['time'])):
        raise ValueError('time must use HH:MM, from 00:00 to 23:59.')
    if 'weekdays' in config:
        days=config['weekdays']
        if not isinstance(days,list) or not days or any(d not in ('MO','TU','WE','TH','FR','SA','SU') for d in days):
            raise ValueError('weekdays must be a nonempty list of MO, TU, WE, TH, FR, SA, SU.')
    if 'language' in config and config['language'] not in ('zh','en'):
        raise ValueError('language must be zh or en.')
    for key in ('sample_mode','immediate_day01'):
        if key in config and type(config[key]) is not bool:
            raise ValueError(key+' must be a boolean.')


def initialize(root,config,plan):
    root=Path(root); root.mkdir(parents=True,exist_ok=True)
    validate_plan(plan); validate_config(config)
    with lock(root):
        if any((root/p).exists() for p in ('config.json','plan.json','state.json')):
            raise ValueError('Project already initialized; existing files were not changed.')
        save(root/'config.json',config); save(root/'plan.json',plan)
        save(root/'state.json',{'schema':1,'status':'awaiting_approval','approved_plan':None,'lessons':{},'schedule':None,'mastery':{}})


def check_approval(root,state):
    if state.get('approved_plan')!=digest(root/'plan.json'): raise ValueError('Current plan has not been approved. Render, inspect, then obtain user approval.')
    if state.get('approved_config')!=digest(root/'config.json'): raise ValueError('Course settings changed; review and approve the updated course settings.')


def manifest_ok(root,manifest):
    for name,sha in manifest['files'].items():
        path=(root/name).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file() or digest(path)!=sha:
            raise ValueError('Document changed or missing: '+name)


def reviewed(root,key):
    m=read(root/'manifests'/f'{key}.json'); manifest_ok(root,m)
    if not m.get('reviewed_at'): raise ValueError('Visual review not recorded.')
    return m


def check_deliveries(root,state):
    for day,record in state['lessons'].items():
        path=root/'manifests'/f'Day{int(day):02d}.json'
        if not path.is_file() or digest(path)!=record['manifest_hash']:
            raise ValueError('Delivered document manifest changed: Day'+f'{int(day):02d}')
        reviewed(root,f'Day{int(day):02d}')


def approve(root):
    with lock(root):
        reviewed(root,'plan'); state=read(root/'state.json')
        if state.get('approved_plan')==digest(root/'plan.json') and state.get('approved_config')==digest(root/'config.json'):
            return  # Repeated approval cannot resume a paused or completed course.
        if state['lessons'] and state.get('approved_plan')!=digest(root/'plan.json'):
            raise ValueError('Changing a started curriculum requires a new project; preserve the old archive.')
        state.update(approved_plan=digest(root/'plan.json'),approved_config=digest(root/'config.json'),status='active'); save(root/'state.json',state)


def next_action(root):
    state=read(root/'state.json'); check_approval(root,state)
    check_deliveries(root,state)
    if state['status'] in ('paused','complete'): return {'action':state['status']}
    plan=read(root/'plan.json'); validate_plan(plan)
    day=next((d for d in plan['days'] if str(d['day']) not in state['lessons']),None)
    if day is None: return {'action':'complete','stop_host_schedule':True}
    if not read(root/'config.json').get('sample_mode') and any(s['delivered_at']==today(root) for s in state['lessons'].values()):
        return {'action':'already_delivered_today','day':max(map(int,state['lessons']))}
    key=f"Day{day['day']:02d}"
    if (root/'manifests'/f'{key}.json').exists():
        m=read(root/'manifests'/f'{key}.json'); manifest_ok(root,m)
        return {'action':'deliver_existing' if m.get('reviewed_at') else 'review_existing','day':day['day'],'topic':day['topic'],'pdf':m['pdf']}
    return {'action':'generate','day':day['day'],'topic':day['topic']}


def deliver(root,day):
    with lock(root):
        state=read(root/'state.json'); check_approval(root,state)
        check_deliveries(root,state)
        if str(day) in state['lessons']:
            m=reviewed(root,f'Day{day:02d}'); return {'action':'already_recorded','pdf':m['pdf']}
        action=next_action(root)
        if action.get('day')!=day or action['action']!='deliver_existing': raise ValueError('Only the next reviewed lesson may be marked delivered.')
        m=reviewed(root,f'Day{day:02d}')
        state['lessons'][str(day)]={'delivered_at':today(root),'pdf':m['pdf'],'manifest_hash':digest(root/'manifests'/f'Day{day:02d}.json')}
        if len(state['lessons'])==len(read(root/'plan.json')['days']): state['status']='complete'
        save(root/'state.json',state)
        return {'status':state['status'],'stop_host_schedule':state['status']=='complete'}


def set_status(root,status):
    with lock(root):
        state=read(root/'state.json'); check_approval(root,state)
        if state['status']=='complete': raise ValueError('Completed course cannot be resumed.')
        state['status']=status; save(root/'state.json',state)


def record_schedule(root,host,job_id):
    with lock(root):
        state=read(root/'state.json'); check_approval(root,state)
        if read(root/'config.json').get('sample_mode'): raise ValueError('Sample projects cannot register live schedules.')
        if state['status']!='active': raise ValueError('Course is not active.')
        if state.get('schedule'): raise ValueError('Schedule already registered; update it in the host instead of creating a duplicate.')
        state['schedule']={'host':host,'job_id':job_id,'registered_at':today(root)}; save(root/'state.json',state)
