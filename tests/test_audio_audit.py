import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from audio_audit import audit

class AuditTests(unittest.TestCase):
    def test_detects_sponsor(self):
        r=audit("1\n00:00:01,000 --> 00:00:04,000\nBrought to you by Acme")
        self.assertEqual(r["candidate_segments"][0]["signals"],["sponsor"])
    def test_ignores_plain_speech(self):
        self.assertEqual(audit("1\n00:00:01,000 --> 00:00:02,000\nHello listeners")["candidate_segments"],[])
    def test_merges_close_cues(self):
        r=audit("1\n00:00:01,000 --> 00:00:02,000\nOur sponsor\n\n2\n00:00:03,000 --> 00:00:04,000\nUse code SAVE20")
        self.assertEqual(len(r["candidate_segments"]),1)
    def test_bad_time_ignored(self):
        self.assertEqual(audit("1\ninvalid --> time\nOur sponsor")["cues_scanned"],0)
if __name__=="__main__":
    unittest.main()
