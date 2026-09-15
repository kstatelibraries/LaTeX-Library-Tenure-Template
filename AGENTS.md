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
uploaded build logs. Preserve that gate and read-only workflow permissions.
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
