import contextlib
import sys
from pathlib import Path

import tomli_w
import tomllib


def main(_pyproject_f: str) -> None:
    _pyproject_fpath = Path(_pyproject_f)
    if not _pyproject_fpath.is_file():
        print(f"ERR: {_pyproject_fpath} doesn't exist!")
        sys.exit(1)

    _loaded = tomllib.loads(_pyproject_fpath.read_text())
    print(f"loaded: {_loaded}")

    _loaded["project"].pop("readme", None)

    with contextlib.suppress(Exception):
        _dynamic = _loaded["project"].pop("dynamic")
        _dynamic.remove("version")
        if _dynamic:
            _loaded["project"]["dynamic"] = _dynamic

    _loaded["project"]["version"] = "0.0.0"
    with contextlib.suppress(Exception):
        _loaded["tool"]["hatch"].pop("version", None)

    with contextlib.suppress(Exception):
        _metadata = _loaded["tool"]["hatch"].pop("metadata")
        _metadata.pop("hooks", None)
        if _metadata:
            _loaded["tool"]["hatch"]["metadata"] = _metadata

    print(f"patched: {_loaded}")
    _pyproject_fpath.write_text(tomli_w.dumps(_loaded))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _pyproject_f = sys.argv[1]
        print(f"Patching {_pyproject_f} ...")
        main(_pyproject_f)
    else:
        print("ERR: expect exactly one argument")
        sys.exit(1)
