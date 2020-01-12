
# -*- coding: utf-8 -*-

'''

chrome webdriver version 79.0.3945.36 win32

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
import os
import sys

from PIL import ImageGrab
import win32gui
import config


###############################
### Cruesoe Proxy Settings ####
###############################

#crusoe_login_url = "X" # 

DEFAULT_DELAY = 12
TAKE_PICTURES = True
input_list = ["hello","שלום","1",""]


def msg(text):
    now = datetime.datetime.now()
    if threading.current_thread() is threading.main_thread():
        print ("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] " + text)
    else:
        print("[" + now.strftime("%Y-%m-%d %H:%M:%S") + " Thread:" + str(threading.current_thread().threadID) + " User:" + threading.current_thread().userCredentials["username"] + "] " + text)



class Tester():
    def __init__(self, username, password):
        self.remote_hub_url = config.crusoe_hub_url 
        self.proxy_host_port = config.crusoe_proxy_host_port
        self.proxy_exclusions = config.crusoe_proxy_exclusions
        self.success=0
        self.fail=0
        
        msg ("Connecting to web driver on hub: " + self.remote_hub_url)
        #webdriver = self.connect_remote_chrome_webdriver_with_proxy(self.remote_hub_url, self.proxy_host_port, self.proxy_exclusions)
        webdriver = self.connect_my_driver() # i dont have access to crusoe's proxy
        self.time_start = str(int(time.time()))
        self.scrnshot_dir="test_"+self.time_start+"_screenshots"
        try:
            self.test_cases(webdriver,input_list)
            print("total tests: ",(self.success+self.fail), "failed: ",self.fail)
            if(self.fail > 0 and TAKE_PICTURES):
                print("you can view screenshots of failed tests at:  ",self.scrnshot_dir)
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
                self.screen_shot(driver,"alert_wrong_text")
                sucess = False
            alert.accept()
            print("alert accepted succesfuly.")
        except TimeoutException:
            print("no alert found.")
            self.screen_shot(driver,"no_alert")
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
                self.screen_shot(driver,"confirm_wrong_text")
            if(confirm):
                alert.accept()
                print("confirm closed succesfuly. (using: ok)") 
            else:
                alert.dismiss()
                print("confirm closed succesfuly. (using: cancel)") 
            
        except TimeoutException:
            print("no confirm found.")
            self.screen_shot(driver,"no_confirm")

    def prompt_check(self, driver, url=None, timeout=DEFAULT_DELAY,confirm=True , text_input=None):
        url = self.__url_check(url,driver)
        print('='*25,"\ntesting for prompt at ",url,"\nconfirm timeout in: ",timeout," sec(s).")
        print("input value: ",text_input)
        try:
            WebDriverWait(driver, timeout).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
            alert = driver.switch_to.alert
            driver.switch_to.alert.send_keys(text_input)    
            if(confirm):
                alert.accept()
                print("prompt closed succesfuly. (using: ok)") 
            else:
                alert.dismiss()
                print("prompt closed succesfuly. (using: cancel)") 
        except TimeoutException:
            print("no prompt found.")
            self.screen_shot(driver,"no_prompt")

    def __url_check(self, url, driver):
        if( url == None ):#prefom check at current page or go to new url.
            try:
                url = driver.current_url
            except: #cant retrive with alert open
                url = "(last url)"
        else:
            driver.get(url)
        return url
    
    def screen_shot(self,driver, name):
        if not TAKE_PICTURES:
            return
        time.sleep(1)
        try:
            os.mkdir(self.scrnshot_dir)
        finally:
            toplist, winlist = [], []          
            win32gui.EnumWindows(lambda hwnd,toplist : winlist.append((hwnd, win32gui.GetWindowText(hwnd))), toplist)
            chrome = [(hwnd, title) for hwnd, title in winlist if 'chrome' in title.lower()]
            chrome = chrome[0]
            hwnd = chrome[0]
            win32gui.SetForegroundWindow(hwnd)
            bbox = win32gui.GetWindowRect(hwnd)
            img = ImageGrab.grab(bbox)
            img.save(self.scrnshot_dir+"/"+name+"_"+str(int(time.time()))+".jpg",format="JPEG")

    def test_cases(self, webdriver, input_list):
        self.alert_cases(webdriver,input_list)
        self.confirm_cases(webdriver,input_list)
        self.prompt_cases(webdriver,input_list)

    def alert_cases(self, webdriver, input_list):
        # code:  https://codepen.io/yairzaff/pen/YzPLQrv
        msg(" --- TESTING ALERTS ---")
        for val in input_list:
            success = self.alert_check(webdriver, url="https://codepen.io/yairzaff/full/YzPLQrv?text="+val, expect_value=True, text_value=val)
            if(success):
                self.success+=1
            else:
                self.fail+=1

    def confirm_cases(self, webdriver, input_list):
        # code: https://codepen.io/yairzaff/pen/ExaLvWp
        msg(" --- TESTING CONFIRMS ---")
        self.confirm_check(webdriver,url="https://codepen.io/yairzaff/full/ExaLvWp?text=choice")
        success = self.alert_check(webdriver,expect_value=True,text_value="ok") #currently checking the returned value in alert since i can't get console.log to work properly.
        if(success):
            self.success+=1
        else:
            self.fail+=1
        self.confirm_check(webdriver,url="https://codepen.io/yairzaff/full/ExaLvWp?text=choice",confirm=False)
        success = self.alert_check(webdriver, expect_value=True, text_value="cancel")
        if(success):
            self.success+=1
        else:
            self.fail+=1

    def prompt_cases(self,webdriver,input_list):
        # code: https://codepen.io/yairzaff/pen/yLyjgdg
        msg(" --- TESTING PROMPTS ---")
        for val in input_list:
            self.prompt_check(webdriver, url="https://codepen.io/yairzaff/full/yLyjgdg", confirm=True, text_input=val)
            success = self.alert_check(webdriver, expect_value=True, text_value=val)
            if(success):
                self.success+=1
            else:
                self.fail+=1
        for i in range(30):
            self.prompt_check(webdriver, url="https://codepen.io/yairzaff/full/yLyjgdg", confirm=True, text_input=str(i))
            success = self.alert_check(webdriver, expect_value=True, text_value=str(i))
            if(success):
                self.success+=1
            else:
                self.fail+=1

mytester = Tester("john", "doe")

