import requests
import json
import time
from pprint import pprint

headers = {
    'X-API-Key' : '162-d4d99873c440d0e294a5e11e4f731df8'
}

def hello():
    r = requests.get('http://2016sv.icfpcontest.org/api/hello', headers=headers)
    time.sleep(1)
    return json.loads(r.text)

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

def submit_problem():
    pass

def submit_solution(problem_id, solution_spec):
    r = requests.post("http://2016sv.icfpcontest.org/api/solution/submit", files=(('problem_id', str(problem_id)), ('solution_spec', solution_spec)), headers=headers)
    time.sleep(1)
    return json.loads(r.text)

def save_problems(problems):
    # 100回近くAPIを使ってしまうので注意
    for i in range(len(problems)):
        problem_spec_hash = problems[i]['problem_spec_hash']
        problem_input = blob_lookup(problem_spec_hash)
        open('problem_inputs/problem-{0:d}.input.txt'.format(problems[i]['problem_id']), 'w').write(problem_input)

def save_json(fname, json_obj):
    json.dump(json_obj, open(fname, 'w'), ensure_ascii=False)

snapshot_hash_json = snapshot()

assert(snapshot_hash_json['ok'])

snapshot_hash = snapshot_hash_json['snapshots'][-1]['snapshot_hash']

snapshot_json = blob_lookup(snapshot_hash)

# save_json('snapshot/' + snapshot_hash + '.json', snapshot_json)

problems = snapshot_json['problems']


