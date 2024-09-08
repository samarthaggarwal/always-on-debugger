import subprocess
import sys
import os
from debugger import Debugger

DEEP_DEBUG_INTERPRETERS: list[str] = ["python"]

class Command:
    def __init__(self, args: list[str]):
        if len(args) == 0:
            print("format: python terminal.py <command>")
            exit(1)
        self.raw_command = " ".join(args)
        self.interpreter = args[0]
        self.filename = args[1] if len(args) > 1 else None
        self.args = args[2:] if len(args) > 2 else []
        self.debugger = Debugger()

    def run(self):
        try:
            result = subprocess.run(self.raw_command, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print("-" * 100 + "\n" + "Debugging..." + "\n" + "-" * 100)
            code_snippet = None
            if self.interpreter.lower() in DEEP_DEBUG_INTERPRETERS:
                filepath = f"{os.path.dirname(os.path.abspath(__file__))}/{self.filename}"
                if os.path.exists(filepath):
                    with open(filepath, 'r') as file:
                        code_snippet = file.read()
                else:
                    code_snippet = "File not found: " + filepath
            resp = self.debugger.debug(self.raw_command, e.stderr, code_snippet)
            print(resp["recommendation"])

if __name__ == "__main__":
    cmd = Command(sys.argv[1:])
    cmd.run()
