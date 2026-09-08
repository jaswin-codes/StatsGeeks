"""Extract reproduced baseline numbers from the executed notebooks and compare
them against the organiser's saved starter references.

Read-only. Run from the repository root:
    python extract_results.py

Starter references come from docs/BASELINE_EXECUTION_PLAN.md "Success Criteria".
They are SAVED ORGANISER OUTPUT, not team-run evidence — this script exists to
compare against them honestly, never to claim agreement that is not there.
"""

import io
import re
import sys
from pathlib import Path

import nbformat

NB3 = Path("working/3-Preprocessing.ipynb")
NB4 = Path("working/4-Modelling.ipynb")

# Starter reference values (macro F1). Source: BASELINE_EXECUTION_PLAN.md.
REF_MADRID_CV = (0.6179, 0.0043)
REF_ZERO_SHOT = 0.3427
REF_PROTO = {
    5:   (0.5437, 0.0324),
    10:  (0.5649, 0.0312),   # organiser-unstated diagnostic budget
    25:  (0.5986, 0.0176),
    50:  (0.6079, 0.0101),
    100: (0.6129, 0.0097),
    200: (0.6150, 0.0036),
}
DIAGNOSTIC_BUDGETS = {10}


def notebook_text(path):
    """Concatenate every stdout / text output in the notebook, in cell order."""
    if not path.exists():
        return None, f"{path} not found"
    nb = nbformat.read(path, as_version=4)
    chunks = []
    n_exec = 0
    errors = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        if cell.get("execution_count") is not None:
            n_exec += 1
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream":
                chunks.append(out.get("text", ""))
            elif out.get("output_type") == "execute_result":
                chunks.append(out.get("data", {}).get("text/plain", ""))
            elif out.get("output_type") == "error":
                errors.append((idx, out.get("ename"), out.get("evalue")))
    return "\n".join(chunks), (n_exec, errors)


def fmt_delta(got, ref):
    d = got - ref
    return f"{d:+.4f}"


print("=" * 78)
print("REPRODUCED BASELINE vs STARTER REFERENCE")
print("=" * 78)

# ---------------------------------------------------------------- Notebook 3
text3, meta3 = notebook_text(NB3)
if text3 is None:
    print(f"Notebook 3: {meta3}")
else:
    n_exec, errors = meta3
    print(f"\nNotebook 3 ({NB3}): {n_exec} code cells executed, {len(errors)} errors")
    for idx, ename, evalue in errors:
        print(f"  ERROR in cell {idx}: {ename}: {evalue}")
    for pat, label in [
        (r"Madrid:\s+([\d,]+)\s+rows", "Madrid raw rows"),
        (r"Amsterdam:\s+([\d,]+)\s+rows", "Amsterdam raw rows"),
        (r"Total features:\s+(\d+)", "Feature count"),
        (r"Saved to:\s+(\S+)\s+\(([\d.]+)\s*MB\)", "Pickle"),
    ]:
        m = re.search(pat, text3)
        if m:
            print(f"  {label}: {' '.join(m.groups())}")
    for m in re.finditer(r"(Madrid|Amsterdam): \((\d+), (\d+)\)\s+NaN check: (\w+)", text3):
        city, rows, cols, status = m.groups()
        print(f"  {city} feature matrix: ({rows}, {cols})  NaN check: {status}")

# ---------------------------------------------------------------- Notebook 4
text4, meta4 = notebook_text(NB4)
if text4 is None:
    print(f"\nNotebook 4: {meta4}")
    print("\n(Notebook 4 has not been executed yet — nothing to compare.)")
    sys.exit(0)

n_exec, errors = meta4
print(f"\nNotebook 4 ({NB4}): {n_exec} code cells executed, {len(errors)} errors")
for idx, ename, evalue in errors:
    print(f"  ERROR in cell {idx}: {ename}: {evalue}")

# CV fits actually completed — count the per-fit lines, do not trust the summary alone.
fit_lines = re.findall(r"Fit\s+(\d+)/(\d+):\s+macro-F1 = ([\d.]+)", text4)
print(f"\n-- Madrid repeated CV --")
print(f"  Completed fit lines found: {len(fit_lines)}")
if fit_lines:
    expected_total = int(fit_lines[0][1])
    print(f"  Expected total fits:      {expected_total}")
    if len(fit_lines) != expected_total:
        print(f"  *** INCOMPLETE: only {len(fit_lines)} of {expected_total} fits present ***")
    scores = [float(f[2]) for f in fit_lines]
    print(f"  Per-fit macro F1 range:   {min(scores):.4f} – {max(scores):.4f}")

m = re.search(r"Mean macro F1:\s+([\d.]+)\s*\+/-\s*([\d.]+)", text4)
if m:
    got_mean, got_std = float(m.group(1)), float(m.group(2))
    ref_mean, ref_std = REF_MADRID_CV
    print(f"  Reproduced: {got_mean:.4f} +/- {got_std:.4f}")
    print(f"  Starter:    {ref_mean:.4f} +/- {ref_std:.4f}")
    print(f"  Delta mean: {fmt_delta(got_mean, ref_mean)}"
          f"   ({abs(got_mean - ref_mean) / ref_std:.2f}x the starter's own fold std)")

m = re.search(r"In-sample accuracy:\s+([\d.]+)", text4)
if m:
    print(f"\n-- Final Madrid RF --\n  In-sample accuracy: {float(m.group(1)):.4f} (expected ~1.0)")

print("\n-- Amsterdam zero-shot --")
m = re.search(r"Zero-shot transfer to Amsterdam.*?Macro F1:\s+([\d.]+)", text4, re.S)
if m:
    got = float(m.group(1))
    print(f"  Reproduced: {got:.4f}")
    print(f"  Starter:    {REF_ZERO_SHOT:.4f}")
    print(f"  Delta:      {fmt_delta(got, REF_ZERO_SHOT)}")

print("\n-- Amsterdam prototype transfer (TARGET-ONLY — not supervised transfer) --")
proto = re.findall(r"(\d+)\s+shots/class:\s+macro-F1 = ([\d.]+)\s*\+/-\s*([\d.]+)", text4)
if proto:
    print(f"  {'Shots':>6} {'Reproduced':>20} {'Starter':>20} {'Delta':>9}")
    for shots, mean, std in proto:
        s = int(shots)
        gm, gs = float(mean), float(std)
        tag = "  (diagnostic)" if s in DIAGNOSTIC_BUDGETS else ""
        if s in REF_PROTO:
            rm, rs = REF_PROTO[s]
            print(f"  {s:>6} {gm:>11.4f} +/-{gs:.4f} {rm:>11.4f} +/-{rs:.4f} {fmt_delta(gm, rm):>9}{tag}")
        else:
            print(f"  {s:>6} {gm:>11.4f} +/-{gs:.4f} {'—':>20} {'—':>9}{tag}")
    found = {int(s) for s, _, _ in proto}
    missing = set(REF_PROTO) - found
    if missing:
        print(f"  *** MISSING BUDGETS: {sorted(missing)} ***")
else:
    print("  No prototype results found.")

print("\n" + "=" * 78)
print("REMINDER: 'Starter' columns are SAVED ORGANISER OUTPUT, never team-run")
print("evidence. Report differences with their explanation; do not tune to match.")
print("=" * 78)
