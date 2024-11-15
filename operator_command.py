import sys
import unittest
from zoautil_py import opercmd, datasets

class OperatorCommandTests(unittest.TestCase):
    """Test cases for operator commands and dataset operations."""

    def test_opercmd(self):
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
        self.assertEqual(response.rc, 0)
        self.assertIn("Return Code: 0", response.stdout_response)
        self.assertIn("Standard Output:", response.stdout_response)
        self.assertIn("Standard Error:", response.stdout_response)

    def test_datasets(self):
        """Test the datasets module."""
        print("Fetching High-Level Qualifier (HLQ) for the current user.")

        # Print the High-Level Qualifier (HLQ) of the current user.
        hlq = datasets.get_hlq()
        
        self.assertIsNotNone(hlq, "Failed to fetch HLQ.")
        print(f"High-Level Qualifier: {hlq}")

        self.assertGreater(len(hlq), 0)
        self.assertIn("High-Level Qualifier:", hlq)

if __name__ == "__main__":
    unittest.main()