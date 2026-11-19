import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audio_audit import audit

class SmokeTest(unittest.TestCase):
    def test_synthetic_report_shape(self):
        sample = "1\n00:00:01,000 --> 00:00:03,000\nThis episode is brought to you by Example"
        result = audit(sample, "Synthetic episode")
        self.assertEqual(result["episode"], "Synthetic episode")
        self.assertEqual(len(result["candidate_segments"]), 1)
        self.assertEqual(result["candidate_segments"][0]["start_ms"], 1000)
        json.dumps(result)
if __name__ == "__main__":
    unittest.main()
