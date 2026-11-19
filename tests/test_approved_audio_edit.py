import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from approved_audio_edit import validate_cuts,keep_intervals

class ApprovedEditTests(unittest.TestCase):
    def test_keep_segments(self):
        cuts=validate_cuts([{"start_ms":2000,"end_ms":4000,"approved":True}],10000)
        self.assertEqual(keep_intervals(cuts,10000),[(0,2000),(4000,10000)])
    def test_reject_unapproved(self):
        with self.assertRaises(ValueError):
            validate_cuts([{"start_ms":2000,"end_ms":4000}],10000)
    def test_reject_overlap(self):
        with self.assertRaises(ValueError):
            validate_cuts([{"start_ms":1000,"end_ms":4000,"approved":True},{"start_ms":3000,"end_ms":5000,"approved":True}],10000)
    def test_reject_bad_bounds(self):
        with self.assertRaises(ValueError):
            validate_cuts([{"start_ms":9000,"end_ms":11000,"approved":True}],10000)
    def test_reject_total_removal(self):
        with self.assertRaises(ValueError):
            validate_cuts([{"start_ms":0,"end_ms":10000,"approved":True}],10000)

if __name__=="__main__":
    unittest.main()
