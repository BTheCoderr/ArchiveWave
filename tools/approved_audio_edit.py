#!/usr/bin/env python3
"""Apply explicit, manually approved millisecond cuts to a COPY of local audio.

Requires ffmpeg/ffprobe. No inference, no automatic ad removal or publishing.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

def probe_ms(path):
    p=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],capture_output=True,text=True,check=True,timeout=30)
    return round(float(p.stdout.strip())*1000)

def validate_cuts(cuts,duration):
    if not isinstance(cuts,list) or not cuts:
        raise ValueError("At least one explicitly approved cut is required")
    cleaned=[]
    for c in cuts:
        if not isinstance(c,dict) or c.get("approved") is not True:
            raise ValueError("Each cut requires approved: true")
        a,b=c.get("start_ms"),c.get("end_ms")
        if type(a) is not int or type(b) is not int or a<0 or b<=a or b>duration:
            raise ValueError("Invalid cut bounds")
        cleaned.append((a,b))
    cleaned.sort()
    if any(cleaned[i][0]<cleaned[i-1][1] for i in range(1,len(cleaned))):
        raise ValueError("Overlapping cuts")
    if cleaned[0][0]==0 and cleaned[-1][1]==duration and sum(b-a for a,b in cleaned)==duration:
        raise ValueError("Cannot remove entire recording")
    return cleaned

def keep_intervals(cuts,duration):
    pos=0
    result=[]
    for a,b in cuts:
        if a>pos:
            result.append((pos,a))
        pos=b
    if pos<duration:
        result.append((pos,duration))
    return result

def run(source,output,approval_path):
    source,output,approval_path=map(Path,(source,output,approval_path))
    if not source.is_file() or not approval_path.is_file():
        raise FileNotFoundError("Audio and written cut approval file required")
    if source.resolve()==output.resolve():
        raise ValueError("Output must differ from source")
    if output.exists():
        raise FileExistsError("Refusing to overwrite existing output")
    spec=json.loads(approval_path.read_text(encoding="utf-8"))
    if spec.get("approval_recorded") is not True or not isinstance(spec.get("approval_reference"),str) or not spec["approval_reference"].strip():
        raise ValueError("Record written approval reference and approval_recorded: true")
    duration=probe_ms(source)
    cuts=validate_cuts(spec.get("cuts"),duration)
    intervals=keep_intervals(cuts,duration)
    if not intervals:
        raise ValueError("No audio would remain")
    with tempfile.TemporaryDirectory(prefix="archivewave-edit-") as temp:
        segments=[]
        for i,(a,b) in enumerate(intervals):
            part=Path(temp)/f"part-{i:03d}.wav"
            subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(source),"-ss",f"{a/1000:.3f}","-t",f"{(b-a)/1000:.3f}","-ar","48000","-ac","2","-c:a","pcm_s16le",str(part)],check=True,timeout=1200)
            segments.append(part)
        concat=Path(temp)/"concat.txt"
        concat.write_text("".join("file '"+str(s).replace("'","'\\''")+"'\n" for s in segments),encoding="utf-8")
        staged=Path(temp)/"output.wav"
        subprocess.run(["ffmpeg","-nostdin","-v","error","-f","concat","-safe","0","-i",str(concat),"-c:a","pcm_s16le",str(staged)],check=True,timeout=1200)
        output.parent.mkdir(parents=True,exist_ok=True)
        staged.replace(output)
    return {"source":str(source),"output":str(output),"approval_reference":spec["approval_reference"],"removed_ms":sum(b-a for a,b in cuts),"cuts":[{"start_ms":a,"end_ms":b} for a,b in cuts],"requires_full_listening_qa":True,"published":False}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("audio",type=Path)
    p.add_argument("--approval",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(run(args.audio,args.output,args.approval),indent=2))
