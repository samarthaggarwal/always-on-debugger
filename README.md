# Always-On Debugger

Automatically debug code from your terminal.

## Overview

Always-On Debugger is a tool that enhances your terminal experience by automatically detecting errors and providing debugging assistance using AI. It acts as a wrapper around your existing terminal, intercepting commands and their outputs to offer real-time debugging support.

## Features

- Mimics the terminal for every command
- Automatically detects errors in command outputs
- Captures context and sends it to an AI language model for analysis
- Provides AI-generated debugging suggestions directly in the terminal

## Setup
_Step 1: Clone the repo_
```bash
cd ~
git clone git@github.com:samarthaggarwal/always-on-debugger.git
```

_Step 2: Update ~/.bashrc_
Add the following to your ~/.bashrc or ~/.zshrc
```
alias debug="python ~/always-on-debugger/terminal.py"
export ANTHROPIC_API_KEY=<PASTE_YOUR_OWN_API_KEY>
```

_Step 3: Source ~/.bashrc or ~/.zshrc . Alternatively, open a new terminal._
```bash
source ~/.bashrc
```

## Usage

Just prefix any terminal command with `debug`. That's it, the debugger will automatically kick in when an error is detected and prints the error along with the suggested course of action. Here's an example:

> Normally, the deverlop would only see the error.
```bash
[14:57:19] ➜  demo git:(main) ✗ python average.py
The average is: 3.0
Traceback (most recent call last):
  File "/Users/samarthaggarwal/personal/always-on-debugger/demo/average.py", line 15, in <module>
    average_of_empty = calculate_average(empty_list)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/samarthaggarwal/personal/always-on-debugger/demo/average.py", line 7, in calculate_average
    return total / count
           ~~~~~~^~~~~~~
ZeroDivisionError: division by zero
```

> Prefixing the same command with `debug` prints the error along with diagnosis and recommendations.

```bash
[14:57:21] ➜  demo git:(main) ✗ debug python average.py
Traceback (most recent call last):
  File "/Users/samarthaggarwal/personal/always-on-debugger/demo/average.py", line 15, in <module>
    average_of_empty = calculate_average(empty_list)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/samarthaggarwal/personal/always-on-debugger/demo/average.py", line 7, in calculate_average
    return total / count
           ~~~~~~^~~~~~~
ZeroDivisionError: division by zero

---------------------------------------------------------------------
Debugging...

---------------------------------------------------------------------
To fix this error and improve the calculate_average function, follow these steps:

1. Modify the calculate_average function to handle empty lists:
   def calculate_average(numbers):
       if not numbers:  # Check if the list is empty
           return 0  # or you could return None, or raise a custom exception
       total = sum(numbers)
       count = len(numbers)
       return total / count

2. This modification checks if the input list is empty before performing any calculations. If it is empty, it returns 0 (or you could choose to return None or raise a custom exception, depending on how you want to handle this case).

3. Test the function with both non-empty and empty lists to ensure it works correctly in all cases.

4. If you want to keep the original loop structure, you can modify it like this:
   def calculate_average(numbers):
       total = 0
       count = 0
       for num in numbers:
           total += num
           count += 1
       if count == 0:
           return 0  # or None, or raise an exception
       return total / count

5. Choose the implementation that best fits your needs and coding style.


By implementing one of these solutions, you will prevent the ZeroDivisionError and handle empty lists gracefully.
```

## How it works?
1. Prefix your terminal commands with `debug`.
2. If an error occurs, Always-On Debugger automatically captures the context.
3. The error context is sent to an AI language model for analysis.
4. Debugging suggestions are printed directly to your terminal.

## Project Structure

- `debugger.py`: Core Python script that orchestrates the debugging flow
- `llm.py`: Handles LLM interaction (prompt generation and response parsing)
- (Additional files for terminal wrapping and packaging)

## License

[MIT License](LICENSE)