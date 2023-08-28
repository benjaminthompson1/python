#!/usr/bin/env python3
import sys
import zoautil_py.opercmd as opercmd
import zoautil_py.datasets as datasets

# This script takes two command line arguments: command and parameters
# command: The operator command you want to issue (e.g., "d")
# parameters: The parameters for the operator command (e.g., "iplinfo")

# Example usage:
# python operator_command.py d iplinfo

# Get the command and parameters from command line arguments
command = sys.argv[1]
parameters = sys.argv[2]

# Issue an operator command
# opercmd.execute method is used to issue operator commands.
# command: The operator command to be issued
# parameters: The parameters for the operator command
# terse: A boolean value that indicates whether the response should be in terse mode or not.
response = opercmd.execute(command=command, parameters=parameters, terse=True)

# Print the response
# response.rc will give the return code of the operator command issued.
print("Return Code:", response.rc)

# Print the high-level qualifier
# datasets.hlq method is used to get the high-level qualifier (HLQ) of the current user.
print("High-Level Qualifier:", datasets.hlq())