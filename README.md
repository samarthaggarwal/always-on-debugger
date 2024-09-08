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

_Step 3: Source ~/.bashrc or ~/.zshrc_
```bash
source ~/.bashrc
```

## Usage

Just prefix any terminal command with `debug`. That's it, the debugger will automatically kick in when an error is detected and prints the error along with the suggested course of action.

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