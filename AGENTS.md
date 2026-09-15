# Software agent guide

This guide applies to the whole repository. Read it before editing. Start with
[README.md](README.md) for the user workflow and [BUILDING.md](BUILDING.md) for
installation, logs, and platform details.

## Purpose and repository identity

This is the reusable **LaTeX Library Tenure Template** for Kansas State University
Libraries, not a live candidate submission. It produces a portfolio and a
standalone CV from public example content adapted from David Molik’s packet.

- Repository: <https://github.com/kstatelibraries/LaTeX-Library-Tenure-Template>
- Design and migration tracking: [Molik-Tenure-Document issue #9](https://github.com/molikd/Molik-Tenure-Document/issues/9)
- Remaining release decisions: [planning/template-release.md](planning/template-release.md)
- License: [MPL-2.0](LICENSE), with provenance in [ATTRIBUTION.md](ATTRIBUTION.md)

The template was imported as a source snapshot onto the new repository’s initial
license commit. Do not import the personal packet’s branches, tags, or ancestors:
they contain records intentionally excluded from this public project. Preserve
third-party and example attribution when editing or moving files.

The Word reference and current institutional rules are not fully reconciled.
Do not present the template as officially approved or turn proposed word limits
into enforced requirements. The reference DOCX is not bundled; do not assume it
exists on another contributor’s machine. Record unverified policy questions
rather than inventing requirements, dates, votes, or outcomes.

## Before changing files

1. Check `git status --short --branch` and `git remote -v`. Work in this repository,
   preserve unrelated changes, and identify the requested scope.
2. Read the relevant sources and tests below. Keep content edits separate from
   presentation or build changes unless the task requires both.
3. Keep the real example narratives and bibliography useful. Do not replace all
   examples with generic filler or silently strengthen a candidate’s claims.
4. For a personal-packet task, work in the user’s private copy. Do not add their
   confidential submission to this public template.

## Source map

| File or directory | Responsibility |
| --- | --- |
| `main.tex` | Portfolio assembly, cover, schedule, form placeholder, section order, and optional supporting documents |
| `main-cv.tex` | Standalone CV root |
| `candidate.tex` | Identity, review settings, optional URLs, and guidance/example switches |
| `achievements.tex`, `goals.tex` | Example accomplishments and five-year goals |
| `directed.tex`, `nondirected.tex`, `researchandcreative.tex` | Example narratives and section evidence bibliographies |
| `cv.tex` | CV body shared by both roots |
| `evidence/records.tex` | Year-organized placeholders for records; no original attachments |
| `shared/preamble.tex` | Article class, packages, bibliography options, heading styles, color, footer, and configuration loading |
| `shared/bibliography.tex` | Bibliography resource registrations |
| `template/layout.tex` | Reusable presentation macros |
| Root `*.bib` files | Public example bibliography records |
| `scripts/build.py` | Dependency checks, static checks, compilation, logs, and PDF audit |
| `scripts/check_confidentiality.py` | Tracked-file and reachable-history confidentiality check |
| `tests/` | Static source checks and unit/integration tests |
| `.github/workflows/test.yml` | Confidentiality gate, static tests, and PDF builds |

Both roots input `shared/preamble.tex`, which issues `\documentclass` itself.
Input it exactly once per document. Shared layout changes affect both outputs;
content files should not load packages or issue their own document class.
The project uses `article`, not ModernCV. Do not reintroduce the removed class,
themes, or icon dependencies for cosmetic changes.

## Layout and content interfaces

Preserve the current design: US Letter, half-inch margins, Latin Modern body
text, royal-purple (`663399`) sans-serif headings, short accent rules, and a
subtle footer. Keep long narratives and CV entries able to break across pages.
Check heading/entry separation, long links, bibliography wrapping, and page breaks
after changes. Do not use shrinking text or suppressed warnings to hide overflow.

| Interface | Contract |
| --- | --- |
| `\PortfolioSection{title}` | Starts a new page, creates a PDF navigation entry, and draws the main heading |
| `\SectionGuidance{text}` | Separate purple bullet beginning `[remove]`; visible when `\ShowGuidancetrue` |
| `\ExampleNote` | Example-attribution label controlled independently by `\ExamplePortfoliotrue` |
| `\LibraryEntry{dates}{title}{institution}{location}{extra}{description}` | Six required argument groups, including any empty `{}` groups; paragraph-based CV/goal entry |
| `\LibraryItem{label}{body}` | Labeled paragraph entry |
| `\EvidenceYear{year label}{calendar year}` | Year subheading for evidence records |
| `\Redacted{label}{explanation}` | Visible placeholder; accepts no original confidential content |
| `\OptionalLink{label}{\URLSetting}` | Displays the configured link or an insertion prompt when empty |
| `\Colorhref{URL}{text}` | Ordinary inline link helper |

Add a `[remove]` guidance item describing what belongs in each new main section.
Keep guidance separate from the candidate’s narrative. Turning off either switch
in `candidate.tex` only hides instructions or labels; it is not redaction and does
not remove the example content or evidence placeholders.

Use LaTeX-safe text. Escape special characters in prose; preserve balanced braces
and complete macro arguments. The static checker rejects narrow no-break spaces
and non-breaking hyphens that break pdfLaTeX.

Bibliography entries need unique keys. Selection uses `keywords`, not filenames;
register new resources in `shared/bibliography.tex`. Both roots use Biber with
`ext-verbose` style and descending-year sorting (`ydnt`). `\nocite{*}` loads all
registered entries, so stale example entries can still appear in filtered lists.
Do not invent missing bibliographic dates to silence a warning.

## Gathering records from Wildcat Scholar and ORCID

For user-authorized profile-based work, follow the
[README profile workflow](README.md#bringing-in-information-from-wildcat-scholar-and-orcid).
Example identities supplied by the owner are
[David Molik’s Wildcat Scholar profile](https://experts.ksu.edu/david.molik) and
[ORCID 0000-0003-3192-6538](https://orcid.org/0000-0003-3192-6538).
These are examples, not defaults for every candidate. Remove incidental trailing
punctuation when interpreting a supplied URL; preserve the actual identifier.

- Confirm identity from the user-supplied profile/iD, name, and affiliation before
  collecting records. Read only the public profile or material the user has
  authorized. Do not change profiles, privacy settings, or external records as
  part of importing information into this repository.
- Prefer official pages, an authorized export, or the documented
  [ORCID read API](https://info.orcid.org/documentation/api-tutorials/api-tutorial-read-data-on-a-record/)
  when appropriate access is available. Follow the service’s access requirements;
  never put credentials in tracked files or logs. Do not invent a Wildcat Scholar
  API or promise an export/import capability that has not been verified.
- If a page needs JavaScript, is inaccessible, or lacks a field, report the limit.
  Request an authorized export when needed. Do not substitute search snippets
  for a complete profile audit or infer missing data from absence in a public view.
- Preserve provenance for each imported item: profile/source URL, retrieval date,
  stable work identifier, reported date/status, and any unresolved conflict.
  Keep notes public-safe in this repository; private exports belong outside it.
- Deduplicate by normalized DOI or another stable identifier, then compare titles,
  authors, and dates. ORCID and Wildcat Scholar may describe the same work. Do not
  double-count it or silently collapse distinct versions, presentations, or roles.
- Verify publication metadata against the underlying work. Distinguish published,
  accepted, submitted, and in-progress items; distinguish proposed and awarded
  funding. Neither a profile entry nor an AI-generated summary proves individual
  contribution, impact, review-period eligibility, or directed-service classification.
- Map verified data to the existing files: identity in `candidate.tex`, CV records
  in `cv.tex`, publication/presentation metadata in the appropriate `.bib`, and
  supported narrative changes in the corresponding section. Add unique citation
  keys and deliberate `keywords`; register new bibliography files. Never replace
  curated records wholesale with an unchecked export.
- After imports, run the static checks, build affected outputs (both for shared
  CV/bibliography changes), inspect citations/layout, and scan confidentiality
  before an authorized public-template commit/push. For private packets, use the
  private-copy workflow below. Summarize sources read, records added/merged,
  unresolved differences, and validation. Do not claim an import when only
  documentation was changed.

[K-State’s user guide](https://www.k-state.edu/next-gen/plan/key-initiatives/other-initiatives/wildcat-scholar/user-guide.html)
describes profile visibility and AI summaries. ORCID documents
[BibTeX export](https://support.orcid.org/hc/en-us/articles/360006971453-Exporting-works-into-a-BibTeX-file)
and its [metadata/encoding limitations](https://support.orcid.org/hc/en-us/articles/360006971433-BibTeX-issues-and-troubleshooting).
This repository currently has no automated profile importer; do not add a new
integration or make account changes unless that work is requested.

## Build and checks

Run commands from the repository root. Python scripts use only the standard
library. The supported Python baseline is 3.10; CI uses Python 3.12 for static
checks. Local validation used Python 3.14 and TeX Live 2026; CI uses TeX Live 2024.
Required executables are `python3`, `latexmk`, `pdflatex`, and `biber`. On Windows,
replace `python3` with `py -3`; see BUILDING.md for setup and PowerShell details.

```sh
python3 tests/check_latex.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build.py
```

Use `python3 scripts/build.py main-cv.tex` to build only the CV, or `--verbose`
for full output. The default builds both roots and runs static checks first.
Latexmk handles the LaTeX/Biber passes; do not hard-code a pass count.

| Change | Validation |
| --- | --- |
| Markdown/documentation | Check links, anchors, commands against actual source, Markdown formatting, and confidentiality. A PDF rebuild is unnecessary unless document sources changed. |
| Narrative, bibliography, candidate settings, or layout | Static checks and affected PDF builds; inspect rendered pages. Shared sources require both roots. |
| Build driver, source checker, or confidentiality detector | Relevant unit tests and failure cases; use synthetic fixtures and temporary copies. Build both roots when compilation behavior changes. |
| Workflow | Inspect permissions, job dependencies, and triggers; verify the GitHub run after an authorized push. |

For changes to compilation/failure handling, also run the opt-in real-compiler
test (requires TeX):

```sh
RUN_LATEX_INTEGRATION=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

This deliberately introduces an error into a temporary copy. A passing test
confirms failure reporting; it is not a failure of the actual portfolio.

Outputs live in ignored `build/`: `main.pdf`, `main-cv.pdf`, native `.log`/`.blg`
files, `*-build.log`, `*-diagnostics.txt`, and `tool-versions.txt`. The driver
requires nonempty PDF and bibliography/compiler logs and returns nonzero on
failure; missing dependencies return status 2. An old PDF may remain after a
failed build, so use the current exit status and logs. The known dateless
`software.bib` entry produces a static warning; it has not been assigned a guessed
date. Investigate new warnings. Never commit generated PDFs, caches, or logs.

## Confidentiality and publication

### Private candidate packets

The intended workflow for confidential evidence is an independent private copy,
with its publication confidentiality job disabled before adding records. Follow
[the README private packet steps](README.md#private-packets-and-confidential-evidence).
GitHub forks of this public repository remain public; do not promise to make a
public fork private. Create an independent repository with private visibility.

For a user-authorized private-packet task:

1. Verify the actual destination repository is private and check the local push
   remote before adding or pushing evidence. A folder name or branch name does
   not establish privacy. If visibility cannot be verified, do not push evidence.
2. In the private copy only, remove the `confidentiality` job from
   `.github/workflows/test.yml` and remove `needs: confidentiality` from both
   `static` and `compile`. Retain the build/static jobs and read-only permissions;
   verify their run after pushing the workflow change.
3. Legitimate evaluations, supervisor comments, votes, and supporting attachments
   may then be added to the private packet as requested. Disabling this publication
   gate is the intended configuration, not a detector exception. Do not weaken the
   scanner or require private packet commits to pass the public publication scan.
   Synthetic detector tests can remain; the local build does not scan the packet.
4. Treat private CI logs and diagnostic artifacts as potentially containing packet
   text. Follow the user's retention needs; the README explains how to remove
   the diagnostic-upload step. Never copy private records into public issues,
   pull requests, or other public output. Keep credentials out of tracked files.
5. Keep evidence and its history in the private repository. Transfer reusable
   improvements through reviewed, public-safe changes on a clean public-template
   branch, not by merging private packet history or changing packet visibility.

### Public template contributions

The requirements below apply to changes intended for this public template.
Keep evaluations, supervisor/committee feedback, tenure votes, signed forms,
private links, and credentials out of tracked files and history. Placeholders
must contain only explanatory text, never originals hidden by color, overlays,
comments, or conditional commands. Do not paste private matches into issues,
PR descriptions, commit messages, or logs.

Before committing, review intended files (including untracked additions), stage
only the intended public changes, and run:

```sh
python3 scripts/check_confidentiality.py --history
```

Repeat after committing and before an authorized push so the exact commit history
is checked. The scanner reads Git-tracked working files; untracked files are not
covered until staged. The history mode requires a full checkout and visits every
commit reachable from HEAD. Removing a confidential file in a later commit does
not remove the original from history. Report a finding without exposing its text
and resolve the affected history before publication; do not rewrite unrelated
personal history.

The checker flags known vote/feedback/rating patterns, confidential markers,
private document links, and credential signals. It rejects binary attachments,
non-UTF-8 content, symlinks, and submodules that need separate review. It is not a
semantic privacy audit and cannot recognize every paraphrase. Do not weaken rules
or add exceptions just to get a real record through CI. Detector tests must use
synthetic examples, never real private feedback or votes.

CI checks full history with `fetch-depth: 0`. Both static and compile jobs depend
on the confidentiality job, preventing detected private records from reaching
uploaded build logs. Preserve that gate and read-only workflow permissions in
the public template; the private-copy exception above does not change this workflow.
The normal local build deliberately does not run the publication scan: users can
build confidential packets in their own private copies.

## Completion and remaining limitations

Before reporting completion, describe what changed, which checks actually ran,
and anything unverified. Link relevant commits/files and, when requested, update
[issue #9](https://github.com/molikd/Molik-Tenure-Document/issues/9) with findings,
edits, validation, and remaining work. Do not mark policy or release tasks complete
based only on a successful compile.

Remaining work includes rules/reference reconciliation, fresh-machine installation
tests, an Overleaf smoke test, accessibility review, and review of retained example
content. PDFs have selectable text and bookmarks but are not certified tagged
PDF/PDF-UA documents. Keep these limits explicit in user-facing documentation.
