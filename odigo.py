#!/usr/bin/env python2

import time
from sys import exit

from fbi import getpassword
from requestium import Session

### Login ###
login = 'rkorniic'
passwd = getpassword('~/.key/odigo.enc')
url = 'https://enregistreur.prosodie.com/odigo4isRecorder/' \
      'EntryPoint?serviceName=LoginHandler'
driver = '/usr/lib/chromium-browser/chromedriver'
s = Session(webdriver_path=driver,
            browser='chrome',
            default_timeout=15,
            webdriver_options={'arguments': ['headless']})
s.driver.get(url)
s.driver.ensure_element_by_name('mail').send_keys(login)
s.driver.ensure_element_by_name('password').send_keys(passwd)
s.driver.ensure_element_by_name('valider').click()

### Search records by date range ###
url = 'https://enregistreur.prosodie.com/odigo4isRecorder/' \
      'EntryPoint?serviceName=CriteresMessagesHandler&lang=en'
s.driver.get(url)
s.driver.ensure_element_by_name('dateDebut').send_keys('07-01-2018')
s.driver.ensure_element_by_name('heureDebut').send_keys('12:00 AM')
s.driver.ensure_element_by_name('dateFin').send_keys('07-17-2018')
s.driver.ensure_element_by_name('heureFin').send_keys('12:00 PM')
s.driver.ensure_element_by_id('button-1009').click()

### Download .MP3 file ###
s.driver.ensure_element_by_class_name('x-action-col-icon').click()
s.driver.switch_to.frame('result_frame')
time.sleep(1)
src = s.driver.ensure_element_by_id('messagePlayer').get_attribute('src')
s.transfer_driver_cookies_to_session()
r = s.get(src, stream=True)
if r.status_code == 200:
    with open('odigo.mp3', 'wb') as f:
        for chunk in r.iter_content(1024*2014):
            f.write(chunk)
else:
    exit(1)
