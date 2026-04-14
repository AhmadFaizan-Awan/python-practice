import os
import sys
import readline
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

def execute_command(command_line):
    """
    Parses and executes a command.
    """
    # 1. Parse the input
    parts = command_line.strip().split()
    if not parts:
        return

    command = parts[0]
    args = parts

    # 2. Handle "Internal" Commands (Commands the shell must do itself)
    if command == "exit":
        print(Fore.GREEN + "Goodbye!")
        sys.exit(0)
    
    elif command == "cd":
        try:
            # If no path is given, go home; otherwise go to target
            target = args[1] if len(args) > 1 else os.path.expanduser("~")
            os.chdir(target)
        except FileNotFoundError:
            print(Fore.RED + f"cd: no such file or directory: {target}")
        except Exception as e:
            print(Fore.RED + f"cd: error: {e}")
        return # We don't fork for 'cd'
    
    elif command == "help":
        print(Fore.CYAN + "MyShell Built-in Commands:")
        print(Fore.YELLOW + "  cd <path>" + Style.RESET_ALL + " - Change directory")
        print(Fore.YELLOW + "  exit" + Style.RESET_ALL + "      - Exit the shell")
        print(Fore.YELLOW + "  help" + Style.RESET_ALL + "      - Show this help message")
        print(Fore.CYAN + "External commands are executed via fork-exec-wait.")
        return

    # 3. Handle "External" Commands (The Real OS Stuff)
    # We use the Fork-Exec-Wait pattern here
    try:
        pid = os.fork()  # Splitting the process into two
    except OSError as e:
        print(Fore.RED + f"Error: Fork failed: {e}")
        return

    if pid == 0:
        # === CHILD PROCESS ===
        # This is the clone. It will become the new program.
        try:
            # os.execvp will replace this script's memory with the new program
            os.execvp(command, args)
        except FileNotFoundError:
            print(Fore.RED + f"{command}: command not found")
            sys.exit(1) # Kill the child safely if it fails
        except Exception as e:
            print(Fore.RED + f"{command}: error executing: {e}")
            sys.exit(1)
    
    elif pid > 0:
        # === PARENT PROCESS ===
        # This is your shell. It waits for the child to finish.
        try:
            _, status = #os.waitpid(pid, 0)
            
            # Optional: Check exit status if needed
            # if os.WIFEXITED(status):
            #     exit_code = os.WEXITSTATUS(status)
            #     if exit_code != 0:
            #         # print(Fore.YELLOW + f"Process exited with code {exit_code}")
            #         pass
            
        except KeyboardInterrupt:
            # If user presses Ctrl+C while child is running, we usually want to let the child handle it
            # or just print a newline. The child process receives the signal too.
            print() 
    
    else:
        # Should be caught by the try-catch block above, but for completeness:
        print(Fore.RED + "Error: Fork failed (pid < 0)")

def get_prompt():
    """
    Returns a colored prompt string with the current directory.
    """
    try:
        current_dir = os.getcwd()
        # Replace home directory with ~ for brevity
        home = os.path.expanduser("~")
        if current_dir.startswith(home):
            current_dir = current_dir.replace(home, "~", 1)
    except Exception:
        current_dir = "?"
        
    return f"{Fore.BLUE}{current_dir} {Fore.GREEN}$> {Style.RESET_ALL}"

def main():
    print(Fore.CYAN + "Welcome to MyShell. Type 'help' for commands or 'exit' to quit.")
    
    # Enable history
    # Save history in the same directory as this script to avoid cluttering home
    script_dir = os.path.dirname(os.path.abspath(__file__))
    histfile = os.path.join(script_dir, ".myshell_history")
    
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass
        
    # Default to emacs mode (standard for terminals) if not set
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
        
    atexit_handler = lambda: readline.write_history_file(histfile)
    import atexit
    atexit.register(atexit_handler)

    while True:
        try:
            prompt = get_prompt()
            # input() automatically uses readline if imported!
            user_input = input(prompt)
            
            execute_command(user_input)
            
            # Auto-save history after each command
            readline.write_history_file(histfile)
            
        except EOFError:
            # Handle Ctrl+D gracefully
            print(Fore.GREEN + "\nExiting...")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully (in the main prompt loop)
            print("\n")

if __name__ == "__main__":
    main()
