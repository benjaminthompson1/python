# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
#!/usr/bin/env python3
import sys
from zoautil_py import opercmd, datasets

def test_opercmd():
    """Test the opercmd module."""

    # Get the command and parameters from command line arguments
    command = sys.argv[1]
    parameters = sys.argv[2]

    # Issue an operator command using the zoautil_py.opercmd module.
    response = opercmd.execute(command=command, parameters=parameters)

    # Print the response details
    assert response.rc == 0
    assert "Return Code: 0" in response.stdout_response
    assert "Standard Output:" in response.stdout_response
    assert "Standard Error:" in response.stdout_response

def test_datasets():
    """Test the datasets module."""

    # Print the High-Level Qualifier (HLQ) of the current user.
    hlq = datasets.get_hlq()
    assert len(hlq) > 0
    assert "High-Level Qualifier:" in hlq