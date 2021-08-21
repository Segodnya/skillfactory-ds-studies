import requests
from bs4 import BeautifulSoup
import time
import json
import csv
import re
import pandas as pd
from multiprocessing import Process
from google.colab import drive
drive.mount('/drive')


def collect_data(ad):
    car_url = ad
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    cookies = {'autoru_gdpr': '1'}

    response = requests.get(car_url, headers=headers, cookies=cookies)
    response.encoding = 'utf-8'
    page = BeautifulSoup(response.text, 'lxml')
    try:
        json_data = json.loads(page.find('script', type="application/ld+json").string)
    except:
        return None

    try:
        catalog_url = page.find('a', class_='Link SpoilerLink CardCatalogLink SpoilerLink_type_default').get('href')
        response_catalog = requests.get(catalog_url, headers=headers)
        response_catalog.encoding = 'utf-8'
        page_catalog = BeautifulSoup(response_catalog.text, 'lxml')  # html.parser
    except:
        page_catalog = None

    try:
        json_data_catalog = json.loads(page_catalog.find('script', type="application/json", id='initial-state').string)
    except:
        json_data_catalog = {}

    try:
        json_data_equip = json.loads(page.find('script', type="application/json", id='initial-state').string)
    except:
        json_data_equip = None

    try:
        json_data['description'] = json_data['description'].replace('\n', ' ')
        json_data['description'] = re.sub('\W+', ' ', json_data['description'])
    except:
        json_data['description'] = ''

    try:
        options_dict = json_data_catalog['state']['compare']['selected'][0]['options']
        options_list = [key for key in list(options_dict.keys()) if options_dict[key] == 1]
    except:
        options_list = []

    try: bodyType = json_data['bodyType']
    except: bodyType = None

    try: brand = json_data['brand']
    except: brand = None

    try: color = json_data['color']
    except: color = None

    try: complectation_dict = options_list
    except: complectation_dict = None

    try: description = json_data['description']
    except: description = None

    try: engineDisplacement = json_data['vehicleEngine']['engineDisplacement']
    except: engineDisplacement = None

    try: enginePower = json_data['vehicleEngine']['enginePower']
    except: enginePower = None

    try: equipment_dict = json_data_equip['card']['vehicle_info']['equipment']
    except: equipment_dict = None

    try: fuelType = json_data['fuelType']
    except: fuelType = None

    try: image = json_data['image']
    except: image = None

    try: mileage = page.find('li', class_='CardInfoRow CardInfoRow_kmAge').find_all('span')[-1].text.replace(u'\xa0', u' ')
    except: mileage = None

    try: modelDate = json_data['modelDate']
    except: modelDate = None
        
    model_info = None

    try: model_name = page.find_all('div', class_='InfoPopup InfoPopup_theme_plain InfoPopup_withChildren BreadcrumbsPopup')[1].text
    except: model_name = None

    try: name = json_data['name']
    except: name = None

    try: numberOfDoors = json_data['numberOfDoors']
    except: numberOfDoors = None

    parsing_unixtime = int(time.time())

    try: price = json_data['offers']['price']
    except: price = None

    try: priceCurrency = json_data['offers']['priceCurrency']
    except: priceCurrency = None

    try: productionDate = json_data['productionDate']
    except: productionDate = None

    try: sell_id = page.find('div', class_='CardHead__infoItem CardHead__id').text[2:]
    except: sell_id = None

    try: super_gen = json.loads(page.find('div', id="sale-data-attributes").get('data-bem'))
    except: super_gen = None

    try: vehicleConfiguration = json_data['vehicleConfiguration']
    except: vehicleConfiguration = None

    try: vehicleTransmission = json_data['vehicleTransmission']
    except: vehicleTransmission = None
        
    vendor = None

    try: owners = page.find('li', class_='CardInfoRow CardInfoRow_ownersCount').find_all('span')[-1].text.replace(u'\xa0', u' ')
    except: owners = None

    try: owning = page.find('li', class_='CardInfoRow CardInfoRow_owningTime').find_all('span')[-1].text
    except: owning = None

    try: pts = page.find('li', class_='CardInfoRow CardInfoRow_pts').find_all('span')[-1].text
    except: pts = None

    try: drive = page.find('li', class_='CardInfoRow CardInfoRow_drive').find_all('span')[-1].text
    except: drive = None

    try: wheel = page.find('li', class_='CardInfoRow CardInfoRow_wheel').find_all('span')[-1].text
    except: wheel = None

    try: status = page.find('li', class_='CardInfoRow CardInfoRow_state').find_all('span')[-1].text
    except: status = None

    try: customs = page.find('li', class_='CardInfoRow CardInfoRow_customs').find_all('span')[-1].text
    except: customs = None

    with open("/drive/My Drive/autoru_result_000000.csv", "a") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                bodyType,
                brand,
                car_url,
                color,
                complectation_dict,
                description, 
                engineDisplacement, 
                enginePower, 
                equipment_dict,
                fuelType, 
                image, 
                mileage, 
                modelDate, 
                model_info, 
                model_name,
                name, 
                numberOfDoors, 
                parsing_unixtime, 
                price,
                priceCurrency,
                productionDate, 
                sell_id, 
                super_gen, 
                vehicleConfiguration,
                vehicleTransmission, 
                vendor, 
                owners, 
                owning, 
                pts,
                drive, 
                wheel, 
                status, 
                customs
            )
        )


df_ads = pd.read_csv('/drive/My Drive/all_ads.csv', sep=',', header=None)
all_ads = df_ads[0].tolist()


def makeDatasetFile(start, end):
    steps = 0

    with open('autoru_result_000000.csv', "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'bodyType',
                'brand',
                'car_url',
                'color',
                'complectation_dict',
                'description', 
                'engineDisplacement', 
                'enginePower', 
                'equipment_dict',
                'fuelType', 
                'image', 
                'mileage', 
                'modelDate', 
                'model_info', 
                'model_name',
                'name', 
                'numberOfDoors', 
                'parsing_unixtime', 
                'price',
                'priceCurrency',
                'productionDate', 
                'sell_id', 
                'super_gen', 
                'vehicleConfiguration',
                'vehicleTransmission', 
                'vendor', 
                'Владельцы', 
                'Владение', 
                'ПТС',
                'Привод', 
                'Руль', 
                'Состояние', 
                'Таможня'
            )
        )

    for ad in all_ads[start:end]:
        collect_data(ad)
        steps += 1
        if steps % 20 == 0:
            print(f'Completed {steps} of total {end-start}')
        time.sleep(1)


# parse top 150k ads
process = Process(target=makeDatasetFile(0, 150000))
process.start()
process.join()

