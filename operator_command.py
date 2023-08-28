#!/usr/bin/env python3
import zoautil_py.opercmd as opercmd

# Issue an operator command
opercmd.execute(command="d", parameters="iplinfo", terse=True)

# Print the response
print("Return Code:", response.rc)