from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import os
import time

driver = webdriver.Chrome()
driver.get("https://codepen.io/yairzaff/full/abzGBpb")

driver.switch_to.alert.accept()