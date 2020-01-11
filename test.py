
# -*- coding: utf-8 -*-

'''

chrome webdrive version 78.0.3904.105 win32

https://chromedriver.storage.googleapis.com/index.html?path=78.0.3904.105/

'''

from selenium import webdriver                                                 #driver for browser
from selenium.webdriver.common.keys import Keys                                #allows to send keys by value
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities #browser settings
from selenium.webdriver.support.ui  import WebDriverWait                       #waiting for an event to occur
from selenium.webdriver.support  import expected_conditions as EC              #exception conditions 
from selenium.common.exceptions  import TimeoutException                       

import time



# configure chrome setting to keep a log of all events, in order to get console.log output. (doesn't work currently, using alerts instead to get values back from page)
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(desired_capabilities=d)
# get_log doesnt show console.log, using alert to return input for checking instead. (code for get_log:)
'''
for entry in driver.get_log('browser'):
    print(entry)
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
            print("error: alert text is not equal to provided text, alert text: ",alert.text)
        alert.accept()
        print("alert accepted succesfuly.")
    except TimeoutException:
        print("error: no alert found.")



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