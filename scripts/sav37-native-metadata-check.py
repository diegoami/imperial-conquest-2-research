#!/usr/bin/env python3
"""Check committed SAV37 scalar/hash receipts, without opening private evidence.

This is NOT verify_native_packet.py and does not rehash private SAV/PNG bytes.
Usage: python3 -I scripts/sav37-native-metadata-check.py CONQUEST --output NEW.json
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess

PIN = '7fe20bedba0b9cdbb012b1b348c96507f6a65768'
BASE = 'runs/experiments/data/run-exp-sav-export37-native/'
CANDIDATES = [
    '5e85a985382dc56ae964889ed01d4fda56b0e2414ccaede5e18d03b3bd2a314c',
    '2afa2d64170a63fefbf12c5678700a02024f01eb0f682a0cbc7efffa63b7288f',
    '5d82f47aa77f2736afddeac8c23754305455afa7e524636b98d12b4c2a88669a',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def audit(repo):
    hashes = {}

    def raw(path):
        data = subprocess.check_output(['git', '-C', str(repo), 'show', PIN + ':' + path])
        hashes[path] = hashlib.sha256(data).hexdigest()
        return data

    def record(name):
        return json.loads(raw(BASE + name))

    tree = subprocess.check_output(
        ['git', '-C', str(repo), 'ls-tree', '-r', '--name-only', PIN, BASE], text=True)
    names = [p for p in tree.splitlines() if p.endswith('.json')]
    for name in names:
        json.loads(raw(name))
    v2, v3 = (record(f'native-packet-validation-v{i}.json') for i in (2, 3))
    for field in ('checks', 'immutable_inputs', 'private_files', 'private_captures'):
        require(v2[field] == v3[field], f'v2/v3 {field}')
    require(v3['native_candidate_sequences_completed'] == v3['required'] == 3, '3/3')
    require(v3['internal_callback_instruction_trace'] == 'UNVERIFIED', 'callback limit')
    cases = []
    for case, candidate in enumerate(CANDIDATES, 1):
        completion = record(f'case{case}-completion-v1.json')
        order = record(f'case{case}-order-effect-v1.json')
        stages = {f['stage']: f for f in v3['private_files'] if f['case'] == case}
        require(stages['I']['sha256'] == stages['L']['sha256'] == candidate, 'initial identity')
        require(stages['E']['sha256'] == stages['R']['sha256'], 'reopen identity')
        require(len({stages[s]['sha256'] for s in ('L', 'O', 'E')}) == 3, 'distinct phases')
        produced = next(f for f in v3['immutable_inputs']
                        if f['case'] == case and f['role'] == 'candidate')
        require(produced['sha256'] == candidate and produced['unchanged'], 'candidate receipt')
        require(order['verified_non_noop_order'] and len(order['queue_changes']) == 1, 'order')
        require(order['queue_changes'][0]['after'][1:3] == [0, 3000], 'recruit LI3000')
        if case == 1:
            require(completion['case1_native_open_order_AND_endturn_newsave_close_freshreopen_sequence']
                    == 'PASS observed', 'case1 completion')
            require(completion['end_turn']['commands_issued'] == 1, 'case1 turn count')
            require(completion['fresh_reopen_save_exact_postturn_byte_identity'], 'case1 reopen')
            require(completion['final_active_original_process_count'] == 0, 'case1 historical exit')
        else:
            require(completion['original_open_order_AND_endturn_newsave_normalclose_freshreopen_sequence']
                    == 'PASS observed', 'completion')
            require(completion['endturn_commands_issued'] == 1, 'turn count')
            require(completion['reopen_exact_postturn_byte_identity'], 'reopen')
            require(completion['final_active_original_processes'] == 0, 'historical exit')
            control = record(f'control{case}-comparison-v1.json')
            require(control['after_sha256'] == candidate and not control['UI_geometry_changes'],
                    'control exact candidate')
            require(control['no_extra_gameplay_changes'], 'control scope')
        cases.append({'case': case, 'candidate_sha256': candidate,
                      'candidate_size': produced['size'],
                      'postturn_and_reopen_sha256': stages['E']['sha256'],
                      'recorded_phase_hash_relations': 'PASS'})
    control1 = record('control1-comparison-v1.json')
    comp = next(c for c in control1['comparisons']
                if c['before'] == 'control_before' and c['after'] == 'control_after')
    require(comp['changed_offsets_decimal'] == [111294, 111330, 111331, 111332, 111333],
            'control1 tax/area geometry')
    require(control1['control1_result']['extra_gameplay_byte_changes'] is False,
            'control1 scope')
    require(control1['control1_result']['viewport_changed'] is False, 'control1 viewport')
    validator = raw('runs/experiments/sav_export37_native/verify_native_packet.py').decode()
    guards = [n for n in ast.walk(ast.parse(validator)) if isinstance(n, ast.Assert)
              and isinstance(n.test, ast.Compare) and ast.unparse(n.test).startswith('len({stage[')]
    require(len(guards) == 1, 'v3 three-phase byte guard')
    code = compile(ast.fix_missing_locations(ast.Module(body=guards, type_ignores=[])),
                   '<actual v3 guard>', 'exec', optimize=0)

    class Value:
        def __init__(self, value):
            self.value = value

        def read_bytes(self):
            return self.value

    for values, rejects in (((b'a', b'b', b'a'), True), ((b'a', b'a', b'b'), True),
                            ((b'a', b'b', b'c'), False)):
        failed = False
        try:
            exec(code, {'stage': dict(zip(('L', 'O', 'E'), map(Value, values)))})
        except AssertionError:
            failed = True
        require(failed == rejects, 'v3 synthetic counterexample')
    return {'scope': 'committed scalar/hash consistency only; no private-byte rehash or game',
            'upstream_pin': PIN, 'metadata_checks': 'PASS', 'cases': cases,
            'current_packet_JSON_files': len(names),
            'historical_v2_parsed_JSON_files': v2['parsed_measurement_JSON_files'],
            'historical_v3_parsed_JSON_files': v3['parsed_measurement_JSON_files'],
            'historical_private_capture_hashes': len(v3['private_captures']),
            'actual_v3_guard_synthetic_cases': 3,
            'native_JSON_conversions': 0, 'internal_callback_trace': 'UNVERIFIED',
            'private_files_opened': 0, 'packet_artifact_sha256': hashes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('conquest', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('output exists; choose a new path')
    result = audit(args.conquest)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('PASS: 3 case receipt chains, controls, v2/v3 consistency and v3 guard counterexamples; metadata only')


if __name__ == '__main__':
    main()
