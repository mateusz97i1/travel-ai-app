web: travel_app.wsgi:application --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn travel_app.wsgi
