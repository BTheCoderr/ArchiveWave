import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from synthetic_pilot import run

class SyntheticPilotTests(unittest.TestCase):
    def test_ten_episode_rehearsal(self):
        result=run()
        summary=result["summary"]
        self.assertEqual(summary["episodes_processed"],10)
        self.assertEqual(summary["candidate_segments"],15)
        self.assertEqual(summary["candidate_segments_needing_human_review"],15)
        self.assertIsNone(summary["actual_pilot_margin"])
        self.assertEqual(summary["revenue_usd"],0)
        for episode in result["episodes"]:
            self.assertTrue(all(s["status"]=="needs_review" for s in episode["candidate_segments"]))

if __name__=="__main__":
    unittest.main()
