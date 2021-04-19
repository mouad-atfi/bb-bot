import time
import requests
import multiprocessing
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = 'C:\\Users\\desktop\\Documents\\bot\\chromedriver.exe'
url = "https://www.bestbuy.ca/identity/global/signin?redirectUrl=https://www.bestbuy.ca/checkout/?qit=1#/en-ca/shipping/BC/V3K&amp;lang=en-CA&amp;contextId=checkout"

profiles = [
    {
         'email': 'mouad.atfi@gmail.com', 
         'password': 'mouad17', 
         'proxy': '138.197.132.33'
    }, 
    {
         'email': 'soloqxss@gmail.com', 
         'password': 'Mouad.17', 
         'proxy': '134.122.34.159'
    }  
]

def Getcookies(email, password, proxy):
  options = webdriver.ChromeOptions()
  proxy = proxy
  options.add_argument('--proxy-server=socks5://' + proxy)
  options.add_argument('--ignore-certificate-errors')
  #options.add_argument("--headless")
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--log-level=3")
  #options.add_argument("--disable-dev-shm-usage")
  options.add_argument('--disable-gpu')
  #options.add_argument("--disable-blink-features")
  options.add_experimental_option('useAutomationExtension', False)
  options.add_experimental_option("excludeSwitches", ["enable-automation"])

  with webdriver.Chrome(executable_path=PATH, options=options) as driver:

      driver.get(url)
      driver.find_element_by_css_selector("#email").send_keys(email)
      driver.find_element_by_css_selector("#password").send_keys(password)
      driver.find_element_by_css_selector("#signIn").click()

      time.sleep(10)

      cookies = driver.get_cookies()
      s = requests.Session()
      for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
      tx = s.cookies.get("tx")
      print (tx)
      if not tx:
        raise error.InternalServerException  
      with open(email, 'wb') as f:
        pickle.dump(s.cookies, f) 
    
def main():
  p = multiprocessing.Pool()
  for i in profiles:
    email = (i['email'])
    password = (i['password'])
    proxy = (i['proxy'])
    p.apply_async(Getcookies, args=(email, password, proxy))
  p.close()
  p.join()   
    
    
'''
    def getToken(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Referer": "https://www.bestbuy.ca/en-ca/basket",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": self.ua,
        }
        payload = {
            "redirectUrl": f"https://www.bestbuy.ca/checkout/?qit=1#/en-ca/shipping/ON/{self.postal}",
            "lang": "en-CA",
            "contextId": "checkout",
        }

        res = self.session.get(
            "https://www.bestbuy.ca/identity/global/signin",
            headers=headers,
            params=payload,
        )

        if not res.ok:
            raise error.InternalServerException(res.reason)

        tx = self.session.cookies.get("tx")

        if not tx:
            raise error.InternalServerException

        self.token = tx
        return tx
'''
