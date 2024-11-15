import sys
from zoautil_py import opercmd, datasets

def test_opercmd():
    """Test the opercmd module."""

    # Get the command and parameters from command line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <command> <parameters>")
        return
    command = sys.argv[1]
    parameters = sys.argv[2]

    print(f"Executing command: {command} with parameters: {parameters}")

    # Issue an operator command using the zoautil_py.opercmd module.
    response = opercmd.execute(command=command, parameters=parameters)

    print(f"Response received: {response}")

    # Print the response details
    assert response.rc == 0
    assert "Return Code: 0" in response.stdout_response
    assert "Standard Output:" in response.stdout_response
    assert "Standard Error:" in response.stdout_response

def test_datasets():
    """Test the datasets module."""

    print("Fetching High-Level Qualifier (HLQ) for the current user.")

    # Print the High-Level Qualifier (HLQ) of the current user.
    hlq = datasets.get_hlq()
    
    if not hlq:
        print("Failed to fetch HLQ.")
        return

    print(f"High-Level Qualifier: {hlq}")

    assert len(hlq) > 0
    assert "High-Level Qualifier:" in hlq

if __name__ == "__main__":
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_opercmd))
    suite.addTest(unittest.makeSuite(test_datasets))
    unittest.TextTestRunner().run(suite)