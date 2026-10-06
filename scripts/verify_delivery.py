"""Inspect actual ZIP membership, links and hashes; run unpacked recovery checks."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote
from build_delivery import ROOT, MANIFEST, digest, link_check, safe_path, package_schema, destination_check, content_policy


def inspect_zip(data: bytes, expected: dict) -> dict[str, bytes]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):
            raise ValueError('Duplicate ZIP member')
        payload={safe_path(name).as_posix():archive.read(name) for name in names}
    meta=json.loads(payload.pop('PACKAGE-MANIFEST.json'))
    inventory={name:digest(data) for name,data in payload.items()}
    if inventory != meta['files'] or inventory != expected['files']:
        raise ValueError('Actual ZIP membership or hash differs from approved build inventory')
    for name in payload:
        destination_check(expected,name)
    content_policy(expected,payload)
    return payload


def private_overlay(run: Path, result: dict, evidence_path: Path, refresh_evidence: bool = False) -> dict:
    payload={}
    for package in result['packages']:
        with zipfile.ZipFile(run/(package['id']+'.zip')) as archive:
            payload.update({name:archive.read(name) for name in archive.namelist() if name!='PACKAGE-MANIFEST.json'})
    detached={}
    supplement_sources=sorted((ROOT/'scripts').glob('*'))
    historical=ROOT/'agentic-workshop/06-runbook/evaluation/p11-package-validation-evidence.json'
    if historical.exists() and historical.resolve()!=evidence_path.resolve():
        supplement_sources.append(historical)
    correction=ROOT/'agentic-workshop/06-runbook/evaluation/consistency-correction-evidence.json'
    if correction.exists() and correction.resolve()!=evidence_path.resolve():
        supplement_sources.append(correction)
    for source in supplement_sources:
        if not source.is_file() or source.suffix not in {'.py','.json','.md'}:continue
        name=source.relative_to(ROOT).as_posix()
        data=source.read_bytes()
        destination=run/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists() and destination.read_bytes()!=data and not (refresh_evidence and source.resolve()==correction.resolve()):
            raise ValueError('Refusing to overwrite differing detached artifact '+name)
        destination.write_bytes(data)
        payload[name]=data
        detached[name]=digest(data)
    evidence_name=evidence_path.resolve().relative_to(ROOT).as_posix()
    payload[evidence_name]=b'{}'
    checked=0;missing=[]
    for name,data in payload.items():
        if not name.endswith('.md'):continue
        for target in re.findall(r'\]\(([^)]+)\)',data.decode('utf-8')):
            target=target.split('#',1)[0].strip('<>')
            if not target or re.match(r'[a-z]+:',target):continue
            resolved=(ROOT/name).parent.joinpath(unquote(target)).resolve()
            key=resolved.relative_to(ROOT).as_posix()
            if key not in payload and not any(n.startswith(key.rstrip('/')+'/') for n in payload):missing.append({'file':name,'target':target})
            checked+=1
    if missing:raise ValueError('Private overlay missing links: '+json.dumps(missing))
    return {'checked':checked,'missing':missing,'detached_artifact_sha256':detached,'mount':'All 13 ZIPs plus detached scripts and package evidence in a private reviewer tree; never learner distribution'}


def verify(run: Path, reuse: Path | None = None) -> dict:
    run = run.resolve()
    run.relative_to(ROOT / 'dist/p11-candidate')
    evidence = json.loads((run/'build-evidence.json').read_text(encoding='utf-8'))
    approved=json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert evidence['manifest_sha256']==digest(MANIFEST.read_bytes()),'Reviewed manifest anchor differs'
    assert {p['id'] for p in evidence['packages']}=={p['id'] for p in approved['packages']}
    approved_by_id={p['id']:p for p in approved['packages']}
    prior=json.loads(reuse.read_text(encoding='utf-8')) if reuse else None
    results=[]
    for package in evidence['packages']:
        path=(ROOT/safe_path(package['zip'])).resolve()
        path.relative_to(run)
        planned=approved_by_id[package['id']]
        expected={e['destination']:e['sha256'] for e in planned['files']}
        expected.update({name:digest(body.encode('utf-8')) for name,body in planned.get('generated',{}).items()})
        assert package['files']==expected,'Build evidence inventory differs from reviewed manifest'
        assert digest(path.read_bytes()) == package['zip_sha256']
        package_schema(package)
        payload=inspect_zip(path.read_bytes(),package)
        links=link_check(payload) if package['role']=='participant' else None
        result=dict(id=package['id'],files=len(payload),zip_sha256=package['zip_sha256'],relative_links=links,membership='PASS')
        if package['id']=='participant-29-b0':
            result['pedagogical_policy']='PASS: original controlled context and three exact ADR retained; generated material has no diagnosis or priority disclosure'
        if package['id'].startswith('recovery-'):
            reused=next((p for p in prior['packages'] if p['id']==package['id'] and p['zip_sha256']==package['zip_sha256'] and 'recovery_checks' in p),None) if prior else None
            if reused:
                result['recovery_checks']=reused['recovery_checks']
                result['environment']=reused['environment']
                result['reused_technical_evidence']={'sha256':digest(reuse.read_bytes()),'reason':'Exact deterministic Recovery ZIP SHA256 unchanged; current ZIP membership verified anew'}
                results.append(result)
                continue
            suffix=0
            target=run/('unpacked-'+package['id'])
            while target.exists():
                suffix+=1
                target=run/('unpacked-'+package['id']+'-'+str(suffix))
            target.mkdir(exist_ok=False)
            for name,data in payload.items():
                out=target/safe_path(name)
                out.parent.mkdir(parents=True,exist_ok=True)
                out.write_bytes(data)
            version=package['source_version'].lower()
            work=target/('recovery-'+version)
            python=ROOT/f'.codex-tmp/{version}-env/Scripts/python.exe'
            env={**os.environ,'PYTHONPATH':str(work/'src'),'PYTHONDONTWRITEBYTECODE':'1'}
            env.pop('PYTEST_ADDOPTS',None)
            env.pop('PYTHONWARNINGS',None)
            commands=[['-m','pip','check'],['-m','pytest','-q','-p','no:cacheprovider'],['-c',"from fastapi.testclient import TestClient; from smart_ticket.main import app; c=TestClient(app); assert c.get('/health').json()=={'status':'ok'}; spec=c.get('/openapi.json').json(); assert len(spec['paths'])==11; r=c.post('/bookings',json={'trip_id':'T001','passengers':[{'passenger_id':'P1','name':'Demo','passenger_type':'ADULT'}]}); assert r.status_code==201,r.text; bid=r.json()['booking_id']; assert c.post('/bookings/'+bid+'/pay').status_code==200; assert c.post('/bookings/'+bid+'/change',json={'target_trip_id':'T005'}).status_code==200; assert c.post('/bookings/'+bid+'/refund').status_code==200; print(app.version,'Health/OpenAPI/create/pay/change/refund PASS')"]]
            commands[-1][-1]="from smart_ticket.main import app; assert app.version=="+repr(version.upper())+"; "+commands[-1][-1]
            logs=[]
            for args in commands:
                completed=subprocess.run([str(python),'-X','utf8',*args],cwd=work,env=env,text=True,encoding='utf-8',capture_output=True)
                logs.append(dict(command=[str(python),'-X','utf8',*args],cwd=work.relative_to(ROOT).as_posix(),exit_code=completed.returncode,stdout=completed.stdout,stderr=completed.stderr))
                assert completed.returncode==0,completed.stdout+completed.stderr
                if '-m' in args and 'pytest' in args:
                    expected=44 if version=='b1' else 55
                    assert re.search(rf'\b{expected} passed\b',completed.stdout),completed.stdout
                    assert not re.search(r'\d+ (skipped|xfailed|xpassed|failed)',completed.stdout),completed.stdout
            result['recovery_checks']=logs
            result['environment']='Existing version-specific Python3.13 venv; no fresh install claimed'
        results.append(result)
    negatives=[]
    for value in ('../escape','.git/config','/absolute','safe/.venv/config'):
        try: safe_path(value)
        except ValueError: negatives.append(dict(case=value,result='REJECTED'))
        else: raise AssertionError(value)
    try: link_check({'test.md':b'[broken](missing.md)'})
    except ValueError: negatives.append(dict(case='missing relative link',result='REJECTED'))
    else: raise AssertionError('link accepted')
    for mutated in ({'id':'../../outside','role':'participant','release_minute':7},
                    {'id':'participant-07-g0','role':'partcipant','release_minute':7},
                    {'id':'recovery-63-b2','role':'participant','release_minute':0,'source_version':'B2'}):
        try: package_schema(mutated)
        except ValueError: negatives.append(dict(case='schema '+str(mutated),result='REJECTED'))
        else: raise AssertionError(mutated)
    sample=evidence['packages'][0]
    original=ROOT/sample['zip']
    for injected in ('.git/config','evaluation/answer.md','future/b3-answer.py'):
        stream=io.BytesIO(original.read_bytes())
        with zipfile.ZipFile(stream,'a') as archive: archive.writestr(injected,b'forbidden')
        try: inspect_zip(stream.getvalue(),sample)
        except ValueError: negatives.append(dict(case='actual ZIP injected '+injected,result='REJECTED'))
        else: raise AssertionError(injected)
    stream=io.BytesIO(original.read_bytes())
    with zipfile.ZipFile(stream) as archive: payload={name:archive.read(name) for name in archive.namelist()}
    first=next(name for name in payload if name!='PACKAGE-MANIFEST.json')
    payload[first]+=b'corrupt'
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as archive:
        for name,data in payload.items():archive.writestr(name,data)
    try: inspect_zip(stream.getvalue(),sample)
    except ValueError: negatives.append(dict(case='actual ZIP byte corruption',result='REJECTED'))
    else: raise AssertionError('corrupt accepted')
    result=dict(build_manifest_sha256=evidence['manifest_sha256'],output=run.relative_to(ROOT).as_posix(),packages=results,negative_checks=negatives,human_recovery='NOT RUN',real_session_preflight='NOT RUN',human_rehearsal='NOT RUN')
    return result


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Verification requires assertions enabled; Python -O is unsupported')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',type=Path)
    parser.add_argument('--evidence',type=Path,required=True)
    parser.add_argument('--reuse-recovery-evidence',type=Path)
    parser.add_argument('--refresh-private-evidence',action='store_true',help='Allow refreshing only the named detached consistency-correction evidence JSON after its actual ZIP check')
    args=parser.parse_args()
    output=verify(args.run,args.reuse_recovery_evidence)
    output['private_overlay_links']=private_overlay(args.run.resolve(),output,args.evidence,args.refresh_private_evidence)
    args.evidence.parent.mkdir(parents=True,exist_ok=True)
    args.evidence.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    detached=args.run.resolve()/args.evidence.resolve().relative_to(ROOT)
    detached.parent.mkdir(parents=True,exist_ok=True)
    detached.write_bytes(args.evidence.read_bytes())
    print(json.dumps({'packages':len(output['packages']),'negative_checks':len(output['negative_checks'])}))
