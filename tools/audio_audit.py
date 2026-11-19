#!/usr/bin/env python3
"""Review timestamped SRT transcripts for possible sponsorship mentions."""
import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "sponsor": re.compile(r"\b(?:sponsor(?:ed|ship)?|brought to you by|thanks to our partner)\b", re.I),
    "promo_code": re.compile(r"\b(?:promo code|discount code|use code|code [A-Z0-9]{3,})\b", re.I),
    "affiliate": re.compile(r"\b(?:affiliate|commission on purchases)\b", re.I),
    "offer": re.compile(r"\b(?:limited.time offer|special offer|save \d+%)\b", re.I),
}
TIME = re.compile(r"(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2})[,.](?P<ms>\d{3})")
def millis(value):
    m = TIME.fullmatch(value.strip())
    if not m:
        raise ValueError("Invalid SRT timestamp")
    return ((int(m["h"])*60+int(m["m"]))*60+int(m["s"]))*1000+int(m["ms"])
def cues(srt):
    for block in re.split(r"\n\s*\n", srt.replace("\r\n","\n").strip()):
        lines=block.splitlines()
        timing=next((line for line in lines if " --> " in line),None)
        if not timing:
            continue
        i=lines.index(timing)
        start,end=timing.split(" --> ",1)
        try:
            a,b=millis(start),millis(end.split()[0])
        except ValueError:
            continue
        if b>=a:
            yield a,b," ".join(lines[i+1:]).strip()
def audit(srt,episode="Untitled episode"):
    items=list(cues(srt))
    segments=[]
    for start,end,text in items:
        signals=[key for key,pattern in PATTERNS.items() if pattern.search(text)]
        if not signals:
            continue
        if segments and start-segments[-1]["end_ms"]<=15000:
            prev=segments[-1]
            prev["end_ms"]=max(prev["end_ms"],end)
            prev["signals"]=sorted(set(prev["signals"]+signals))
            prev["evidence"].append(text[:400])
        else:
            segments.append({"start_ms":start,"end_ms":end,"signals":signals,"evidence":[text[:400]],"status":"needs_review"})
    return {"episode":episode,"cues_scanned":len(items),"candidate_segments":segments,"limitations":"Keyword candidates only; verify audio and sponsorship contracts before editing."}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("srt",type=Path)
    p.add_argument("--episode",default="Untitled episode")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=audit(a.srt.read_text(encoding="utf-8-sig"),a.episode)
    output=a.output or a.srt.with_suffix(".audit.json")
    output.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(output)
