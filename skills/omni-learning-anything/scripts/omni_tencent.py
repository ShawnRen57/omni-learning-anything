"""Tencent Docs COS pre-import, asynchronous conversion and DOCX readback."""
import base64
import hashlib
import io
import os
from zipfile import ZipFile
from omni_http import HTTP, business, segment, document_data, check_text, check_links, verified
from omni_delivery import verify_url

BASE = 'https://docs.qq.com/openapi/drive/v2/files'


def upload_cos(path, info):
    from qcloud_cos import CosConfig, CosS3Client
    # These short-lived credentials remain in memory and are never checkpointed.
    def decode(field):
        return base64.b64decode(info[field], validate=True).decode()
    config = CosConfig(Region=info['COSRegion'], SecretId=decode('COSSecretID'),
                       SecretKey=decode('COSSecretKey'), Token=decode('COSToken'), Scheme='https')
    client = CosS3Client(config)
    with path.open('rb') as f:
        client.put_object(Bucket=info['COSBucket'], Key=info['COSFileKey'], Body=f,
                          EnableMD5=True)


def check_docx(contents, data):
    from docx import Document
    document = Document(io.BytesIO(contents))
    text = '\n'.join(p.text for p in document.paragraphs)
    check_text(text, data)
    if not document.inline_shapes:
        raise ValueError('Exported Tencent document is missing its figure.')
    with ZipFile(io.BytesIO(contents)) as z:
        check_links(z.read('word/_rels/document.xml.rels').decode(), data)


def publish(root, manifest, target, receipt, checkpoint, client=None, cos_upload=None):
    client = client or HTTP(); cos_upload = cos_upload or upload_cos
    refs = target['credential_env']
    headers = {'Client-Id': os.environ[refs['client_id']], 'Open-Id': os.environ[refs['open_id']],
               'Access-Token': os.environ[refs['token']]}
    path = root / manifest['artifacts']['docx']; data = document_data(root, manifest)
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValueError('Tencent import limit is 100 MB for DOCX.')
    md5 = hashlib.md5(path.read_bytes()).hexdigest()
    if not receipt.get('task_id') and not receipt.get('remote_id'):
        info = business(client.json('POST', BASE + '/pre-import', headers=headers,
                                   data={'fileMD5': md5, 'fileName': path.name, 'fileSize': path.stat().st_size}), 'ret')
        if not info.get('COSFileExisted'):
            cos_upload(path, info)
        checkpoint(status='creating')
        result = business(client.json('POST', BASE + '/async-import', headers=headers,
             data={'fileMD5': md5, 'fileName': path.name, 'COSFileKey': info['COSFileKey'],
                   'parent': target['destination']['folder_id']}), 'ret')
        checkpoint(task_id=result['progressQueryID'], status='pending')
    if not receipt.get('remote_id'):
        result = business(client.json('GET', BASE + '/import-progress', headers=headers,
                         params={'progressQueryID': receipt['task_id']}), 'ret')
        if result.get('progress') != 100:
            return {'status': 'pending'}
        if result.get('type') not in ('doc', 'docx') or not result.get('ID'):
            raise ValueError('Tencent returned a file instead of an editable document.')
        verify_url('tencent', result['url'])
        checkpoint(remote_id=result['ID'], url=result['url'], status='pending')
    # Import completion alone cannot prove that figure, text and links survived conversion.
    result = business(client.json('GET', BASE + '/' + segment(receipt['remote_id']) + '/export', headers=headers), 'ret')
    if not result.get('url'):
        raise ValueError('Tencent readback export unavailable; grant export scope or inspect through host tools.')
    contents = client.download(result['url'])
    check_docx(contents, data)
    return verified(receipt['remote_id'], receipt['url'], note='Exported imported Tencent document and checked text, embedded figure and hyperlinks')
