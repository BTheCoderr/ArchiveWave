# ArchiveWave

Independent podcast archive intelligence prototype built with Next.js 15, React 19, and TypeScript. No standalone HTML pages and no paid API dependencies.

## Run locally

```bash
npm install
npm run dev
```

Open http://localhost:3000. Use `/scanner` to upload an RSS XML file, inspect episode-description keyword matches, and export a JSON report. All analysis runs in the browser. It does **not** transcribe audio, confirm expired sponsorships, estimate revenue, or edit published episodes. Remote RSS URL fetching is intentionally disabled pending SSRF-safe implementation. The sample email address on the marketing page is not a live intake channel.

## Next steps

1. Verify dependency installation and production build in CI.
2. Add a secure remote RSS fetcher with DNS/IP and redirect checks.
3. Add local Whisper transcription and human review for audio-level findings.
4. Connect a real intake form after deciding on the contact destination.
5. Deploy to a free Netlify site after verifying the build.

ArchiveWave Studios is a future section. No paid services required.