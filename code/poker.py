
# Python Script to automatically Poke people on facebook
# By Sebin Thomas
# USE AT YOUR OWN RISK
# It was written in a Hurry so no error handling whatsoever and there may be a zillion Bugs
# And it's not Safe 
# THOSE WHO USE THIS CODE ARE DOING SO IN THEIR OWN RISK AND THE AUTHOR 
# IS NOT ACCOUNTABLE FOR ANY DAMAGE WHATSOEVER
# Usage : poke.py Username password
import argparse
import contextlib
import urllib2
from BeautifulSoup import BeautifulSoup
import sys
import requests
import time
import logbook

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, help="Your Facebook Username")
parser.add_argument('-p', '--password', required=True, help="Your Facebook Password")
parser.add_argument('-t', '--two-step', required=False, 
                    help="Your one time use Facebook Two Step Verification Code")
parser.add_argument('-l', '--log-level', default='INFO')
args = parser.parse_args()

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1


#logging.basicConfig() 
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

log = logbook.Logger("Poker")

FORMAT_STRING = u' '.join([
    '{record.level_name[0]}',
    '[{record.time:%Y-%m-%d %H:%M:%S.%f}]',
    '[{record.channel}:{record.func_name}:{record.lineno}]',
    '[{record.extra[trace_id]}/{record.extra[request_id]}]',
    '{record.message}',
])

Session = requests.Session()

@contextlib.contextmanager
def logging_handler(level='INFO'):
    handler = logbook.StreamHandler(
        sys.stdout,
        format_string=FORMAT_STRING,
        level=level,
        bubble=False,
    )
    with logbook.NullHandler(), handler:
        yield

def handle_login_response(r):
    log.debug("Handle Login Response")
    if "Remember Browser" in r.text:
        remember_browser(r)
        return
    
    if "New! Log In Faster" in r.text:
        login_faster(r)
        return
    
    if "Review recent login" in r.text:
        review_login(r)
        return
    
    if "Enter Security Code to Continue" in r.text:
        two_step(r)
        return
    
    if "Log Out" in r.text:
        log.info("Login Success")
        return
    
    log.critical("Login Failure")
    print r.text
    sys.exit()

def two_step(r):
    log.info("2 step Verify")
    if args.two_step is None:
        log.critical("Two Step Verification Code is required, but was not defined")
        sys.exit()
    soup = BeautifulSoup(r.text)
    url = "https://m.facebook.com" + soup.find('form').get('action')
    data = {
        'lsd': soup.find('input', {'name': 'lsd'}).get('value'),
        'charset_test': soup.find('input', {'name': 'charset_test'}).get('value'), 
        'codes_submitted': soup.find('input', {'name': 'codes_submitted'}).get('value'), 
        'nh': soup.find('input', {'name': 'nh'}).get('value'), 
        'submit[Submit Code]': 'Submit Code'
        
    }
    
    data["approvals_code"] = args.two_step

    r = Session.post(url, data=data)
    r.raise_for_status()
    
    handle_login_response(r)

def login_faster(r):
    log.info("Login Faster")
    soup = BeautifulSoup(r.text)
    URL = "https://m.facebook.com/login/device-based/update-nonce/"
    
    data = {
        'fb_dtsg': soup.find('input', {'name': 'fb_dtsg'}).get('value'),
        'charset_test': soup.find('input', {'name': 'charset_test'}).get('value'), 
        'flow': soup.find('input', {'name': 'flow'}).get('value'), 
        'next': ''
        
    }
    
    r = Session.post(url, data=data)
    r.raise_for_status()
    
    handle_login_response(r)
    
def review_login(r):
    log.info("Review Recent Login")
    soup = BeautifulSoup(r.text)
    URL = "https://www.facebook.com/checkpoint/"
    
    data = {
        'lsd': soup.find('input', {'name': 'lsd'}).get('value'),
        'charset_test': soup.find('input', {'name': 'charset_test'}).get('value'), 
        'nh': soup.find('input', {'name': 'nh'}).get('value'), 
        'submit[Continue]': 'Continue'
        
    }
    
    r = Session.post(URL, data=data)
    r.raise_for_status()
    
    data = {
        'lsd': soup.find('input', {'name': 'lsd'}).get('value'),
        'charset_test': soup.find('input', {'name': 'charset_test'}).get('value'), 
        'nh': soup.find('input', {'name': 'nh'}).get('value'), 
        'submit[This is Okay]': 'This is Okay'
        
    }
    
    r = Session.post(URL, data=data)
    r.raise_for_status()
    
    handle_login_response(r)
    
def remember_browser(r):
    log.info("Remember Browser")
    soup = BeautifulSoup(r.text)
    url = "https://m.facebook.com/login/checkpoint/"
    data = {
        'lsd': soup.find('input', {'name': 'lsd'}).get('value'),
        'charset_test': soup.find('input', {'name': 'charset_test'}).get('value'), 
        'name_action_selected': "save_device",
        'nh': soup.find('input', {'name': 'nh'}).get('value'), 
        'submit[Continue]': 'Continue'
        
    }
    
    r = Session.post(url, data=data)
    r.raise_for_status()
    
    handle_login_response(r) 

def login():
    log.info("Login")
    r = requests.get('https://m.facebook.com/')
    soup = BeautifulSoup(r.text)
    data = {
        'lsd': soup.find('input', {'name': 'lsd'}).get('value'),
        'charset_test': soup.find('input', {'name': 'charset_test'}).get('value'), 
        'version': soup.find('input', {'name': 'version'}).get('value'),
        'ajax': soup.find('input', {'id': 'ajax'}).get('value'),
        'width': soup.find('input', {'id': 'width'}).get('value'),
        'pxr': soup.find('input', {'id': 'pxr'}).get('value'),
        'gps': soup.find('input', {'id': 'gps'}).get('value'),
        'dimensions': soup.find('input', {'id': 'dimensions'}).get('value'),
        'li': soup.find('input', {'name': 'li'}).get('value'),
        'm_ts': soup.find('input', {'name': 'm_ts'}).get('value'),
    }
    data["email"] = args.username
    data["pass"] = args.password
    
    url = soup.find('form').get('action')    
    r = Session.post(url, data=data)
    
    r.raise_for_status()
    
    handle_login_response(r)

def get_pokes():
    log.info("Get Pokes")
    
    URL = "https://m.facebook.com/pokes/"
    r = Session.get(URL)
    r.raise_for_status()
    
    soup = BeautifulSoup(r.text)
    
    poke_area = soup.find("div", {"id":"poke_area"})
    
    out = []

    for element in poke_area:
        if "poked you" in element.text:
            poke_url = element.find("a", {"class":"bz y z bb"}).get("href")
            user_info_element = element.find("div", {"class":"bw"})
            user_name = user_info_element.text.split("poked you")[0]
            
            out.append(
                {
                    "name": user_name,
                    "poke_url": poke_url
                }
            )
            
    return out

def poke(user):
    log.info("Poking " + user["name"])
    URL = "https://m.facebook.com" + user["poke_url"]
    r = Session.get(URL)
    r.raise_for_status()

def main():
    log.info('Starting')
    login()
    while 1:
        for user in get_pokes():
            poke(user)
        log.info("Waiting")
        time.sleep(2)

 

if __name__=="__main__":
    with logging_handler(args.log_level):
        main()