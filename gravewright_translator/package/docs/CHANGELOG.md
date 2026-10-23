# Histórico

## 0.1.3

- 572 entradas adicionadas aos catálogos de inglês, português e espanhol, agora
  com 3.584 chaves iguais por idioma, preservando os 3.012 pares anteriores.
- Sincronização de textos nativos revisados do host para preparação de campanha,
  Map Builder, relógios, pistas, mapas mentais, PDF e referências de diários.
- Rótulos e descrições do painel de visibilidade, incluindo visão completa.
- Preservação de marcadores nomeados e numéricos e dos limites nas mensagens.
- Extração de chamadas `t(...)` e `.t(...)`, inclusive rótulos com parâmetros.

A tradução do título com ícone e das mensagens dinâmicas do painel exige
também a correção correspondente no host; alterar só o catálogo não muda esse código.

## 0.1.2

- Revisão de 258 textos de interface em português e espanhol.
- Catálogos de autoria com 3.012 entradas por idioma e as mesmas chaves.
- Extração ampliada para chamadas de tradução nativas, com caminhos de inventário
  normalizados e exclusão de testes e bibliotecas de terceiros.
- Validação de parâmetros nomeados e numéricos no build.
- Documentação da integração de módulos e sistemas por `context.i18n` e
  `context.api.i18n`, acompanhada de exemplos JavaScript e JSON.
- Guia de uso, referência da API, desenvolvimento e histórico incluídos no ZIP.

A API de integração e as correções do carregamento inicial de idioma, fallback e
proteção de conteúdo dos usuários são mudanças do **host**, preparadas junto com
esta revisão. O ZIP oferece os catálogos e a documentação; sua instalação não
adiciona essas capacidades a versões antigas do VTT. Veja [README.md](README.md).

## 0.1.1

Traduções revisadas para permissões de documentos, compartilhamento, referências
de mapas, controles de janela, atualização e remoção de pacotes e mensagens do
Runner. Compatibilidade com ativação global e preferências pessoais de idioma.

## 0.1.0

Versão inicial dos catálogos de português do Brasil e espanhol, com aplicativo
Django de autoria, build determinístico e distribuição assinada via Marketplace.
