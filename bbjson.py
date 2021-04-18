from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time
import os
import sys
import subprocess
import json
import multiprocessing
import random
import requests

PATH = 'C:\\Users\\mouad.atfi\\Documents\\bot\\chromedriver.exe'

skus = {'nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/': '15166285',
        'nvidia-geforce-rtx-3070-8gb-gddr6-video-card-only-at-best-buy/': '15078017',
        'evga-nvidia-geforce-rtx-3060-ti-ftw3-ultra-8gb-gddr6-video-card/': '15229237',
        'evga-geforce-rtx-3070-xc3-ultra-8gb-gddr6-video-card/': '15147122',
        'evga-nvidia-geforce-rtx-3060-xc-12gb-dddr6-video-card/': '15318940',
        'evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6x-video-card/': '15084753',
        'asus-tuf-gaming-geforce-gtx-1660-super-oc-6gb-ddr6-video-card/': '14969729',
        #'asus-tuf-gaming-nvidia-geforce-rtx-3070-2x-oc-8gb-gddr6-video-card/': '15053087',
        #'asus-dual-nvidia-geforce-rtx-3070-2x-oc-8gb-gddr6-video-card/': '15053086',
        #'asus-tuf-gaming-geforce-rtx-3060-ti-oc-8gb-gddr6-video-card/': '15201200',
        #'asus-tuf-gaming-geforce-rtx-3060-oc-12gb-gddr6x-video-card/': '15309513',
        #'msi-nvidia-geforce-rtx-3070-ventus-3x-oc-8gb-gddr6-video-card/': '15038016',
        #'msi-nvidia-geforce-rtx-3080-ventus-3x-10gb-gddr6x-video-card/': '14950588',
        'asus-tuf-gaming-nvidia-geforce-rtx-3080-10gb-gddr6x-video-card/': '14953248',
        'asus-rog-strix-nvidia-geforce-rtx-3080-10gb-gddr6x-video-card/': '14954116',
        }

   

def checkBB(position, a, event):

    #options = webdriver.ChromeOptions()
    options = uc.ChromeOptions()
    options.headless=True
    proxy = a
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
    driver.set_page_load_timeout(5)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    while True:
        for y in skus.keys():
            try:
                t0= time.perf_counter()
                sku = skus[y]
                #print(sku)
                driver.delete_all_cookies()
                url = f'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&postalCode=E5S&skus={sku}'
                driver.get(url)
                #print (url)
                #print (driver.page_source)
                webElement = driver.find_element_by_tag_name('body')
                match = json.loads(webElement.text)
                t1 = time.perf_counter() - t0
                #print ('\r{:.2f} sec'.format(t1))                
                for value in match['availabilities']:
                    status = value['shipping']['status']
                    quantity = value['shipping']['quantityRemaining']
                    print(sku, quantity, '{:.2f} sec'.format(t1))
                    if quantity > 40:
                        addtocart(sku)
                        pushmessage(sku)
                        event.set()
            except Exception as e:

                print('==========>>>>>>>>', proxy)
                print(e)                
                driver.quit()    
        time.sleep(40)

def pushmessage(sku):
   
    user = "Default"
    path_autorun_html = 'c:\\Users\\mouad.atfi\\Documents\\bot\\ui.vision.html'
    browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe --profile-directory="{}" %s'.format(user)
    
    args = r'file:///' + path_autorun_html + '?macro=bb-paypal&direct=1&closeRPA=1&nodisplay=1'
    #proc = subprocess.Popen([browser_path, args], shell=True)
    #print(args)
    webbrowser.get(browser_path).open(args)
    
    msg = 'https://www.pushsafer.com/api?k=EmsCLL0BTspCz2b7Upgl&pr=2&m=bb'
    response2 = requests.get(msg)


def addtocart(sku):

    profile = "e3820a63-43aa-4dba-a782-fc23656d7d5f"
    sku = sku

    cookies1 = {
        'enabled': '1',
        'ReturnUrl': 'https://www.bestbuy.ca/',
        'surveyOptOut': '1',
        'CS_Culture': 'en-CA',
        'cartId': profile,
    }

    headers1 = {
        'authority': 'www.bestbuy.ca',
        'region-code': 'BC',
        'content-type': 'application/json',
        'postal-code': 'V3Z',
        'accept-language': 'en-CA',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'accept': '*/*',
        'origin': 'https://www.bestbuy.ca',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bestbuy.ca/en-ca/product/' + sku,
    }

    data1 = '{"id":"' + profile + '","lineItems":[{"sku":"' + sku + '","quantity":1}]}'

    response1 = requests.post('https://www.bestbuy.ca/api/basket/v2/baskets', headers=headers1, cookies=cookies1, data=data1)


    cookies2 = {
        'dtCookie': '1$1F4B84C6FC98577139CF7CBB87E2D13CC|ea7c4b59f27d43eb|0',
        'ai_user': 'xa4Zqi/jC+b8rk36IUdGRC|2021-04-09T17:11:49.835Z',
        'clientId': 'GoSJzZhLWhV8oX20',
        'surveyOptOut': '1',
        'ReturnUrl': 'https://www.bestbuy.ca/',
        'enabled': '1',
        'AMCVS_D6E638125859683E0A495D2D%40AdobeOrg': '1',
        'fdb7491a5cc3d693edd0926b3a48659f': 'fbf513653e7a2e1ffefe994e06261b60',
        'tia': '0d932bfc512fb305e72658b9ad345d041eb9985e5c40cdfd95fb5e07f37cbc01',
        '4b92e78b2a2c24b9f5aaf8ff1d99b6ef': 'f78cc4904cb5737cbe293e4b94430e4a',
        'CS_Culture': 'en-CA',
        'lastUsedLocations': '%7b%22shippingLocation%22%3a%7b%22city%22%3a%22Laval%22%2c%22postalCode%22%3a%22H7P%22%2c%22region%22%3a%22QC%22%7d%2c%22pickupLocation%22%3a%7b%22city%22%3a%22Laval%22%2c%22postalCode%22%3a%22H7P%22%2c%22region%22%3a%22QC%22%7d%7d',
        'criteoVisitorId': '6985ce09-f3a6-41d5-97cf-ede834dd6e18',
        '14455e30937321eff175c1c41b837a02': '06e6ecd517dfae48da95c6c5a86175a0',
        '47236a0d189c10314faac13e28785259': '4c59c9d16c15721ba53a253a51eb5dc7',
        'e13d5bc268331a905ff9fe23a1820225': '418038c55c2cc6e31edcbeb6f8b98ec3',
        'd610aaaf3438bb52dd98fd19edd17a8c': '4ccf4c563b1a77f85d4c78d565cf0413',
        '6b687dd1c7f018d0fd4348da771427e5': 'b5916803aaf5b52a7f988979cb289e3f',
        'cid': '%7B%22email%22%3A%22mouad.atfi%40gmail.com%22%2C%22id%22%3A%22%7Be3820a63-43aa-4dba-a782-fc23656d7d5f%7D%22%2C%22firstName%22%3A%22mouad%22%2C%22lastName%22%3A%22Atfi%22%2C%22authenticationState%22%3A%22AUTHENTICATED%22%7D',
        'tir': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7ZTM4MjBhNjMtNDNhYS00ZGJhLWE3ODItZmMyMzY1NmQ3ZDVmfSJ9.G6P5BK4FDd8J43PqcPLETTZ8OqKGxx3bOIyd8EA3fi4',
        'tx': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlZDZiYmVjYy1hYjAyLTQyNmQtYmJmZC0yZjAxNWMxNjhhNTcifQ.jyTGg-F_u8U82Z7iE-qSguSSn7qPfvNKrrPwamm7jA8',
        'bm_sz': 'F369E4A130C97D6B5ADE40B7102D26E5~YAAQnxTorBCKznd4AQAArVryxQtCIvpKNwLcx74YegqhMbLoGIVTP5XeJKV9HAqrkercT8x6GgS8k/8B/me/7koIZ5wkdiZNk8wXdRGNJHsv34L6RdL1moDyRuPdwdRtoKThreEL/mrlmNfmu6XMC4PNeYUaHE+jP3V9n1KaLFv63huQkoCUhLWGKNuo5Zmj1WAfwoyl00ZDZLojMT2txqPDV9JUqx6HrucZn01VJDpgB61769+8fB6eXTPyW5it77gu5W7/RTSty1hlYiHE4LNMpAb7s9O8yjAr',
        '_abck': '08E84068B3B0413F199BCF17B97E6AA8~0~YAAQnxTorBGKznd4AQAArVryxQXfNKcvpSzgd8wpGgcS6P0RT7RyRBCCqZ5OGo7qPIUdpEQTa+nYtPYUQ9v4RpIv1LTIQvjQS67uzfRFq+1b9jXoOw1T7NEJs48UnwFYgtxkbcPHJFCCEvYCyvo0dIDLqrAFfaa9Krdoxv3GIAPp7eF98IOAKISNc2gvDJV/++b142jbq+Rr8UfVNTydftAa1A9xfzcW95M1i4lf2ch3L6k02EkSRONRIdTb86nLWccdQFce7R/xIHMrMKsphfLfwfr1gSfrzH2CJfP22qCuubSWda09KWoHP+PTCvcfobRCklkubJsKb+0M3qM6z4Osl0WR536/LUNAMY/ktnEqA+AxpQbRObYp782pLdral8Q+Sz2gdDNAS0iNthI2GNOJLSdXSq1H0U+2sZyROTE8UkUGUNY7RFrjFNceLUY=~-1~-1~-1',
        'BVImplmain_site': '18193',
        'ak_bmsc': '9FDBFD077E524D6C27D3D364ABCDD470ACE8147C233A00002E6C7460EEC0C068~pli9Vko2xgJudNAHg2vhyd5V6ZjK8sYLXmWY69js2xgJGYbB9LTByjmBxTwO3b+TjirtW6bd1dUOG6kJqfCmfTR0q0BBe4bJYqIa2zwa3Hx+6mUzX2KPj5DyLcE6DBiEQKDKDP/imvwn25I3NQWo8OogFmq4NsZ5VCVBclnsDC5x6cq0Sd1otElH5zVwjtmMeoiOnllmzbqIhEUEHUWIDz/ZIa0KkzuHQ9UCbPy2eyjNU=',
        'ta': '8156b954-d977-4d72-8199-3f6ffc0466b1',
        'tr': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzZTBmNGIxZS0wNjc1LTQwMmItYTNjNi1kOTlhNDIwNzgxZjkiLCJhY2Nlc3NfdG9rZW4iOiI4MTU2Yjk1NC1kOTc3LTRkNzItODE5OS0zZjZmZmMwNDY2YjEiLCJleHAiOjE2MjM0MjY2MzB9.LC2Ld4KwzDFU_dFf_YDWg49czBzEcVdw8P6M3EL7O2g',
        'ti': 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1vdWFkLmF0ZmlAZ21haWwuY29tIiwiYWNjZXNzX3Rva2VuIjoiODE1NmI5NTQtZDk3Ny00ZDcyLTgxOTktM2Y2ZmZjMDQ2NmIxIiwic3ViIjoie2UzODIwYTYzLTQzYWEtNGRiYS1hNzgyLWZjMjM2NTZkN2Q1Zn0iLCJleHAiOjE2MTgyNDgwMzB9.JMWFMG7So_whyN_c3C-iIVBGOFW5daft1GbovHjU6tw',
        'AMCV_D6E638125859683E0A495D2D%40AdobeOrg': '-1303530583%7CMCIDTS%7C18729%7CMCMID%7C91494251778150006132009545553870500528%7CMCAID%7CNONE%7CMCOPTOUT-1618249808s%7CNONE%7CvVersion%7C3.3.0',
        'mbox': 'session#7e2f6bb8845a473385f3aa0d508dcd23#1618244469',
        'QueueITAccepted-SDFrts345E-V3_prebf012020browse': 'EventId%3Dprebf012020browse%26QueueId%3Da0aec8b2-893c-4a1e-a6e7-7e1ce91d4fe3%26RedirectType%3Dsafetynet%26IssueTime%3D1618242608%26Hash%3D4420b264d3491750e88d6c089e7384a24c2c8001ac31532736337882c5b2b07b',
        'bm_mi': 'A3E7FA92E020EE3E156014E3259F611F~2RfKoZEvECi+MzImphgK67kemvcjWnN2Ix+RzEAtQ0eNbKBcE/tdk5pAJuNEHqThjRuXXCwzT4ts5kWcyckMZZGq5GAmhTYYywnIeqMSRF2Z226ugZR0/pF2gxIoRfvKK86InDTagxLHGvl1/GT/F5UAvMFCNaEGq54qeqKevDMQyWqcJTcFD6c3EEJw9peKlV8oCfhfTH1g8NokQKF6HHI6wM3i8m1CR/dG+CShgPY=',
        'nps': '{"currentUrlPath":"/en-ca","hasSurveyBeenDisplayed":false,"heartBeat":1618242978,"isInSampling":false,"pageViewCount":2,"surveyLastDisplayed":1649522516}',
        'bm_sv': '96F76785AE8C7F34F724B9BC1C58586D~elKqYP/btRc3uHeinNYWAX1wmxl+mxyLuc8rvmvZsXc3IeBSmHkJRGBzH2+EVnClTKk3ue55AJ3XAu6WGtVmp81PEKmvGcClEQ2234AxoHH/r90kVZbw7pPsuYaSZfshcPU6L6aRVH0f9eHSIFDtCVADtcSiBG/JXh54Ixf0nMA=',
        'ai_session': 'j7sftnSYHOxN4C/sBOq/W7|1618242607978|1618242988186',
        'cartId': 'e3820a63-43aa-4dba-a782-fc23656d7d5f',
    }

    headers2 = {
        'authority': 'www.bestbuy.ca',
        'region-code': 'ON',
        'postal-code': 'M5G 2C3',
        'accept-language': 'en-CA',
        'sec-ch-ua-mobile': '?0',
        'authorization': 'Bearer 8156b954-d977-4d72-8199-3f6ffc0466b1',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bestbuy.ca/en-ca',
    }

    response = requests.get('https://www.bestbuy.ca/api/basket/v2/baskets/e3820a63-43aa-4dba-a782-fc23656d7d5f', headers=headers2, cookies=cookies2)





    url = "https://www.bestbuy.ca/api/checkout/checkout/orders/submit"

    cookies3 = {
        'bm_sz': '5BA53A140B4A2D4CD09BBB9B33D3C2A7~YAAQ1hTorCwdq7F4AQAAYk2etwtqkNqfKnFboB4JNgd7M1cpECnkaBtR1W9BcT6bWmAnLaYT4DG0h665xA0WNxNPT4/nit/pqonoKhljUCDRFH7quNajJhVu7RKpMzOnvHcKVTdOy4ZRcvemCX5KkNe14Rs13OkMweiTNifHh9gXOYxi1udzQdEJqOhQoEyf4YUqjsjVNh1IF0g4816N5Nt7Ff86mF+CYxqcK1Ovnj+boZYsYgxYwZY7+5lzMRYfSFpceBnY3hEqCKhjybVajNJW+nXPGcb6VxKlcGU=',
        'dtCookie': '1$1F4B84C6FC98577139CF7CBB87E2D13CC|ea7c4b59f27d43eb|0',
        'ai_user': 'xa4Zqi/jC+b8rk36IUdGRC|2021-04-09T17:11:49.835Z',
        'clientId': 'GoSJzZhLWhV8oX20',
        'enabled': '1',
        'ReturnUrl': 'https://www.bestbuy.ca/',
        'surveyOptOut': '1',
        'AMCVS_D6E638125859683E0A495D2D%40AdobeOrg': '1',
        'fdb7491a5cc3d693edd0926b3a48659f': 'fbf513653e7a2e1ffefe994e06261b60',
        'tia': '0d932bfc512fb305e72658b9ad345d041eb9985e5c40cdfd95fb5e07f37cbc01',
        'cid': '%7B%22email%22%3A%22mouad.atfi%40gmail.com%22%2C%22id%22%3A%22%7Be3820a63-43aa-4dba-a782-fc23656d7d5f%7D%22%2C%22firstName%22%3A%22mouad%22%2C%22lastName%22%3A%22Atfi%22%2C%22authenticationState%22%3A%22AUTHENTICATED%22%7D',
        'tir': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7ZTM4MjBhNjMtNDNhYS00ZGJhLWE3ODItZmMyMzY1NmQ3ZDVmfSJ9.G6P5BK4FDd8J43PqcPLETTZ8OqKGxx3bOIyd8EA3fi4',
        '_abck': '08E84068B3B0413F199BCF17B97E6AA8~0~YAAQ1hTorNceq7F4AQAAdqyetwXWdFsg1QscHJ0fSS4TF9tMn0cIz62SyUm7eU3lofe9o4ua9YxRLeUOP21V8dJLV5gn70zDX+tIMKbk5xPc/grVd9wMWcxRgF+aKCqien4q4jt+hPvpC4MFwuk/h105ycL7mf/DFCrhhZ2n+ojPzKKR2bulndhr/piOolsylYxx/iptqtlyBlXzn6HSztIOB3fVXL6kDfAx3qLd/1zi+ylppAeUm8y+Xq5OeWY342+90LMLDUJsupjKpQ9EHiwZr6gN/YTVldQaxqzFBiM7SwoVXMS94yejuW7FAs3RxgBg6aQUOuzCrdAAF/vWY3MKW5CaIWoGotcQ8zqK3z6RP4ubOalizjPOJk0WSX6rVDeeeYptNi7RnOEbLk540PhZlndGeuyfF0V0nyUMHi3stOp1qIfihVi4jFXOPnw=~-1~-1~-1',
        '4b92e78b2a2c24b9f5aaf8ff1d99b6ef': 'f78cc4904cb5737cbe293e4b94430e4a',
        'CS_Culture': 'en-CA',
        'lastUsedLocations': '%7b%22shippingLocation%22%3a%7b%22city%22%3a%22Laval%22%2c%22postalCode%22%3a%22H7P%22%2c%22region%22%3a%22QC%22%7d%2c%22pickupLocation%22%3a%7b%22city%22%3a%22Laval%22%2c%22postalCode%22%3a%22H7P%22%2c%22region%22%3a%22QC%22%7d%7d',
        'ak_bmsc': '67BD3C3E1CBFF2229A42A6AA232AA1EBACE814D555130000F8B6706008E5657D~plRXN59dbh2uqQ19UJJCAgPDnUw+M8yQ6TPoCgbTHjSBN1niwegvd7tM7vdaL3hoB4VAlElR8slUzCfv6bcO2kTSHOxC+wP8TL+xYoLY7c9NYHsTXyvs/Kd5s5mKlOSPe/IaBh3Elw8WVPM54VQzhfxBAIH+S4SGkimVoThYc3vA9HCCv4Fnruu3OyZUj9NHfpI2WTW5UTtxUSbAFLdbuUAu3S9/1E4l4ySNDbxG4v2z8=',
        'AMCV_D6E638125859683E0A495D2D%40AdobeOrg': '-1303530583%7CMCIDTS%7C18727%7CMCMID%7C91494251778150006132009545553870500528%7CMCAID%7CNONE%7CMCOPTOUT-1618006809s%7CNONE%7CvVersion%7C3.3.0',
        'criteoVisitorId': '6985ce09-f3a6-41d5-97cf-ede834dd6e18',
        'ta': 'ddc87e44-616e-45ad-abc9-9139f7fa0185',
        'tr': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI3ZWI4YzAzMi1mNDg5LTQyNjYtOTg3NS1jYjRhNWVmNjRkMzkiLCJhY2Nlc3NfdG9rZW4iOiJkZGM4N2U0NC02MTZlLTQ1YWQtYWJjOS05MTM5ZjdmYTAxODUiLCJleHAiOjE2MjMxODM2MTV9.O9v7ZS3pyoX8T-B4TuKG0FV7miOmX5kd_Zd_De_YsH8',
        'ti': 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1vdWFkLmF0ZmlAZ21haWwuY29tIiwiYWNjZXNzX3Rva2VuIjoiZGRjODdlNDQtNjE2ZS00NWFkLWFiYzktOTEzOWY3ZmEwMTg1Iiwic3ViIjoie2UzODIwYTYzLTQzYWEtNGRiYS1hNzgyLWZjMjM2NTZkN2Q1Zn0iLCJleHAiOjE2MTgwMDUwMTV9.PPMmOMexWncxQhjeDPrE-8ZhSjNDl5XaOj3eONagCak',
        'mbox': 'session#21131636c56d4c8a9b8a9098b1113679#1618001471',
        'QueueITAccepted-SDFrts345E-V3_prebf012020browse': 'EventId%3Dprebf012020browse%26QueueId%3Dc87df1ba-25fe-4cb0-9009-9b33bbe4a15f%26RedirectType%3Dsafetynet%26IssueTime%3D1617999611%26Hash%3D9d0be4a5b546bcae13928e78d843c81de0a33145079e897a73362f1e5641a6b6',
        'ai_session': 'Qux9rnBHZRYztEvYemtZ5h|1617999610534|1617999805865',
        'nps': '{"currentUrlPath":"/en-ca/basket","hasSurveyBeenDisplayed":false,"heartBeat":1617999807,"isInSampling":false,"pageViewCount":0,"surveyLastDisplayed":1649522516}',
        'tx': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwMGZkYTNhMy1jYzk3LTRjMmEtYjgxNy02ZGFmMTQ4ZWFjOGIifQ.36JYFgS14JACFFy384qXYJ_eH_TbdmxTNRwBJatMW20',
        'bm_mi': '56C97007AE710A4D67A6497A1FDEED61~ZRGtDahNKXJhYs1udTbOTmh/QybUWipg1ONxXsPicIuEo75lZq+rzi8RVrINP2yzNwh72nqmAQJMawC3FfulHLnxyHk3FTnroiB1YCsCL/Oz0mmamIpwppeyuL/IiRBW7hyCqav9psDi/lz207pu8iqtSoPuV9WXINcNge9fsuB28tFZxZ2jnKhgB/D1uhF/ZOz/dkNbEum2qfYamWeF5ab4caaSdg7cbUYXnqzARdo=',
        '14455e30937321eff175c1c41b837a02': '06e6ecd517dfae48da95c6c5a86175a0',
        'cartId': 'e3820a63-43aa-4dba-a782-fc23656d7d5f',
        '47236a0d189c10314faac13e28785259': '4c59c9d16c15721ba53a253a51eb5dc7',
        'bm_sv': 'BA4C19B4626EADEB37C3D855B7DAA1B5~9F2UI7PPCvK7Rymo8FA50LX0/jRyaSQodxbO6nih+KmhPenouHe0kGrSdHqdOgcFKC6z0HeGB0SCrmTk9+PPcrLZaxDsbRyLr/nLQn3jLaP/EdS+i40iW6MdlTHNpkx2vjOp8owPmSVjL2L2aWa9C0YccDDBhut1b6+rmf6ccTE=',
    }

    headers3 = {
        'authority': 'www.bestbuy.ca',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'x-tx': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwMGZkYTNhMy1jYzk3LTRjMmEtYjgxNy02ZGFmMTQ4ZWFjOGIifQ.36JYFgS14JACFFy384qXYJ_eH_TbdmxTNRwBJatMW20',
        'accept-language': 'en-ca',
        'sec-ch-ua-mobile': '?0',
        'authorization': 'Bearer ddc87e44-616e-45ad-abc9-9139f7fa0185',
        'content-type': 'application/json',
        'accept': 'application/vnd.bestbuy.checkout+json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'origin': 'https://www.bestbuy.ca',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bestbuy.ca/checkout/?qit=1',
    }

    data3 = '{"cvv":"349","email":"mouad.atfi@gmail.com","id":"e3820a63-43aa-4dba-a782-fc23656d7d5f","totalPurchasePrice":' + price + '}'


    resp = requests.post(url, headers=headers3, cookies=cookies3, data=data3)

    print(resp.text)


def main():

    #response = requests.get("https://proxy.webshare.io/proxy/list/download/eehomixvnaqhykpqgjxcrqjauhjzdfwtatfxsxiw/-/socks/port/direct/")
    #proxies = response.text.split('\n')
    with open('./socks.txt') as f:
        proxies = f.read().splitlines()

    p= multiprocessing.Pool(60) 
    m = multiprocessing.Manager()
    event = m.Event()
    for i, proxy in enumerate(proxies, 1):
        p.apply_async(checkBB , args=(i, proxy, event))
        time.sleep(3)
    p.close()
    event.wait()
    p.terminate()


if __name__ == "__main__":
    main()