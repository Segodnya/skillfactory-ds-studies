import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import re
import pandas as pd

from google.colab import drive
drive.mount('/drive')

def getPagesCount():
    first_page = 'https://auto.ru/cars/all/?damage_group=ANY&customs_state_group=DOESNT_MATTER&has_image=false&currency=RUR&output_type=list&page_num_offers=1'
    response_list_ads = requests.get(first_page)
    response_list_ads.encoding = 'utf-8'

    page_list_ads = BeautifulSoup(response_list_ads.text, 'html.parser')
    ads_total = page_list_ads.find('button', class_='Button Button_color_blue Button_size_m Button_type_button Button_width_full')\
    .find('span', class_='ButtonWithLoader__content').text
    ads_total = ads_total.replace(u'\xa0', u' ').split()[1:3]
    ads_total = int(''.join(ads_total)) - 20000 # exclude bottom 20k ads
    number_of_pages = int(ads_total / 38) # 38 ads on one page
    return number_of_pages


def getLinks():
    # collect all links from range of pages
    base_url = 'https://auto.ru/cars/all/?damage_group=ANY&customs_state_group=DOESNT_MATTER&has_image=false&currency=RUR&output_type=list&page_num_offers='
    number_of_pages = getPagesCount()
    all_ads = []

    for i in range(0, number_of_pages): # Number of pages you want to parse
        print('Page in progress:', i, 'Total Pages:', number_of_pages)
        url_with_list_of_ads = base_url + str(i)

        response_list_ads = requests.get(url_with_list_of_ads)
        response_list_ads.encoding = 'utf-8'

        page_list_ads = BeautifulSoup(response_list_ads.text, 'html.parser')
        cars_from_page = page_list_ads.find_all('a', class_='Link ListingItemTitle__link')
        cars_from_page_list = [elem.get('href') for elem in cars_from_page]

        with open('/drive/My Drive/all_ads_9.csv', 'a') as myfile:
            wr = csv.writer(myfile)
            for elem in cars_from_page_list:
                wr.writerow([elem])
                all_ads.append(elem)

    return all_ads

all_ads = getLinks()
