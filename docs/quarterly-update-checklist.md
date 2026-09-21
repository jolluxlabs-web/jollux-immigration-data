# Quarterly DOL Disclosure-Data Update Checklist

Use this checklist when evaluating a new quarterly or annual Office of Foreign Labor Certification (OFLC) disclosure release. It is intended for maintainers of this package. It does not require source workbooks or generated datasets to be committed to Git.

## 1. Confirm the official source

- [ ] Open the U.S. Department of Labor OFLC [Performance Data](https://www.dol.gov/agencies/eta/foreign-labor/performance) page.
- [ ] Confirm the fiscal year, quarter, program, disclosure filename, and publication date when available.
- [ ] Locate the record layout published alongside each disclosure file.
- [ ] Use the PWD files from the Prevailing Wage section and the PERM files from the PERM section.
- [ ] Record the source page and filenames in the pull request or maintenance notes.

Do not use a third-party mirror as the authoritative source.

## 2. Keep downloaded files outside Git

- [ ] Download disclosure workbooks and record layouts to a directory outside this repository.
- [ ] Do not copy source workbooks, bulk CSV exports, or normalized bulk output into the repository.
- [ ] Confirm that local input and output paths are covered by an appropriate ignore rule before running tools from the repository directory.
- [ ] Delete temporary outputs when they are no longer needed.

The repository should continue to contain synthetic fixtures only.

## 3. Compare record layouts with supported columns

Compare the official record layouts with the required-column sets in:

- `src/jollux_immigration_data/pwd.py`
- `src/jollux_immigration_data/perm.py`

For each program:

- [ ] Check whether every required input column still exists.
- [ ] Check for renamed columns, changed definitions, or changed value formats.
- [ ] Review newly added columns and decide whether they are within the package's focused scope.
- [ ] Confirm that removed or renamed fields produce a clear schema-validation error.
- [ ] Avoid adding fields solely because they appear in the new file; document the reusable use case first.

## 4. Review PWD and PERM schema differences

- [ ] Review PWD and PERM separately. Do not assume that similarly named fields have the same meaning.
- [ ] Check whether the release includes multiple form versions or separate old-form and revised-form files.
- [ ] Confirm which employer, job, worksite, wage, status, filing, decision, and recruitment fields apply to each program.
- [ ] Check whether the active worksheet and header row still match the current reader assumptions.
- [ ] Document any fiscal-year or form-version limitation introduced by the update.

If one mapping cannot describe all supported files clearly, prefer a small, explicit schema mapping over silent fallback behavior.

## 5. Review normalization and date behavior

### Dates

- [ ] Test Excel serial dates, native spreadsheet dates, and documented text-date formats present in the release.
- [ ] Confirm that emitted dates remain ISO `YYYY-MM-DD` values.
- [ ] Check missing and malformed dates without inventing replacement values.

### Employers

- [ ] Preserve the source employer name alongside the normalized matching key.
- [ ] Review whether new punctuation or legal-suffix patterns change normalization results.
- [ ] Check potential collisions where different source names produce the same normalized key.

### Locations

- [ ] Review state and territory values against `location.py`.
- [ ] Preserve unknown values for review rather than silently mapping them to an unrelated code.
- [ ] Test any newly observed documented state or territory representation with synthetic examples.

### Wage levels

- [ ] Compare documented wage-level values with `wage.py`.
- [ ] Confirm that recognized representations normalize consistently.
- [ ] Preserve unrecognized values rather than guessing their meaning.

### Recruitment interval

- [ ] Confirm that recruitment start and received dates retain their documented meanings.
- [ ] Continue to describe the start-to-filing interval as a derived statistic, not official PERM processing time.

## 6. Update synthetic fixtures only when needed

- [ ] Add or change a fixture only when it exercises a supported schema or behavior change.
- [ ] Use invented case numbers, employers, people, jobs, wages, and locations.
- [ ] Do not copy a row from an official disclosure file or a production system.
- [ ] Keep fixtures small and readable.
- [ ] Add focused tests for each new mapping, format, warning, or edge case.

## 7. Run the test suite

From an environment with the test dependencies installed, run:

```bash
pytest
```

- [ ] Confirm the complete suite passes.
- [ ] Review failures as possible schema changes rather than weakening assertions to accept unknown input.
- [ ] Confirm tests do not require network access, credentials, or downloaded datasets.

## 8. Review documentation and release notes

- [ ] Update `README.md` if supported fields, limitations, usage, or methodology changed.
- [ ] Update `CHANGELOG.md` for user-visible changes.
- [ ] Document the affected fiscal year, quarter, or form version when relevant.
- [ ] Keep the official source link current.
- [ ] State compatibility limits without implying support for files that have not been tested.

## 9. Perform a pre-commit repository audit

Before committing, inspect the complete diff and tracked-file list:

- [ ] No `.env` files, credentials, tokens, private keys, or database URLs.
- [ ] No analytics identifiers or database code.
- [ ] No deployment, Vercel, Cloudflare, or OpenAI configuration.
- [ ] No production exports, website code, generated website data, or private assets.
- [ ] No downloaded DOL workbooks or bulk derived datasets.
- [ ] No unintended binary files, archives, notebook caches, or machine-specific paths.
- [ ] Only synthetic fixtures are present.
- [ ] `git status` contains only the intended source, test, and documentation changes.

## 10. Choose the version impact

Use [Semantic Versioning](https://semver.org/) for the package version:

- **Patch release (`0.1.x`)**: Documentation corrections, test-only changes, or compatible parsing fixes that do not change the documented public API or normalized output schema.
- **Minor release (`0.x.0`)**: Backward-compatible support for a new quarter, form version, optional field, normalization behavior, warning, or output capability. Existing documented callers should continue to work.
- **Major release (`x.0.0`)**: Incompatible changes to the public Python API, CLI, required inputs, filtering rules, normalized field names or meanings, output schema, or established normalization behavior.

Before choosing a major version bump, first consider whether an explicit versioned schema mapping can preserve compatibility. Record the decision and migration notes in `CHANGELOG.md`.
