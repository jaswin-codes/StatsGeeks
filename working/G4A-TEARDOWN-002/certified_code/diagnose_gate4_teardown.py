"""Reproduce old cleanup with contemporaneous observation; no reaping intervention."""
import json
from pathlib import Path
from gate4_production_boundary import run, sanitize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'working/G4A-TEARDOWN-002'


def main():
    p = json.loads((ROOT / 'working/G4A-PRODUCTION-001/current_packet.json').read_text())
    code = (ROOT / 'working/gate4_production_probe.py').read_bytes()
    for i in range(3):
        raw, ev = run(p, code, timeout=60, lifecycle_reap=False)
        ev['diagnostic_only_not_certification'] = True
        ev['constant_probe_output_valid'] = ev['returncode'] == 0 and set(sanitize(raw, p)) == {1}
        with (OUT / f'lifecycle_diagnostic_{i+1}.json').open('x') as f:
            json.dump(ev, f, indent=2, sort_keys=True)
        print(json.dumps({'attempt':i+1,'immediate':ev['lifecycle']['immediate_post_wait'],
                          'last':ev['lifecycle']['final_survivors'],
                          'transitions':[(x['stage'], x['pid'], x['process']['state'] if x['process'] else None,
                                          x['process']['ppid'] if x['process'] else None) for x in ev['lifecycle']['events'] if x['kind']=='observation']}))
        if ev['stderr'] or not ev['lifecycle']['pass_']:
            raise RuntimeError('Diagnostic failed or process persisted beyond bounded observation')


if __name__ == '__main__':
    main()
