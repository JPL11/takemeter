"""Run three trials of the committed criteria; preserve raw CLI output."""
import csv
import json
from pathlib import Path
import subprocess
import sys


def batch(folder, name, lines):
    log = folder / f'{name}.jsonl'
    result = subprocess.run([sys.executable, 'run.py', '--log', str(log)], input='\n'.join(lines)+'\n', text=True, capture_output=True)
    (folder / f'{name}.stdout').write_text(result.stdout)
    (folder / f'{name}.stderr').write_text(result.stderr)
    records = [json.loads(line) for line in log.read_text().splitlines()]
    return result, records


def main():
    folder = Path(sys.argv[1])
    folder.mkdir(parents=True, exist_ok=False)
    texts = [row['text'] for row in list(csv.DictReader(open('test_split.csv')))[:10]]
    lines = [json.dumps({'text': text}) for text in texts]
    from run import Classifier
    reference = Classifier('models/takemeter')
    reference_labels = [reference.predict(text)['label'] for text in texts]
    (folder / 'reference.json').write_text(json.dumps(reference_labels))
    summary = []
    for trial in range(1, 4):
        print(f'Trial {trial}', flush=True)
        result, records = batch(folder, f't{trial}-valid', lines)
        valid = sum(r['status']=='ok' and r['output']['label'] in {'experience','argument','assertion','chatter'} and 0 <= r['output']['confidence'] <= 1 for r in records)
        regression = sum(r['status']=='ok' and r['output']['label']==label for r, label in zip(records, reference_labels))
        mixed_result, mixed = batch(folder, f't{trial}-mixed', lines[:8]+['{','not json'])
        fields = {'timestamp','input','output','status','duration_ms','cpu_seconds'}
        logged = sum(fields <= r.keys() and r['duration_ms']>=0 and r['cpu_seconds']>=0 for r in mixed)
        isolated = 0
        for i, bad in enumerate(['{','{}','{"text":""}','{"text":42}','[]']):
            res, rec = batch(folder, f't{trial}-bad{i}', [bad, lines[0]])
            isolated += len(rec)==2 and rec[0]['status']=='error' and rec[1]['status']=='ok' and res.returncode==1 and 'Traceback' not in res.stderr
        _, warm = batch(folder, f't{trial}-warm', [lines[0]]+lines)
        fast = sum(r['status']=='ok' and r['duration_ms']<=500 for r in warm[1:])
        summary.append({'trial':trial, 'standalone':f'{valid}/10', 'logging':f'{logged}/{len(mixed)}', 'isolation':f'{isolated}/5', 'latency':f'{fast}/10', 'regression':f'{regression}/10', 'met':[valid==10 and len(records)==10 and result.returncode==0, logged==10 and len(mixed)==10, isolated==5, fast>=9, regression==10]})
        (folder / 'summary.json').write_text(json.dumps(summary, indent=2))
    # Ten warm inference requests, explicit cost basis, plus separately visible startup.
    _, cost = batch(folder, 'cost', [lines[0]]+lines)
    measurement = {'n':10, 'mean_cpu_seconds':sum(r['cpu_seconds'] for r in cost[1:])/10, 'mean_wall_seconds':sum(r['duration_ms'] for r in cost[1:])/10000, 'cold_first_request_seconds':cost[0]['duration_ms']/1000, 'scope':'warm request CPU process time; excludes setup, model load, GPU, idle time'}
    (folder / 'cost.json').write_text(json.dumps(measurement, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
