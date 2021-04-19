import time
import requests
import multiprocessing
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_stealth import stealth
import undetected_chromedriver as uc

PATH = 'C:\\Users\\desktop\\Documents\\bot\\chromedriver.exe'
url = "https://www.bestbuy.ca/identity/global/signin?redirectUrl=https://www.bestbuy.ca/checkout/?qit=1#/en-ca/shipping/BC/V3K&amp;lang=en-CA&amp;contextId=checkout"

profiles = [
    {
         'user': 'mouadatfi',
         'email': 'mouad.atfi@gmail.com',
         'password': 'mouad17', 
         'proxy': '138.197.132.33:8388'
    }, 
    {
         'user': 'meriemcharaf',
         'email': 'soloqxss@gmail.com', 
         'password': 'Mouad.17', 
         'proxy': '134.122.34.159:8388'
    }  
]

def Getcookies(user, email, password, proxy):
    options = uc.ChromeOptions()
    proxy = proxy
    options.add_argument('--proxy-server=socks5://' + proxy)
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument('--disable-gpu')
    #options.add_argument("--disable-blink-features")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])


    with uc.Chrome(options=options) as driver:

      driver.get(url)
      driver.find_element_by_css_selector("#username").send_keys(email)
      driver.find_element_by_css_selector("#password").send_keys(password)
      driver.find_element_by_xpath('//*[@id="signIn"]/div/button').click()

      time.sleep(10)

      cookies = driver.get_cookies()
      s = requests.Session()
      for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
      tx = s.cookies.get("tx")
      print (tx)
      if not tx:
        raise error.InternalServerException  
      with open(user, 'wb') as f:
        pickle.dump(s.cookies, f)
      #time.sleep(320)   
    
def main():
  p = multiprocessing.Pool()
  for i in profiles:
    user = (i['user'])
    email = (i['email'])
    password = (i['password'])
    proxy = (i['proxy'])
    #print(email, password, proxy)
    p.apply_async(Getcookies, args=(user, email, password, proxy))
  p.close()
  p.join()   
    
if __name__ == "__main__":
    main()
