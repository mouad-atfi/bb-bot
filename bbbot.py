from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import os
import time
import sys
import random

PATH = 'C:\\Users\\desktop\\Documents\\bot\\chromedriver.exe'

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/89.0.774.75",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"]

proxies = []

with open('./socks.txt') as f:
        proxies = f.read().splitlines()


def getCookies():
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=socks5://' + proxy)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(executable_path=PATH, options=options)
    driver.get("https://www.bestbuy.ca/en-ca/basket")




def checkBB():

        for prox in proxies:
            proxy = { 'https': 'socks5://'+prox}
            user_agent = random.choice(user_agent_list)
            try:
                #url = 'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&postalCode=E5S&skus=15084753|14953248|14954116|15166285|15078017|15229237'
                headers = {
                    'authority': 'www.bestbuy.ca',
                    'upgrade-insecure-requests': '1',
                    'user-agent': user_agent,
                    'referer': 'https://www.bestbuy.ca/en-ca/product/msi-nvidia-geforce-rtx-3060-ti-ventus-2x-oc-8gb-gddr6-video-card/15178453',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-US,en;q=0.9',
                }

                params = (
                    ('accept', 'application/vnd.bestbuy.standardproduct.v1+json'),
                    ('accept-language', 'en-CA'),
                    ('skus', '15084753|14953248|14954116|15166285|15078017|15229237'),
                )

                response = requests.get('https://www.bestbuy.ca/ecomm-api/availability/products', headers=headers, params=params, proxies=proxy, timeout=5)
                response.raise_for_status()
                decoded_data = response.content.decode('utf-8-sig')

                match = json.loads(decoded_data)
                print(response.elapsed.total_seconds())
                for i in range(6):
                    status = str(match['availabilities'][i]['shipping']['status'])
                    quantity = str(match['availabilities'][i]['shipping']['quantityRemaining'])
                    print(status, quantity)
                countdown(1)    

            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)    


def countdown(t):
    while t > 0:
        sys.stdout.write('\rWaiting : {}s '.format(t))
        t -= 1
        sys.stdout.flush()
        time.sleep(1)

def main():

    while True:
        getCookies()
        checkBB()


if __name__ == "__main__":
    main()
