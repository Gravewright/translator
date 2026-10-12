// Copy messages.json to locales/messages.json in your own module package.
export default {
  async start(context) {
    if (!context.i18n) {
      throw new Error('This module requires a Gravewright host with context.i18n.');
    }
    context.i18n.register(await context.assets.json('locales/messages.json'));
  },
  register({ register }) {
    register('actor.directory', ({ root, api }) => {
      root.setAttribute('translate', 'no');
      const heading = document.createElement('h2');
      const greeting = document.createElement('p');
      root.replaceChildren(heading, greeting);
      const render = () => {
        heading.textContent = api.i18n.t('sheet.title');
        greeting.textContent = api.i18n.t('sheet.greeting', { name: 'Arin' });
      };
      render();
      api.i18n.onChange(render);
    });
  },
};
