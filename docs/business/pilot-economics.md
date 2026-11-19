# ArchiveWave — Pilot economics and evidence

## What is verified by the synthetic test
Run `python3 tools/synthetic_pilot.py /tmp/archivewave-synthetic-report.json` and `python3 -m unittest discover -s tests -v`.

The rehearsal processes 10 **invented SRT transcripts** (not audio recordings) and expects 15 candidate segments requiring human review. This validates the candidate report path only. It does **not** validate audio transcription, actual ad expiration, edit quality, turnaround, delivery, demand, or profit.

## Pricing sensitivity for a proposed $400 pilot
Gross contribution before overhead = $400 - direct labor - direct external costs. At $0 direct external cost:

| Total human hours | Effective gross contribution before overhead |
| --- | --- |
| 5 hours | $400 minus 5 × hourly labor cost |
| 10 hours | $400 minus 10 × hourly labor cost |
| 20 hours | $400 minus 20 × hourly labor cost |

At a hypothetical $25/hour labor cost, the contributions are $275, $150, and -$100 respectively. These are scenarios, **not measured results**. Include sales, revisions, storage, support, and delivery costs when known.

## Actual pilot measurement
For each authorized episode log duration, local transcription wall time, transcript review time, edits requested/approved, edit time, full listen/QA time, revisions, storage/delivery cost, and customer acceptance. Total labor and costs across all ten episodes are required to assess whether $400 is sustainable.

## Release gate
Do not market an automated end-to-end cleanup workflow until one authorized or owned audio sample has passed full transcription, approved edit, listening QA, and delivery. Keep the public metadata scanner's limitations explicit.
