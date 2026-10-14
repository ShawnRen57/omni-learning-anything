#!/usr/bin/env python3
"""Omni Learning Anything deterministic helpers. Run --help for commands."""
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ required; current interpreter is " + sys.version.split()[0] + ". Select a supported Python interpreter and retry.")

import argparse
import json
import tempfile
from pathlib import Path
import omni_core as c


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=Path.cwd())
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    p=sub.add_parser('init'); p.add_argument('--config',type=Path,required=True); p.add_argument('--plan',type=Path,required=True)
    p=sub.add_parser('render'); p.add_argument('--input',type=Path,required=True); p.add_argument('--key',required=True)
    p=sub.add_parser('review'); p.add_argument('--key',required=True); p.add_argument('--note',required=True)
    sub.add_parser('approve'); sub.add_parser('next'); sub.add_parser('pause'); sub.add_parser('resume')
    p=sub.add_parser('delivered'); p.add_argument('--day',type=int,required=True)
    p=sub.add_parser('schedule-record'); p.add_argument('--host',required=True); p.add_argument('--job-id',required=True)
    args=parser.parse_args(); root=args.project.resolve(); result={'ok':True}
    try:
        if args.command=='doctor':
            import omni_pdf
            writable=False
            if root.is_dir():
                try:
                    with tempfile.TemporaryFile(dir=root): writable=True
                except OSError: pass
            result={'python':sys.version.split()[0],'xelatex':omni_pdf.executable('xelatex'),'output_writable':writable,'note':'Search, image generation, scheduler and notification require host capability checks.'}
        elif args.command=='init': c.initialize(root,c.read(args.config),c.read(args.plan))
        elif args.command=='render':
            import omni_pdf
            m=omni_pdf.render(root,args.input,args.key); result={k:v for k,v in m.items() if k!='files'}
        elif args.command=='review':
            import omni_pdf
            omni_pdf.review(root,args.key,args.note)
        elif args.command=='approve': c.approve(root)
        elif args.command=='next': result=c.next_action(root)
        elif args.command=='delivered': result=c.deliver(root,args.day)
        elif args.command in ('pause','resume'): c.set_status(root,'paused' if args.command=='pause' else 'active')
        elif args.command=='schedule-record': c.record_schedule(root,args.host,args.job_id)
    except (ValueError,RuntimeError,OSError,KeyError) as e:
        parser.exit(1,json.dumps({'ok':False,'error':str(e)},ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
