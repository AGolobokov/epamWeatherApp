import time
from weather_application.celery import app
import requests
from bs4 import BeautifulSoup

import sqlite3 as sql

def parsing_gismeteo(year, month)->list:

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    url_spb = f'https://www.gismeteo.ru/diary/4079/{year}/{month}/'

    res = requests.get(url_spb, headers=headers, timeout=5).text
    weather_content_soup = BeautifulSoup(res, "html.parser")

    table = weather_content_soup.find('tbody')

    for row in table.findAll('tr')[0:]:
        data_row = row.findAll('td')
        print(data_row)
        day = data_row[0].text
        print(day)
        temp = data_row[1].text
        # print('temp ', temp)
        precipitation = data_row[4].find('img')
        if precipitation:
            precipitation = (precipitation.get('src').split('/')[-1]).split('.')[0]

        wind = data_row[5].text.split(' ')[-1]

        wind_direction = data_row[5].text.split(' ')[0]
        return ["Saint-Petersburg", temp, precipitation, wind, wind_direction]


def write_to_database():
    pass


counter = 0

@app.task
def endure_ten_seconds():
    print("Start period task")
    print(counter)
    time.sleep(1)
    print("End period task")



