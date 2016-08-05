import requests
import json
import time
from pprint import pprint
from glob import glob
import sys
import subprocess

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

def submit_problem(solution_spec, publish_time):
    r = requests.post("http://2016sv.icfpcontest.org/api/solution/submit", files=(('solution_spec', solution_spec), ('publish_time', str(publish_time))), headers=headers)
    time.sleep(1)
    return json.loads(r.text)

def submit_solution(problem_id, solution_spec):
    r = requests.post("http://2016sv.icfpcontest.org/api/solution/submit", files=(('problem_id', str(problem_id)), ('solution_spec', solution_spec)), headers=headers)
    time.sleep(1)
    return json.loads(r.text)

# def save_problems(problems):
#     # 100回近くAPIを使ってしまうので注意
#     for i in range(len(problems)):
#         problem_spec_hash = problems[i]['problem_spec_hash']
#         problem_input = blob_lookup(problem_spec_hash)
#         open('problem_inputs/problem-{0:d}.input.txt'.format(problems[i]['problem_id']), 'w').write(problem_input)

def save_json(fname, json_obj):
    json.dump(json_obj, open(fname, 'w'), ensure_ascii=False)

def load_json(fname):
    return json.load(open(fname, 'r'))

def get_solution_spec(problem_spec):
    p = subprocess.Popen('./solve', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    solution_spec = p.communicate(problem_spec)[0]
    return solution_spec

if time.time() - int(glob('./latest_snap_*')[-1].split('_')[-1]) >= 3600:
    print('Please execute update_snap.py')
    sys.exit(1)

problems = load_json('problem_list')
problem_spec_dict = load_json('problem_spec')

for problem in problems:
    solution_spec = get_solution_spec(problem_spec_dict[problem['problem_id']])
    res = submit_solution(problem['problem_id'], solution_spec)
    print('problem_id : {0}, resemblance : {1}'.format(problem['problem_id'], res['resemblance']))
























