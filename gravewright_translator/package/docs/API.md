# API de tradução para módulos e sistemas

## Disponibilidade

Módulos e sistemas recebem um adaptador vinculado ao próprio ID:

- `context.i18n` no contexto de ativação;
- `context.api.i18n` no mesmo contexto;
- `api.i18n` no contexto entregue ao renderizador de uma superfície.

Não importe o `main.js` do Translator nem use globais do host como API de um módulo.
A implementação pertence ao VTT. Pacotes de idioma fornecem os idiomas que o
usuário pode escolher; o adaptador fornece registro e consulta de traduções.
Sem pacotes de idioma ativos, o adaptador de um host compatível usa inglês.

Em hosts antigos, detecte a capacidade e apresente uma mensagem de atualização ou
use a interface original do seu módulo:

```javascript
start(context) {
  if (!context.i18n) {
    throw new Error('This module requires a Gravewright host with context.i18n.');
  }
  context.i18n.register({ en: { title: 'My module' } });
}
```

Esse trecho é um método do objeto exportado pelo módulo. Veja o exemplo completo
em [examples/main.js](examples/main.js).

## Registro e renderização

Registre os catálogos em `start(context)`, para que permaneçam disponíveis durante
a ativação do módulo. O registro é síncrono e não persiste entre carregamentos.

```javascript
export default {
  start({ i18n }) {
    i18n.register({
      en: { greeting: 'Welcome, {name}', total: '{0} characters' },
      'pt-BR': { greeting: 'Boas-vindas, {name}', total: '{0} personagens' },
      es: { greeting: 'Bienvenido, {name}', total: '{0} personajes' },
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

`actor.directory` é apenas uma superfície de exemplo; escolha a superfície
apropriada à sua integração. Ao assumir uma superfície, seu módulo também assume
sua apresentação e comportamento.

Use `translate="no"` no elemento de interface controlado pelo seu módulo para
evitar que a tradução automática legada do DOM reinterprete seus textos. Renderize
com `textContent`; `t()` não escapa HTML e não deve ser inserido em `innerHTML` com
parâmetros de usuários.

## Referência

| Membro | Resultado e comportamento |
| --- | --- |
| `i18n.locale` | String com o idioma atual, por exemplo `pt-BR`. É uma propriedade, não uma função. |
| `i18n.t(key, params = {})` | String traduzida, com substituição de parâmetros. Se não encontrar a chave, retorna a própria chave. |
| `i18n.has(key)` | Booleano indicando se há tradução em algum idioma da cadeia de fallback. Não significa tradução específica no idioma atual. |
| `i18n.number(value, options = {})` | String formatada por `Intl.NumberFormat` no idioma atual, com suas opções usuais. |
| `i18n.register(catalogs)` | Registra catálogos e retorna `dispose()`, que os remove. |
| `i18n.onChange(handler)` | Inscreve `handler(locale)` nos eventos de idioma e retorna uma função para cancelar a inscrição. |

### Chaves, parâmetros e fallback

Use chaves estáveis como `sheet.title` e `combat.next`. O inglês pode ser o texto
de fallback, sem exigir que a chave seja uma frase em inglês.

A busca tenta o idioma exato, o idioma base, o inglês e, por último, a chave. Para
`pt-BR`: `pt-BR → pt → en → key`. O adaptador de um módulo não busca textos privados
de outro módulo nem os catálogos nativos do host.

Parâmetros aceitam nomes (`{name}`, `{actor.name}`) e índices (`{0}`). O nome com
ponto é uma chave literal do objeto; não há navegação de propriedades. Valores são
convertidos para string, sem pluralização automática, ICU ou avaliação de código.
Parâmetros ausentes conservam seu marcador.

```javascript
i18n.t('greeting', { name: 'Arin' });
i18n.t('total', { 0: i18n.number(1200) });
i18n.number(0.25, { style: 'percent' });
```

### Formato de catálogo e validação

`register()` recebe um objeto `locale → objeto de mensagens`. `en` é obrigatório;
outros idiomas podem ser parciais. Cada chave traduzida precisa existir em `en`
com uma string e exatamente os mesmos marcadores, inclusive suas repetições.

Os códigos aceitos começam com 2 ou 3 letras minúsculas e podem ter subtags
alfanuméricas de 2 a 8 caracteres, como `en`, `pt-BR` e `es`. Use a grafia exata
do idioma informado pelo host; o registro não normaliza códigos.

Limites por chamada de registro:

- Até 15.000 entradas somando todos os idiomas.
- Chaves e textos não vazios, com até 12.000 caracteres cada.
- Mensagens em objetos; arrays e traduções não textuais são rejeitados.

A validação ocorre antes do registro: um catálogo inválido não deixa registro
parcial. O adaptador copia os dados; mutar o objeto original não muda o catálogo.

### Arquivos JSON

Inclua os catálogos nos arquivos do seu pacote e carregue-os com o leitor de assets:

```javascript
async start(context) {
  const catalogs = await context.assets.json('locales/messages.json');
  context.i18n.register(catalogs);
}
```

O arquivo tem o mesmo formato recebido por `register()`; veja
[examples/messages.json](examples/messages.json). Copie-o para
`locales/messages.json` no seu pacote. Esse carregamento não exige permissão de
HTTP externo. Não confunda esses catálogos privados com `manifest.locales`, que
declara idiomas de interface instaláveis e usa catálogos nativos por frase-fonte.

### Isolamento e ciclo de vida

Os catálogos são isolados por ID de módulo e compartilhados entre seus contextos
na página. Dois módulos podem usar `sheet.title` com traduções diferentes.
O adaptador fornecido ao módulo não permite escolher o namespace de outro módulo.

Vários registros do mesmo módulo podem coexistir. Dentro de cada idioma da cadeia
de fallback, o registro mais recente tem prioridade. Removê-lo restaura o anterior.
Uma tradução específica em um registro antigo tem prioridade sobre o inglês de um
registro recente, pois a escolha do idioma antecede a do registro.

O encerramento do contexto proprietário remove automaticamente seus catálogos e
listeners. Um registro feito em uma superfície dura só até o encerramento dela;
por isso, registre traduções compartilhadas no contexto de ativação. As funções
de descarte podem ser chamadas antecipadamente e mais de uma vez.

`onChange()` não chama o handler imediatamente. Renderize primeiro e inscreva o
handler se precisar acompanhar eventos em tempo de execução. A mudança de idioma
pela interface atualmente recarrega a página; não dependa de um evento antes de
uma navegação.

```javascript
const render = () => { root.textContent = api.i18n.t('greeting', { name: 'Arin' }); };
root.setAttribute('translate', 'no');
render();
api.i18n.onChange(render); // Cancelado automaticamente ao encerrar a superfície.
```

### Erros

Operações inválidas de registro, chaves não textuais em `t()` ou handlers inválidos
em `onChange()` geram `GravewrightError` com `error.code === 'invalid_data'`.
Usar o adaptador após o encerramento do contexto gera `stale_context`.
`number()` também pode lançar os erros nativos de `Intl.NumberFormat` para opções
inválidas. Não use a mensagem do erro como identificador; trate `error.code`.

## Roteiro de verificação para autores

Teste inglês, português e espanhol, ausência de uma chave no idioma atual,
parâmetros faltantes, números, conteúdo de usuário e reabertura de superfícies.
Verifique também desativação/reativação do módulo, ausência do Translator e a
presença de outro módulo com as mesmas chaves. Traduza rótulos e mensagens de
interface; preserve nomes, textos de ficha e outros dados dos usuários.
