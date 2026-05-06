#!/bin/bash
set -e

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
