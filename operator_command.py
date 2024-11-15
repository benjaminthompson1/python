import unittest
from zoautil_py import datasets

class DatasetTests(unittest.TestCase):
    """Test cases for dataset operations."""

    def test_get_hlq(self):
        """Test retrieving the High-Level Qualifier (HLQ)."""
        print("Fetching High-Level Qualifier (HLQ) for the current user.")

        # Get the High-Level Qualifier (HLQ) of the current user
        hlq = datasets.get_hlq()
        
        self.assertIsNotNone(hlq, "Failed to fetch HLQ")
        print(f"High-Level Qualifier: {hlq}")

        self.assertGreater(len(hlq), 0)

if __name__ == "__main__":
    unittest.main()