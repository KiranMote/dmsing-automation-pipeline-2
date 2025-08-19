import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_USER = os.getenv('SSH_USER')
SSH_KEY_PATH = os.getenv('SSH_KEY_PATH')
REMOTE_SCRIPT_PATH = os.getenv('REMOTE_SCRIPT_PATH')


def run_remote_script():
    try:
        key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=SSH_HOST, username=SSH_USER, pkey=key)
        print(f"Connected to {SSH_HOST} as {SSH_USER}")

        stdin, stdout, stderr = client.exec_command(f"bash {REMOTE_SCRIPT_PATH}")
        output = stdout.read().decode()
        error = stderr.read().decode()
        print("--- Job Status Output ---")
        print(output)
        if error:
            print("--- Errors ---")
            print(error)
        client.close()

        # Check for success in output
        if ('Success' in output) or ('Pass' in output):
            return True, output
        else:
            return False, output
    except Exception as e:
        print(f"Error: {e}")
        return False, str(e)

if __name__ == "__main__":
    success, result = run_remote_script()
    if success:
        print("All Unix jobs succeeded. Proceeding to SQL tests.")
    else:
        print("Unix job failure detected. Aborting SQL tests.")
    exit(0 if success else 1)
