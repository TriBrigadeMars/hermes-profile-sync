#!/usr/bin/env python3
import argparse, json
from pathlib import Path
ALLOWED={'document_info','create_layer','rename_layer','set_visibility','save','save_as','export'}

def main():
    ap=argparse.ArgumentParser(description='Create one allowlisted Krita local-plugin job.')
    ap.add_argument('--job-file',required=True); ap.add_argument('--operation',required=True,choices=sorted(ALLOWED))
    ap.add_argument('--name'); ap.add_argument('--from-name'); ap.add_argument('--to-name'); ap.add_argument('--path'); ap.add_argument('--visible',choices=['true','false'])
    a=ap.parse_args(); op={'op':a.operation}
    if a.name: op['name']=a.name
    if a.from_name: op['from']=a.from_name
    if a.to_name: op['to']=a.to_name
    if a.path: op['path']=str(Path(a.path).expanduser())
    if a.visible is not None: op['visible']=a.visible=='true'
    Path(a.job_file).write_text(json.dumps({'operations':[op]},indent=2),encoding='utf-8')
    print(f'wrote {a.job_file}')
if __name__=='__main__': main()
