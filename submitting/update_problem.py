import requests
import json
import time
from glob import glob
import sys
import os.path

headers = {
    'X-API-Key' : '162-d4d99873c440d0e294a5e11e4f731df8'
}

def blob_lookup(blob_hash):
    r = requests.get('http://2016sv.icfpcontest.org/api/blob/' + blob_hash, headers=headers)
    time.sleep(1)
    try:
        res = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        res = r.text
    return res

def snapshot():
    r = requests.get('http://2016sv.icfpcontest.org/api/snapshot/list', headers=headers)
    time.sleep(1)
    return json.loads(r.text)

def save_json(fname, json_obj):
    json.dump(json_obj, open(fname, 'w'), ensure_ascii=False)

def load_json(fname):
    return json.load(open(fname, 'r'))

if not os.path.exists('problem_list'):
    save_json('problem_list', [])

if not os.path.exists('problem_spec'):
    save_json('problem_spec', {})

if glob('./latest_snap_*') != []:
    if time.time() - int(glob('./latest_snap_*')[-1].split('_')[-1]) < 3600:
        sys.exit(0)

snapshot_hash_json = snapshot()

snapshot_hash = snapshot_hash_json['snapshots'][-1]['snapshot_hash']
snapshot_time = snapshot_hash_json['snapshots'][-1]['snapshot_time']

snapshot_json = blob_lookup(snapshot_hash)

save_json('latest_snap_{0:d}'.format(snapshot_time), snapshot_json)

problem_list = load_json('problem_list')
if len(problem_list) != len(snapshot_json['problems']):
    diff_problem_list = snapshot_json['problems'][len(problem_list) - len(snapshot_json['problems']):]
    problem_spec = load_json('problem_spec')
    for i in range(len(diff_problem_list)):
        problem_spec[diff_problem_list[i]['problem_id']] = blob_lookup(diff_problem_list[i]['problem_spec_hash'])
    save_json('problem_spec', problem_spec)

save_json('problem_list', snapshot_json['problems'])






