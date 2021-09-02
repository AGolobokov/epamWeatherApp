FROM python:3.8.5
ENV PYTHONUNBUFFERED=1
RUN pip3 install --upgrade pip
COPY . /
EXPOSE 8000
RUN pip3 install -r requirements.txt
RUN redis-server
RUN celery -A weather_application beat -l info
RUN celery worker -A weather_application --loglevel=INFO
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
