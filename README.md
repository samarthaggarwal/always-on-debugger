# Always-On Debugger

Automatically debug code from your terminal.

## Overview

Always-On Debugger is a tool that enhances your terminal experience by automatically detecting errors and providing debugging assistance using AI. It acts as a wrapper around your existing terminal, intercepting commands and their outputs to offer real-time debugging support.

## Features

- Mimics the terminal for every command
- Automatically detects errors in command outputs
- Captures context and sends it to an AI language model for analysis
- Provides AI-generated debugging suggestions directly in the terminal

## Installation

```bash
pip install always-on-debugger
```

```
brew install auto-debugger
```

## Usage

Once installed, Always-On Debugger runs in the background of your terminal sessions. Here's how it works:

1. Execute commands as you normally would in your terminal.
2. If an error occurs, Always-On Debugger automatically captures the context.
3. The error context is sent to an AI language model for analysis.
4. Debugging suggestions are printed directly to your terminal.

No additional user input is required - the debugging process happens automatically when an error is detected.

## Project Structure

- `debugger.py`: Core Python script that orchestrates the debugging flow
- `llm.py`: Handles LLM interaction (prompt generation and response parsing)
- (Additional files for terminal wrapping and packaging)

## License

[MIT License](LICENSE)