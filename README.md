# Translator

Translator adds installation-wide English, Brazilian Portuguese and Spanish interface options to Gravewright VTT. The owner activates it in **Installed modules**. Each user then chooses **Settings → Interface language**. No language selector appears in table settings and the module cannot be activated per campaign.

**Preview compatibility:** v0.1.0 requires the Gravewright host changes that implement `manifest.locales`, global package activation and account locale preferences. It does not work on older hosts that only support per-table JavaScript modules. Those integration changes are currently in the development checkout; this release is a prerelease, not a declaration of compatibility with every SDK 1.0 host.

## Install

Configure the signed [Gravewright Marketplace](https://github.com/Gravewright/marketplace), install **Translator**, open **Installed modules**, and select **Activate languages**. Users choose English, Português (Brasil), or Español in their internal account settings. The selection survives reloads. Disabling Translator removes the selector and restores English on subsequent page loads. Already open pages should be reloaded.

The Django app is the authoring/build application. The marketplace artifact contains JSON catalogs, a manifest and a no-op module entry; the host never imports Python downloaded from a marketplace ZIP. There are no translation APIs, API keys, or model downloads at runtime.

## Build offline

Use the Gravewright Python environment and this repository on `PYTHONPATH`:

```sh
cd ../gravewright
PYTHONPATH=../translator DJANGO_SETTINGS_MODULE=gravewright_translator.dev_settings \
  uv run --locked python manage.py build_translator --output ../translator/dist
```

`build_translator` checks matching source sets and placeholders, then writes a deterministic ZIP, SHA-256 checksum and catalog coverage report. To extract an updated source inventory, run `extract_translator --source . --output ../translator/source-inventory.json` with the same environment. Update all three catalog files and review translations before releasing.

Sign the completed archive using `scripts/sign_release.py --key /outside/repository/key.pem --archive dist/translator-0.1.0.zip --output dist/catalog.json`. The signing environment needs `cryptography`. Keep the private key outside repositories. The public key belongs in the trusted marketplace configuration.

## Validation

```sh
../gravewright/.venv/bin/python tests/browser.py --host ../gravewright --keys ../marketplace/trusted-keys.json
../gravewright/.venv/bin/python tests/browser.py --host ../gravewright --keys ../marketplace/trusted-keys.json --online
```

The offline test loads the signed local ZIP into an isolated host using the Django authoring app. Its database and media are removed afterward. The online test starts with a fresh database, no offline package and no Translator Django app in `INSTALLED_APPS`; Chromium installs the actual public release through the marketplace and repeats the language checks. Reports/screenshots go to ignored `test-results/`.

## Coverage and limits

The catalogs cover extracted native message dictionaries, static template labels, and recognized browser UI literals. `source-inventory.json` maps source phrases to files; `dist/coverage.json` measures catalog completeness, **not proof that every possible screen or dynamic message is translated**. The browser report records unmatched controls on visited pages.

Campaign names, player names, chat messages, editable journals, PDF content, imported rules, third-party module content and other user-authored data retain their original text. Generated sentences and UI added after this inventory may need additional catalog entries. Initial catalogs use offline machine assistance with manually reviewed common controls; longer or uncommon phrases may still need linguistic review. Report untranslated or incorrect UI strings with their source text and screen.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for generation tools/model attribution. Models are not distributed or required at runtime.
