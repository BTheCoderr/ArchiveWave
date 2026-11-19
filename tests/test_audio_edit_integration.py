"""End-to-end approved edit test with synthetic audio; no speech-to-text model."""
import json
import math
import shutil
import struct
import sys
import tempfile
import unittest
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from approved_audio_edit import probe_ms, run

@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg and ffprobe required")
class AudioEditIntegrationTests(unittest.TestCase):
    def test_approved_edit_preserves_source_and_reduces_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            source=root/"synthetic.wav"
            with wave.open(str(source),"wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(16000)
                for i in range(16000*3):
                    sample=int(5000*math.sin(2*math.pi*440*i/16000))
                    wav.writeframesraw(struct.pack("<h",sample))
            original=source.read_bytes()
            approval=root/"approval.json"
            approval.write_text(json.dumps({
                "approval_recorded":True,
                "approval_reference":"SYNTHETIC-TEST-ONLY",
                "cuts":[{"start_ms":1000,"end_ms":2000,"approved":True}]
            }))
            output=root/"edited.wav"
            result=run(source,output,approval)
            self.assertTrue(output.is_file())
            self.assertEqual(source.read_bytes(),original)
            self.assertEqual(result["removed_ms"],1000)
            self.assertTrue(result["requires_full_listening_qa"])
            self.assertFalse(result["published"])
            self.assertAlmostEqual(probe_ms(output),2000,delta=100)
            with self.assertRaises(FileExistsError):
                run(source,output,approval)

if __name__=="__main__":
    unittest.main()
