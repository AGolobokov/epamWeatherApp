from django.db import models

# Create your models here.


class Weather(models.Model):
    city_name = models.CharField(max_length=50)
    date = models.DateField()
    temp = models.CharField(max_length=50)
    precipitation = models.CharField(max_length=50)
    wind = models.CharField(max_length=50)
    wind_direction = models.CharField(max_length=50)

    class Meta:
        db_table = 'weather_db'


class City(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

