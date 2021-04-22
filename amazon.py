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
PATH = 'C:\\Users\\mouad.atfi\\Documents\\bot\\chromedriver.exe'

offeridlist = ['UY1epatIWfF3MNA8YEyITOpaHDmhCUsNXK6dOGB8%2FBsb%2Fx19D2vH4BJCd6JUCAFy6UjqJPpdHztHxzbplj4B2bNBN7EDEQjuzCSben8MOjJR6g67yfz5DUwcKgpheap0LvbFFibok8MosmOzEzIn8w%3D%3D',
           # 'y3R1UdH251cREqi83DvayyqeRMzELG2W6NBWm7JQplCsJQQ3aoYZmbYoFs7wchAJkSHvTjYme89beUs3JY8WKg79XhDTex65fAGH8qlgbv1LcUHBx3CqY7G1OHuSrpfs91bO8jekMTjqrMCTtO0G7g%3D%3D',
           # 'sEstwZmJjcNQYLV8cVAtgvs1hVJjsDdJLE0mpu4blmCjZWnPzbEs78cWfFoC7Fw3f1TKg7hG55vjkWRtV9%2FjvpBGqDh%2B3CHHuYk8dAR63FZP7fFqin3q45en2jzMaiIVBOqv26l%2BrHiN%2Bpf2RSir3Q%3D%3D',
           # '3UlxQRWI%2BkroT%2FPzmwoI3ml9HpwL2gQu3WDvEyd0HppIf%2F13mhOFqoNCq3ZjNNCJ6ze4gAeUmJMkabj01tf0%2B0T2GNBE5JuRDdcb4IFNbeSGAAHYWNk64Vw27H0Z0Wc95pQAP2Ugd4KjAooe9Zvj7w%3D%3D',
            'XxPFA2X73me9%2BD6uuisgJFQy1KGmyOndrdObETZCZkWQPWi18SvUKztmJhCHyRkIiptvUuUKhB6JxrztDyvJ18T45kQroVgbaRQIYdTl%2FZ5MtMLH%2FliEKVKoGiC%2BSvbTdvcpCcFvfGN7b5Lve7Px1A%3D%3D',
           # '5OWZDJsyFvtDylhF%2BN5umyzDgISwzmz7r%2F6wlwBGWeqSJvCfGkmfwjMiEkdtM2eAERfF5Fvc6Z3jaGLz%2BiVht76nQHkzlIGqFNIAqDE8VRSNVbraQH%2BdsmejoIKOUVVVlpSiMNik6SOSrTGBT8GSBg%3D%3D',
           # '94zSXPjJ063cuJSTenOo%2FtGj4p8NoLgmTtLuMGd6CmEb2b%2F0XmefWSw50Gas8MOqSe5mVApTaKsj4wWH9RCFRi2X5EyueLyJU%2F2D7UCZMOYniVCvFiBSFEyFmYCszYtDxEZN%2FlaledHjNzGVOGNgIw%3D%3D',
           # '8r0UVxTtC73d5kH4RKIJjBHW1k1sKdXXE%2FNYtS6q4M2mNmR%2FZcW8%2FJV%2BFFGDDvWzFPHhdtjJwTDvyijM66Wl6UgotuHZ9m18LKgdZwNKfC7V5ofGi%2FmIo5vC87MvVA4Co6fcQ%2F3D60IQ%2F1MdNnmVKQ%3D%3D',
           # '8r0UVxTtC73d5kH4RKIJjBHW1k1sKdXXE%2FNYtS6q4M2mNmR%2FZcW8%2FJV%2BFFGDDvWzFPHhdtjJwTDvyijM66Wl6UgotuHZ9m18LKgdZwNKfC7V5ofGi%2FmIo5vC87MvVA4Co6fcQ%2F3D60IQ%2F1MdNnmVKQ%3D%3D',
           # 'IxFSurbOSFvHXinfpn1jIJc%2FZrsKedmcI9rDB0Zy3EQq12ZxQk%2F%2FRAGvW93sLQ2ZKIwokbMu9uN%2F7tmM%2BY6GzJKZNFzJKSobk7act7CsBLPdy1A97oLa5BJbothkF%2BsQ4nEQ032ihdIz7jU6a5wBMA%3D%3D'
           'ggis6d38qwrxGxl0wKUjXf06D0hKZTQg6E4J%2BbAQBvRcYFdD55dH5NhOkhvD0Fp6hlxFem%2FoVdrdvsoNFYixAePVDIjKouLkGJKOiDz9iKdnQZo8wChG5NKWl8EpUB%2FZ6NpRaF7axNaUhz9acBljzw%3D%3D',
           'Vp7Q5CHUqNqFYzXR7Fb4Ogo1MbAyT1scYM7eI%2FPUI9IvO15AP%2BZM%2BndrftFiIWzdexzwqbICHVugB8j3WE4qLpe7Xm6ecZTqDt15X1W2TUlEZ9aJx%2B3NaIOToY3RHiZWS%2F6lo3Slol%2BG5wFFk5TWGw%3D%3D'
           ]
asins = ['B08L8KC1J7', 'B08L8LG4M3', 'B08HH5WF97', 'B08HR3Y5GQ', 'B08MT6B58K']

def checkBB(proxy,event):

       #options = webdriver.ChromeOptions()
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--proxy-server=socks5://' + proxy)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        #options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--disable-gpu')
        #options.add_argument("--disable-blink-features")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2, 'profile.managed_default_content_settings.images': 2})
        driver = uc.Chrome(options=options) 
        #driver = webdriver.Chrome(executable_path=PATH, options=options) 
        #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})
        #print(driver.execute_script("return navigator.userAgent;"))
        driver.set_page_load_timeout(10)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        while True:
            for asin in asins:
                try:
                    #multi_url = 'https://smile.amazon.com/gp/aws/cart/add.html?OfferListingId.1={}&Quantity.1=1&OfferListingId.2={}&Quantity.2=1&OfferListingId.3={}&Quantity.3=1&OfferListingId.4={}&Quantity.4=1&OfferListingId.5={}&Quantity.5=1&confirmPage=confirm'
                    #url = f'https://smile.amazon.com/gp/aws/cart/add.html?OfferListingId.1={offerid}&Quantity.1=1&confirmPage=confirm'
                    url = f'https://amazon.com/gp/aod/ajax/ref=aod_f_primeEligible?asin={asin}'
                    t0= time.perf_counter()
                    print(asin)

                    driver.get(url)

                    t1 = time.perf_counter() - t0
                    print ('\r{:.2f} sec'.format(t1))
                    try:
                        #item = driver.find_element_by_xpath("/html/body/div[3]/div/div/form/span/table/tbody/tr[2]/td[2]/a").text
                        offerid = driver.find_element_by_name("offeringID.1").get_attribute('value')
                        print (offerid)
                        

                        if offerid:
                            print('Checking out ATM')
                            turboATC(asin,offerid)
                            event.set()
                            
                    except Exception as e:
                        #print (e)
                        pass  # it was a string, not an int.             
                except Exception as e:

                    print('==========>>>>>>>>', proxy)
                    print(e)        
            time.sleep(45)

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
            'cookie': 'at-main=Atza|IwEBIANS8LCatNBDJo2J_wjq-uigErWwDsgKNm4Xp-0xF5ewndZ5ZMmkP4Txd9OPdzeH-o8Emh-1px30PYMx77-z8aibDpI5KJKDSoNymxtYG8__yg10ZgcMIoHMEdhk2f6rK3ApIIyzWOUfcbm7TE3Y6B_r9XgMDq3YvwxOsjytLCXvezi3JBd13IR8b-4VNSYFBo-MZco58C28__JYZM0_BCAOUO0zGkkX6hJsps6YvGmH2Q; aws_lang=en; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1618496195610-717256; i18n-prefs=USD; lc-main=en_US; regStatus=pre-register; s_campaign=PSM%7Cpsc-2021-ec2_ec2_amd-adop-namer-fb-prospect-itpro-right_size%7CFB%7CPSC-CI%7CEC2%20Adoption%20AMD%7C3128864%7CAustin%7C%7CSC%7Cright_size%7C1200x628%7C%7CPROS%7CPersona%7C%7CAMD%7CEN%7CPA%7CAll%7CIT%20Pro%7CCompute%7CNAMER%7CNAMER%7Cpsm_a134p000006peeSAAQ; s_cc=true; s_eVar60=psm_a134p000006peeSAAQ; s_fid=10D65790BD3E9662-0E495B7B175F9B10; sess-at-main="JYhh8gxiBslO/kqg9CLHKB+7ZINYTzfeMyPRXcV0brQ="; session-id=133-9013249-1407720; skin=noskin; sst-main=Sst1|PQFaGWu7J2h5IuNc2LZKdajtCRijIOMekV60ZkJVaTETGt9Loyl_4O82jLyfB5QYyq6TY-rSsBxVJhk3kuFn_9xsnDC0L9EQqP857UtdoSRpyqj4thl_5zBbMX1d6bHj6RRgin08pEXCVtTX0sKjTXXQAAdwxDUehWJ3zMYqvrbzfdgYUsSfaIi2z4JXly2KCTnJ2x7S1ZPsT01icJ9eaxXiYpplO4zC8oBX_mQgNk77Wk2QebA9cKgra0Su2ZSDjIReHc8QJKuf-gHtcJyFIX0I1kaHUdNRbmjhrTM2i5EVokQ; ubid-main=133-1834581-4094037; x-main="v8pymdSmc?mZyoO??ZV5X9VnBaWJ064XPW1uo4wPrlMJqOzapjWNf2wzacd?aXtC"; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiMGQ3NmRiIiwia2V5IjoiaEFMdGhoWGdqcU5qRHd4U2wrZDYyY3M5ZCs0akZLWncyQWFuZzdaMG5yK2YvRGRZcldTTGczckFoMzVkVU5qU3pUQ0lzMzlJeU9IZCtnby9BRy8vdjFUKy9RdHRaUXJZMnk1cDVNbnA3SVJtcXRlNE1DQmFRRGRWS1NTOHFQYm9NUDNsd3BuQzJPZjJyZG1BMWVXMUZUNDNyZ1FSanRkK1VaemV4eEpjb3JwZll6bnJWbVhuNzJDSGRHUTdZVVl4TEJQMWQ5OFBHWk1BLzJHSzhiRUlZNlhyZm1hNHBRMzVta1dsS3BDMEp6ZUJqNDE2Y2hWY2ZVTHhsMkJhdHovZGlDeVE5TlIzZTFsVDhUY0ZuZUorSXF0dDFpMytFcjhaTTduWTBlSUw3aFJqUVErWjMvRkFPTUxrY2kvUDlIdlFxRzVRT0IrejJ3c29TR2hmMmVLY0tBPT0ifQ==; s_nr=1619097147581-New; s_vnum=2051097147582%26vn%3D1; s_dslv=1619097147582; s_sq=%5B%5BB%5D%5D; session-id-time=2082787201l; session-token="3voPf4tRNo/RYAK8fK1frf1aD7SEOMvaFee6HcJuBidLHz4qfoJhUjcL4x2729nwhN/50vHsCw3qyMPuAzLWufsYuNZ/ojYQdcsaBzMAYnWVBJ/hEi1GAVG6ygBVfhk2RtpENUYa3QdB0hSwVGifQ3x6wotRj1uPAokETI8kfzoJLR3S648BZ4M1wRbw3ppYnaDjp1e0t7R/PCUJXIGBDytpHjmShQWyQAuZgsR7TPo60VbTXUtQmdAzGrKaYwqE/p54YSP7Ntk5deWYIAbpmw=="; csm-hit=tb:XDS3FJT93JVQH5T22H65+b-G382SR5EN2TS8TJF7WJ6|1619107560227&t:1619107560227&adb:adblk_no',
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
            'cookie': 'at-main=Atza|IwEBIANS8LCatNBDJo2J_wjq-uigErWwDsgKNm4Xp-0xF5ewndZ5ZMmkP4Txd9OPdzeH-o8Emh-1px30PYMx77-z8aibDpI5KJKDSoNymxtYG8__yg10ZgcMIoHMEdhk2f6rK3ApIIyzWOUfcbm7TE3Y6B_r9XgMDq3YvwxOsjytLCXvezi3JBd13IR8b-4VNSYFBo-MZco58C28__JYZM0_BCAOUO0zGkkX6hJsps6YvGmH2Q; aws_lang=en; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1618496195610-717256; i18n-prefs=USD; lc-main=en_US; regStatus=pre-register; s_campaign=PSM%7Cpsc-2021-ec2_ec2_amd-adop-namer-fb-prospect-itpro-right_size%7CFB%7CPSC-CI%7CEC2%20Adoption%20AMD%7C3128864%7CAustin%7C%7CSC%7Cright_size%7C1200x628%7C%7CPROS%7CPersona%7C%7CAMD%7CEN%7CPA%7CAll%7CIT%20Pro%7CCompute%7CNAMER%7CNAMER%7Cpsm_a134p000006peeSAAQ; s_cc=true; s_eVar60=psm_a134p000006peeSAAQ; s_fid=10D65790BD3E9662-0E495B7B175F9B10; sess-at-main="JYhh8gxiBslO/kqg9CLHKB+7ZINYTzfeMyPRXcV0brQ="; session-id=133-9013249-1407720; skin=noskin; sst-main=Sst1|PQFaGWu7J2h5IuNc2LZKdajtCRijIOMekV60ZkJVaTETGt9Loyl_4O82jLyfB5QYyq6TY-rSsBxVJhk3kuFn_9xsnDC0L9EQqP857UtdoSRpyqj4thl_5zBbMX1d6bHj6RRgin08pEXCVtTX0sKjTXXQAAdwxDUehWJ3zMYqvrbzfdgYUsSfaIi2z4JXly2KCTnJ2x7S1ZPsT01icJ9eaxXiYpplO4zC8oBX_mQgNk77Wk2QebA9cKgra0Su2ZSDjIReHc8QJKuf-gHtcJyFIX0I1kaHUdNRbmjhrTM2i5EVokQ; ubid-main=133-1834581-4094037; x-main="v8pymdSmc?mZyoO??ZV5X9VnBaWJ064XPW1uo4wPrlMJqOzapjWNf2wzacd?aXtC"; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiMGQ3NmRiIiwia2V5IjoiaEFMdGhoWGdqcU5qRHd4U2wrZDYyY3M5ZCs0akZLWncyQWFuZzdaMG5yK2YvRGRZcldTTGczckFoMzVkVU5qU3pUQ0lzMzlJeU9IZCtnby9BRy8vdjFUKy9RdHRaUXJZMnk1cDVNbnA3SVJtcXRlNE1DQmFRRGRWS1NTOHFQYm9NUDNsd3BuQzJPZjJyZG1BMWVXMUZUNDNyZ1FSanRkK1VaemV4eEpjb3JwZll6bnJWbVhuNzJDSGRHUTdZVVl4TEJQMWQ5OFBHWk1BLzJHSzhiRUlZNlhyZm1hNHBRMzVta1dsS3BDMEp6ZUJqNDE2Y2hWY2ZVTHhsMkJhdHovZGlDeVE5TlIzZTFsVDhUY0ZuZUorSXF0dDFpMytFcjhaTTduWTBlSUw3aFJqUVErWjMvRkFPTUxrY2kvUDlIdlFxRzVRT0IrejJ3c29TR2hmMmVLY0tBPT0ifQ==; s_nr=1619097147581-New; s_vnum=2051097147582%26vn%3D1; s_dslv=1619097147582; s_sq=%5B%5BB%5D%5D; session-id-time=2082787201l; session-token="3voPf4tRNo/RYAK8fK1frf1aD7SEOMvaFee6HcJuBidLHz4qfoJhUjcL4x2729nwhN/50vHsCw3qyMPuAzLWufsYuNZ/ojYQdcsaBzMAYnWVBJ/hEi1GAVG6ygBVfhk2RtpENUYa3QdB0hSwVGifQ3x6wotRj1uPAokETI8kfzoJLR3S648BZ4M1wRbw3ppYnaDjp1e0t7R/PCUJXIGBDytpHjmShQWyQAuZgsR7TPo60VbTXUtQmdAzGrKaYwqE/p54YSP7Ntk5deWYIAbpmw=="; csm-hit=tb:XDS3FJT93JVQH5T22H65+b-G382SR5EN2TS8TJF7WJ6|1619107560227&t:1619107560227&adb:adblk_no',
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