# LaTeX Library Tenure Template

A working LaTeX template for Kansas State University Libraries reappointment and
tenure portfolios, with a standalone CV. It includes real examples adapted from
David Molik’s tenure document. Confidential attachments, evaluations, and prior
tenure votes are replaced by labeled placeholders in the example files.

**Development status:** the layout is being aligned with Tara’s January 15, 2026
Word template and the applicable updated rules. This is not yet an approved
Libraries template. The project was imported as a source snapshot onto this
repository’s own history; the personal packet’s ancestors were not transferred.
See [the release plan](planning/template-release.md).

## Start here

1. Install **Python 3.10 or newer** and a **TeX Live distribution** that includes
   `pdflatex`, `latexmk`, and `biber`. The Python scripts use the standard library;
   no pip packages or virtual environment are required.
2. Follow the [installation instructions](BUILDING.md#installation) for your OS.
3. From the repository folder, build both examples:

   ```sh
   python3 scripts/build.py
   ```

   On Windows, use `py -3 scripts/build.py`.
4. Open `build/main.pdf` (portfolio) and `build/main-cv.pdf` (CV).
5. Edit `candidate.tex`, then replace the example narratives and references with
   your own work. Rebuild after editing.

Use `python3 scripts/build.py main-cv.tex` for only the CV, or add `--verbose` for
full compiler output. [BUILDING.md](BUILDING.md) explains logs and troubleshooting.

## Customize your portfolio

| File | What to edit |
| --- | --- |
| `candidate.tex` | Name, rank, role, review year/type, confirmed review dates, and optional document/calendar/worksheet URLs |
| `main.tex` | Portfolio order and optional supporting documentation |
| `achievements.tex`, `goals.tex` | Accomplishments and five-year goals |
| `directed.tex`, `nondirected.tex`, `researchandcreative.tex` | Service and RSCAD examples |
| `evidence/records.tex` | Year-by-year position descriptions, evaluations, and letters |
| `cv.tex` | CV content shared by both outputs |
| `*.bib`, `shared/bibliography.tex` | Bibliographic records, resources, and section keyword filters |
| `template/layout.tex`, `shared/preamble.tex` | Shared presentation; ordinary users should not need to edit these |

The example is labeled on the cover and in narrative sections. After replacing
all example content, change `\ExamplePortfoliotrue` to `\ExamplePortfoliofalse`
in `candidate.tex`. This only controls the example label; it does not redact or
remove content. Empty URL settings display a prompt instead of a broken link.
Each main portfolio and CV section begins with a separate purple `[remove]`
guidance item. Delete that section’s `\SectionGuidance{...}` call when no longer
needed, or set `\ShowGuidancefalse` in `candidate.tex` to hide all guidance. This
is independent of the example labels and does not remove confidential content.
The independent layout uses royal-purple headings, short accent rules, and a
quiet running footer; it does not depend on ModernCV.

Use LaTeX escaping for characters such as `&`, `%`, and `_` in ordinary text.

Your original documents belong in your private submission copy. Replace evidence
placeholders there with authorized links or use `\includepdf[pages=-]{path.pdf}`
after the relevant year heading. Never add confidential records to the shared
example. Existing placeholders contain no underlying evaluation text or votes.

The examples illustrate writing and layout, not universally applicable review
requirements or verified model accomplishments. Confirm section requirements and
reporting periods for your review stage. Proposed word limits are not enforced.

## Development

```sh
python3 scripts/check_confidentiality.py --history
python3 tests/check_latex.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Build both outputs after layout changes and inspect their pages. See
[BUILDING.md](BUILDING.md) for the optional real-compiler failure test and
accessibility limitations. See [ATTRIBUTION.md](ATTRIBUTION.md) for project origins
and the licensing decision still needed before distribution.

## Confidentiality check

GitHub Actions checks tracked files and every commit reachable from the tested
branch for common confidential-record signals: vote counts, labeled supervisor
or committee feedback, individual ratings, private document links, and secrets.
It also rejects binary attachments, including PDFs and images, because text
matching cannot safely inspect their hidden content or metadata. Keep supporting
records in your private submission copy. Adding a public binary asset requires
an explicit review and policy change.

Stage intended files before running `python3 scripts/check_confidentiality.py --history` locally. The check reports file paths and rule names, not matching
text. Resolve findings before pushing; do not paste confidential content into
issues or Actions logs. Deleting a file in the latest commit is insufficient when
an earlier commit still contains it.

This is a deterministic review aid, not a guarantee that every confidential
statement or paraphrase will be recognized. Review real examples before sharing.
The check runs before build jobs so a detected record cannot enter uploaded
compiler logs. Maintainers can require **Confidentiality check** in branch rules.
