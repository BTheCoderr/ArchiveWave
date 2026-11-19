# Audio proof — 2026-11-19

An original synthetic spoken-audio sample was generated locally using espeak and ffmpeg. The 22.68-second original has three passages, including a fictional sponsor read at approximately 7.30–14.41 seconds. A separate 15.56-second WAV was assembled from the surrounding passages, preserving the original. A PDF sample report and JSON evidence were generated locally (not committed to GitHub).

## Verified
- WAV file generation and ffprobe duration inspection.
- Deterministic removal of a known fictional middle passage using audio assembly.
- A sample report identifying the edit boundaries and clear limitations.

## Not verified
- Whisper transcription (whisper-cli and a local model unavailable in the test environment).
- Automated sponsor recognition from audio rather than a supplied script.
- Full listening QA, click-free boundaries, loudness matching, customer approvals, or commercial profitability.

## Reproduction outline
Use espeak to generate three separate fictional speech passages as WAV files, then ffmpeg concat to create an original three-part WAV and a demo edit from parts one and three. Record SHA-256 hashes of both. This is a synthetic proof only, not a completed customer pilot.

## Next release gate
Run the local whisper.cpp transcription pipeline with an installed model against consented or owned audio, inspect detected timestamps, perform human listening QA, and measure the real editing labor before promoting the cleanup service as production-ready.
