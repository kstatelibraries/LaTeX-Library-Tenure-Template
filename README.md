# LaTeX Library Tenure Template

[![Checks](https://github.com/kstatelibraries/LaTeX-Library-Tenure-Template/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/kstatelibraries/LaTeX-Library-Tenure-Template/actions/workflows/test.yml)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-663399.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](BUILDING.md#installation)
[![LaTeX](https://img.shields.io/badge/LaTeX-pdfLaTeX-008080?logo=latex&logoColor=white)](BUILDING.md)
[![Download template](https://img.shields.io/badge/Download-Template_ZIP-663399?logo=github&logoColor=white)](https://github.com/kstatelibraries/LaTeX-Library-Tenure-Template/archive/refs/heads/main.zip)

A LaTeX starting point for Kansas State University Libraries reappointment and
tenure portfolios, with a matching standalone CV. Real examples from David
Molik’s tenure document show how the sections can be used. Confidential records,
evaluations, and previous tenure votes are replaced with labeled placeholders.

**Software agents:** read [AGENTS.md](AGENTS.md) before working in this repository.

**New to LaTeX? Start with the numbered guide below.** You do not need Git or a
GitHub account to download the template and work on your own computer.

**Development status:** this is a working template, not yet an approved Libraries
template. Confirm the rules and reporting period for your review. The layout is
being aligned with Tara’s January 15, 2026 Word template and applicable updates;
proposed word limits are not enforced. See [the release plan](planning/template-release.md).

[How to use](#how-to-use-the-template) · [File guide](#which-file-do-i-edit) ·
[Wildcat Scholar and ORCID](#bringing-in-information-from-wildcat-scholar-and-orcid) ·
[Overleaf](#using-overleaf-instead) · [Troubleshooting](#if-something-goes-wrong) ·
[Contributing](#contributing-to-the-shared-template) · [Software agents](#software-agents)

## What you will make

The same source files produce two documents:

- **Portfolio:** `build/main.pdf`, containing the cover, narratives, evidence sections, and CV.
- **Standalone CV:** `build/main-cv.pdf`, containing the CV on its own.

A `.tex` file is an editable text file containing your writing and formatting
commands. A `.bib` file holds references. **Building** means turning these source
files into a PDF. Make changes in the source files, then build again; changes made
directly to a generated PDF will not carry back into the template.

## How to use the template

### 1. Download your own copy

1. Click the **Download Template ZIP** badge above, or the green **Code** button
   on this repository’s main page and choose **Download ZIP**.
2. Extract the ZIP. On macOS, double-click it. On Windows, right-click it and
   choose **Extract All**. Work in the extracted folder, not inside the ZIP.
3. Move the extracted folder to your Documents folder and rename it
   `My-Tenure-Portfolio`.
4. Open that folder. You should see `README.md`, `candidate.tex`, `main.tex`, and
   folders named `scripts`, `shared`, `template`, and `evidence`. If you see just
   one more folder, open that inner folder to find the files.

Keep all these files together: the template needs more than `main.tex` to build.
The ZIP is a snapshot, so later changes to this shared repository will not
silently overwrite your work. [GitHub’s download guide](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)
explains the download options.

Use your own local or private copy for your packet. This repository is public;
do not upload your completed evaluations, letters, or other confidential records
to it. Downloading the ZIP does not create a connection that uploads your edits.
For GitHub-backed confidential evidence, follow the
[private packet workflow](#private-packets-and-confidential-evidence) before adding records.

### 2. Install the software once

You need two things: **Python 3.10 or newer** to run the build helper, and a
**TeX distribution** to turn LaTeX into PDFs. No extra Python packages are needed.

| Your computer | What to install |
| --- | --- |
| macOS | Install [Python 3](https://www.python.org/downloads/macos/) and the full [MacTeX](https://tug.org/mactex/mactex-download.html) distribution. Follow the [macOS setup steps](BUILDING.md#macos). |
| Windows | Install [Python 3](https://www.python.org/downloads/windows/), including its launcher, and [TeX Live](https://tug.org/texlive/acquire-netinstall.html) with a full installation. Follow the [Windows setup steps](BUILDING.md#windows). |
| Ubuntu or Debian Linux | Follow the copy-and-paste [Linux installation commands](BUILDING.md#ubuntu-and-debian). |

Allow the installers to finish, then open a **new** terminal window so it can
find the installed tools. On macOS, open the Terminal app; on Windows, open
PowerShell; on Linux, open your terminal application. This is where you type the
commands below. Copy one line at a time and press Enter after each line.

**macOS or Linux:**

```sh
python3 --version
pdflatex --version
latexmk --version
biber --version
```

**Windows PowerShell:**

```powershell
py -3 --version
pdflatex --version
latexmk --version
biber --version
```

Each command should print a version, rather than “not found” or “not recognized.”
If one fails, use the [installation troubleshooting](BUILDING.md#troubleshooting-and-validation)
before continuing. You only need to install the software once on each computer.

### 3. Build the unchanged example first

Building before editing confirms your setup works and gives you a PDF to compare
with your changes.

In the terminal, move into the folder you created in step 1. If you used the
suggested folder name and location:

**macOS or Linux:**

```sh
cd "$HOME/Documents/My-Tenure-Portfolio"
ls README.md
python3 scripts/build.py
```

**Windows PowerShell:**

```powershell
cd "$HOME\Documents\My-Tenure-Portfolio"
Get-Item README.md
py -3 scripts/build.py
```

If Documents is stored elsewhere, such as in OneDrive, replace the quoted path
with your folder’s actual location. You can copy it from your file manager’s
address bar. The `README.md` check should find that file; if it does not, you are
not yet in the correct folder.

Let the build finish. Multiple passes through LaTeX and the bibliography are
normal. On success, the terminal prints `Stage: output ready` for both PDFs.
Open the new `build` folder in your file manager, then double-click `main.pdf`
and `main-cv.pdf`. You should see David’s example text, royal-purple headings,
and `[remove]` instruction items.

### 4. Put your information on the cover

Open `candidate.tex` in a plain-text or code editor, not Microsoft Word. Change
the text inside the **second pair of braces** on each setting. For example:

```tex
\newcommand{\CandidateName}{Riley Example}
\newcommand{\CandidateRank}{Assistant Professor}
\newcommand{\CandidateRole}{Your position title}
\newcommand{\CandidateUnit}{Kansas State University Libraries}
\newcommand{\ReviewYear}{2026}
\newcommand{\ReviewType}{Annual Reappointment}
```

Replace those sample values with your own. Keep the command names, backslashes,
and braces. Fill in your appointment date and confirmed review dates. If a date
is not confirmed, resolve it before submitting; do not borrow the example’s dates.

Optional links start with empty braces. To add a document collection link:

```tex
\newcommand{\CollectionURL}{https://example.org/your-document-collection}
```

Use your actual authorized URL. Leave the braces empty while drafting if you do
not have one yet; the PDF will show an “Insert current URL” prompt. Remove or
resolve that prompt in the final document. Save the file, run the build command
again, and check that the PDF reflects your changes.

### 5. Replace the example narratives and CV

Use the [file guide below](#which-file-do-i-edit) to work through one section at a
time. Read its purple `[remove]` item first: it explains what belongs there.
Replace David’s examples with your own writing, and save and rebuild after each
small set of changes. Updating your name does **not** replace the example content.

Keep the formatting commands around the text you are editing. For example, a
list looks like this:

```tex
\begin{itemize}
  \item Describe one activity, your role, and its outcome.
  \item Describe another activity and point to supporting evidence.
\end{itemize}
```

Each `\item` becomes a bullet. Add or remove complete `\item` entries while
keeping the opening and closing lines. A blank line between ordinary paragraphs
starts a new paragraph.

For a CV appointment, the six groups in `\LibraryEntry` mean dates, title,
institution, location, additional detail, and description:

```tex
\LibraryEntry{2025--present}{Your title}{Your institution}{Your location}{}{
Describe your responsibilities and contributions.
}
```

The empty `{}` is intentional; keep it if you do not need that optional detail.
Other existing examples span several lines but use the same six groups.

Some characters need a backslash in ordinary LaTeX text:

| To display | Type |
| --- | --- |
| `&` | `\&` |
| `%` | `\%` |
| `_` | `\_` |
| `$` | `\$` |
| `#` | `\#` |

For links in narrative text, use `\href{https://example.org}{Readable link text}`
or `\url{https://example.org}`. The special-character table applies to prose;
keep a URL’s characters intact inside `\url{...}`.

### 6. Update references and evidence

Already have records in Wildcat Scholar or ORCID? Follow the
[profile workflow below](#bringing-in-information-from-wildcat-scholar-and-orcid)
to gather and reconcile them before editing your references.

**References:** replace the example records in the `.bib` files with your own.
Most journal records belong in `journal.bib`, presentations in `talks.bib`, and
service references in `service.bib`. Each record needs a unique key. Its
`keywords` field controls where it appears, so follow the examples already in
that file; for example, `journal` selects the CV’s collaborative-articles list
and `creative` selects the RSCAD evidence list. A filename alone does not decide
where a record appears. Save and rebuild to refresh the bibliography.

If you add a new `.bib` file, also add an
`\addbibresource{your-file.bib}` line to `shared/bibliography.tex`. Remove unwanted
example records as you go so they do not remain in your finished bibliography.

**Evidence:** open `evidence/records.tex`. Add or adjust the `\EvidenceYear` blocks
for your review years and replace the corresponding placeholders in your private
submission copy. For example, to include an authorized PDF stored at
`evidence/my-position-description.pdf`, use:

```tex
\EvidenceYear{Year One}{2025}
\includepdf[pages=-]{evidence/my-position-description.pdf}
```

That inserts all pages without rewriting the source PDF. Use your own year and
filename, or provide an authorized link instead. Confirm reviewers can access
links you supply. The shared repository’s confidentiality check deliberately
rejects attachments and confidential records; those belong only in your private
packet. The local PDF build does not run that publication check.

### 7. Remove drafting instructions and inspect the result

Once the example content has been replaced, change these two settings in
`candidate.tex`:

```tex
\ExamplePortfoliofalse
\ShowGuidancefalse
```

The first hides the “Example adapted from David Molik’s tenure document” labels.
The second hides the purple `[remove]` instructions. To remove instructions for
just one section, delete its entire `\SectionGuidance{...}` command instead.
**These settings only hide labels and guidance. They do not delete examples,
redact private information, or remove the evidence placeholders.**

Build again and read both PDFs from beginning to end. Check that:

- Your name, role, dates, reporting period, and review type are correct.
- All remaining accomplishments, CV entries, and references are yours.
- No `[remove]` instructions, “Insert” prompts, unwanted example text, or redacted-example placeholders remain.
- Evidence is complete, links work for the intended reviewers, and headings and page breaks look sensible.
- The document meets the requirements for your particular review stage.

Keep a backup of your whole source folder as well as your finished PDFs. Submit
the appropriate documents through your institution’s review process.

## Which file do I edit?

| File | What it controls |
| --- | --- |
| [`candidate.tex`](candidate.tex) | Cover information, review dates, optional links, and instruction/example-label switches |
| [`achievements.tex`](achievements.tex) | Statement of accomplishments |
| [`goals.tex`](goals.tex) | Five-year goals |
| [`directed.tex`](directed.tex) | Directed service narrative |
| [`nondirected.tex`](nondirected.tex) | Non-directed service narrative |
| [`researchandcreative.tex`](researchandcreative.tex) | Research, scholarly and creative activities, and discovery (RSCAD) |
| [`evidence/records.tex`](evidence/records.tex) | Year-by-year position descriptions, evaluations, and reappointment letters |
| [`cv.tex`](cv.tex) | CV content used in both PDFs |
| `*.bib` and [`shared/bibliography.tex`](shared/bibliography.tex) | Reference records and the list of bibliography files to load |
| [`main.tex`](main.tex) | Portfolio assembly, recommendation-form placeholder, and optional supporting documentation |
| [`template/layout.tex`](template/layout.tex), [`shared/preamble.tex`](shared/preamble.tex) | Fonts, colors, spacing, headings, and other presentation settings |

Start with the content files. You generally do not need to change the layout
files or the build helper in `scripts` to write your packet.

## Bringing in information from Wildcat Scholar and ORCID

You can use your existing scholarly profiles to gather publications, appointments,
teaching, and service information before writing your packet. This template does
not automatically fetch or synchronize profiles: review the records, then copy
verified information into the appropriate `.tex` and `.bib` files.

Example profiles supplied for this template:

- [David Molik on Wildcat Scholar / K-State Experts](https://experts.ksu.edu/david.molik)
- [David Molik on ORCID](https://orcid.org/0000-0003-3192-6538)

Use **your own** profile when building your packet. Confirm the person’s name,
affiliation, and ORCID iD before using records; a matching name alone is not enough.

### Gather information from Wildcat Scholar

1. Open your public profile at [K-State Experts](https://experts.ksu.edu/). The
   public directory displays information from Wildcat Scholar; K-State’s
   [user guide](https://www.k-state.edu/next-gen/plan/key-initiatives/other-initiatives/wildcat-scholar/user-guide.html)
   explains profiles and their privacy settings.
2. Review the available publication, professional-activity, teaching, appointment,
   and other relevant entries. Note titles, dates, your role, and links to the
   underlying work. Record the profile URL and the date you checked it.
3. Open publication links to verify bibliographic details against the publisher
   or DOI record. Treat profile summaries as starting points, not evidence of
   your individual contribution or a tenure classification.
4. Copy verified items into the files listed in the table below. If you already
   have an authorized export from your account, review it item by item in the
   same way; do not assume the public profile offers a particular export format.

K-State distinguishes public, internal, and private profile information. Keep
internal/private exports in your private packet, and use only appropriate public
material in contributions to this repository. Absence from a public profile does
not mean an activity did not happen. Check missing or conflicting information
against your own records rather than inventing details.

### Bring publication records across from ORCID

1. Open your ORCID record and confirm the iD. Review the listed works and their
   persistent identifiers, such as DOIs.
2. To export your own records, sign in and go to **Works**. Select the desired
   works, use **Actions → Export works** (or **Export all works**), then choose
   **Export selected works to BibTeX**. Follow the current
   [ORCID export instructions](https://support.orcid.org/hc/en-us/articles/360006971453-Exporting-works-into-a-BibTeX-file)
   if the interface differs.
3. Save the downloaded `.bib` file somewhere you can review it before merging it
   into the template. ORCID exports can preserve errors and may omit metadata;
   check authors, title, date, publication status, venue, DOI, and character
   encoding. See [ORCID’s BibTeX notes](https://support.orcid.org/hc/en-us/articles/360006971433-BibTeX-issues-and-troubleshooting).
4. Compare against your existing references and Wildcat Scholar records. Merge
   duplicates by DOI where available, then compare title, authors, and year.
   Keep a preprint and a published article distinguishable when both are relevant.
5. Copy the reviewed records into the appropriate existing `.bib` file, give
   every record a unique key, and add the template’s `keywords`. For example,
   `keywords = {journal,creative}` places a suitable article in the collaborative
   CV publication list and RSCAD evidence list. Choose keywords for the actual
   item; exported records do not automatically have the template’s classifications.
6. If you keep a new bibliography filename, register it in
   `shared/bibliography.tex`. Build again and check that each record appears in
   the intended section without duplicates.

### Put each verified item in the right place

| Information you gathered | Where it can go |
| --- | --- |
| Confirmed identity and appointment information | `candidate.tex` and the appropriate entries in `cv.tex` |
| Publications and presentations | Relevant `.bib` files, with the appropriate section keywords |
| Teaching, professional roles, awards, and service | `cv.tex` and the relevant narrative section, after checking your role and review-period relevance |
| Significance, impact, and individual contribution | Your own explanation in the narrative files, supported by evidence; do not infer these from a profile listing |

Keep source URLs and access dates in your working notes, or as non-confidential
comments alongside imported bibliography entries. If the two profiles disagree,
record the discrepancy and verify the underlying source. Do not silently choose
the more favorable date, claim an unconfirmed award, or convert an in-progress
work into a publication. Apply your review’s reporting period after gathering the
records; profiles may cover an entire career.

Then run the normal build command and inspect both PDFs. For changes intended for
this shared repository, also run the confidentiality check before committing and
pushing, as described under [Contributing](#contributing-to-the-shared-template).

## Using Overleaf instead

Overleaf is an alternative for working in a browser without a local Python or
TeX installation. The local build route above has been tested; this template’s
Overleaf route still needs a full smoke test.

1. Download the template ZIP from the badge at the top of this README.
2. In your Overleaf dashboard, choose **New Project → Upload Project** and select
   the ZIP. See [Overleaf’s upload guide](https://www.overleaf.com/learn/latex/Kb/Uploading_a_project).
3. Set the project’s main document to `main.tex` and its compiler to **pdfLaTeX**.
4. Click **Recompile** and check the example PDF before editing.
5. Follow steps 4–7 above to personalize the files. Use **Recompile** wherever
   those steps say to run the local build command.
6. To produce only the CV, select `main-cv.tex` as the main document and recompile.

Keep the project private and follow your institution’s rules for uploading
confidential documents to external services. Overleaf compiles the LaTeX directly;
it does not run this repository’s Python checks or GitHub confidentiality Action.

## If something goes wrong

| What you see | What to do next |
| --- | --- |
| `python3` or `py` is not found | Check the Python installation, then reopen the terminal. Windows commands use `py -3`. |
| `Missing dependency: latexmk`, `pdflatex`, or `biber` | Finish the TeX installation and reopen the terminal. See [installation help](BUILDING.md#installation). |
| Python cannot open `scripts/build.py` | Move into the extracted folder that contains both `README.md` and `scripts`. |
| A missing `.sty` file | A TeX package is missing. Follow the full installation route in [BUILDING.md](BUILDING.md). |
| An error appears after an edit | Check the first reported file and line number. Look for a missing brace, an unescaped special character, or an incomplete command. Undo the last small change and rebuild if necessary. |
| The PDF still shows old text | Save your source file and check that the latest build succeeded. Reopen the PDF from your current folder’s `build` directory. An older PDF can remain after a failed build. |
| A citation or bibliography record is missing | Check its unique key, `keywords`, and that its `.bib` file is loaded in `shared/bibliography.tex`. |

For more detail, run `python3 scripts/build.py --verbose`, or
`py -3 scripts/build.py --verbose` on Windows. Logs are in `build`; the
`*-diagnostics.txt` files summarize problems. More help is in
[BUILDING.md](BUILDING.md#troubleshooting-and-validation).

You can [open an issue](https://github.com/kstatelibraries/LaTeX-Library-Tenure-Template/issues/new)
with your operating system, tool versions, and a small non-confidential example
of the problem. Review log excerpts before sharing them: logs can contain your
source text.

## Software agents

[AGENTS.md](AGENTS.md) is the repository-wide guide for AI coding assistants and
other software agents. It covers the source map, LaTeX macro interfaces, build and
test commands, confidentiality checks, publication workflow, and known limitations.
Read it before making changes. The guide also links to
[the design and migration discussion in issue #9](https://github.com/molikd/Molik-Tenure-Document/issues/9).

## Private packets and confidential evidence

The intended personal-packet workflow is to make your own **private repository**,
turn off its publication confidentiality check, and then add the evidence needed
for your review, including evaluations, supervisor comments, and tenure votes.
The shared public template keeps its confidentiality check enabled.

### Create a private copy first

GitHub’s **Fork** button creates a public fork of this public repository, and you
cannot change that fork’s visibility independently. Use an independent private
copy for your packet. See [GitHub’s fork visibility rules](https://docs.github.com/en/pull-requests/reference/forks).

1. Download and extract the clean template ZIP as described in
   [step 1](#1-download-your-own-copy). Do this before adding personal evidence.
2. On GitHub, create a **new repository** under your account or an approved
   organization. Choose **Private** before creating it. Give it a name such as
   `My-Tenure-Portfolio`.
3. Confirm that the repository page displays **Private** and that its access
   settings include only the intended collaborators. A private repository is
   accessible to people granted access; use an institution-approved account and
   sharing arrangement for your records.
4. Add the extracted template files to this new repository using GitHub Desktop
   or Git. Include the hidden `.github` directory and retain `LICENSE` and
   `ATTRIBUTION.md`. Set the new private repository as the push destination;
   verify the destination before pushing. Start from the clean template, without
   importing a personal packet’s old branches or history.

### Turn off the publication check in your private copy

After confirming the destination is private, edit
[`.github/workflows/test.yml`](.github/workflows/test.yml) **in that private copy**:

1. Remove the entire `confidentiality:` job, from that line through its last
   step, stopping before `static:`. Keep the surrounding `jobs:` line.
2. Remove `needs: confidentiality` from **both** `static:` and `compile:`.
   Otherwise those build checks still depend on the removed job.
3. Keep the static tests, PDF build, and read-only workflow permissions. Commit
   and push this workflow change to the private repository. Check its **Actions**
   tab to confirm that the remaining jobs run successfully.

The remaining detector unit tests use synthetic examples; they do not scan your
packet. You do not need to delete the detector or weaken its matching rules.
The normal local build (`python3 scripts/build.py`) also does not run the
publication confidentiality scan.

You can now add the confidential evidence and replace the placeholders in your
private packet. Build logs can include document text and filenames; the workflow
retains diagnostic artifacts for 14 days. If you do not want these retained on
GitHub, remove the **Retain build diagnostics** step in your private copy and
use local logs for troubleshooting.

Keep the packet and its history private. Do not open a pull request containing
personal evidence against the shared template or make the completed packet
repository public. For reusable improvements, copy only reviewed, public-safe
changes into a clean branch of the public template and run its confidentiality
check there. Turning off the check allows private evidence; it does not redact
files, history, logs, or PDFs for publication.

## Contributing to the shared template

The steps above are for writing your own packet. To improve the shared template,
work in a Git branch and open a pull request with reusable changes and public
examples. Keep personal submissions out of that contribution.

Stage the intended files with Git, then run:

```sh
python3 scripts/check_confidentiality.py --history
python3 tests/check_latex.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

The confidentiality check inspects tracked files and every commit reachable from
the branch. It looks for common vote counts, labeled supervisor/committee records,
individual ratings, private links, and secrets. It also rejects binary attachments
that can conceal content or metadata. It reports paths and rule names, not matched
text. A finding in history is not fixed by deleting only the current file.

This check is a review aid, not a guarantee that all sensitive prose will be
recognized. GitHub runs it before the test and PDF-build jobs. Build both outputs
and inspect their pages after presentation changes; see [BUILDING.md](BUILDING.md)
for the optional compiler-failure test and accessibility limitations.

See [LICENSE](LICENSE) for the repository’s MPL-2.0 license and
[ATTRIBUTION.md](ATTRIBUTION.md) for the original template and example attribution.
