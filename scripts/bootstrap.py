"""Create the repository-local environment; never modify global Python or Node packages."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]

def main():
    if sys.version_info < (3, 10):
        raise SystemExit('Python 3.10+ is required.')
    node = shutil.which('node')
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    if not node or not npm:
        raise SystemExit('Install Node.js 22.20+ (with npm), then rerun this command.')
    version = tuple(int(n) for n in subprocess.check_output([node, '--version'], text=True).strip().lstrip('v').split('.'))
    if version < (22,20,0):
        raise SystemExit('Node.js 22.20+ is required. Check that node --version resolves to the current installation.')
    env_dir = ROOT / '.venv'
    python = env_dir / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(env_dir)
    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(ROOT/'requirements.txt')], check=True)
    subprocess.run([npm, 'ci' if (ROOT/'package-lock.json').exists() else 'install', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=ROOT, check=True)
    subprocess.run([str(python), str(ROOT/'scripts/doctor.py')], check=True, cwd=ROOT)
    print('\nReady. Run: python scripts/run.py')

if __name__ == '__main__':
    main()
