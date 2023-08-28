#!/usr/bin/env python3
import zoautil_py

# Issue an operator command
response = zoautil_py.issue_operator_command("d iplinfo")

# Print the response
print(response)