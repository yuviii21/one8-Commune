#!/bin/bash
set -e

python -m pip install --upgrade pip --break-system-packages
python -m pip install -r requirements.txt --break-system-packages
python manage.py collectstatic --noinput
python manage.py migrate
python populate_restaurants.py
