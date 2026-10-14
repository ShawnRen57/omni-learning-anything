"""Use the official authenticated dws CLI; never pass credentials through a shell."""
import json
import re
import subprocess
from omni_http import document_data, check_text, check_links, verified
from omni_delivery import verify_url


def run(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError('dws command failed.')
        value = json.loads(result.stdout)
        if not isinstance(value, dict): raise ValueError('dws did not return a JSON object.')
        if value.get('success') is False or value.get('ok') is False:
            raise ValueError('dws operation was rejected.')
        return value
    except Exception:
        raise RuntimeError('dws operation failed; check authentication and reconcile saved task/document.') from None


def unwrap(value):
    return value['data'] if isinstance(value.get('data'), dict) else value


def publish(root, manifest, target, receipt, checkpoint, runner=None):
    runner = runner or run; data = document_data(root, manifest)
    if not receipt.get('remote_id'):
        if receipt.get('task_id'):
            response = runner(['dws', 'doc', 'import', 'get', '--task-id', receipt['task_id'], '--format', 'json'])
        else:
            args = ['dws', 'doc', 'import', '--file', str(root / manifest['artifacts']['docx']),
                    '--name', data['title'], '--format', 'json']
            dest = target['destination']
            if dest.get('folder_id'): args.extend(['--folder', dest['folder_id']])
            else: args.extend(['--workspace', dest['workspace_id']])
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
        checkpoint(remote_id=result['nodeId'], url=url, status='pending')
    info = unwrap(runner(['dws', 'doc', 'info', '--node', receipt['remote_id'], '--format', 'json']))
    content_type = info.get('contentType') or info.get('documentType') or info.get('extension')
    if content_type not in ('ALIDOC', 'adoc', 'doc'):
        raise ValueError('DingTalk metadata does not confirm an editable text document.')
    response = unwrap(runner(['dws', 'doc', 'read', '--node', receipt['remote_id'], '--content-format', 'markdown', '--format', 'json']))
    text = response.get('markdown') or response.get('content') or ''
    if not isinstance(text, str): raise ValueError('DingTalk readback did not return Markdown.')
    check_text(text, data); check_links(text, data)
    if not re.search(r'!\[[^\]]*\]\(https://[^\s)]+\)', text):
        raise ValueError('DingTalk readback is missing a remote figure.')
    return verified(receipt['remote_id'], receipt['url'])
