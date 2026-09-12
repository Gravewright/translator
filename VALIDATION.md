# v0.1.0 validation

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
