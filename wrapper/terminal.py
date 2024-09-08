import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)

while True:
    user_input = input("Enter a command (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    run_command(user_input)
