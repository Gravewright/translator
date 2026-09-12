# Translation generation

Initial catalog drafts were generated locally with CTranslate2 and SentencePiece, then common interface controls were reviewed in `scripts/reviewed.json`. No player data was used.

- Portuguese: [Argos Translate EN–PT 1.5](https://huggingface.co/cnmoro/ArgosTranslate-EN-PT), an Argos/OpenNMT translation model. See [Argos Translate](https://github.com/argosopentech/argos-translate).
- Spanish: [CTranslate2 conversion by Rohan Saxena](https://huggingface.co/rohanksaxena/opus-mt-en-es) of [Helsinki-NLP/opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es), CC-BY-4.0.
- [CTranslate2](https://github.com/OpenNMT/CTranslate2), MIT; [SentencePiece](https://github.com/google/sentencepiece), Apache-2.0.

Models and tokenizers are not included in the Django app or marketplace release. Catalogs are editable translation data. Machine-assisted output is not certified linguistic coverage.
