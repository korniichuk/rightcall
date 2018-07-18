#!/usr/bin/env python2

import time
from sys import exit

from bs4 import BeautifulSoup
from fbi import getpassword
from requestium import Session

username = 'rkorniic'
passwd = getpassword('~/.key/odigo.enc')
start_date = '07-01-2018'
start_time = '12:00 AM'
end_date = '07-01-2018'
end_time = '11:59 PM'

driver = '/usr/lib/chromium-browser/chromedriver'
s = Session(webdriver_path=driver,
            browser='chrome',
            default_timeout=15,
            webdriver_options={'arguments': ['headless']})

def login(s, username, passwd):
    """Login to www.prosodie.com with username/passwd pair and return session.
    Input:
        s -- Requestium session (required |
             type: requestium.requestium.Session);
        username -- username on www.prosodie.com (required | type: str);
        passwd -- password for username on www.prosodie.com (required |
                  type: str).
    Output:
        s -- Requestium session (required |
             type: requestium.requestium.Session).

    """

    url = 'https://enregistreur.prosodie.com/odigo4isRecorder/' \
          'EntryPoint?serviceName=LoginHandler'
    s.driver.get(url)
    s.driver.ensure_element_by_name('mail').send_keys(username)
    s.driver.ensure_element_by_name('password').send_keys(passwd)
    s.driver.ensure_element_by_name('valider').click()
    return s

def search_by_range(s, start_date=None, start_time=None, end_date=None,
                    end_time=None):
    """Search records on www.prosodie.com by date range and return session.
    Input:
        s -- Requestium session (required |
             type: requestium.requestium.Session);
        start_date -- start date (not required | type: str). Format:
                      'mm:dd:yyyy'. Example: '03-05-1991';
        start_time -- start time (not required | type: str). Example:
                      '12:00 AM';
        end_date -- end date (not required | type: str). Format:
                    'mm:dd:yyyy'. Example: '03-05-1991';
        end_time -- end time (not required | type: str). Example: '12:00 PM'.
    Output:
        s -- Requestium session (required |
             type: requestium.requestium.Session).

    """

    url = 'https://enregistreur.prosodie.com/odigo4isRecorder/' \
          'EntryPoint?serviceName=CriteresMessagesHandler&lang=en'
    s.driver.get(url)
    if start_date:
        s.driver.ensure_element_by_name('dateDebut').send_keys(start_date)
    if start_time:
        s.driver.ensure_element_by_name('heureDebut').send_keys(start_time)
    if end_date:
        s.driver.ensure_element_by_name('dateFin').send_keys(end_date)
    if end_time:
        s.driver.ensure_element_by_name('heureFin').send_keys(end_time)
    s.driver.ensure_element_by_id('button-1009').click()
    return s

def search_by_ref(s, ref):
    """Search record on www.prosodie.com by ref number and return session.
    Input:
        s -- Requestium session (required |
             type: requestium.requestium.Session);
        ref -- ref number (required | type: str). Example: '3905beTOd10339'.
    Output:
        s -- Requestium session (required |
             type: requestium.requestium.Session).

    """

    url = 'https://enregistreur.prosodie.com/odigo4isRecorder/' \
          'EntryPoint?serviceName=CriteresMessagesHandler&lang=en'
    s.driver.get(url)
    s.driver.ensure_element_by_name('refEr').send_keys(ref)
    s.driver.ensure_element_by_id('button-1009').click()
    return s

def download_mp3(s, path=None):
    """Download .MP3 file from www.prosodie.com page and return session.
    Input:
        s -- Requestium session (required |
             type: requestium.requestium.Session);
        path -- mp3 file absolute path (not required | type: str).
    Output:
        s -- Requestium session (required |
             type: requestium.requestium.Session).

    """

    s.driver.ensure_element_by_class_name('x-action-col-icon').click()
    s.driver.switch_to.frame('result_frame')
    time.sleep(1)
    # Get ref number
    soap = BeautifulSoup(s.driver.page_source, 'lxml')
    ref = soap.findAll('div', class_='x-grid-cell-inner')[1].text
    # Get URL of .MP3 file
    src = s.driver.ensure_element_by_id('messagePlayer').get_attribute('src')
    # Selenium --> Requests
    s.transfer_driver_cookies_to_session()
    # Download
    r = s.get(src, stream=True)
    if path == None:
        path = '%s.mp3' % ref
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024*2014):
                f.write(chunk)
    else:
        return 1
    # Requests --> Selenium
    s.transfer_session_cookies_to_driver()
    return s

### Download .MP3 file by 3905beTOd10339 ref number ###
s = login(s, username, passwd)
s = search_by_ref(s, '3905beTOd10339')
result = download_mp3(s)
if result != 1:
   s = result
else:
   exit(1)
