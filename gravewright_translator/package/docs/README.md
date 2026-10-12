# Translator 0.1.2

O Translator fornece catálogos de tradução para o Gravewright VTT. Inglês é o idioma
de origem; esta versão inclui português do Brasil (`pt-BR`) e espanhol (`es`), com
3.012 entradas em cada catálogo de autoria. Os idiomas disponíveis podem ser
ampliados por pacotes de idioma compatíveis com o host.

## Documentação

- [API para módulos e sistemas](API.md): referência, exemplos, ciclo de vida e erros.
- [Desenvolvimento e distribuição](DEVELOPMENT.md): catálogos, build, testes e assinatura.
- [Notas da versão](CHANGELOG.md): mudanças e compatibilidade.
- [Exemplo de integração](examples/main.js) e [catálogos do exemplo](examples/messages.json).

## Instalação e uso

1. Configure o Marketplace oficial no Gravewright e instale o Translator assinado.
2. Na administração dos módulos instalados, ative os idiomas do Translator.
   A ativação vale para a instalação; não depende de ativar o módulo em cada mesa.
3. Dentro de uma mesa, abra **Configurações → Preferências → Idioma da interface**.
4. Selecione **English**, **Português (Brasil)** ou **Español**.

A escolha é pessoal e fica salva na conta. Ela se aplica à interface do VTT,
inclusive nas próximas sessões. A mudança recarrega a página preservando a URL da
mesa. Não altera o idioma dos demais jogadores.

Ao desativar o Translator, os idiomas fornecidos por ele deixam de estar
disponíveis. Recarregue as páginas abertas para voltar ao inglês quando não houver
outro pacote fornecendo o idioma escolhido.

## Compatibilidade e arquitetura

O manifesto declara SDK `>=1.0.0 <2.0.0`. Para os catálogos, o host precisa oferecer
pacotes declarativos de idioma, ativação global e preferência de idioma por conta.
Para a nova integração de outros módulos, também precisa oferecer
`context.i18n` / `context.api.i18n`.

**A API é implementada pelo host atualizado em conjunto com esta versão.** Instalar
somente o ZIP 0.1.2 em um VTT antigo não adiciona a API JavaScript. Autores devem
verificar a presença de `context.i18n` antes de usá-la; consulte [API.md](API.md).

O pacote de Marketplace contém manifesto, entrada JavaScript sem efeitos de mesa,
catálogos JSON, licença e esta documentação. O aplicativo Django serve para autoria
e build; seu código Python não é distribuído no ZIP de Marketplace. Não há serviço
de tradução externo, chave de API ou download de modelos em tempo de execução.

## O que é traduzido

Os catálogos cobrem textos nativos extraídos de templates, dicionários e controles
JavaScript. Esta revisão inclui combate, régua, desenho, efeitos, áudio, cartas,
quadro de missões, permissões, controles de janela, PDF System e dados.

Nomes de personagens e mesas, mensagens de chat, conteúdo de PDFs, diários e textos
criados pelos usuários conservam o conteúdo original. Módulos e sistemas de
terceiros podem traduzir sua própria interface registrando catálogos privados na API.
O Translator não traduz automaticamente regras ou documentos importados.

A contagem de entradas indica cobertura do inventário, não de todas as telas
possíveis. Parte dos catálogos tem origem em tradução assistida por máquina;
frases incomuns podem precisar de revisão. Informe problemas com o texto original,
idioma, tela e versão do VTT.

## Resolução de problemas

| Sintoma | Verificação |
| --- | --- |
| Seletor de idioma ausente | Confirme a ativação global e a compatibilidade do host; recarregue a página. |
| Um módulo continua em inglês | Confirme que ele registra traduções para o idioma selecionado. |
| `context.i18n` ausente | Atualize o host; o ZIP do Translator sozinho não implementa a API. |
| Texto mostra `sheet.title` | A chave não foi registrada ou o contexto que possuía o catálogo foi encerrado. |
| `{name}` aparece no texto | Passe o parâmetro correspondente para `t()`. |
| Tradução mudou após atualizar | Recarregue páginas antigas para carregar os novos catálogos. |
| Instalação rejeita o ZIP local | Builds locais não têm assinatura de Marketplace; publique pelo fluxo de assinatura. |

## Licença

Translator: MIT, conforme `LICENSE.txt` na raiz do ZIP. A atribuição das ferramentas
de geração está em `THIRD_PARTY_NOTICES.md` no repositório de autoria. Modelos não
são distribuídos neste pacote.
