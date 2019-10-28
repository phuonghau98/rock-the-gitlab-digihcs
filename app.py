from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import getpass
import os

gitUsn = input("Enter git username: ")
gitPwd = getpass.getpass("Enter git password: ")

chrome_options = Options()
chrome_options.add_argument('headless')
browser = webdriver.Chrome(options=chrome_options, executable_path=os.getcwd() + '/chromedriver')
url = "http://118.69.83.58"

def sshPathTransform (path):
  return path.replace('http://118.69.83.58', 'ssh://git@118.69.83.58:1210')

def login (browser, usn, pwd):
  usnEl = browser.find_element_by_id("user_login")
  pwdEl = browser.find_element_by_id("user_password")
  time.sleep(1)
  usnEl.send_keys(usn)
  pwdEl.send_keys(pwd)
  pwdEl.send_keys(Keys.ENTER)

def scanAll (browser):
  pathSet = set()
  while True:
    try:
      paths = browser.find_elements_by_css_selector('div.project-title a')
      for path in paths:
        pathSet.add(sshPathTransform(path.get_attribute('href')))
      nextBtn = browser.find_element_by_css_selector('li.js-next-button a')
      nextBtn.click()
    except (NoSuchElementException, ElementClickInterceptedException) as e:
      break
  return pathSet

browser.get(url)
login(browser, gitUsn, gitPwd)
resultPaths = scanAll(browser)
browser.close()

for path in resultPaths:
  os.system('git clone ' + path)