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


def run_wiz_scan(args: argparse.Namespace) -> int:
    """
    Runs the 'wizcli iac scan' command with the given parameters.

    Args:
        args: The parsed command-line arguments.

    Returns:
        The exit code of the command.
    """
    # The command to be executed.
    command = ['wizcli', 'iac', 'scan']

    for arg, value in vars(args).items():
        if value is not None:
            arg_name = f'--{arg.replace("_", "-")}'
            if isinstance(value, list):
                for v in value:
                    command.extend([arg_name, str(v)])
            elif isinstance(value, bool) and value:
                command.append(arg_name)
            elif isinstance(value, bool) and not value:
                pass
            else:
                command.extend([arg_name, str(value)])

    # Get the absolute path of the current working directory.
    current_directory = os.getcwd()

    print(f"Executing command: {shlex.join(command)} in directory: {current_directory}")

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
    parser.add_argument('--path', required=True, action='append', help='File/directory to scan (required)')
    parser.add_argument('--policy', action='append', help='Scan policy to use')
    parser.add_argument('--application', action='append', help='Defines the code application environment')
    parser.add_argument('--apply-filter-to-analytics', action='store_true', help='Apply the console output filter to all results and analytics')
    parser.add_argument('--dir-traversal-workers', type=int, help='Number of workers used during directory traversal phase')
    parser.add_argument('--discovered-resources', action='store_true', help='Discover cloud resources and include them in the scan\'s JSON output')
    parser.add_argument('--expand-cloudformation-intrinsics', action='store_true', help='Expand intrinsic functions when processing CloudFormation templates')
    parser.add_argument('--format', help="Scan's output format. Available options are [human, json, sarif]")
    parser.add_argument('--ignore-comments', action='store_true', help='Enable ignore comments')
    parser.add_argument('--include-audit-policy-hits', action='store_true', help='Include audit policy hits in the output')
    parser.add_argument('--keep-false-conditions', action='store_true', help='Keep false conditions when processing CloudFormation templates')
    parser.add_argument('--legacy-secret-scanner', action='store_true', help='Use legacy secret scanner')
    parser.add_argument('--max-cloudformation-intrinsics-depth', type=int, help='Maximum depth of intrinsic functions')
    parser.add_argument('--max-file-size', help='Maximum file size to scan')
    parser.add_argument('--name', help='Scan name')
    parser.add_argument('--no-publish', action='store_true', help='Disable publishing scan results to portal')
    parser.add_argument('--output', action='append', help='Output to file')
    parser.add_argument('--parameter-files', action='append', help='Comma separated list of globs of external parameter files')
    parser.add_argument('--policy-hits-only', action='store_true', help='Only display results that failed the applied policies')
    parser.add_argument('--project', help="Scan's scoped project UUID")
    parser.add_argument('--rule-evaluation-workers', type=int, help='Number of workers used during rule evaluation phase')
    parser.add_argument('--secrets', action='store_true', help='Scan secrets')
    parser.add_argument('--show-grace-period-findings', action='store_true', help='Show findings that were ignored by grace period')
    parser.add_argument('--show-secret-snippets', action='store_true', help='Enable snippets in secrets')
    parser.add_argument('--tag', action='append', help='Tags to mark the scan with')
    parser.add_argument('--tag-file', help='External tag files')
    parser.add_argument('--timeout', help='Operation timeout')
    parser.add_argument('--types', action='append', help='Narrow down the scan to specific types')
    parser.add_argument('--wiz-configuration-file', help='Path to the Wiz configuration file')
    parser.add_argument('--log', help='File path at which to write debug logs')
    parser.add_argument('--no-color', action='store_true', help='Disable color output')
    parser.add_argument('--no-style', action='store_true', help='Disable stylized output')
    parser.add_argument('--no-telemetry', action='store_true', help='Disable telemetry')

    args = parser.parse_args(argv)

    return run_wiz_scan(args)


if __name__ == "__main__":
    sys.exit(main())