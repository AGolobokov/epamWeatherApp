import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
import datetime
from bs4 import BeautifulSoup

# Create your views here.


def parsing_gismeteo(year, month, req_day)->list:

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    url_spb = f'https://www.gismeteo.ru/diary/4079/{year}/{month}/'

    res = requests.get(url_spb, headers=headers, timeout=5).text
    weather_content_soup = BeautifulSoup(res, "html.parser")

    table = weather_content_soup.find('tbody')

    for row in table.findAll('tr')[0:]:
        data_row = row.findAll('td')
        day = data_row[0].text
        if day == req_day:
            temp = data_row[1].text
            precipitation = data_row[4].find('img')
            if precipitation:
                precipitation = (precipitation.get('src').split('/')[-1]).split('.')[0]

            wind = data_row[5].text.split(' ')[-1]

            wind_direction = data_row[5].text.split(' ')[0]
            return ["Saint-Petersburg", temp, precipitation, wind, wind_direction]


def index(request):
    # 1 dsy = 86400 seconds

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    last_query_city = list(City.objects.all())
    if last_query_city == []:
        last_query_city[-1].start_date = datetime.datetime(2021, 8, 25)
        last_query_city[-1].end_date = datetime.datetime(2021, 8, 25)
    else:
        print("Start date")
        print(last_query_city[-1].start_date)

        print("End date")
        print(last_query_city[-1].end_date)

    requested_year = last_query_city[-1].start_date.year

    requested_month = 0
    if last_query_city[-1].start_date.month >= 10:
        requested_month = last_query_city[-1].start_date.month
    else:
        requested_month = '0' + str(last_query_city[-1].start_date.month)

    requested_day = last_query_city[-1].start_date.day

    data_list = parsing_gismeteo(str(requested_year), str(requested_month), str(requested_day))
    print(data_list)

    city_info = {
        'city': data_list[0],
        'temp': data_list[1],
        'temp_min': data_list[1],
        'temp_mid': data_list[1],
        'temp_max': data_list[1],
        'icon': 'A',
        'clouds': data_list[2],
        'wind': data_list[3],
        'wind_deg': data_list[4],
    }

    context = {'info': city_info, 'form': form}
    return render(request, 'weather/index.html', context)
