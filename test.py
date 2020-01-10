
# -*- coding: utf-8 -*-

'''

chrome webdrive version 78.0.3904.105 win32

https://chromedriver.storage.googleapis.com/index.html?path=78.0.3904.105/

'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

import os
import time

driver = webdriver.Chrome()

#alert
driver.get("https://codepen.io/yairzaff/full/abzGBpb")
driver.switch_to.alert.accept()

#prompt
driver.get("https://codepen.io/yairzaff/full/yLyjgdg")
driver.switch_to.alert.send_keys("abcd")
driver.switch_to.alert.accept()
