# Install and build

The build driver uses Python’s standard library and runs static checks, latexmk,
pdfLaTeX, and Biber. No pip dependencies are required. Use Python 3.10 or newer;
this is the supported baseline, not a claim that older interpreters were tested.

## Installation

### macOS

1. Install Python 3 from the [official Python downloads](https://www.python.org/downloads/macos/).
2. Install the full [MacTeX distribution](https://tug.org/mactex/mactex-download.html).
   It supplies TeX Live and avoids the extra package setup required by BasicTeX.
3. Open a new terminal. If the TeX commands cannot be found, ensure
   `/Library/TeX/texbin` is on your PATH.
4. Run the verification commands below, then build the examples.

### Windows

1. Install Python 3 from the [official Python downloads](https://www.python.org/downloads/windows/),
   including the Python launcher.
2. Use the [TeX Live Windows installer](https://tug.org/texlive/acquire-netinstall.html)
   and select a full installation. Follow its PATH setup instructions, then open
   a new terminal. [TeX Live’s Windows notes](https://tug.org/texlive/windows.html)
   cover installation and environment troubleshooting.
3. Use `py -3` in place of `python3` in this guide. Verify with `py -3 --version`.

### Ubuntu and Debian

Install Python and the TeX packages through the distribution package manager:

```sh
sudo apt update
sudo apt install python3 latexmk biber texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-bibtex-extra texlive-fonts-recommended lmodern
```

Alternatively, use the full [upstream TeX Live installation](https://tug.org/texlive/quickinstall.html)
and follow its PATH instructions. Use one TeX installation consistently so Biber
and biblatex versions agree. Package names can differ on other Linux distributions.

### Verify the tools

```sh
python3 --version
pdflatex --version
latexmk --version
biber --version
```

The template directly loads `fontenc`, `lmodern`, `geometry`, `parskip`, `titlesec`,
`enumitem`, `needspace`, `xcolor`, `fancyhdr`, `pdfpages`, `biblatex` (with `biblatex-ext`’s
`ext-verbose` style), `hyperref`, and `xurl`. The installations above are intended
to supply these and their dependencies. ModernCV and icon-font packages are no
longer needed.

## Build

From the repository folder:

```sh
python3 scripts/build.py
python3 scripts/build.py main-cv.tex
python3 scripts/build.py --verbose
```

The first command builds both outputs; the others demonstrate one output and
verbose diagnostics. PDFs are written to `build/main.pdf` and `build/main-cv.pdf`.
The driver invokes latexmk, which schedules the required LaTeX and Biber passes.

For a direct build without Python’s checks and diagnostic summaries:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex main-cv.tex
```

To start fresh, delete only the generated `build` folder using your file manager.
Generated PDFs, logs, and caches are ignored by Git.

## Troubleshooting and validation

A missing executable returns status 2. Fix the installation or PATH and retry.
A missing `.sty` file indicates an incomplete TeX installation; consult the
package list above. A Biber/biblatex version mismatch requires a consistent TeX
installation rather than a change to bibliography content.

A failed static check or compilation returns a nonzero status. Do not treat an
older PDF left in `build` as evidence that the latest build succeeded.

- `build/*-build.log`: commands, output, elapsed time, and exit status.
- `build/*.log` and `build/*.blg`: native compiler and bibliography logs.
- `build/*-diagnostics.txt`: errors and layout warnings with line numbers.
- `build/tool-versions.txt`: versions used for the current build.

```sh
python3 tests/check_latex.py
python3 -m unittest discover -s tests -p 'test_*.py'
RUN_LATEX_INTEGRATION=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

The last command is optional and requires TeX. It introduces an intentional
compiler error in a temporary copy and verifies the build fails with useful
logs. In PowerShell set `$env:RUN_LATEX_INTEGRATION='1'` before running the tests.
The dateless software example currently produces a bibliography warning; it is
not assigned an invented date. Investigate new warnings after edits.

## Validation status and CI

This branch has been built locally with Python 3.14 and TeX Live 2026: both
outputs compile without layout warnings, and all twelve tests pass, including
the intentional compiler-failure test. CI is configured for
Python 3.12 static tests and a frozen TeX Live 2024 image for compilation; the
changed template must pass CI before release. Windows/Linux installation paths
are documented but have not yet been exercised on fresh machines for this
branch. Fresh-machine onboarding remains a release task.

CI runs the confidentiality check on tracked files and full reachable history
before running tests or the build driver. It retains diagnostic logs for 14 days
only from build jobs that pass that gate. Logs can
contain document text: keep confidential submissions in private repositories.
Different tool/font versions may change line wrapping and pagination.

### Build failure behavior (issue #2)

The compile action stops at the first failed document; its nonzero exit fails the
job and workflow. The diagnostic-upload step uses `if: always()`, so available
logs are retained even after failure. Neither the compile job nor its build step
uses GitHub's `continue-on-error` override.

The removed `with.continue_on_error: true` setting was a different option:
[the LaTeX action implementation](https://github.com/xu-cheng/latex-action/blob/v3/entrypoint.sh)
tries subsequent documents but still returns a nonzero exit if compilation fails.
Thus the earlier claim that this input made broken builds green was incorrect;
removing it makes failure handling stop immediately rather than repairing a
suppressed exit status. See [review issue #2](https://github.com/kstatelibraries/LaTeX-Library-Tenure-Template/issues/2).

The month regression test owns a small synthetic bibliography and checks both a
record without a month and numeric, textual, and macro month values. It remains
active even if every month field is removed from the example bibliography.
The opt-in compiler-failure test checks the driver's failure status and logs in
CI's TeX environment. It does not assert the final GitHub workflow conclusion;
a separate deliberately failing workflow run would be needed to verify that
end to end. No intentionally failing workflow is added to routine checks.


## Overleaf

For a private copy, upload the current source tree with `candidate.tex`, `shared`,
`template`, `evidence`, and bibliography files. Select pdfLaTeX and choose
`main.tex` or `main-cv.tex` as the main document. The inputs use relative paths.
Overleaf compiles LaTeX directly; the local Python checks and diagnostic driver
are not part of that route. This revised template still needs an Overleaf smoke
test before claiming platform support.

## PDF review

Inspect the cover, long headings/URLs, evidence placeholders, bibliographies,
and CV after changes. PDFs have selectable text and bookmarks but are not
certified tagged PDF/PDF-UA documents. Reading order and assistive-technology
support need a separate accessibility review; embedded private PDFs retain their
own limitations.
