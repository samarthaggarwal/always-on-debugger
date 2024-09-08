import subprocess
import sys
import os
from debugger import Debugger

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

            # Detect file path
            filepath = self.debugger.detect_file_path(self.raw_command, e.stderr)
            if filepath is not None and not os.path.exists(filepath):
                filepath = None

            # Read code snippet
            code_snippet = None
            if filepath is not None:
                with open(filepath, 'r') as file:
                    code_snippet = file.read()
            response = self.debugger.debug(self.raw_command, e.stderr, code_snippet)
            print(response["recommendation"])

if __name__ == "__main__":
    cmd = Command(sys.argv[1:])
    cmd.run()
