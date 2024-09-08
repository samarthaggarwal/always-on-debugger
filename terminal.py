import subprocess
import sys
from debugger import Debugger

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        print("-" * 100 + "\n" + "Debugging..." + "\n" + "-" * 100)
        debugger = Debugger()
        resp = debugger.debug(e.stderr, command)
        print(resp["recommendation"])

def get_command():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    else:
        print("format: python terminal.py <command>")
        exit(1)

if __name__ == "__main__":
    run_command(get_command())
