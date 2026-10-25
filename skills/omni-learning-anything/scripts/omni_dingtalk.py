"""Use the official authenticated dws CLI; never pass credentials through a shell."""
import json
import html
import re
import subprocess
from omni_http import document_data, check_text, check_links, verified
from omni_delivery import verify_url


def run(args):
    try:
        # Initial import includes the CLI's five-minute conversion poll, plus upload.
        initial_import = args[1:3] == ['doc', 'import'] and '--file' in args
        result = subprocess.run(args, capture_output=True, text=True, timeout=600 if initial_import else 60)
        if result.returncode:
            raise RuntimeError('dws command failed.')
        value = json.loads(result.stdout)
        if not isinstance(value, dict): raise ValueError('dws did not return a JSON object.')
        pending_import = initial_import and value.get('timed_out') is True and value.get('status') == 'processing' and value.get('taskId')
        if (value.get('success') is False and not pending_import) or value.get('ok') is False:
            raise ValueError('dws operation was rejected.')
        return value
    except Exception:
        raise RuntimeError('dws operation failed; check authentication and reconcile saved task/document.') from None


def unwrap(value):
    return value['data'] if isinstance(value.get('data'), dict) else value


def profile_args(target):
    profile=target.get('cli_profile') or target.get('account_id')
    return ['--profile',profile] if profile else []


def check_identity(target,runner=None):
    value=unwrap((runner or run)(['dws','auth','status','--format','json']+profile_args(target)))
    if value.get('authenticated') is not True or not value.get('corp_id') or not value.get('user_id'):raise ValueError('Complete official dws authorization for the selected organization.')
    identity=value['corp_id']+':'+value['user_id']
    if target.get('account_id') and identity!=target['account_id']:raise ValueError('DingTalk account/organization changed; preserve the approved course.')
    return {'id':identity,'name':value.get('user_name','')}


class DingTalkCLI:
    def __init__(self,target,runner=None):self.target=target;self.runner=runner or run
    def check_identity(self):return check_identity(self.target,self.runner)
    def check_destination(self,dest):
        args=['--folder',dest['folder_id']] if dest.get('folder_id') else ['--workspace',dest['workspace_id']]
        response=unwrap(self.runner(['dws','doc','list','--limit','1','--format','json']+args+profile_args(self.target)))
        if response.get('success') is False:raise ValueError('DingTalk destination is unavailable.')


def publish(root, manifest, target, receipt, checkpoint, runner=None):
    base_runner=runner or run
    if target.get('account_id'):check_identity(target,base_runner)
    runner=lambda args:base_runner(args+profile_args(target))
    data = document_data(root, manifest)
    if not receipt.get('remote_id') or receipt.get('placement_verified') is False:
        dest = target['destination']
        location = ['--folder', dest['folder_id']] if dest.get('folder_id') else ['--workspace', dest['workspace_id']]
        if receipt.get('task_id'):
            response = runner(['dws', 'doc', 'import', 'get', '--task-id', receipt['task_id'], '--format', 'json'] + location)
        else:
            if receipt.get('remote_id'):
                raise ValueError('DingTalk destination is unverified; reconcile the existing document before retrying.')
            args = ['dws', 'doc', 'import', '--file', str(root / manifest['artifacts']['docx']),
                    '--name', data['title'], '--format', 'json']
            args.extend(location)
            checkpoint(status='creating'); response = runner(args)
        result = unwrap(response)
        if result.get('converted') is False or result.get('fallback') == 'upload':
            checkpoint(status='failed', remote_id=result.get('nodeId'))
            raise ValueError('DingTalk uploaded a file without converting it to an editable document.')
        if result.get('taskId'): checkpoint(task_id=result['taskId'], status='pending')
        if not result.get('nodeId'):
            if receipt.get('task_id'): return {'status': 'pending'}
            raise ValueError('dws returned no document or task identifier.')
        url = result.get('documentUrl') or 'https://alidocs.dingtalk.com/i/nodes/' + result['nodeId']
        verify_url('dingtalk', url)
        checkpoint(remote_id=result['nodeId'], url=url, status='pending', placement_verified=result.get('verified'))
        if result.get('verified') is False:
            raise ValueError('DingTalk destination readback was not verified; preserve the existing task/document.')
    info = unwrap(runner(['dws', 'doc', 'info', '--node', receipt['remote_id'], '--format', 'json']))
    content_type = info.get('contentType') or info.get('documentType') or info.get('extension')
    if content_type not in ('ALIDOC', 'adoc', 'doc'):
        raise ValueError('DingTalk metadata does not confirm an editable text document.')
    response = unwrap(runner(['dws', 'doc', 'read', '--node', receipt['remote_id'], '--content-format', 'markdown', '--format', 'json']))
    text = response.get('markdown') or response.get('content') or ''
    if not isinstance(text, str): raise ValueError('DingTalk readback did not return Markdown.')
    plain=re.sub(r'\\([\\`*_{}\[\]()#+.!<>|~-])',r'\1',text)
    plain=html.unescape(re.sub(r'<[^>]+>','',plain))
    check_text(plain, data)
    hrefs={html.unescape(v) for v in re.findall(r'\]\((https://[^\s)]+)(?:\s+"[^"]*")?\)',text)}
    if not {s['url'] for s in data['sources']}.issubset(hrefs):raise ValueError('DingTalk readback is missing semantic source links.')
    if not re.search(r'!\[[^\]]*\]\(https://[^\s)]+(?:\s+"[^"]*")?\)', text):
        raise ValueError('DingTalk readback is missing a remote figure.')
    return verified(receipt['remote_id'], receipt['url'])
