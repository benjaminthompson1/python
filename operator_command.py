#!/usr/bin/env python3
import zoautil_py.opercmd as opercmd
import zoautil_py.datasets as datasets

# Issue an operator command
response = opercmd.execute(command="d", parameters="iplinfo", terse=True)

# Print the response
print("Return Code:", response.rc)

# Print the high-level qualifier
print("High-Level Qualifier:", datasets.hlq())