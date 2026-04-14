import pexpect
import sys
import os
import time

def verify_shell():
    print("Starting shell verification...")
    # Start the shell process
    child = pexpect.spawn('python3 myshell.py', encoding='utf-8')
    
    # Expect the welcome message
    child.expect('Welcome to MyShell')
    print("✅ Shell started successfully")
    
    # 1. Test External Command (ls)
    child.expect(r'\$>')
    child.sendline('ls')
    child.expect('myshell.py')
    print("✅ External command 'ls' works")

    # 2. Test Built-in Command (cd)
    child.expect(r'\$>')
    child.sendline('cd ..')
    child.expect(r'\$>')
    child.sendline('pwd')
    # Expect parent directory name in path
    child.expect('programs') 
    print("✅ Built-in command 'cd' works")

    # 3. Test History (using pexpect is tricky for arrow keys, verifying persistence instead)
    # We will send a unique command, exit, restart, and see if it's in history file
    unique_cmd = "echo verification_unique_string"
    child.expect(r'\$>')
    child.sendline(unique_cmd)
    child.expect('verification_unique_string')
    
    child.expect(r'\$>')
    child.sendline('exit')
    child.expect(pexpect.EOF)
    print("✅ Shell exited cleanly")
    
    # Check history file (in the same dir as the script now)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hist_path = os.path.join(script_dir, ".myshell_history")
    if os.path.exists(hist_path):
        with open(hist_path, 'r') as f:
            content = f.read()
            if unique_cmd in content:
                print("✅ History persistence verified (found command in history file)")
            else:
                print("❌ History persistence failed: command not found in file")
    else:
        print("❌ History file not created")

if __name__ == "__main__":
    try:
        verify_shell()
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        sys.exit(1)
