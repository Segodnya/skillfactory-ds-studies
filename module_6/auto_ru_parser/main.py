import requests
from bs4 import BeautifulSoup
import time
import json
import re
import pandas as pd
from multiprocessing import Process
from google.colab import drive
drive.mount('/drive')


def add_ad_to_car_dict(ad):
    car_url = ad

    response = requests.get(car_url)
    response.encoding = 'utf-8'
    page = BeautifulSoup(response.text, 'html.parser')
    try:
        json_data = json.loads(page.find('script', type="application/ld+json").string)
    except:
        json_data = None

    catalog_url = page.find('a', class_='Link SpoilerLink CardCatalogLink SpoilerLink_type_default').get('href')
    response_catalog = requests.get(catalog_url)
    response_catalog.encoding = 'utf-8'
    page_catalog = BeautifulSoup(response_catalog.text, 'html.parser')
    try:
        json_data_catalog = json.loads(page_catalog.find('script', type="application/json", id='initial-state').string)
    except:
        json_data_catalog = None

    try: json_data_equip = json.loads(page.find('script', type="application/json", id='initial-state').string)
    except: json_data_equip = None

    try:
        json_data['description'] = json_data['description'].replace('\n', ' ')
        json_data['description'] = re.sub('\W+',' ', json_data['description'])
    except:
        json_data['description'] = ''

    try:
        options_dict = json_data_catalog['state']['compare']['selected'][0]['options']
        options_list = [key for key in list(options_dict.keys()) if options_dict[key] == 1] 
    except:
        options_list = []

    # 'vendor' feature will be added during EDA
    # 'model_info' feature is about transcribing models into russian, pass
    car_dict.update({ad: {}})

    try: car_dict[ad]['car_url'] = json_data['offers']['url']
    except: car_dict[ad]['car_url'] = None

    try: car_dict[ad]['bodyType'] = json_data['bodyType']
    except: car_dict[ad]['bodyType'] = None
    
    try: car_dict[ad]['brand'] = json_data['brand']
    except: car_dict[ad]['brand'] = None

    try: car_dict[ad]['color'] = json_data['color']
    except: car_dict[ad]['color'] = None

    try: car_dict[ad]['complectation_dict'] = options_list
    except: car_dict[ad]['complectation_dict'] = None

    try: car_dict[ad]['description'] = json_data['description']
    except: car_dict[ad]['description'] = None

    try: car_dict[ad]['engineDisplacement'] = json_data['vehicleEngine']['engineDisplacement']
    except: car_dict[ad]['engineDisplacement'] = None

    try: car_dict[ad]['enginePower'] = json_data['vehicleEngine']['enginePower']
    except: car_dict[ad]['enginePower'] = None

    try: car_dict[ad]['equipment_dict'] = json_data_equip['card']['vehicle_info']['equipment']
    except: car_dict[ad]['equipment_dict'] = None
    
    try: car_dict[ad]['fuelType'] = json_data['fuelType']
    except: car_dict[ad]['fuelType'] = None
    
    try: car_dict[ad]['image'] = json_data['image']
    except: car_dict[ad]['image'] = None

    try: car_dict[ad]['mileage'] = page.find('li', class_='CardInfoRow CardInfoRow_kmAge').find_all('span')[-1].text.replace(u'\xa0', u' ')
    except: car_dict[ad]['mileage'] = None

    try: car_dict[ad]['modelDate'] = json_data['modelDate']
    except: car_dict[ad]['modelDate'] = None

    try: car_dict[ad]['model_name'] = page.find_all('div', class_='InfoPopup InfoPopup_theme_plain InfoPopup_withChildren BreadcrumbsPopup')[1].text
    except: car_dict[ad]['model_name'] = None

    try: car_dict[ad]['name'] = json_data['name']
    except: car_dict[ad]['name'] = None

    try: car_dict[ad]['numberOfDoors'] = json_data['numberOfDoors']
    except: car_dict[ad]['numberOfDoors'] = None

    try: car_dict[ad]['parsing_unixtime'] = int(time.time())
    except: car_dict[ad]['parsing_unixtime'] = None

    try: car_dict[ad]['price'] = json_data['offers']['price']
    except: car_dict[ad]['price'] = None

    try: car_dict[ad]['priceCurrency'] = json_data['offers']['priceCurrency']
    except: car_dict[ad]['priceCurrency'] = None

    try: car_dict[ad]['productionDate'] = json_data['productionDate']
    except: car_dict[ad]['productionDate'] = None

    try: car_dict[ad]['sell_id'] = page.find('div', class_='CardHead__infoItem CardHead__id').text[2:]
    except: car_dict[ad]['sell_id'] = None

    try: car_dict[ad]['views'] = page.find('div', class_='CardHead__infoItem CardHead__views').text.split()[0]
    except: car_dict[ad]['views'] = None

    try: car_dict[ad]['date_added'] = page.find('div', class_='CardHead__infoItem CardHead__creationDate').text
    except: car_dict[ad]['date_added'] = None

    try: car_dict[ad]['super_gen'] = json.loads(page.find('div', id="sale-data-attributes").get('data-bem'))
    except: car_dict[ad]['super_gen'] = None

    try: car_dict[ad]['vehicleConfiguration'] = json_data['vehicleConfiguration']
    except: car_dict[ad]['vehicleConfiguration'] = None

    try: car_dict[ad]['vehicleTransmission'] = json_data['vehicleTransmission']
    except: car_dict[ad]['vehicleTransmission'] = None

    try: car_dict[ad]['Владельцы'] = page.find('li', class_='CardInfoRow CardInfoRow_ownersCount').find_all('span')[-1].text.replace(u'\xa0', u' ')
    except: car_dict[ad]['Владельцы'] = None

    try: car_dict[ad]['Владение'] = page.find('li', class_='CardInfoRow CardInfoRow_owningTime').find_all('span')[-1].text
    except: car_dict[ad]['Владение'] = None

    try: car_dict[ad]['ПТС'] = page.find('li', class_='CardInfoRow CardInfoRow_pts').find_all('span')[-1].text
    except: car_dict[ad]['ПТС'] = None

    try: car_dict[ad]['Привод'] = page.find('li', class_='CardInfoRow CardInfoRow_drive').find_all('span')[-1].text
    except: car_dict[ad]['Привод'] = None

    try: car_dict[ad]['Руль'] = page.find('li', class_='CardInfoRow CardInfoRow_wheel').find_all('span')[-1].text
    except: car_dict[ad]['Руль'] = None

    try: car_dict[ad]['Состояние'] = page.find('li', class_='CardInfoRow CardInfoRow_state').find_all('span')[-1].text
    except: car_dict[ad]['Состояние'] = None

    try: car_dict[ad]['Таможня'] = page.find('li', class_='CardInfoRow CardInfoRow_customs').find_all('span')[-1].text
    except: car_dict[ad]['Таможня'] = None

    try: car_dict[ad]['region'] = page.find('div', class_='CardBreadcrumbs').find_all('div', class_='CardBreadcrumbs__item')[-1].text.replace(u'\xa0', u' ')
    except: car_dict[ad]['region'] = None


df_ads = pd.read_csv('/drive/My Drive/all_ads.csv', sep=',', header=None)
all_ads = df_ads[0].tolist()

car_dict = {}

def makeDatasetFile(start, end):
    steps = 0
    for ad in all_ads[start:end]:
        add_ad_to_car_dict(ad)
        steps += 1
        if steps % 10 == 0:
            print(f'Completed {steps} of total {end-start}') 
        else:
            continue

    df = pd.DataFrame.from_dict(car_dict, orient='index')
    df.to_csv(f'/drive/My Drive/autoru_result_{file_number}.csv')


process = Process(target=makeDatasetFile(0, 300000))
process.start()
process.join()
