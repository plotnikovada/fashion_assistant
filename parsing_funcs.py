#функции парсинга
import requests
import json
import shutil

wb_headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&search=%D0%B1%D0%B5%D0%BB%D0%B0%D1%8F%20%D1%80%D1%83%D0%B1%D0%B0%D1%88%D0%BA%D0%B0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'x-queryid': 'qid1060877181170836523520240325194128',
    }


def parse_top_wildberriest(text):
    '''
        надо: 
        - засунуть текст в ссылку
        - добавить хедеры и сходить по этой ссылке в WB
        - распарсить ответ и взять топ10

    '''
    wb_params = {
        'ab_testing': 'false',
        'appType': '1',
        'curr': 'rub',
        'dest': '-1257786',
        'query': text,
        'resultset': 'catalog',
        'sort': 'popular',
        'spp': '30',
        'suppressSpellcheck': 'false',
    }

    response = requests.get('https://search.wb.ru/exactmatch/ru/common/v5/search', params=wb_params, headers=wb_headers)
    # url = f"https://www.wildberries.ru/catalog/{}/detail.aspx"
    products = []
    try:
        response = response.json()
        for i, item in enumerate(response['data']['products']):
            if i == 10:
                break
            url = f"https://www.wildberries.ru/catalog/{item['id']}/detail.aspx"
            name = item['name']
            price = float(item['sizes'][0]['price']['total']) / 100
            vol = item['id'] // 100000
            host = ""
            if (vol >= 0 and vol <= 143):
                host = "//basket-01.wbbasket.ru"
            elif (vol >= 144 and vol <= 287):
                host = "//basket-02.wbbasket.ru"
            elif (vol >= 288 and vol <= 431):
                host = "//basket-03.wbbasket.ru"
            elif (vol >= 432 and vol <= 719):
                host = "//basket-04.wbbasket.ru"
            elif (vol >= 720 and vol <= 1007):
                host = "//basket-05.wbbasket.ru"
            elif (vol >= 1008 and vol <= 1061):
                host = "//basket-06.wbbasket.ru"
            elif (vol >= 1062 and vol <= 1115):
                host = "//basket-07.wbbasket.ru"
            elif (vol >= 1116 and vol <= 1169):
                host = "//basket-08.wbbasket.ru"
            elif (vol >= 1170 and vol <= 1313):
                host = "//basket-09.wbbasket.ru"
            elif (vol >= 1314 and vol <= 1601):
                host = "//basket-10.wbbasket.ru"
            elif (vol >= 1602 and vol <= 1655):
                host = "//basket-11.wbbasket.ru"
            elif (vol >= 1656 and vol <= 1919):
                host = "//basket-12.wbbasket.ru"
            elif (vol >= 1920 and vol <= 2045):
                host = "//basket-13.wbbasket.ru"
            elif (vol >= 2046 and vol <= 2189):
                host = "//basket-14.wbbasket.ru"
            else:
                host = "//basket-15.wbbasket.ru"
            part = item['id'] // 1000
            id = item['id']
            pic_url = f'https:{host}/vol{vol}/part{part}/{id}/images/c516x688/1.jpg'
            response = requests.get(pic_url, stream=True)
            with open(f"pic{id}.jpg", 'w') as а:
                pass
            with open(f"pic{id}.jpg", 'wb') as a:
                shutil.copyfileobj(response.raw, a)
            products.append([url, name, price, f"/home/bigsister/fashion_assistant/pic{id}.jpg"])
        return products
    except:
        return []

def parse_top_lamoda(text):
    '''
        надо: 
        - засунуть текст в ссылку
        - добавить хедеры и сходить по этой ссылке в lamoda
        - распарсить ответ и взять топ10

    '''
    text = text.replace(' ', '+')
    response = requests.get(f'https://www.lamoda.ru/catalogsearch/result/?q={text}&page=1&json=1')
    try:
        response = response.json()
        data = response['payload']['products']
        products = []
        for i, item in enumerate(data):
            if i == 10:
                break
            url = f"https://www.lamoda.ru/p/{item['sizes'][0]['full_sku']}"
            pic_url = f"https://a.lmcdn.ru/img600x866{item['gallery'][0]}"
            name = item['name']
            price = float(item['price_amount'])
            products.append([url, name, price, pic_url])
        return products
    except:
        return []

def parse_top_aliexpress(text):
    '''
        надо: 
        - засунуть текст в ссылку
        - добавить хедеры и сходить по этой ссылке в aliexpress
        - распарсить ответ и взять топ10

    '''

    cookies = {
        'JSESSIONID': '1FE4AE725953D70513E03D65554667B6',
        'acs_usuc_t': 'acs_rt=336bfdc6665d4678adcbaf83ebc8c26f&x_csrf=1ep2lz6yarcer',
        'aep_usuc_f': 'b_locale=ru_RU&c_tp=RUB&region=RU&site=rus&province=917477830000000000&city=917477836880000000',
        'aer_abid': 'f12ed5db9aeb9c63..3afe865287be0dfe',
        'aer_ec': 'fCrpXaTU9Fd065WTJ8K9PHhB+mDz03ZlTVVVum8oTURsBCxfKRey8N8OtiZMiVY39jjV633XTcwiAYtiweaOrguz7tZ27NQhYcNIuz9Kdew=',
        'aer_rh': '842297271',
        'ali_apache_id': '33.22.74.14.1712589525487.494936.5',
        'intl_common_forever': 'YuWrJ29z5wlIHWNW6y2Y8nAp/mxIyUx+pN9+YLCJMABprUj1ZtuYGw==',
        'xman_f': 'uBlNAFhcW5TyNGkBCVNys2F61zPK03Rx05ql1gtfhzeObgMTvwCWGQ5itGVpxUkYM85CeBLu9COugRGX5ZJHpHZwbXISKUg5+J1+PBKsaBtOW4sirHnQGA==',
        'xman_t': 'paR84K4BrCc+zqi37qQLlDFE2bb2IzVCYYRXkHrlGL3+kH1kmm6HAEibfIRai7KV',
        'xman_us_f': 'x_locale=ru_RU&x_l=0&acs_rt=80a06ba76cf84056b0da36f236dce317',
    }

    text = text.replace(' ', '+')
    data = {"keyword" : text,
            "count" : "11",
            "offset" : "0"}
    response = requests.post('https://aliexpress.ru/aer-webapi/v2/recommend', json=data, cookies=cookies, headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    })
    try:
        data = response.json()['data']['snippets']
        products = []
        for i, item in enumerate(data):
            if i == 10:
                break
            ref = item['productUrl']
            url = f'https:{ref}'
            ref_pic = item['imgSrc']
            pic_url = f'https:{ref_pic}'
            name = item['productTitle']
            price = item['finalPrice'][:-2].strip()
            products.append([url, name, price, pic_url])
        return products
    except:
        return []
