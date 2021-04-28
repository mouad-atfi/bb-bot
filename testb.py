import random
import requests
import json
import time
import sys
import pickle
import cookies
#from requests_toolbelt.utils import dump

PATH = 'C:\\Users\\desktop\\Documents\\bot\\chromedriver.exe'

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/89.0.774.75",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"]

proxies = []
with open('./socks.txt') as f:
        proxies = f.read().splitlines()

profiles = [
    {
         'user': 'mouadatfi',
         'email': 'mouad.atfi@gmail.com',
         'address': '{"address":"214-19138 26 Ave, Suite N327198","apartmentNumber":"","city":"Surrey","country":"CA","firstName":"Mouad","lastName":"Atfi","phones":[{"ext":"","phone":"4388660094"}],"postalCode":"V3Z 3V7","province":"BC"',
         'submit': '{"cvv":"349","email":"mouad.atfi@gmail.com","id":"e3820a63-43aa-4dba-a782-fc23656d7d5f","totalPurchasePrice":', 
         'cartId': 'e3820a63-43aa-4dba-a782-fc23656d7d5f', 
         'proxy': '138.197.132.33:8388'
    }, 
    {
         'user': 'meriemcharaf',
         'email': 'soloqxss@gmail.com', 
         'address': '{"address":"214-19138 26 Ave, Suite N330440","apartmentNumber":"","city":"Surrey","country":"CA","firstName":"Meriem","lastName":"Charaf","phones":[{"ext":"","phone":"5148174913"}],"postalCode":"V3Z 3V7","province":"BC"',
         'submit': '{"cvv":"617","email":"soloqxss@gmail.com","id":"2d96fc2d-5694-484e-8c7c-aece9d663371","totalPurchasePrice":', 
         'cartId': '2d96fc2d-5694-484e-8c7c-aece9d663371', 
         'proxy': '134.122.34.159:8388'
    }  
]

products = [      
    {
         'sku': '15166285',
         'name': 'NVIDIA GeForce RTX 3060 Ti 8GB GDDR6 Video Card',
         'offerId': '2b866380-e1f8-4992-ad53-9fad31d51d4e',
         'total': '549.99'     
    },
    {
         'sku': '15078017',
         'name': 'NVIDIA GeForce RTX 3070 8GB GDDR6 Video Card - Only at Best Buy',
         'offerId': 'a16ece97-cf5d-4843-9901-55369d36f036',
         'total': '679.99' 
    },
    {
         'sku': '15084753',
         'name': 'EVGA GeForce RTX 3080 XC3 Ultra Gaming 10GB GDDR6X Video Card',
         'offerId': '182a59a8-2b28-4c19-8255-4a5d54978243',
         'total': '1149.99'
    },
    {
         'sku': '14953248',
         'name': 'ASUS TUF Gaming NVIDIA GeForce RTX 3080 10GB GDDR6X Video Card',
         'offerId': 'b30ccb4b-c7b9-40b3-89bc-1c5c5e055c74',
         'total': '1199.99' 
    },  
    {
         'sku': '14969729',
         'name': 'ASUS TUF Gaming GeForce GTX 1660 Super OC 6GB DDR6 Video Card',
         'offerId': 'baf1befb-6ab2-49f6-a5e3-21fa1cb70797',
         'total': '369.99' 
    },
    {
         'sku': '14193869',
         'name': 'Corsair TM30 Performance Thermal Paste',
         'offerId': 'e90f8974-b6bf-43aa-9175-f5e729183a2c',
         'total': '10.99' 
    }                        
]



            
def addtocart(proxy,cartId,sku):

    cookies = {
      'enabled': '1',
      'ReturnUrl': 'https://www.bestbuy.ca/',
      'surveyOptOut': '1',
      'CS_Culture': 'en-CA',
      'cartId': cartId,
    }

    headers = {
      'authority': 'www.bestbuy.ca',
      'region-code': 'BC',
      'content-type': 'application/json',
      'postal-code': 'V3Z',
      'accept-language': 'en-CA',
      'sec-ch-ua-mobile': '?0',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
      'accept': '*/*',
      'origin': 'https://www.bestbuy.ca',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://www.bestbuy.ca/en-ca/product/' + sku,
    }

    data = '{"id":"' + cartId + '","lineItems":[{"sku":"' + sku + '","quantity":1}]}'
    response = requests.post('https://www.bestbuy.ca/api/basket/v2/baskets', headers=headers, cookies=cookies, data=data, proxies=proxy)


def order(s,token,proxy,email,name,offerid,sku,total,address):
    #order call
    headers = {
    'authority': 'www.bestbuy.ca',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'x-tx': token,
    'accept-language': 'en-ca',
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/json',
    'accept': 'application/vnd.bestbuy.checkout+json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'origin': 'https://www.bestbuy.ca',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.ca/checkout/?qit=1',
    }
    data = f'{{"email":"{email}","lineItems":[{{"lineItemType":"Product","name":"{name}","offerId":"{offerid}","quantity":1,"sellerId":"bbyca","sku":"{sku}","total":{total}}}],"shippingAddress":{address}}}}}'
    order_call = s.post('https://www.bestbuy.ca/api/checkout/checkout/orders', headers=headers, data=data, proxies=proxy)
    print(order_call)

def submit(s,token,proxy,checkout,total):            
    #Submit call
    headers = {
    'authority': 'www.bestbuy.ca',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'x-tx': token,
    'accept-language': 'en-ca',
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/json',
    'accept': 'application/vnd.bestbuy.checkout+json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'origin': 'https://www.bestbuy.ca',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.ca/checkout/?qit=1',
    }
    a = total
    p = 0.05
    g = 0.07
    f = float(a)
    price = round((f + (f*p) +(f*g)), 2)

    data = f'{checkout}{price}}}'
    submit_call = s.post('https://www.bestbuy.ca/api/checkout/checkout/orders/submit', headers=headers, data=data, proxies=proxy)
    print(submit_call.text)
    #resp = session.send(prepped, verify=False)

def checkout(sku):
    for i in profiles:
        for x in products:
            sku = sku
            user = (i['user'])
            email = (i['email'])
            address = (i['address'])
            checkout = (i['submit'])
            cartId = (i['cartId'])
            proxy = (i['proxy'])

            isku = (x['sku'])
            name = (x['name'])
            offerid = (x['offerId'])
            total = (x['total'])

            proxy = { 'https': 'socks5://'+proxy}   
            s = requests.session()

            with open(user, 'rb') as f:
                  s.cookies.update(pickle.load(f))   
            token = s.cookies['tx']

            if sku == isku:
                addtocart(proxy,cartId,sku)
                order(s,token,proxy,email,name,offerid,sku,total,address)
                countdown(1) 
                submit(s,token,proxy,checkout,total)


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
                    ('skus', '15166285|15078017|15084753|14953248|15229237'),
                )

                response = requests.get('https://www.bestbuy.ca/ecomm-api/availability/products', headers=headers, params=params, proxies=proxy, timeout=5)
                response.raise_for_status()
                decoded_data = response.content.decode('utf-8-sig')

                match = json.loads(decoded_data)
                print(response.elapsed.total_seconds())
                for i in range(5):
                    status = str(match['availabilities'][i]['shipping']['status'])
                    quantity = float(match['availabilities'][i]['shipping']['quantityRemaining'])
                    sku = str(match['availabilities'][i]['sku'])
                    print(status, quantity, sku)
                    #if status != 'InStock' and sku != '14969729' and status == 'SoldOutOnline':
                          #print('refresh cookies')
                          #cookies.main()
                          #continue
                    if quantity >= 10:
                          #addtocart(sku)    
                          checkout(sku)
                          break    
                #countdown(3)    

            except requests.exceptions.RequestException as err:
                print ("Oops: Something Else",err)
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
        cookies.main()
        checkBB()


if __name__ == "__main__":
    main()
