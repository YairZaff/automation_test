
# -*- coding: utf-8 -*-

'''

chrome webdrive version 79.0.3945.36 win32

https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/

'''

from selenium import webdriver                                                 #driver for browser
from selenium.webdriver.common.keys import Keys                                #allows to send keys by value
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities #browser settings
from selenium.webdriver.support.ui  import WebDriverWait                       #waiting for an event to occur
from selenium.webdriver.support  import expected_conditions as EC              #exception conditions 
from selenium.common.exceptions  import TimeoutException                       

import time
import threading
import datetime
import sys


###############################
### Cruesoe Proxy Settings ####
###############################

crusoe_login_url = "X" # 
crusoe_proxy_host_port = "host:port" 
crusoe_proxy_exclusions = "Y"
crusoe_hub_url = "http://IP:PORT/wd/hub"
test_cycles_per_browser = sys.maxsize

DEFAULT_DELAY = 5

def msg(text):
    now = datetime.datetime.now()
    if threading.current_thread() is threading.main_thread():
        print ("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] " + text)
    else:
        print("[" + now.strftime("%Y-%m-%d %H:%M:%S") + " Thread:" + str(threading.current_thread().threadID) + " User:" + threading.current_thread().userCredentials["username"] + "] " + text)

input_list = ["hello","שלום","1",""]

class Tester():
    def __init__(self, username, password):
        self.remote_hub_url = crusoe_hub_url 
        self.proxy_host_port = crusoe_proxy_host_port
        self.proxy_exclusions = crusoe_proxy_exclusions
        self.success=0
        self.fail=0
        msg ("Connecting to web driver on hub: " + self.remote_hub_url)
        #webdriver = self.connect_remote_chrome_webdriver_with_proxy(self.remote_hub_url, self.proxy_host_port, self.proxy_exclusions)
        webdriver = self.connect_my_driver() # i dont have access to crusoe's proxy
        self.time_start = str(int(time.time()))
        try:
            self.test_cases(webdriver,input_list)
            print("total tests: ",(self.success+self.fail), "failed: ",self.fail)
        finally:
            webdriver.quit()

    def connect_remote_chrome_webdriver_with_proxy(self, remote_hub_url, proxy_host_port, proxy_exclusions):
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=%s' % proxy_host_port)
        options.add_argument('--proxy-bypass-list=%s' % proxy_exclusions.replace(',',';'))
        options.add_argument('--ignore-certificate-errors')
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = { 'browser':'ALL' }
        driver = webdriver.Remote(
            command_executor=remote_hub_url,
            options=options,
            desired_capabilities=d)
        return driver

    def connect_my_driver(self):
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = { 'browser':'ALL' }
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=1")
        driver = webdriver.Chrome(desired_capabilities=d,options=options)
        return driver

    def login_to_crusoe(self, driver, crusoe_url, username, password):
        if not crusoe_url:
            msg("login url not definied, skipping login")
            return
        url = crusoe_url.replace("//", "//" + username + ":" + password + "@")
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        crusoecontent = wait.until(EC.presence_of_element_located((By.ID, "content")))
        if (crusoecontent.text!="Sorry, an error occurred while processing your request..."):
            raise ValueError("Unexcpected string while login to crusoe")

    def alert_check(self, driver, url=None, timeout=DEFAULT_DELAY, expect_value=False, text_value=None):
        url = self.__url_check(url,driver)
        sucess = True
        print('='*25,"\ntesting for alert at ",url,"\nalert timeout in: ",timeout," sec(s).")
        if(expect_value):
            print("expected value: ",text_value)
        try:
            WebDriverWait(driver, timeout).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
            alert = driver.switch_to.alert
            if( expect_value and alert.text == text_value ):
                print("alert text is equal to provided text.")
            if( expect_value and alert.text != text_value ):
                print("alert text is not equal to provided text, alert text: ",alert.text)
                sucess = False
            alert.accept()
            print("alert accepted succesfuly.")
        except TimeoutException:
            print("no alert found.")
            sucess = False
        return sucess
    
    def confirm_check(self, driver, url=None, timeout=DEFAULT_DELAY, confirm=True, expect_value=False, text_value=None):
        url = self.__url_check(url,driver)
        print('='*25,"\ntesting for confirm at ",url,"\nconfirm timeout in: ",timeout," sec(s).")
        if(expect_value):
            print("expected value: ",text_value)
        try:
            WebDriverWait(driver, timeout).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
            alert = driver.switch_to.alert
            if( expect_value and alert.text == text_value ):
                print("confirm text is equal to provided text.")
            if( expect_value and alert.text != text_value ):
                print("confirm text is not equal to provided text, confirm text: ",alert.text)
            if(confirm):
                alert.accept()
            else:
                alert.dismiss()
            print("confirm closed succesfuly.") 
        except TimeoutException:
            print("error: no confirm found.")

    def __url_check(self, url, driver):
        if( url == None ):#prefom check at current page or go to new url.
            try:
                url = driver.current_url
            except: #cant retrive with alert open
                url = "(last url)"
        else:
            driver.get(url)
        return url
    
    def test_cases(self, webdriver, input_list):
        
        self.alert_cases(webdriver,input_list)
        self.confirm_cases(webdriver,input_list)

    def alert_cases(self,webdriver,input_list):
        msg(" --- TESTING ALERTS ---")
        for val in input_list:
            success = self.alert_check(webdriver, url="https://codepen.io/yairzaff/full/YzPLQrv?text="+val, expect_value=True, text_value=val)
            if(success):
                self.success+=1
            else:
                self.fail+=1

    def confirm_cases(self, webdriver, input_list):
        msg(" --- TESTING CONFIRMS ---")
        for i in range(6):
            self.confirm_check(webdriver,url="https://codepen.io/yairzaff/full/ExaLvWp?text=choice")
            time.sleep(i*2)
            success = self.alert_check(webdriver,expect_value=True,text_value="ok")
            if(success):
                self.success+=1
            else:
                self.fail+=1


mytester = Tester("john", "doe")


'''
for entry in driver.get_log('browser'):
    print(entry)
'''



'''
def alert_check(url=None,timeout=3,expect_value=False,text_value=None):
    if(url==None):#check at current or go to new url.
        try:
            url=driver.current_url
        except: #cant retrive with alert open
            url="(current url)"
    else:
        driver.get(url)
        print('='*25)
    print("testing for alert at ",url,"\nalert timeout in: ",timeout," sec(s).")
    if(expect_value):
        print("expected value: ",text_value)
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
        alert = driver.switch_to.alert
        if(expect_value and alert.text==text_value):
            print("alert text is equal to provided text.")
        if(expect_value and alert.text!=text_value):
            print("alert text is not equal to provided text, alert text: ",alert.text)
        alert.accept()
        print("alert accepted succesfuly.")
    except TimeoutException:
        print("no alert found.")



def confirm_check(url=None,timeout=3,confirm=True,expect_value=False,text_value=None):
    if(url==None):#check at current or go to new url.
        try:
            url=driver.current_url
        except: #cant retrive with alert open
            url="(current url)"
    else:
        driver.get(url)
        print('='*25)
    print("testing for confirm at ",url,"\nconfirm timeout in: ",timeout," sec(s).")
    if(expect_value):
        print("expected value: ",text_value)
    driver.get(url)
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
        alert = driver.switch_to.alert
        if(expect_value and alert.text==text_value):
            print("confirm text is equal to provided text.")
        if(expect_value and alert.text!=text_value):
            print("error: confirm text is not equal to provided text, confirm text: ",alert.text)
        if(confirm):
            alert.accept()
        else:
            alert.dismiss()
        print("alert accepted succesfuly.")
        
    except TimeoutException:
        print("error: no confirm found.")


def prompt_test(txt): 
    driver.get("https://codepen.io/yairzaff/full/yLyjgdg")
    driver.switch_to.alert.send_keys(txt)
    driver.switch_to.alert.accept()
    returned_text=driver.switch_to.alert.text
    driver.switch_to.alert.accept()

#no alert expected. source: https://codepen.io/yairzaff/pen/YzPLVBx
alert_check("https://codepen.io/yairzaff/full/YzPLVBx")

#expecting alert. source: https://codepen.io/yairzaff/pen/abzGBpb
alert_check("https://codepen.io/yairzaff/full/abzGBpb")

#expecting alert with text "hello"
alert_check("https://codepen.io/yairzaff/full/abzGBpb",expect_value=True,text_value="hello")

#expecting alert with text "שלום"
alert_check("https://codepen.io/yairzaff/full/rNavwOx",expect_value=True,text_value="שלום")
'''