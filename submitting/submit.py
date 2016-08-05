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

def submit_solution():
    pass

def save_problems():
    for i in range(len(problems)):
    problem_spec_hash = problems[i]['problem_spec_hash']
    problem_input = blob_lookup(problem_spec_hash)
    open('problem_inputs/problem-{0:d}.input.txt'.format(i), 'w').write(problem_input)


snapshot_hash_json = snapshot()

assert(snapshot_hash_json['ok'])

snapshot_hash = snapshot_hash_json['snapshots'][-1]['snapshot_hash']

snapshot_json = blob_lookup(snapshot_hash)

problems = snapshot_json['problems']


