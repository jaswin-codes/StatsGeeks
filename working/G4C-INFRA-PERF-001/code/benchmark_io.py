"""Read-only RF I/O benchmark plus authorized hash-identical native cache creation.

No worker launch or model unpickling. stdout is the complete measurement record.
"""
import argparse
import json
from pathlib import Path
import platform
import time

from immutable_io import RF_SHA256, sha256, stage_frozen_file


def timed_hash(path):
    start = time.perf_counter()
    digest = sha256(path)
    if digest != RF_SHA256:
        raise RuntimeError("RF digest mismatch")
    return time.perf_counter() - start


def timed_stream(path):
    start = time.perf_counter()
    size = 0
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            size += len(block)
    return {"seconds": time.perf_counter() - start, "bytes": size}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    staging = stage_frozen_file(args.source, args.cache, RF_SHA256)
    destination = Path(staging["path"])
    samples = []
    for i in range(3):
        # Alternate order to reduce systematic warm-cache order bias.
        order = [("source", args.source), ("native", destination)]
        if i % 2:
            order.reverse()
        sample = {"repeat": i + 1}
        for name, path in order:
            sample[name + "_hash_seconds"] = timed_hash(path)
            sample[name + "_stream"] = timed_stream(path)
        samples.append(sample)
    print(json.dumps({"platform": platform.platform(), "staging": staging,
                      "samples": samples, "workers_launched": 0,
                      "models_loaded": 0, "experiments_started": 0}, indent=2))


if __name__ == "__main__":
    main()
