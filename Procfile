web: travel_ai.wsgi:application --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn travel_ai.wsgi
