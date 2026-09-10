"""One-time documentation relocation; never traverses scientific directories for edits."""
from pathlib import Path
import json
import re
import shutil
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'reproducibility/release'

def main():
    moves = {}
    for p in ROOT.glob('*.md'):
        if p.name != 'README.md':
            moves[p.relative_to(ROOT).as_posix()] = 'archive/release_history/' + p.name
    active = {
        'METHOD.md': 'methodology', 'PIPELINE.md': 'methodology',
        'REPRODUCIBILITY.md': 'reproducibility', 'LICENSE_STATUS.md': 'reproducibility',
        'LIMITATIONS.md': 'methodology', 'FAQ.md': 'judge',
        'WRITTEN_JUSTIFICATION.md': 'judge', 'PROJECT_SUMMARY.md': 'judge',
        'PRESENTATION_OUTLINE.md': 'judge', 'SUBMISSION_INVENTORY.md': 'judge',
    }
    keep = {'AGENTS.md', 'MASTER_PLAN.md', 'Hackathon_Analysis_Report.md',
            'building_age_transfer_learning_hackathon.md', 'hackathon_computing_resources.md',
            'METRIC_LEARNING_APPROACH.md'}
    for p in (ROOT / 'docs').glob('*.md'):
        if p.name in keep:
            continue
        dest = 'docs/' + active[p.name] if p.name in active else 'archive/team_history'
        moves[p.relative_to(ROOT).as_posix()] = dest + '/' + p.name
    # Retire unsafe/stale release generators, not research implementations.
    for name in ['build_repository_polish.py', 'write_repository_polish_reports.py']:
        moves['scripts/' + name] = 'archive/release_history/scripts/' + name
    moves['presentation/build_deck.py'] = 'archive/release_history/presentation/build_deck.py'
    for old, new in moves.items():
        target = ROOT / new
        if target.exists():
            raise FileExistsError(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(ROOT / old, target)
    # Rebase Markdown links in editable documentation only. Frozen evidence stays untouched.
    import os
    candidates = [ROOT / 'README.md'] + list((ROOT / 'docs').rglob('*.md'))
    candidates += [ROOT / n for n in moves.values() if n.endswith('.md')]
    reverse = {v: k for k, v in moves.items()}
    for p in candidates:
        if p.name in {'AGENTS.md', 'Hackathon_Analysis_Report.md'}:
            continue
        now = p.relative_to(ROOT).as_posix()
        old = reverse.get(now, now)
        def fix(match):
            value = match.group(2)
            path, sep, anchor = value.partition('#')
            if not path or re.match(r'\w+://|mailto:', path):
                return match.group(0)
            absolute = (ROOT / old).parent / unquote(path)
            rel = os.path.relpath(absolute.resolve(), ROOT).replace('\\', '/')
            if rel.startswith('../'):
                return match.group(0)
            target = ROOT / moves.get(rel, rel)
            value = os.path.relpath(target, p.parent).replace('\\', '/') + (sep + anchor if sep else '')
            return match.group(1) + value + match.group(3)
        text = p.read_text(encoding='utf-8')
        changed = re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))', fix, text)
        if changed != text:
            p.write_text(changed, encoding='utf-8')
    (DEST / 'moves.json').write_text(json.dumps(moves, indent=2), encoding='utf-8')
    print(f'Relocated {len(moves)} documentation/build files; scientific paths unchanged.')

if __name__ == '__main__':
    main()
