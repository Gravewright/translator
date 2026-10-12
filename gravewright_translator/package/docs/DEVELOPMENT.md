# Desenvolvimento e distribuição

## Estrutura do repositório de autoria

| Caminho | Função |
| --- | --- |
| `gravewright_translator/catalogs/en.json` | Inventário de frases-fonte em inglês. |
| `gravewright_translator/catalogs/pt-BR.json` e `es.json` | Traduções nativas. |
| `gravewright_translator/package/manifest.json` | Identidade, SDK, versão e idiomas. |
| `gravewright_translator/package/main.js` | Entrada declarativa sem efeitos na mesa. |
| `gravewright_translator/package/docs/` | Documentação e exemplos incluídos no ZIP. |
| `source-inventory.json` | Origem das frases extraídas no VTT. |
| `scripts/sign_release.py` | Assinatura de um ZIP já construído. |

O inglês é o fallback do host; o ZIP inclui os catálogos de português e espanhol.
Os catálogos nativos usam frases-fonte como chaves. Catálogos privados de outros
módulos podem usar IDs semânticos, conforme [API.md](API.md).

## Pré-requisitos

Use Python 3.12 ou superior e o ambiente Django do checkout do Gravewright.
Adicione o repositório Translator ao `PYTHONPATH`. Os comandos abaixo assumem
PowerShell, executados na raiz do VTT, com Translator em `data/translator-source`.
Nenhum comando de build precisa acessar banco de dados ou rede.

```powershell
$env:PYTHONPATH = (Resolve-Path data/translator-source).Path
$env:DJANGO_SETTINGS_MODULE = 'gravewright_translator.dev_settings'
.venv/Scripts/python.exe -X utf8 manage.py build_translator --output data/translator-source/dist
```

Em Linux/macOS, ajuste o caminho do Python para `.venv/bin/python` e use as
atribuições de ambiente do seu shell.

## Atualizar catálogos

```powershell
.venv/Scripts/python.exe -X utf8 manage.py extract_translator --source . --output data/translator-source/source-inventory.json
```

A extração produz um inventário de candidatos; não sobrescreve as traduções.
Revise quais strings são interface e atualize os três catálogos com as mesmas
chaves. Preserve espaços significativos e marcadores como `{name}` e `{0}`.
Não traduza nomes de usuários, conteúdo de documentos ou identificadores técnicos.

Para adicionar um idioma nativo nesta implementação, inclua seu JSON em `catalogs/`,
adicione nome e caminho em `manifest.locales` e atualize a lista de idiomas em
`build_translator.py` e os testes. A lista de build atual é explicitamente
`pt-BR` e `es`; editar apenas o manifesto não inclui um novo catálogo no ZIP.

## Versões e artefatos

Mantenha a mesma versão em `pyproject.toml`, `gravewright_translator/__init__.py`
e `package/manifest.json`. Atualize as notas e os guias antes de construir.

O build verifica chaves, textos e marcadores e produz:

- `translator-<versão>.zip`: pacote instalável após o processo de assinatura;
- `SHA256SUMS.txt`: hash SHA-256 do ZIP;
- `coverage.json`: entradas, traduções ausentes e textos iguais à fonte por idioma.

Entradas iguais à fonte podem ser nomes próprios ou termos técnicos, mas também
podem indicar traduções pendentes. O relatório não atesta a qualidade linguística.

A ordenação dos arquivos, timestamp e permissões do ZIP são fixados para obter
saída repetível com o mesmo conteúdo e ambiente de compressão. O pacote contém
somente assets permitidos; nenhum código Python do aplicativo de autoria é enviado.
Mantenha `.env`, chaves e dados privados fora dos arquivos de pacote/documentação.

## Testes

Na raiz do repositório Translator, usando o Python do VTT:

```powershell
../../.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p test_build.py
```

O teste reconstrói o ZIP duas vezes, compara bytes e checksum, confere manifesto,
catálogos e documentação. No checkout do VTT, execute também:

```powershell
.venv/Scripts/python.exe -X utf8 scripts/audit_translations.py --catalogs data/translator-source/gravewright_translator/catalogs
.venv/Lib/site-packages/playwright/driver/node.exe --test tests/modules/i18n.test.mjs tests/modules/native-localization.test.mjs
```

Para aceitação por Chromium, na raiz do Translator:

```powershell
../../.venv/Scripts/python.exe -X utf8 tests/browser.py --host ../.. --keys CAMINHO/trusted-keys.json
```

O teste cria banco e mídia temporários e instala o ZIP local. `--online` testa a
versão **já publicada** no Marketplace, não o artefato local novo. Os relatórios
ficam em `test-results/`. Antes de reutilizar esse teste, confira seus seletores:
a interface de preferências mudou desde sua versão inicial.

Teste também as superfícies do módulo em cada idioma e confirme que textos de
usuários permanecem intactos. A evidência de validação de cada release fica em
`VALIDATION.md` no repositório; não confunda relatórios antigos com testes novos.

## Assinar e publicar

O build local não publica nada nem gera uma assinatura confiável. A publicação
oficial ocorre no workflow **Sign and publish package** do repositório
[Gravewright Marketplace](https://github.com/Gravewright/marketplace), selecionando
`translator` e o commit exato do código-fonte. O ambiente protegido
`release-signing` fornece a chave. Os artefatos são disponibilizados em
[releases do Marketplace](https://github.com/Gravewright/marketplace/releases).

Para uma distribuição independente com sua própria chave confiável:

```powershell
../../.venv/Scripts/python.exe -X utf8 scripts/sign_release.py --key CAMINHO_EXTERNO/key.pem --key-id SUA_CHAVE --archive dist/translator-0.1.2.zip --output dist/catalog.json
```

Configure a chave pública no host e um endereço HTTPS real usando `--download`
quando não hospedar no Marketplace oficial. Nunca coloque a chave privada no
repositório ou ZIP. O catálogo assinado contém ID, versão, compatibilidade, URL,
checksum e assinatura; ele é um artefato separado. Não modifique o ZIP após assinar.
As categorias padrão são Tradução, Idiomas e Interface; `--tag` permite substituí-las.
