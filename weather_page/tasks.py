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
    one_month_weather_data_list = list()

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

        one_day_weather = ["Saint-Petersburg", day, month, year, temp, precipitation, wind, wind_direction]
        one_month_weather_data_list.append(one_day_weather)
    return one_month_weather_data_list


def write_to_database():
    pass


real_counter = 0
today_is = datetime.datetime.now()


def real_count_id():
    global real_counter
    real_counter += 1
    return real_counter


def reset_real_count_id():
    global real_counter
    real_counter = 0
    return real_counter

month_counter = 12
required_month = required_year = 0

@app.task
def periodic_task():
    print("Start period task")

    global month_counter
    global required_month
    global required_year
    print('month_counter =', month_counter)

    if month_counter == 12:
        print(today_is)
        required_month = today_is.month - 1
        required_year = today_is.year

    if month_counter > 0:

        if required_month == 1:
            required_month = 12
            required_year = required_year - 1

        prepare_month_value = 1
        prepare_year_value = required_year

        if required_month >= 10:
            prepare_month_value = required_month
        else:
            prepare_month_value = '0' + str(required_month)

        weather_list = parsing_gismeteo(prepare_year_value, prepare_month_value)

        for note in weather_list:
            print(note)
            real_id_counter = real_count_id()
            print("real_id_counter = ", real_id_counter)

            city_name = "Saint-Petersburg"
            date = datetime.datetime(int(note[3]), int(note[2]), int(note[1]))
            if note[5]:
                precipitation_value = note[5]
            else:
                precipitation_value = 'No precipitation'
            weather_write_db = Weather(real_id_counter, city_name, date, note[4], precipitation_value, note[6], note[7])

            weather_write_db.save()

        required_month = required_month - 1
        month_counter = month_counter - 1








    print("End period task")



