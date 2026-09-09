"""Explicit scenario estimates, NOT candidate runtime certification."""
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT/'working/G4C-INFRA-PERF-001/evidence'


def main():
    io = json.loads((EVIDENCE/'native_io_benchmark.json').read_text())
    coord = json.loads((EVIDENCE/'coordinator_benchmark.json').read_text())
    source_hash = statistics.mean(s['source_hash_seconds'] for s in io['samples'])
    native_hash = statistics.mean(s['native_hash_seconds'] for s in io['samples'])
    stream_gain = statistics.mean(s['source_stream']['seconds']-s['native_stream']['seconds'] for s in io['samples'])
    scan_gain = statistics.mean(s['before_seconds']-s['after_seconds'] for s in coord['samples'])
    base = 5750.0  # Previous 52-episode trace extrapolation: approximately 5600-5900 s.
    # Preserve both existing RF hash checks; staging adds one native verification.
    gain_per_episode = 2*(source_hash-native_hash)-native_hash + 2*scan_gain + stream_gain
    point = base - 60*gain_per_episode + io['staging']['seconds']
    # Historical faster /mnt/c hash, slowest measured native hash, minimum bounded
    # read gain, and ZERO credit for forest deserialization I/O savings.
    slow_native = max(s['native_hash_seconds'] for s in io['samples'])
    conservative_gain = 2*(13.174825191-slow_native)-slow_native + 2*min(
        s['before_seconds']-s['after_seconds'] for s in coord['samples'])
    conservative = base-60*conservative_gain+io['staging']['seconds']
    result = {
        'estimate_only': True, 'baseline_E3_generation_seconds': [5600, 5900],
        'E3_point_generation_seconds': point,
        'E3_conservative_scenario_generation_seconds': conservative,
        'E3_point_savings_per_episode_seconds': gain_per_episode,
        'E3_conservative_margin_to_5000_seconds': 5000-conservative,
        'E4_generation_proxy_seconds': [2200, 3000],
        'E4_basis': 'Unmeasured E4; E2 2570.845 s proxy, bounded signature improvement; include 61st zero-shot record',
        'E5_generation_seconds': None,
        'E5_basis': 'No authorized worker measurements; leaf-loop time and 180 s worker-cap compliance unknown',
        'E5_planning_formula': 'approximately 1500 + 60 * native-worker-seconds; not a measurement',
        'independent_validation_seconds': {'E3': None, 'E4': None, 'E5': None},
        'phase_3_decision': 'NOT_TRIGGERED: E3 prediction-generation projection below 5000; do not redesign for unmeasured E5',
        'limitations': [
            'Different-time I/O measurements cannot establish an end-to-end speedup.',
            'Native staging verification adds a full hash; included in estimates.',
            'Sequential-read benchmark is an I/O proxy, not measured pickle-load time.',
            'Runtime increases under memory pressure or cold caches remain possible.',
            'Scoring and independent candidate validation durations not included or certified.',
            'No optimized workers or experiments launched.'
        ]
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
