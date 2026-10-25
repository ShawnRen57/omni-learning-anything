#!/usr/bin/env python3
"""Omni Learning Anything deterministic helpers. Run --help for commands."""
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ required; current interpreter is " + sys.version.split()[0] + ". Select a supported Python interpreter and retry.")

import argparse
import json
import tempfile
import shutil
import re
from pathlib import Path
import omni_core as c


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    version=re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',(Path(__file__).resolve().parents[1]/'SKILL.md').read_text(),re.M).group(1)
    parser.add_argument('--version',action='version',version='omni-learning-anything '+version)
    parser.add_argument('--project',type=Path,default=Path.cwd())
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('connect'); p.add_argument('--platform',choices=['notion','feishu','obsidian']); p.add_argument('--location'); p.add_argument('--connection'); p.add_argument('--save-as'); p.add_argument('--cli-profile'); p.add_argument('--workspace-id'); p.add_argument('--subdir',default='Omni Learning')
    p=sub.add_parser('connection-show'); p.add_argument('--name',required=True)
    sub.add_parser('connection-list')
    sub.add_parser('doctor')
    p=sub.add_parser('init'); p.add_argument('--config',type=Path,required=True); p.add_argument('--plan',type=Path,required=True)
    p=sub.add_parser('render'); p.add_argument('--input',type=Path,required=True); p.add_argument('--key',required=True); p.add_argument('--format',dest='formats',action='append',choices=['pdf','markdown','docx'])
    p=sub.add_parser('review'); p.add_argument('--key',required=True); p.add_argument('--note',required=True)
    sub.add_parser('approve'); sub.add_parser('next'); sub.add_parser('pause'); sub.add_parser('resume')
    p=sub.add_parser('delivered'); p.add_argument('--day',type=int,required=True)
    p=sub.add_parser('schedule-record'); p.add_argument('--host',required=True); p.add_argument('--job-id',required=True)
    sub.add_parser('delivery-check')
    for command in ('publish','delivery-status'):
        p=sub.add_parser(command); p.add_argument('--key',required=True)
    p=sub.add_parser('receipt-record'); p.add_argument('--key',required=True); p.add_argument('--receipt',type=Path,required=True)
    p=sub.add_parser('reconcile'); p.add_argument('--key',required=True); p.add_argument('--remote-id'); p.add_argument('--url'); p.add_argument('--task-id')
    args=parser.parse_args(); root=args.project.resolve(); result={'ok':True}
    try:
        if args.command=='connect':
            from omni_connections import connect
            result=connect(args.platform,args.location,connection=args.connection,save_as=args.save_as,cli_profile=args.cli_profile,workspace_id=args.workspace_id,subdir=args.subdir)
        elif args.command=='connection-list':
            from omni_connections import list_connections
            result={'connections':list_connections()}
        elif args.command=='connection-show':
            from omni_connections import load
            result={'delivery':load(args.name)}
        elif args.command=='doctor':
            writable=False
            if root.is_dir():
                try:
                    with tempfile.TemporaryFile(dir=root): writable=True
                except OSError: pass
            result={'python':sys.version.split()[0],'xelatex':shutil.which('xelatex'),'output_writable':writable,'note':'XeLaTeX is required only for PDF. Search, images, scheduler and host document tools require capability checks.'}
            if (root/'config.json').exists():
                from omni_delivery import preflight,default_formats
                config=c.read(root/'config.json'); result.update(formats=default_formats(config),delivery=preflight(config.get('delivery')))
        elif args.command=='init': c.initialize(root,c.read(args.config),c.read(args.plan))
        elif args.command=='render':
            from omni_document import render
            from omni_delivery import default_formats
            m=render(root,args.input,args.key,args.formats or default_formats(c.read(root/'config.json'))); result={k:v for k,v in m.items() if k!='files'}
        elif args.command=='review':
            from omni_document import review
            review(root,args.key,args.note)
        elif args.command=='approve': c.approve(root)
        elif args.command=='next': result=c.next_action(root)
        elif args.command=='delivered': result=c.deliver(root,args.day)
        elif args.command in ('pause','resume'): c.set_status(root,'paused' if args.command=='pause' else 'active')
        elif args.command=='schedule-record': c.record_schedule(root,args.host,args.job_id)
        elif args.command=='delivery-check':
            from omni_delivery import preflight
            result=preflight(c.read(root/'config.json').get('delivery'))
        elif args.command=='publish':
            from omni_delivery import publish
            result=publish(root,args.key)
        elif args.command=='delivery-status':
            from omni_delivery import status
            result=status(root,args.key)
        elif args.command=='receipt-record':
            from omni_delivery import record_receipt
            result=record_receipt(root,args.key,c.read(args.receipt))
        elif args.command=='reconcile':
            from omni_delivery import reconcile
            result=reconcile(root,args.key,args.remote_id,args.url,args.task_id)
    except (ValueError,RuntimeError,OSError,KeyError) as e:
        parser.exit(1,json.dumps({'ok':False,'error':str(e)},ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
