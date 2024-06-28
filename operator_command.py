#!/usr/bin/env python3
import sys
from zoautil_py import opercmd, datasets

# Get the command and parameters from command line arguments
command = sys.argv[1]
parameters = sys.argv[2]

# Issue an operator command using the zoautil_py.opercmd module.
response = opercmd.execute(command=command, parameters=parameters)

# Print the response details
print("Return Code:", response.rc)
print("Standard Output:", response.stdout_response)
print("Standard Error:", response.stderr_response)

# Print the High-Level Qualifier (HLQ) of the current user.
print("High-Level Qualifier:", datasets.get_hlq())