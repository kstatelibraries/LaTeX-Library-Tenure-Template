# Libraries template development and release

Working name: LaTeX Library Tenure Template. The project lives in `kstatelibraries/LaTeX-Library-Tenure-Template`.
The preparation branch is `codex/library-tenure-template`.
Tracking discussion: [issue 9](https://github.com/molikd/Molik-Tenure-Document/issues/9).

## Reference and interpretation

The layout is based on the locally supplied `Tenure Portfolio Template - Jan. 15,
2026.docx`: Letter paper, half-inch margins, large plain section headings,
employment history before the recommendation, five narrative sections, annual
evidence, CV, and optional supporting documentation. Latin Modern is used as a
portable typeface rather than attempting exact Word font matching. Pagination
follows the amount of content. Royal-purple sans-serif headings, short accent rules, a quiet running footer,
and PDF bookmarks support navigation. Each main section also includes a
removable `[remove]` authoring item, controlled separately from example labels.

The initial source comparison is not a policy ruling. Before release, retain an
accessible copy/version of the reference and reconcile the updated rules for
annual review, mid-probation review, and final tenure. Proposed 800/400-word
limits are not enforced. Confirm applicable requirements before presenting this
as an approved Libraries template.

## Example content and redaction

Real narrative, goal, CV, and publication examples from David’s packet remain.
The current working tree removes evaluation/recommendation PDFs, private source
attachments, private evidence registers, contact details, and internal document
URLs. Confidential evidence is represented by text-only placeholders. Some
working consultation/proposal details are omitted while retaining the surrounding
examples. This is an initial redaction pass, not completed publication clearance.

The original files remain recoverable on the personal portfolio branch. Do not
rewrite that branch or modify its signed originals. The new repository imports a source snapshot of preparation commit `5327737`
onto its existing license commit, rather than importing the personal repository’s
Git ancestry. The original repository and its branches remain unchanged. A
full-history confidentiality scan checks the exact new history before pushing.

## Release checklist

- [ ] Review the retained examples and references for any remaining confidential
  details, including source comments, filenames, metadata, generated PDFs, and
  extracted text. Verify redactions remove underlying data rather than covering it.
- [ ] Review the applicable rules and template fidelity, including representative
  Word and LaTeX page renderings.
- [ ] Test documented dependency installation on fresh supported systems,
  compile both outputs in CI, and smoke-test Overleaf.
- [ ] Review PDF accessibility and document remaining limitations.
- [ ] Settle licensing and attribution for reusable code and example content.
- [x] Import the current source snapshot onto the destination’s initial commit;
  retain its MPL-2.0 license and historical attribution notices.
- [x] Add a confidentiality job that inspects tracked files and full reachable
  history before build jobs, with synthetic regression tests.
- [x] Inspect and scan the imported files and initial destination history.
  Repeat the scan after committing and before the push; transfer no personal
  branches or tags.
- [ ] Confirm maintainers and document the contribution/PR workflow. Require the
  confidentiality check in the repository’s branch rules if desired.
