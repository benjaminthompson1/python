#!/usr/bin/env python3
import sys
import zoautil_py.opercmd as opercmd
from zoautil_py.datasets import Dataset

# This script issues an operator command in a z/OS environment using the zoautil_py package.
# It takes two command line arguments:
# - command: The operator command to be issued (e.g., "d")
# - parameters: The parameters for the operator command (e.g., "iplinfo")
# Example usage:
# python3 operator_command.py d iplinfo

# Get the command and parameters from command line arguments
command = sys.argv[1]
parameters = sys.argv[2]

# Issue an operator command using the zoautil_py.opercmd module.
# - command: The operator command to be issued.
# - parameters: The parameters for the operator command.
# - terse: A boolean value that indicates whether the response should be in terse mode or not.
response = opercmd.execute(command=command, parameters=parameters, terse=True)

# Print the response details
print("Return Code:", response.rc)
print(dir(response))  # List all attributes and methods of the response object
print("Standard Output:", response.stdout_response)
print("Standard Error:", response.stderr_response)

# Print the High-Level Qualifier (HLQ) of the current user.
print("High-Level Qualifier:", Dataset.hlq())