# Independent offline audit

## Independence and scope

`code/audit_offline.py` does not import the production candidate/coordinator implementations. It independently hashes historical artifacts and recomputes archived E2 metrics from saved prediction arrays in a separate process. It is not an independent human sign-off.

It does not launch workers, deserialize the RF, fit/adapt a candidate, evaluate partial E3 predictions, or manufacture E4/E5 outputs.

## Why the scientific transformation is unchanged

1. Source fitting and episode prediction workers are copied byte-for-byte from the proven infrastructure; no expression, reduction order, feature selection, estimator parameter, tie-break, or dtype conversion changes.
2. Moving a fully hash-verified RF byte sequence changes host I/O locality only. The worker still opens `/app/rf_final.pkl` under the same sandbox and imports the same numerical runtime. The approved exact-file read-only mount, SHA256 checks, resource limits, descriptor policy and process reaping remain in the unchanged boundary/worker code.
3. The bounded signature read returns the same first 16 bytes for empty, short and long files. Full content SHA256, metadata safeguards and historical inventory checks remain present at the same call sites and frequency. The offline before/after integrity results matched on all paired trials.
4. The trusted transport submits the same decoded packet and sealed worker bytes. Its added I/O record contains cache provenance, not query labels, source transforms or adaptation state. It does not modify the packet delivered to a worker.
5. The E3 coordinator metric functions, support/query construction, RNG replay, phase barrier before scoring, per-episode artifact serializer, paired comparisons and success criteria are unchanged by the bounded-read transformation. Future run-identity changes are explicit provenance changes, not episode identity changes.
6. No cached success flag replaces a content hash. The native file is rehashed by cache reuse, the original boundary and the original worker. The original Windows source remains covered by both coordinator integrity scans. A corrupt native cache causes an error rather than repair or fallback.

## Evidence

- 11 synthetic/static Linux tests passed, including corruption rejection, failed-copy non-publication, source symlink rejection, exact byte preservation, bounded read size and mocked transport packet identity.
- 33 protected artifacts unchanged.
- 216 E2 and 184 E3 inventoried payloads unchanged.
- 60 archived E2 episodes / 300 method-metric records exactly matched independent macro-F1, per-class-F1 and confusion calculations.
- The native RF matched the expected digest on each benchmark pass.
- No candidate metrics or conclusions were produced during the upgrade.

## Limits and blockers

- Static transformation equivalence and archived metric replay do not constitute a fresh optimized prediction-equivalence run.
- Independent E3/E4/E5 end-to-end validation is not certified by replaying E2 metrics.
- E3 timing is a projection; E4 timing is a proxy; E5 timing is unknown. The 180-second worker cap cannot establish E5 performance without an authorized measurement.
- The package prepares the existing E3 coordinator only. E4/E5 transport compatibility does not mean complete candidate-specific coordinator and validator integrations have been approved or tested.
- No resumable coordinator or signed episode ledger is implemented. This follows the conditional Phase 2 stop rule, not a claim that restart safety is already provided.
- Read-only mode and hashes do not defend against an owner/root attacker who controls the kernel and trusted coordinator. The existing trusted-host threat model is unchanged.

## Audit disposition

**OFFLINE INFRASTRUCTURE CHECKS PASS. FULL EXECUTION READINESS CERTIFICATION PENDING.**

The scientific validity argument is unchanged code plus identical frozen bytes and inputs. Empirical confirmation of newly generated optimized predictions remains outside the no-worker authorization. The audit deliberately does not assert readiness for all E3/E4/E5 executions without that evidence.
