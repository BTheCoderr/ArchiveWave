# ArchiveWave release gate — founder approval required

## Verified
- PR verification and risk-map workflows passed for commit 550f7e2 (2026-11-19).
- Audio-edit integration test uses synthetic WAV and approved cut manifest.
- Netlify Forms setting enabled on archivewavee project (form registration and notifications unverified).

## Recheck on final candidate
- [ ] Latest PR commit passes build, TypeScript, Python tests, and risk-map.
- [ ] Confirm ffmpeg and ffprobe available during CI (no skipped audio test).
- [ ] Test private local whisper.cpp model against authorized audio; inspect timestamp accuracy.
- [ ] Full human listening QA on before/after audio; document click-free boundaries and continuity.
- [ ] Finalize and approve privacy disclosures and retention/deletion practices before real customer data.
- [ ] Confirm request form is registered after deployment and receives synthetic submission.
- [ ] Confirm notification to Bferrell514@gmail.com (test without customer data).
- [ ] Verify mobile layout, links, and scanner limitations.
- [ ] Obtain founder's explicit approval for merging PR and production deployment.

## First pilot gate
- [ ] Written customer authorization and sponsor obligations reviewed.
- [ ] Signed scope, pricing, and file-handling terms.
- [ ] Secure audio transfer and preservation of originals.
- [ ] Human review and written approval of each proposed edit.
- [ ] Delivery acceptance and actual time/cost recorded.

Do not interpret a green build as proof of product readiness or customer demand.
