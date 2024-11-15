"""
Test script for retrieving z/OS dataset High-Level Qualifier (HLQ).
This test validates that we can successfully retrieve the current user's HLQ
using the zoautil_py library.

Usage:
    test_zos_hlq.py
"""

import unittest
from zoautil_py import datasets

class DatasetTests(unittest.TestCase):
    """Test cases for z/OS dataset operations."""

    def test_get_hlq(self):
        """Verify that we can retrieve the current user's HLQ.
        
        Tests:
            - HLQ retrieval is successful (not None)
            - HLQ has valid length
        """
        print("Fetching High-Level Qualifier (HLQ) for the current user.")

        hlq = datasets.get_hlq()
        
        self.assertIsNotNone(hlq, "Failed to fetch HLQ")
        print(f"High-Level Qualifier: {hlq}")

        self.assertGreater(len(hlq), 0)

if __name__ == "__main__":
    unittest.main()