# ArchiveWave — Intake operations (manual, no paid CRM)

## Form infrastructure
The public static page at /request-audit.html uses Netlify Forms with a hidden form-name field and honeypot. **This is not verified live until deployed and tested on the connected Netlify project.** Netlify form availability, submission quotas, spam filtering, notifications, and data retention depend on project settings and plan. Never claim a request was received before the Netlify dashboard confirms it.

## Owner setup and verification
1. Deploy once after founder approval and passing PR checks.
2. In the connected Netlify project, confirm the form archivewave-audit-request appears in Forms. Configure submission notifications to Bferrell514@gmail.com (owner-provided contact); verify delivery with a synthetic submission. Notification configuration is not yet verified.
3. Submit one clearly labeled synthetic test inquiry; verify it appears in Forms and notification routing works. Remove the test entry afterward.
4. Review Netlify data handling and publish a privacy notice appropriate to the business before collecting real inquiries. If privacy/compliance review is incomplete, do not promote the form.
5. Monitor spam and limits. Never copy private submission contents into public issues or CI logs.

## Internal intake stages
New → Qualification → Rights/authorization pending → Audit scoped → Audit in progress → Manual review → Proposal sent → Approved cleanup → QA/delivery → Closed.
Maintain private records outside the public repository. For each inquiry track received date, stage, source, response due, next action, scope, approval evidence, and outcome.

## Qualification response
Confirm podcast ownership/representation, episode scope, whether sponsorship rights may limit removal, and what outcome is desired. No audio download or edits until explicit authorization.

## Operational policy
- The free public RSS scanner uses public metadata; it is not a verified audio audit.
- The proposed $400 pilot covers up to 10 episodes subject to a mutually agreed written scope.
- No guaranteed revenue increase, ad expiration, or turnaround.
- Keep originals, document approvals, and deliver edited files only through an agreed secure channel.
