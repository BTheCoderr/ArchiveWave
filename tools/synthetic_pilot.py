#!/usr/bin/env python3
"""Deterministic ten-episode transcript audit rehearsal; no real customer data."""
import json
import sys
import time
from pathlib import Path
from audio_audit import audit

def sample(index):
    lines = [
        ("00:00:01,000", "00:00:04,000", f"Welcome to synthetic episode {index}."),
        ("00:00:30,000", "00:00:35,000", "Our sponsor is Fictional Coffee. This is a made-up example."),
        ("00:00:37,000", "00:00:42,000", "Use code SAMPLE20 for a fictional discount."),
        ("00:02:00,000", "00:02:06,000", "Today we talk about the creative process and our guests."),
        ("00:04:00,000", "00:04:06,000", "Thanks for listening. See you next time."),
    ]
    if index % 2 == 0:
        lines.insert(4, ("00:03:00,000", "00:03:04,000", "We may receive an affiliate commission."))
    return "\n\n".join(f"{n}\n{start} --> {end}\n{text}" for n,(start,end,text) in enumerate(lines,1))

def run():
    start = time.perf_counter()
    episodes = [audit(sample(i), f"Synthetic episode {i:02d}") for i in range(1,11)]
    count = sum(len(e["candidate_segments"]) for e in episodes)
    elapsed = time.perf_counter()-start
    return {
        "rehearsal": "SYNTHETIC TRANSCRIPTS ONLY — NOT AUDIO QA OR A CUSTOMER PILOT",
        "episodes": episodes,
        "summary": {
            "episodes_processed": len(episodes),
            "candidate_segments": count,
            "candidate_segments_needing_human_review": count,
            "transcript_audit_runtime_seconds": round(elapsed,6),
            "manual_review_minutes": None,
            "audio_editing_minutes": None,
            "transcription_minutes": None,
            "delivery_qa_minutes": None,
            "revenue_usd": 0,
            "actual_pilot_margin": None,
            "pricing_conclusion": "Cannot establish $400 pilot profitability from synthetic transcript matching."
        },
        "required_next_steps": [
            "Run local whisper.cpp transcription on consented or synthetic recorded audio.",
            "Manually review every flagged segment and document false positives.",
            "Edit only specifically approved segments in copies; preserve originals.",
            "Listen to entire edits, verify technical audio output, and record human labor.",
            "Calculate direct costs and pilot margin from observed work, not runtime alone."
        ]
    }

if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv)>1 else Path("synthetic-pilot-report.json")
    result = run()
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(f"Rehearsed {result['summary']['episodes_processed']} synthetic transcripts; {result['summary']['candidate_segments']} candidate segments. Output: {output}")
