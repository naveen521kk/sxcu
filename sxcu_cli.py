import sys
from pathlib import Path

# If we're run uninstalled, add the script directory to sys.path to ensure that
# we always import the correct mesonbuild modules even if PYTHONPATH is mangled
sxcu_exe = Path(sys.argv[0]).resolve()
if (sxcu_exe.parent / "sxcu").is_dir():
    sys.path.insert(0, str(sxcu_exe.parent))

from sxcu.cli import app  # noqa: isort

if __name__ == "__main__":
    sys.exit(app(prog_name="sxcu"))
