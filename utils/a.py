#!/usr/bin/env python3
import logging
logging.basicConfig(level=logging.INFO)

import subprocess
import time
import json
API_KEY = '162-d4d99873c440d0e294a5e11e4f731df8'
def api_without_cache(query, params=None, json=False):
    logging.info('api: %s %s', query, params)
    time.sleep(1.1)
    command = [ 'curl', '-s', '--compressed', '-L', '-H', 'Expect:', '-H', 'X-API-Key: ' + API_KEY, 'http://2016sv.icfpcontest.org/api/' + query ]
    if params:
        for key, val in params.items():
            command += [ '--form-string', key + '=' + val ]
    p = subprocess.run(command, stdout=subprocess.PIPE)
    p.check_returncode()
    if json:
        return globals()['json'].loads(p.stdout.decode())
    else:
        return p.stdout

hello = 'hello'
blob = lambda hash: 'blob/' + hash
snapshot_list = 'snapshot/list'
problem_submit = 'problem/submit'
solution_submit = 'solution/submit'

import os
import subprocess
def cache_directory():
    s = subprocess.run([ 'git', 'rev-parse', '--show-toplevel' ], stdout=subprocess.PIPE)
    return os.path.join(s.stdout.decode().strip(), 'cache')

import datetime
import time
def current_hour():
    now = datetime.datetime.utcnow()
    now = datetime.datetime(now.year, now.month, now.day, now.hour)
    return int(time.mktime(now.timetuple()))

def api(query, params=None, volatile=False, json=False): # with cache
    if params:
        return api_without_cache(query, params, json=json)
    else:
        cache = cache_directory()
        if volatile:
            cache = os.path.join(cache, str(current_hour()))
        cache = os.path.join(cache, query)
        if not os.path.exists(os.path.dirname(cache)):
            os.makedirs(os.path.dirname(cache))
        if os.path.exists(cache):
            logging.info('cached: %s %s', query, params)
            with open(cache) as fh:
                s = fh.buffer.read()
        else:
            s = api_without_cache(query)
            with open(cache, 'w') as fh:
                fh.buffer.write(s)
        if json:
            return globals()['json'].loads(s.decode())
        else:
            return s

def get_latest_snapshot():
    snapshots = api(snapshot_list, volatile=True, json=True)
    assert snapshots['ok']
    snapshots = snapshots['snapshots']
    latest_snapshot_hash = max(snapshots, key=lambda x: x['snapshot_time'])['snapshot_hash']
    snapshot = api(blob(latest_snapshot_hash), json=True)
    return snapshot

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparser = subparsers.add_parser('update')
    subparser = subparsers.add_parser('snapshot')
    subparser = subparsers.add_parser('solve')
    subparser.add_argument('solver')
    subparser.add_argument('problem', nargs='*', type=int)
    args = parser.parse_args()

    if args.command == 'update':
        snapshot = get_latest_snapshot()
        for problem in snapshot['problems']:
            api(blob(problem['problem_spec_hash']))

    elif args.command == 'snapshot':
        snapshot = get_latest_snapshot()
        print(json.dumps(snapshot))

    elif args.command == 'solve':
        snapshot = get_latest_snapshot()
        problems = snapshot['problems']
        if args.problem:
            problems = [ x for x in problems if x['problem_id'] in args.problem ]
        for problem in problems:
            logging.info('problem: %d', problem['problem_id'])
            p = subprocess.Popen(args.solver, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            problem_spec = api(blob(problem['problem_spec_hash']))
            logging.info('problem_spec: %s', problem_spec)
            solution_spec = p.communicate(problem_spec)[0]
            logging.info('solution_spec: %s', solution_spec)
            params = { 'problem_id': str(problem['problem_id']), 'solution_spec': solution_spec.decode() }
            resp = api_without_cache(solution_submit, params, json=True)
            logging.info('reuslt: %s', json.dumps(resp))
            assert resp['ok']

    else:
        assert False
