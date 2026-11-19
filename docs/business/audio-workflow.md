# Local audio audit → review → approved edit

**Status: implementation for testing, not verified end-to-end with whisper.cpp or listening QA.**

1. Obtain written permission to process owned/customer audio. Never place it in GitHub.
2. Install ffmpeg, ffprobe, whisper.cpp CLI and a local model on the operator's computer.
3. Run: `python3 tools/transcribe_and_audit.py /private/episode.wav --model /private/ggml-model.bin --output /private/episode.audit.json`.
4. Import the audit JSON in the scanner's Transcript Review. Candidate flags are NOT proof of expired ads. Listen to the audio and review sponsorship contracts.
5. Record written authorization for exact edit boundaries. Create a **private** approval JSON, e.g.:

```json
{
  "approval_recorded": true,
  "approval_reference": "PRIVATE-WRITTEN-APPROVAL-ID",
  "cuts": [
    {"start_ms": 7300, "end_ms": 14410, "approved": true}
  ]
}
```

6. Run: `python3 tools/approved_audio_edit.py /private/episode.wav --approval /private/approval.json --output /private/episode-edited.wav`.
7. Listen to the full output, check boundaries for clicks, continuity, audio levels, lost content, and record a change log. This tool does not crossfade, loudness-match, or publish. Never overwrite the source. Deliver only after customer acceptance and secure transfer.

## Current limitations
- Timestamp accuracy depends on Whisper transcription and human verification.
- The approved editor makes hard cuts; audible artifacts may occur.
- Audio is converted to stereo 48 kHz PCM WAV; do not claim preservation of original encoding or metadata.
- No automatic publishing, cloud audio upload, or automated sponsor deletion.
- Profitability requires actual labor measurements.
