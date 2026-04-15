# MyShell

A lightweight Python shell implementation demonstrating core operating system concepts with a simple interactive CLI.

## Overview

`myshell.py` is a custom shell that supports:
- external commands via the `fork` → `exec` → `wait` flow
- built-in commands executed inside the shell process
- command history saved across sessions
- graceful error handling and terminal-friendly output

This project is intended as an educational example of how shells manage processes, internal commands, and user interaction in Unix-like environments.

## Features

- `fork()` to create a child process for external commands
- `execvp()` to replace the child process with the requested program
- `waitpid()` to pause the shell until the child command finishes
- built-in command support: `cd`, `exit`, `help`
- persistent history using `readline` and a local `.myshell_history` file
- colored prompt and output using `colorama`

## Requirements

- Python 3.12 or newer
- `colorama`
- `pexpect` (only required for `verify_shell.py`)

Dependencies are listed in `pyproject.toml`.

## Installation

1. Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install directly from `pyproject.toml` dependencies:

```bash
pip install colorama pexpect
```

## Usage

Run the shell with:

```bash
python3 myshell.py
```

You will see a prompt showing the current working directory. Enter commands as you would in a normal shell.

Example commands:

```bash
ls
pwd
cd ..
help
exit
```

## Built-in Commands

- `cd <path>` — change the shell's current working directory
- `exit` — quit the shell
- `help` — display built-in command help

External commands like `ls`, `grep`, `python`, and any executable available in your `PATH` are launched in a child process.

## Verification

An automated verification script is included in `verify_shell.py`. It launches the shell and checks:
- external command execution
- built-in `cd` behavior
- clean shutdown
- history persistence

Run it with:

```bash
python3 verify_shell.py
```

## Project Files

- `myshell.py` — main shell implementation
- `verify_shell.py` — automated shell verification script
- `main.py` — placeholder module for project entrypoint
- `pyproject.toml` — project metadata and dependencies

## Notes

This shell is designed for learning and experimentation. It is not intended to replace a full-featured system shell.
