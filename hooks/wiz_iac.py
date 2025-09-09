"""
This script is a pre-commit hook that runs the 'wizcli iac scan' command.
"""

import argparse
import os
import shlex
import subprocess
import sys
from typing import List, Optional, Sequence

# Define constants for exit codes to improve readability.
PASS = 0
FAIL = 1


def run_wiz_scan(path: str, policy_name: Optional[str]) -> int:
    """
    Runs the 'wizcli iac scan' command with the given parameters.

    Args:
        path:   The file or directory to scan.
        policy: The scan policy(s) to use for the scan.

    Returns:
        The exit code of the command.
    """
    # The command to be executed.
    command = ['wizcli', 'iac', 'scan', '--path', path]
    if policy_name:
        command.extend(['--policy', policy_name])

    # Get the absolute path of the current working directory.
    current_directory = os.getcwd()

    print(f"Executing command: \"{shlex.join(command)}\" in directory: {current_directory}")

    try:
        result = subprocess.run(
            command,
            cwd=current_directory,
            capture_output=True,
            text=True,
            check=True,
        )

        print("Scan successful:")
        print(result.stdout)
        if result.stderr:
            print("Stderr:")
            print(result.stderr)
        return PASS

    except FileNotFoundError:
        print(
            "Error: 'wizcli' command not found. "
            "Please ensure the Wiz CLI is installed and in your system's PATH."
        )
        return FAIL
    except subprocess.CalledProcessError as e:
        print(f"Scan failed with exit code {e.returncode}:")
        print(e.stderr)
        return FAIL
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return FAIL


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    Parses command-line arguments and runs the 'wizcli iac scan' command.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='.', help='The path to the directory to scan.')
    parser.add_argument('--policy-name', help='The name of the policy to use for the scan.')
    args = parser.parse_args(argv)

    return run_wiz_scan(args.path, args.policy_name)


if __name__ == "__main__":
    sys.exit(main())