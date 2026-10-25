"""Guided read-only connection checks and metadata-only reusable profiles."""
import json
import os
import re
import shutil
import stat
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from omni_delivery import validate_delivery
from omni_official_cli import CLIError,NotionCLI,FeishuCLI
from omni_http import business

GUIDE='references/onboarding.md'
INSTALL={'notion':'npm install --global ntn','feishu':'npx @larksuite/cli@latest install'}


def location(platform,value):
    if platform=='obsidian':
        path=Path(value).expanduser().resolve()
        if not path.is_dir():raise ValueError('Select an existing Obsidian Vault directory.')
        return {'vault_path':str(path)}
    u=urlsplit(value);host=u.hostname or ''
    if u.scheme!='https' or u.username or u.password or u.port not in (None,443) or any(re.search(r'token|secret|key|auth',k,re.I) for k in parse_qs(u.query)):
        raise ValueError('Use an official page/folder HTTPS link without credentials.')
    if platform=='notion':
        if not any(host==h or host.endswith('.'+h) for h in ('notion.so','notion.site','notion.com')):raise ValueError('Select a Notion parent-page link.')
        found=re.search(r'([a-fA-F0-9]{32}|[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12})/?$',u.path)
        if not found:raise ValueError('Notion parent link needs a page identifier.')
        return {'parent_page_id':found.group(1).replace('-','').lower()}
    if platform=='feishu':
        found=re.fullmatch(r'/drive/folder/([a-zA-Z0-9]+)/?',u.path)
        if not (host=='feishu.cn' or host.endswith('.feishu.cn')) or not found:raise ValueError('Select a Feishu course folder link, not a document or Wiki link.')
        return {'folder_token':found.group(1)}
    raise ValueError('Guided connect currently supports Notion, Feishu and Obsidian.')


def directory(base=None):
    return Path(base) if base is not None else Path.home()/'.config/omni-learning-anything/connections'


def profile_path(name,base=None):
    if not isinstance(name,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',name):raise ValueError('Connection name: lowercase letters, digits, hyphens or underscores; start with a letter.')
    return directory(base)/(name+'.json')


def load(name,base=None):
    path=profile_path(name,base)
    if path.is_symlink():raise ValueError('Connection profiles cannot be symlinks.')
    info=path.stat()
    if os.name=='posix' and (info.st_uid!=os.getuid() or stat.S_IMODE(info.st_mode)&0o077):raise ValueError('Connection profile must be owned by this user with owner-only permissions.')
    value=json.loads(path.read_text())
    if not isinstance(value,dict) or set(value)!={'version','delivery'} or value['version']!=1:raise ValueError('Invalid connection profile.')
    validate_delivery(value['delivery'])
    return value['delivery']


def save(name,target,base=None):
    validate_delivery(target);path=profile_path(name,base)
    if path.exists() or path.is_symlink():
        if load(name,base)==target:return
        raise ValueError('Connection name already exists; choose a new name to preserve approved courses.')
    parent=path.parent
    if parent.is_symlink():raise ValueError('Connection directory cannot be a symlink.')
    parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    value=json.dumps({'version':1,'delivery':target},ensure_ascii=False,indent=2)
    flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0)
    fd=os.open(path,flags,0o600)
    with os.fdopen(fd,'w') as f:f.write(value+'\n')


def list_connections(base=None):
    result=[];parent=directory(base)
    if not parent.exists():return result
    for path in sorted(parent.glob('*.json')):
        if path.is_symlink():continue
        try:target=load(path.stem,base)
        except (ValueError,OSError):continue
        result.append({'name':path.stem,'delivery':target})
    return result


def blocked(platform,stage,action,command=None,scopes=()):
    result={'ready':False,'platform':platform,'stage':stage,'next_action':action,'guide':GUIDE}
    if command:result['agent_command']=command
    if scopes:result['missing_scopes']=list(scopes)
    return result


def connect(platform=None,value=None,*,client=None,save_as=None,profile_dir=None,connection=None,cli_profile=None,workspace_id=None,subdir='Omni Learning'):
    if connection:
        if any(x is not None for x in (platform,value,cli_profile,workspace_id)):raise ValueError('Reuse the saved connection without overriding its account/destination; create a new named connection for changes.')
        target=load(connection,profile_dir);platform=target['platform']
    else:
        if platform not in ('notion','feishu','obsidian'):raise ValueError('Choose Notion, Feishu or Obsidian.')
        if not value:return blocked(platform,'location','Ask only for the course parent-page/folder link, or the local Vault path.')
        dest=location(platform,value)
        if platform=='obsidian':dest['subdir']=subdir
        if platform=='notion' and workspace_id:dest['workspace_id']=workspace_id
        target={'platform':platform,'mode':'local' if platform=='obsidian' else 'cli','destination':dest}
        if cli_profile:
            if platform!='feishu':raise ValueError('CLI profiles apply only to Feishu.')
            target['cli_profile']=cli_profile
    validate_delivery(target)
    if platform=='obsidian':
        path=Path(target['destination']['vault_path'])
        if not path.is_dir() or not os.access(path,os.W_OK):return blocked(platform,'destination','Make the confirmed Vault directory available and writable.')
        identity=None
    else:
        binary={'notion':'ntn','feishu':'lark-cli'}[platform]
        if not shutil.which(binary):return blocked(platform,'install','Agent installs ' + binary + ' from its official distribution, then checks existing authorization.',INSTALL[platform])
        client=client or (NotionCLI(target) if platform=='notion' else FeishuCLI(target))
        try:
            identity=client.check_identity()
            target['account_id']=identity['id']
        except (CLIError,ValueError,RuntimeError) as error:
            config=platform=='feishu' and isinstance(error,CLIError) and error.kind=='config'
            command='ntn login --no-browser' if platform=='notion' else ('lark-cli config init --new --brand feishu --lang zh' if config else 'lark-cli auth login --domain docs --domain drive --no-wait --json')
            return blocked(platform,'authorization','Agent initiates official authorization; user reviews the account and requested document permissions. Do not paste passwords or tokens into chat.',command,getattr(error,'scopes',()))
        try:
            if platform=='notion':
                page=client.json('GET','https://api.notion.com/v1/pages/'+target['destination']['parent_page_id'])
                if str(page.get('id','')).replace('-','').lower()!=target['destination']['parent_page_id'].replace('-','').lower() or page.get('archived') or page.get('in_trash'):raise ValueError('Parent unavailable.')
            else:
                business(client.json('GET','https://open.feishu.cn/open-apis/drive/v1/files',params={'folder_token':target['destination']['folder_token'],'page_size':1}),'code')
        except Exception as error:
            return blocked(platform,'destination','The current identity cannot confirm the requested destination. Check the original link/access or exact missing permission; preserve this platform.',scopes=getattr(error,'scopes',()))
    if save_as:save(save_as,target,profile_dir)
    result={'ready':True,'platform':platform,'delivery':target,'guide':GUIDE,'note':'Read-only connection check; publish and inspect an actual document before claiming successful delivery.'}
    if identity:result['account']={'id':identity['id'],'name':identity.get('name','')}
    if save_as or connection:result['connection']=save_as or connection
    return result
