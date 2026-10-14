"""Import an embedded-image DOCX into Feishu and resume saved import tickets."""
import json
import os
from omni_http import HTTP, business, segment, document_data, check_text, check_links, verified
from omni_delivery import verify_url

BASE = 'https://open.feishu.cn/open-apis'


def publish(root, manifest, target, receipt, checkpoint, client=None):
    client = client or HTTP(); refs = target['credential_env']
    if refs.get('token'):
        token = os.environ[refs['token']]
    else:
        response = client.json('POST', BASE + '/auth/v3/tenant_access_token/internal',
                               json={'app_id': os.environ[refs['app_id']], 'app_secret': os.environ[refs['app_secret']]})
        business(response, 'code'); token = response['tenant_access_token']
    headers = {'Authorization': 'Bearer ' + token}; data = document_data(root, manifest)
    path = root / manifest['artifacts']['docx']
    if path.stat().st_size > 20 * 1024 * 1024:
        raise ValueError('Feishu media upload is limited to 20 MB; reduce the image.')
    if not receipt.get('task_id') and not receipt.get('remote_id'):
        if not receipt.get('upload_token'):
            with path.open('rb') as f:
                response = client.json('POST', BASE + '/drive/v1/medias/upload_all', headers=headers,
                    data={'file_name': path.name, 'parent_type': 'ccm_import_open', 'parent_node': '', 'size': str(path.stat().st_size)},
                    files={'file': (path.name, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
            checkpoint(upload_token=business(response, 'code')['file_token'])
        checkpoint(status='creating')
        response = client.json('POST', BASE + '/drive/v1/import_tasks', headers=headers,
            json={'file_extension': 'docx', 'file_token': receipt['upload_token'], 'type': 'docx',
                  'file_name': data['title'], 'point': {'mount_type': 1, 'mount_key': target['destination']['folder_token']}})
        checkpoint(task_id=business(response, 'code')['ticket'], status='pending')
    if not receipt.get('remote_id'):
        response = client.json('GET', BASE + '/drive/v1/import_tasks/' + segment(receipt['task_id']), headers=headers)
        result = business(response, 'code')['result']
        if result.get('job_status') == 1:
            return {'status': 'pending'}
        if result.get('job_status') != 0:
            return {'status': 'failed', 'error': 'Feishu import failed; inspect the saved task before retrying.'}
        if not result.get('token') or not result.get('url'):
            raise ValueError('Feishu import result lacks a document identifier.')
        verify_url('feishu', result['url'])
        checkpoint(remote_id=result['token'], url=result['url'], status='pending')
    doc_id = segment(receipt['remote_id'])
    response = client.json('GET', BASE + '/docx/v1/documents/' + doc_id + '/raw_content', headers=headers)
    text = business(response, 'code').get('content', ''); check_text(text, data)
    items = []; page_token = None
    for _ in range(100):
        params = {'page_size': 500}
        if page_token: params['page_token'] = page_token
        response = client.json('GET', BASE + '/docx/v1/documents/' + doc_id + '/blocks', headers=headers, params=params)
        result = business(response, 'code'); items.extend(result.get('items', []))
        if not result.get('has_more'): break
        page_token = result.get('page_token')
        if not page_token: raise ValueError('Incomplete Feishu block pagination.')
    else:
        raise ValueError('Feishu block pagination limit exceeded.')
    if not any(item.get('block_type') == 27 and item.get('image', {}).get('token') for item in items):
        raise ValueError('Imported Feishu document has no image block.')
    check_links(json.dumps(items, ensure_ascii=False), data)
    return verified(receipt['remote_id'], receipt['url'])
