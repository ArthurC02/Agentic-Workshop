"""Package the reviewed participant HTML only; never distribute source folders."""
from pathlib import Path
import hashlib
import io
import json
import sys
import zipfile

import build_materials as bm


def package(edition=bm.MAIN):
    expected, _ = bm.build_runbook(edition=edition)
    source = bm.outputs(edition.materials)["runbook"]
    if bm.read_bytes(source) != expected:
        raise bm.BuildError("Runbook is stale; run build_materials.py first")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        entry = zipfile.ZipInfo("runbook.html", (2026, 1, 1, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, expected)
    data = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        assert archive.namelist() == ["runbook.html"]
        assert archive.read("runbook.html") == expected
    target = bm.ROOT / edition.package_output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(json.dumps({"output": target.relative_to(bm.ROOT).as_posix(),
                      "members": ["runbook.html"], "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()}, ensure_ascii=False))
    return target


if __name__ == "__main__":
    package(bm.load_edition(sys.argv[1] if len(sys.argv) > 1 else "main"))  # usage: package_materials.py [main|dlc]
