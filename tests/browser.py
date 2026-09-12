"""Offline/online acceptance through Chromium, with disposable host DB and media.
Run with the Gravewright Python environment: tests/browser.py --host ../gravewright
Offline reads dist/catalog.json and dist/translator-0.1.0.zip; online fetches GitHub.
"""
import argparse,json,os,subprocess,sys,tempfile,time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import expect,sync_playwright

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--host',type=Path,required=True)
parser.add_argument('--keys',type=Path,required=True)
parser.add_argument('--online',action='store_true')
parser.add_argument('--catalog',default='https://raw.githubusercontent.com/Gravewright/marketplace/main/gravewright.marketplace.json')
args=parser.parse_args();host=args.host.resolve()
sys.path.insert(0,str(host/'tests/e2e'))
from https import free_port
seed='''
import django,json,os
from pathlib import Path
django.setup()
from django.conf import settings
from django.test import Client
from gravewright.accounts.models import User
from gravewright.campaigns.models import Campaign,Membership,Onboarding
from gravewright.modules.models import Package
assert not Package.objects.exists()
assert 'gravewright_translator' not in settings.INSTALLED_APPS or os.environ['TEST_OFFLINE']=='1'
u=User.objects.create_user('translator@test.local','translator-password-123',name='Settings',role='owner')
c=Campaign.objects.create(owner=u,name='Settings',description='Save language')
m=Membership.objects.create(campaign=c,user=u,role='gm');Onboarding.objects.create(membership=m,dismissed=True)
if os.environ['TEST_OFFLINE']=='1':
 from gravewright.modules.packages import host
 root=Path(os.environ['TRANSLATOR_SOURCE'])
 host().install(json.loads((root/'dist/catalog.json').read_text())[0],(root/'dist/translator-0.1.0.zip').read_bytes())
client=Client();client.force_login(u)
print(json.dumps({'cookie':{'name':settings.SESSION_COOKIE_NAME,'value':client.session.session_key},'campaign':str(c.pk)}))
'''
mode='online' if args.online else 'offline'
report={'mode':mode,'checks':[],'unmappedControls':{}}
with tempfile.TemporaryDirectory(prefix='translator-'+mode+'-') as tmp:
 directory=Path(tmp)
 env={**os.environ,'DJANGO_SETTINGS_MODULE':'config.settings' if args.online else 'gravewright_translator.dev_settings',
      'PYTHONPATH':str(host) if args.online else str(ROOT)+os.pathsep+str(host),
      'DJANGO_DEBUG':'true','DJANGO_ALLOWED_HOSTS':'127.0.0.1,localhost,testserver',
      'GRAVEWRIGHT_DATABASE':str(directory/'db.sqlite3'),'GRAVEWRIGHT_MEDIA_ROOT':str(directory/'media'),
      'GRAVEWRIGHT_PUBLIC_ORIGIN':'','DJANGO_SECURE_COOKIES':'false','GRAVEWRIGHT_REDIS_URL':'',
      'TRUSTED_PROXIES':'','GRAVEWRIGHT_RELEASES_REPOSITORY':'',
      'GRAVEWRIGHT_MARKETPLACE_URL':args.catalog,'GRAVEWRIGHT_MARKETPLACE_KEYS_FILE':str(args.keys.resolve()),
      'TRANSLATOR_SOURCE':str(ROOT),'TEST_OFFLINE':'0' if args.online else '1'}
 subprocess.run([sys.executable,'manage.py','migrate','--noinput'],cwd=host,env=env,check=True,stdout=subprocess.DEVNULL)
 state=json.loads(subprocess.check_output([sys.executable,'-c',seed],cwd=host,env=env,text=True))
 address='127.0.0.1:'+str(free_port());base='http://'+address
 with (directory/'server.log').open('w') as log:
  server=subprocess.Popen([sys.executable,'manage.py','runserver',address,'--noreload'],cwd=host,env=env,stdout=log,stderr=log)
  try:
   for _ in range(100):
    try:urlopen(base,timeout=1).close();break
    except OSError:time.sleep(.1)
   with sync_playwright() as pw:
    browser=pw.chromium.launch();context=browser.new_context();context.add_cookies([{**state['cookie'],'url':base}])
    page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base+'/inside?section=settings');expect(page.locator('[data-language-settings]')).to_have_count(0)
    if args.online:
     assert page.request.get(base+'/api/module-packages').json()==[]
     page.goto(base+'/inside?section=marketplace')
     card=page.locator('.module-catalog__card').filter(has=page.get_by_role('heading',name='Translator',exact=True))
     expect(card).to_be_visible(timeout=30000)
     card.locator('[data-action=install]').click()
     expect(card.locator('[data-status]')).to_have_text('Installed',timeout=60000)
     report['checks'].append('installed through marketplace using public signed catalog and release URL')
    page.goto(base+'/inside?section=addons')
    expect(page.locator('.module-catalog__card h3')).to_have_text('Translator',timeout=15000)
    page.locator('[data-action=global-activation]').click()
    page.wait_for_function("document.querySelector('[data-action=global-activation]')?.textContent.includes('Deactivate')")
    report['checks'].append('listed in installed modules; owner activates installation-wide')
    for locale,title,save in [('pt-BR','Configurações','Salvar idioma'),('es','Configuración','Guardar idioma'),('en','Settings','Save language')]:
     page.goto(base+'/inside?section=settings')
     expect(page.locator('[name=locale] option')).to_have_count(3)
     page.locator('[name=locale]').select_option(locale)
     page.locator('[data-language-settings] button').click()
     expect(page.locator('html')).to_have_attribute('lang',locale,timeout=15000)
     expect(page.locator('.account-settings h1')).to_have_text(title)
     expect(page.locator('[data-language-settings] button')).to_have_text(save)
     expect(page.locator('input[name=name]')).to_have_value('Settings')
     page.reload();expect(page.locator('html')).to_have_attribute('lang',locale,timeout=15000)
     for section in ['campaigns','systems','addons','administration']:
      page.goto(base+'/inside?section='+section)
      expect(page.locator('html')).to_have_attribute('lang',locale,timeout=15000)
      if section=='campaigns':
       expect(page.locator('.gw-campaign h2')).to_have_text('Settings')
      report['unmappedControls'][locale+'/'+section]=page.evaluate('window.gravewrightTranslator?.missing() || []')
     page.goto(base+'/game/'+state['campaign'])
     expect(page.locator('html')).to_have_attribute('lang',locale,timeout=15000)
     expect(page.locator('[name=locale]')).to_have_count(0)
     expect(page.locator('[data-table-modules] .module-marketplace__header')).to_have_count(1)
     expect(page.locator('[data-table-modules] .module-marketplace__item')).to_have_count(0)
     # User-owned text inside excluded DOM must retain the exact original.
     page.evaluate("document.body.insertAdjacentHTML('beforeend','<div class=chat-message><button>Settings</button></div>')")
     expect(page.locator('.chat-message button').last).to_have_text('Settings')
     report['unmappedControls'][locale+'/table']=page.evaluate('window.gravewrightTranslator?.missing() || []')
     (ROOT/'test-results').mkdir(exist_ok=True)
     page.screenshot(path=str(ROOT/'test-results'/f'{mode}-{locale}-table.png'))
    page.goto(base+'/inside?section=addons');page.locator('[data-action=global-activation]').click()
    page.wait_for_function("document.querySelector('[data-action=global-activation]')?.textContent.includes('Activate')")
    page.goto(base+'/inside?section=settings');expect(page.locator('[name=locale]')).to_have_count(0)
    expect(page.locator('html')).to_have_attribute('lang','en')
    assert not errors,errors
    report['checks']+=['three languages persist across reloads and pages','selector only in internal account settings','account and campaign names and protected chat remain unchanged','deactivation removes selector and restores English','no browser JavaScript errors']
    browser.close()
  except Exception:
   log.flush();print((directory/'server.log').read_text()[-1500:]);print('ERRORS',errors);raise
  finally:
   server.terminate();server.wait(timeout=15)
 report['checks'].append('offline package/database/media removed' if not args.online else 'fresh host without Django authoring app or offline package')
(ROOT/'test-results'/f'{mode}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
