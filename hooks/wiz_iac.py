
import os
import subprocess
import argparse

PASS = 0
FAIL = 1

def main() -> int:
    """
    Runs the 'wizcli iac scan' command in the directory where this script is located.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--policy-name', help='The name of the policy to use for the scan.')
    args = parser.parse_args()

    # Get the absolute path of the directory containing this script.
    current_directory = os.getcwd()    

    # The command to be executed.
    command = ['wizcli', 'iac', 'scan', '--path', '.']
    if args.policy_name:
        command.extend(['--policy', args.policy_name])

    print(f"Executing command: \"{' '.join(command)}\" in directory: {current_directory}")

    try:
        exit_code = PASS

        # Execute the command with the script's directory as the current working directory.
        result = subprocess.run(
            command,
            cwd=current_directory,
            capture_output=True,
            text=True,
            check=True  # This will raise a CalledProcessError if the command returns a non-zero exit code.
        )
        
        print("Scan successful:")
        print(result.stdout)
        if result.stderr:
            print("Stderr:")
            print(result.stderr)

    except FileNotFoundError:
        print("Error: 'wizcli' command not found. Please ensure the Wiz CLI is installed and in your system's PATH.")
        exit_code |= FAIL
    except subprocess.CalledProcessError as e:
        print(f"Scan failed with exit code {e.returncode}:")
        print(e.stderr)
        exit_code |= FAIL
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit_code |= FAIL
    
    return exit_code

if __name__ == "__main__":
    main()
