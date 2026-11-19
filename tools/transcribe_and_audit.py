#!/usr/bin/env python3
"""Optional local whisper.cpp transcription; no paid cloud APIs."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from audio_audit import audit

def run(audio:Path,model:Path,whisper_bin:str,output:Path):
    if not audio.is_file() or not model.is_file():
        raise FileNotFoundError("Audio and local Whisper model must exist")
    exe=shutil.which(whisper_bin) or (str(Path(whisper_bin).resolve()) if Path(whisper_bin).is_file() else None)
    if not exe or not shutil.which("ffmpeg"):
        raise FileNotFoundError("Install ffmpeg and whisper.cpp CLI before running")
    with tempfile.TemporaryDirectory(prefix="archivewave-") as tmp:
        wav=Path(tmp)/"audio.wav"
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-i",str(audio),"-ar","16000","-ac","1","-c:a","pcm_s16le",str(wav)],check=True,timeout=1200)
        prefix=Path(tmp)/"transcript"
        subprocess.run([exe,"-m",str(model),"-f",str(wav),"-osrt","-of",str(prefix)],check=True,timeout=7200)
        srt=prefix.with_suffix(".srt")
        if not srt.is_file():
            raise RuntimeError("Whisper did not produce SRT")
        report=audit(srt.read_text(encoding="utf-8-sig"),audio.stem)
        report["transcription_engine"]="local whisper.cpp"
        output.write_text(json.dumps(report,indent=2),encoding="utf-8")
        return report
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("audio",type=Path)
    p.add_argument("--model",type=Path,required=True)
    p.add_argument("--whisper-bin",default="whisper-cli")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=run(a.audio,a.model,a.whisper_bin,a.output or a.audio.with_suffix(".audit.json"))
    print(f"Found {len(result['candidate_segments'])} candidates")
