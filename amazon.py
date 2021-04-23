from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time
import random
import sys
import subprocess
import multiprocessing
import re
import requests
import pickle

# make sure this path is correct
PATH = 'C:\\Users\\desktop\\Documents\\bot\\chromedriver.exe'

domains = ['smile.amazon.com', 'amazon.com']

asins = [      
    {
         'asin': 'B08L8KC1J7',
         'price': '780'    
    },
    {
         'asin': 'B08L8LG4M3',
         'price': '750'    
    },
    {
         'asin': 'B08HH5WF97',
         'price': '900'    
    },
    {
         'asin': 'B08HR3Y5GQ',
         'price': '950'    
    },
    {
         'asin': 'B08MT6B58K',
         'price': '700'    
    },
    {
         'asin': 'B08KWLMZV4',
         'price': '700'    
    },
    {
         'asin': 'B08L8L9TCZ',
         'price': '750'    
    },
    {
         'asin': 'B08L8L71SM',
         'price': '750'    
    },                        
]

def checkBB(proxy,event):

       #options = webdriver.ChromeOptions()
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--proxy-server=socks5://' + proxy)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_argument('--disable-gpu')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = uc.Chrome(options=options) 
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})
        driver.set_page_load_timeout(10)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
        while True:
            for domain in domains:
                for i in asins:
                    asin = (i['asin'])
                    price = (i['price'])
                    try:
                        #multi_url = 'https://smile.amazon.com/gp/aws/cart/add.html?OfferListingId.1={}&Quantity.1=1&OfferListingId.2={}&Quantity.2=1&OfferListingId.3={}&Quantity.3=1&OfferListingId.4={}&Quantity.4=1&OfferListingId.5={}&Quantity.5=1&confirmPage=confirm'
                        url = f'https://{domain}/gp/aod/ajax/ref=aod_f_primeEligible?asin={asin}'
                        t0= time.perf_counter()
                        driver.get(url)
                        t1 = time.perf_counter() - t0
                        #print(driver.page_source)
                        print ('\r{:.2f} sec'.format(t1)) 
                        name = driver.find_element_by_id('aod-asin-title-text').text
                        print(name)
                        
                        try:
                            offerid = driver.find_element_by_name("offeringID.1").get_attribute('value')
                            digits = driver.find_element_by_xpath("//span[contains(@class,'a-offscreen')]").text
                            aprice = digits.strip('$').replace(',','')
                            if float(aprice) < price:
                                print('Checking out ATM: ', asin)
                                turboATC(asin,offerid)
                                event.set()
                                
                        except Exception as e:
                            pass
                        time.sleep(2)                    
                    except Exception as e:
                        print('error')
                        pass
                    time.sleep(2)       
            time.sleep(30)

#def pushmessage(offerid,sessionid):

#    user = "Default"
#    path_autorun_html = 'c:\\Users\\mouad.atfi\\Documents\\bot\\ui.vision.html'
#    browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe --profile-directory="{}" %s'.format(user)

#    args = r'file:///' + path_autorun_html + '?macro=amazon-buy&cmd_var1=' + offerid + '&cmd_var2=' + sessionid + '&direct=1&closeRPA=1&nodisplay=1'
#    webbrowser.get(browser_path).open(args)

def turboATC(asin,offerid):
    try:

        asin = asin
        offerid = offerid
        cookies = 'session-id=135-7453302-3097227; ubid-main=132-8488874-8720246; session-token=ir3BkkeQGW5l67J5L5jUkJSRCPTQdKktZeGrXpPQqg8qFYbCR7S+33To25HJp1aqlTNypW7z55nCYpdYg5+XOOzYIZ3XQAGj7MPVRoLTGZnrC4mkVNxjOyi2vNI0A2gwTDLjt32kIqwOcMgmugFszaHPJWBCeXqnegj2IRkTcc6vlee4E3YPyliV+aABVfDjy3PJi6BGUvBzeuSxeLqXDJvBqAaPiAXJ6p8XjT9LTlQ+eZmAqujgZ5S6aanCl2wbYgDQ488d/GchbOsV4l08o8PU1aoFVmo+; x-main="wnXTsEtTTO60xCASCXppECESjLW@Ex372XzdMQu4l1Zihd1fZ2AzVOcABXlohf6A"; at-main=Atza|IwEBID8XyMiRIKDS5l3-jjXAIeK1tAt1KofkwdZOYXdi0HFIaSD6PSTJ_8DEwyMSEeCDyRFzViS7LnXcRHF2801OGF_azOfA9iZEwl_YBFohWm_jViLVLNGy2zpGySlkiVQPG8juMJsxS1L0cG0SrRgUNEZYaaScppf6M2CRaskN7G_vvtG6XhLz8vYd8g-0eW-XDehi2T3csZ5XEhZVc1mbQdTx; sess-at-main="rTclxCG9/5QLKfCbIXOOluZtOyXBiqA2hIyQpFwZa6Y="; sst-main=Sst1|PQHvOKKBBMZMQnFDmkKG5dRdCYlSMRf_7r0hholWo8c16JIJo07BYc_kqCRCvzTcojeXrEyq3LpK8rlcTUjIY__VjAeYr1kGlydK4xsXIS-XYERrgR7U4MKUWzDa9IyiCxC8zVSNYwgIj20Lb3GFZ-ZYtv8tZpaj1LIVdarEKPlP7pyKPm0JFWaomSjn4Z9O-SQvCC0huq80R1kKRCluUczYgRqMLlMIT3Kw9aiu3iTDCYxWS1GU7fQI8QdO4q3udfRcgDqNrVsKfspRd3VkV2yjrpVb9Mh-RdNGhcDe9WqQY4E; lc-main=en_US; i18n-prefs=USD; session-id-time=2082787201l; csm-hit=tb:s-BF5R1C07DQ94X06P2GSF|1619196547447&t:1619196547453&adb:adblk_no'   

        headers = {
            'authority': 'smile.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'x-amz-checkout-entry-referer-url': f'https://smile.amazon.com/gp/product/{asin}/',
            'rtt': '50',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'x-amz-support-custom-signin': '1',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'x-amz-turbo-checkout-dp-url': f'https://smile.amazon.com/dp/{asin}/',
            'downlink': '10',
            'ect': '4g',
            'origin': 'https://smile.amazon.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://smile.amazon.com/gp/product/{asin}/',
            'accept-language': 'en-US,en;q=0.9,fr-CA;q=0.8,fr;q=0.7,ar;q=0.6,la;q=0.5',
            'cookie': cookies,
        }

        params = (
            ('ref_', 'dp_start-bbf_1_glance_buyNow_2-1'),
            ('referrer', 'detail'),
            ('pipelineType', 'turbo'),
            ('clientId', 'retailwebsite'),
            ('weblab', 'RCX_CHECKOUT_TURBO_DESKTOP_NONPRIME_87784'),
            ('temporaryAddToCart', '1'),
        )

        data = {
          'isAsync': '1',
          'addressID': 'nhjhoummqqkq',
          'asin.1': asin,
          'offerListing.1': offerid,
          'quantity.1': '1'
        }

        response = requests.post('https://smile.amazon.com/checkout/turbo-initiate', headers=headers, params=params, data=data)
        print("sent first request")
        f = response.text
        print(f)
        RequestId = re.findall(r'currentRequestId":"(.*?)"',f)[0]
        pid = re.findall(r'pid=(.*?)&',f)[0] 
        csrftoken = re.findall(r"csrftoken-a2z' value='(.*?)'",f)[0]
        print(RequestId)
        print(pid)
        print(csrftoken)

        headers2 = {
            'authority': 'smile.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'x-amz-checkout-entry-referer-url': f'https://smile.amazon.com/dp/{asin}/',
            'anti-csrftoken-a2z': csrftoken,
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://smile.amazon.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://smile.amazon.com/checkout/spc?pid={pid}&pipelineType=turbo&clientId=retailwebsite&temporaryAddToCart=1&hostPage=detail&weblab=RCX_CHECKOUT_TURBO_DESKTOP_NONPRIME_87784',
            'accept-language': 'en-US,en;q=0.9,fr-CA;q=0.8,fr;q=0.7,ar;q=0.6,la;q=0.5',
            'cookie': cookies,
        }
         
        
         
        params2 = (
            ('ref_', 'chk_spc_placeOrder'),
            ('_srcRID', RequestId),
            ('clientId', 'retailwebsite'),
            ('pipelineType', 'turbo'),
            ('pid', pid),
        )

        data2 = {
          'ref_': 'chk_spc_placeOrder',
          'referrer': 'spc',
          'pid': pid,
          'pipelineType': 'turbo',
          'clientId': 'retailwebsite',
          'temporaryAddToCart': '1',
          'hostPage': 'detail',
          'weblab': 'RCX_CHECKOUT_TURBO_DESKTOP_NONPRIME_87784',
          'isClientTimeBased': '1'
        }

        response = requests.post('https://smile.amazon.com/checkout/spc/place-order', headers=headers2, params=params2, data=data2)
        print (f'Checkout {asin} complete, exiting')
    except Exception as e:
        print (e)

def main():
    with open('./socks.txt') as f:
        proxies = f.read().splitlines()
    random.shuffle(proxies)
    p= multiprocessing.Pool(60) 
    m = multiprocessing.Manager()
    event = m.Event()
    for proxy in proxies:
        p.apply_async(checkBB , args=(proxy,event))
        time.sleep(3)
    p.close()
    event.wait()
    p.terminate()    



if __name__ == "__main__":
    main()
