"""Portable entry point; finds its own environment even when called from another directory."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    a = argparse.ArgumentParser(description='Build the four-format editorial example.')
    a.add_argument('--input', type=Path, default=ROOT/'assets/example.json')
    a.add_argument('--out', type=Path, default=ROOT/'out')
    a.add_argument('--name', default='克劳德设计_示例')
    o, extra = a.parse_known_args()
    py = ROOT/'.venv'/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not py.exists():
        raise SystemExit('Run python scripts/bootstrap.py first.')
    cmd = [str(py), str(ROOT/'scripts/build.py'), '--input', str(o.input.resolve()), '--out', str(o.out.resolve()), '--name', o.name, *extra]
    subprocess.run(cmd, check=True, cwd=ROOT)
    subprocess.run([str(py), str(ROOT/'scripts/verify.py'), str(o.out.resolve()), '--name', o.name], check=True)

if __name__ == '__main__':
    main()
