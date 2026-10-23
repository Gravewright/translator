# Translator 0.1.2

Translator supplies installation-wide language catalogs for Gravewright VTT.
English is the source language; the published 0.1.2 release has 3,012 catalog
entries for Brazilian Portuguese and Spanish. Users choose their personal interface language
inside a table's **Settings → Preferences**. The choice is saved to their account;
switching language reloads the page while preserving the table URL.

Install the signed Translator package through the Gravewright Marketplace and
activate its languages in Installed modules. Reload open pages after activation
or deactivation. No external translation service, API key or model download is
required at runtime.

## Unreleased catalog updates

The working catalogs contain 3,584 entries per language: 572 additions covering
native Translator calls, campaign preparation, Map Builder, clocks, clues, mind
maps, PDF fields and journal references. Existing catalog pairs remain unchanged;
new entries reuse reviewed host translations where available and preserve all
named and numbered parameters. The visibility-panel labels include full vision
and its mode descriptions. These source updates have not changed the published
0.1.2 signed package. See the unreleased changelog before building a local package.

## Documentation / Documentação

The release ZIP includes the complete Portuguese documentation and integration
example assets:

- [Guia de instalação, compatibilidade e solução de problemas](gravewright_translator/package/docs/README.md)
- [Referência da API para módulos e sistemas](gravewright_translator/package/docs/API.md)
- [Desenvolvimento, build, testes e distribuição](gravewright_translator/package/docs/DEVELOPMENT.md)
- [Notas da versão](gravewright_translator/package/docs/CHANGELOG.md)
- [Exemplo JavaScript](gravewright_translator/package/docs/examples/main.js) e [catálogos JSON](gravewright_translator/package/docs/examples/messages.json)
- [Validation evidence](VALIDATION.md)
- [Generation tools and attribution](THIRD_PARTY_NOTICES.md)

## Compatibility

The package declares SDK `>=1.0.0 <2.0.0`. Language catalogs require a host with
declarative language packages, installation-wide activation and account locale
preferences. Third-party integrations additionally require the updated host's
`context.i18n` / `context.api.i18n` adapter. **Installing this ZIP on an older host
does not add that JavaScript API.** Feature-detect it before using it.

The marketplace ZIP contains JSON catalogs, a manifest, a no-op JavaScript entry,
license and documentation. The Django app is for authoring/building; Python code
is never loaded from this marketplace package.

## Module integration

Register private catalogs in the activation's `start(context)` and translate using
the adapter supplied to the module or surface:

```javascript
export default {
  start({ i18n }) {
    i18n.register({
      en: { greeting: 'Welcome, {name}' },
      'pt-BR': { greeting: 'Boas-vindas, {name}' },
      es: { greeting: 'Bienvenido, {name}' },
    });
  },
  register({ register }) {
    register('actor.directory', ({ root, api }) => {
      root.setAttribute('translate', 'no');
      root.textContent = api.i18n.t('greeting', { name: 'Arin' });
    });
  },
};
```

Catalogs are isolated by module ID. Lookup falls back from exact locale to base
language, English and finally the key. The API supports named/numbered parameters,
`has()`, `number()`, `onChange()` and automatic lifetime cleanup. English entries
are mandatory; other languages may be partial with matching placeholders.
Register again on every activation. `translate="no"` protects owned UI from the
legacy DOM translator; render plain text using `textContent`.

## Build and release

From the Gravewright checkout in PowerShell, with this repository at
`data/translator-source`:

```powershell
$env:PYTHONPATH = (Resolve-Path data/translator-source).Path
$env:DJANGO_SETTINGS_MODULE = 'gravewright_translator.dev_settings'
.venv/Scripts/python.exe -X utf8 manage.py build_translator --output data/translator-source/dist
```

The deterministic build emits the ZIP, `SHA256SUMS.txt` and `coverage.json`.
See the development guide for extraction, tests and signing. Official production
releases use the Marketplace's **Sign and publish package** workflow with an exact
source commit and the protected `release-signing` environment. A local build is
neither signed nor published.

## Coverage and license

Catalog coverage is inventory coverage, not a guarantee that every possible screen
is translated. Campaign/player names, chat, PDFs and authored documents remain
unchanged. Third-party modules translate their own UI through their private API
catalogs. Some uncommon machine-assisted strings may still need linguistic review.

MIT. See `gravewright_translator/LICENSE.txt` and `THIRD_PARTY_NOTICES.md`. Translation
models are not distributed or required at runtime.
