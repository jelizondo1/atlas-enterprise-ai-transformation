# Final public-package validation

Executed 2026-09-08 on Windows with Python 3.12, Streamlit 1.63.0 and jsonschema 4.26.0.

| Verification | Result |
|---|---|
| Public software suite | 121 tests passed; zero failures/errors |
| Public package checks | 267 passed; zero failures |
| Browser interaction checks | 6 passed; four real screenshots visually inspected |
| Fresh environment / relocated repository | 6 passed |
| Dependency consistency | pip check: no broken requirements |
| Secret / absolute-machine-path scan | Zero findings in selected public files |
| Supplemental local username / encoding scan | Zero matches |
| Live model attempts / semantic reviews | 0 / 0; pending credential and independent review |

The software suite includes 21 map tests (one valid artifact and twenty rejected mutations), 32 ROI/control tests, 32 workbench/measurement tests, 34 mocked-integration/evaluation tests and 2 offline demo tests. No software test is counted as a live model result.

Package checks verify original source bytes, public lineage hashes, schemas, opportunity source pointers, source-isolated contexts, request bounds, fail-closed state, precise baseline arithmetic, unknown ROI and all local Markdown links including README image links. These checks do not establish semantic correctness of future generated prose. External web links are not a live availability guarantee.

The demo rendered all twelve cases with no API. Browser checks exercised the three curated cases, numbered evidence, rejection of blank review and a cited session assessment that retained Solara's hold. All four screenshots are actual local UI captures. Visual review corrected currency formatting and the written supplier attribution for Apex case 0018.

A separate fresh virtual environment installed only public requirements. A relocated copy reproduced the authoritative quantitative output exactly, built twelve read-only dossiers and 28 diagnosis source sections, preserved unsized ROI, rejected missing live credentials before any request and prepared three explicitly dry requests. Temporary files were excluded from the public repository. No hidden external workspace paths are required at runtime.

The repeated verification after export caught and corrected inherited links, source newline/hash mismatches and encoding conversion. Final source bytes and hashes pass. No original authoritative package was changed.

Evidence: [software results](software_checks.json), [package results](package_checks.json), [browser results](browser_checks.json), [clean-environment results](clean_environment_checks.json), [scrub scope](public_release_scrub.md).

## Reproduce

```sh
python -m unittest discover -s tests -v
python tests/check_package.py
python tests/run_validation.py --output runs/software_checks.json
```

Readiness is limited to this reviewed public POC package. Live model performance, independent semantic acceptance, production controls and realized benefits remain unestablished. Publication still requires user approval.
