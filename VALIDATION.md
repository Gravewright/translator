# Validation

## 0.1.3 — local release validation, 2026-10-23

- All three authoring tests passed, including two byte-identical deterministic
  builds and extraction of direct and adapter translation calls.
- Python project, application and manifest versions match at `0.1.3`.
- Each catalog contains 3,584 entries with matching keys and placeholders.
- All 3,012 original key/value pairs in each 0.1.2 catalog remain unchanged.
- The host translation audit returned no errors and no unmatched native calls.
- The build test checked portable ZIP contents, documentation links and examples.

The candidate is built from the source prepared for 0.1.3. Local checks do not
claim Marketplace signing, publication or acceptance of the final signed package.
The visibility title and dynamic messages also require the corresponding host
code fixes; this catalog release does not update the VTT application.

## 0.1.2 — local release validation, 2026-10-11

- The Django build test passed: two builds produced identical bytes and SHA-256.
- Python project, application and manifest versions match at `0.1.2`.
- Each authoring catalog contains 3,012 entries; key and placeholder validation passed.
- The host translation audit returned no errors and no unmatched native translation calls.
- Five host JavaScript tests passed for isolation, lifecycle, locale fallback,
  placeholder validation, listeners and initial native locale configuration.
- Documentation, example assets and all relative Markdown links inside the ZIP
  were checked by the build test.
- The documented JavaScript example ran against the real host translation adapter
  in English, Portuguese and Spanish, including locale events and lifecycle cleanup.
- The broader pre-release translation review exercised English, Portuguese and
  Spanish with Playwright on isolated host data; this was a host/source review,
  not a Marketplace installation of the final 0.1.2 ZIP.

The local artifact is `dist/translator-0.1.2.zip`; its checksum is recorded in
`dist/SHA256SUMS.txt`. This validation does not claim signing, publication or online
acceptance of 0.1.2. The updated host API must be deployed with compatible modules.

## 0.1.0 — historical validation

The observations below describe the interface and release at that time. Current
language preferences are inside the table; see the current documentation.

Offline Chromium acceptance passed with the development Gravewright host and the final signed ZIP. The isolated package, database and media were removed when the test finished.

- Translator appears in Installed modules and has installation-wide activation.
- English, Brazilian Portuguese and Spanish can be selected only in internal account settings.
- Selected languages survive reloads and apply to campaigns, systems, installed modules, administration and the table shell.
- Translator is absent from per-table extension activation; no language selector appears on the table.
- Account/campaign names and protected chat content retain their original text.
- Deactivation removes the selector and restores English on reload.
- No JavaScript errors or unmapped controls were recorded on the visited pages.
- Django build validation checks complete catalog key sets, placeholders, archive contents and deterministic SHA-256 output.

The final catalog contains 2,607 entries per language. This is inventory coverage, not exhaustive screen coverage or a full linguistic review. User documents, PDFs and third-party interfaces are outside its scope. Longer machine-assisted translations may still need review.

Online Chromium acceptance also passed against the public catalog on marketplace `main` (commit `693da84`) and the GitHub v0.1.0 ZIP. The test began with an empty package database and no Translator Django authoring app. Installation used the actual Marketplace button, verified the signed record/archive, and repeated all three languages and deactivation checks. No unmapped controls were recorded on the visited pages.

Final ZIP SHA-256: `bd2f829639b5a75557b373cef48c408ebeb5e4565b6df03372eb27a7943caa29`.

Host regression validation: 279 Django tests, 62 JavaScript map model tests, and the signed-system marketplace Chromium test passed. The required host integration changes remain in the local Gravewright development checkout; they have not been published as part of the Translator repository.
