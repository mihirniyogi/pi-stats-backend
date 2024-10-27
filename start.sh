#!/bin/bash
source ./venv/bin/activate
exec gunicorn project.wsgi:application --bind 0.0.0.0:5000 --workers 3