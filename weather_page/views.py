import requests
from django.shortcuts import render
from .models import City, Weather
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
        #create default object
        last_query_city.append(City("Saint-Petersburg", datetime.datetime(2021, 8, 25), datetime.datetime(2021, 8, 25)))
    else:
        print(last_query_city[-1].name)
        print("Start required date")
        print(last_query_city[-1].start_date)

        print("End required date")
        print(last_query_city[-1].end_date)

    # city_name = models.CharField(max_length=50)
    # date = models.DateField()
    # temp = models.CharField(max_length=50)
    # precipitation = models.CharField(max_length=50)
    # wind = models.CharField(max_length=50)
    # wind_direction = models.CharField(max_length=50)

    processing_temp = processing_max_temp = processing_min_temp = 0
    processing_wind = processing_wind_dir = 0
    processing_precip = 0

    print("WE fine name", last_query_city[-1].name)
    weather_data_from_db = list(Weather.objects.filter(city_name=last_query_city[-1].name).exclude(date__gte=last_query_city[-1].end_date).filter(date__gte=last_query_city[-1].start_date))

    print("LIST = ", weather_data_from_db)

    for elm in weather_data_from_db:
        print('NOTE', elm)
        print(elm.city_name)
        print(elm.date)

    if weather_data_from_db:
        print("City in database")

        data_list = [weather_data_from_db[0].city_name, weather_data_from_db[0].temp, weather_data_from_db[0].precipitation,
                     weather_data_from_db[0].wind, weather_data_from_db[0].wind_direction]

        city_info = {
            'city': data_list[0],
            'temp_average': data_list[1],
            'temp_min': data_list[1],
            'temp_mid': data_list[1],
            'temp_max': data_list[1],
            'clouds': data_list[2],
            'wind': data_list[3],
            'wind_deg': data_list[4],
        }
    else:
        print("City NOT in database -> find current temp")
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
            'temp_average': data_list[1],
            'temp_min': data_list[1],
            'temp_mid': data_list[1],
            'temp_max': data_list[1],
            'clouds': data_list[2],
            'wind': data_list[3],
            'wind_deg': data_list[4],
        }

    context = {'info': city_info, 'form': form}
    return render(request, 'weather/index.html', context)
