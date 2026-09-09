"""Profile unchanged vs bounded integrity scans; no main(), workers, or fitting."""
import json
from pathlib import Path
import sys
import time
import types

from prepare_assets import PROVEN, bounded_coordinator, digest


def module_from_bytes(source, filename, name):
    module = types.ModuleType(name)
    module.__file__ = str(filename.resolve())
    exec(compile(source, str(filename), "exec"), module.__dict__)
    return module


def main():
    path = PROVEN / "execution_coordinator.py"
    source = path.read_bytes()
    changed = bounded_coordinator(source)
    before = module_from_bytes(source, path, "profile_original")
    after = module_from_bytes(changed, path, "profile_bounded")
    samples = []
    for repeat in range(3):
        order = [("before", before), ("after", after)]
        if repeat % 2:
            order.reverse()
        sample = {"repeat": repeat + 1}
        results = {}
        for name, module in order:
            start = time.perf_counter()
            results[name] = module.preexisting_integrity()
            sample[name + "_seconds"] = time.perf_counter() - start
        sample["same_result"] = results["before"] == results["after"]
        if not sample["same_result"]:
            raise RuntimeError("Integrity outputs changed during paired measurement")
        samples.append(sample)
    print(json.dumps({"source_sha256": digest(source), "bounded_sha256": digest(changed),
                      "python": sys.version, "samples": samples,
                      "integrity_checks_skipped": 0, "workers_launched": 0,
                      "experiments_started": 0}, indent=2))


if __name__ == "__main__":
    main()
