import time
from weather_application.celery import app
import requests
from bs4 import BeautifulSoup
import datetime
import os
import django
from django.conf import settings
django.setup()
from .models import Weather

os.environ['DJANGO_SETTINGS_MODULE']='weather_application.settings'
# from django import db
#
# import sqlite3 as sql

def parsing_gismeteo(year, month)->list:

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    url_spb = f'https://www.gismeteo.ru/diary/4079/{year}/{month}/'
    print(url_spb)

    res = requests.get(url_spb, headers=headers, timeout=5).text
    weather_content_soup = BeautifulSoup(res, "html.parser")

    table = weather_content_soup.find('tbody')


    for row in table.findAll('tr')[0:]:
        data_row = row.findAll('td')
        # print(data_row)
        day = data_row[0].text
        # print(day)
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
today_is = datetime.datetime.now()

def count_id():
    global counter
    counter += 1
    return counter


@app.task
def endure_ten_seconds():
    print("Start period task")
    weather_data_list = list()

    note_id = count_id()

    time.sleep(1)
    print(today_is)
    print('day ', today_is.day, ' month ', today_is.month, ' year ',today_is.year)
    prepare_month_value = 1
    if today_is.month >= 10:
        prepare_month_value = today_is.month
    else:
        prepare_month_value = '0' + str(today_is.month-1)
    print(prepare_month_value)
    weather_data_list = parsing_gismeteo(today_is.year, prepare_month_value)
    # city_name = models.CharField(max_length=50)
    # date = models.DateField()
    # temp = models.CharField(max_length=50)
    # precipitation = models.CharField(max_length=50)
    # wind = models.CharField(max_length=50)
    # wind_direction = models.CharField(max_length=50)
    date = datetime.datetime(today_is.year, today_is.month, today_is.day)
    city_n = "Saint-Petersburg"
    weather_write_db = Weather(note_id, city_n, date,'+30', 'rain', '1m/c', 'N')
    weather_write_db.save()
    print(weather_data_list)
    print("End period task")



