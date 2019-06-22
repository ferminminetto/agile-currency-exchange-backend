#!/bin/bash

cd /app

CREATED_FLAG=/created
if [ ! -f "$CREATED_FLAG" ]; then
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py test

    # NEVER execute this command in production environment - TODO: Seeder
    if [ $ENVIRONMENT  = 'dev' ]; then
        python manage.py development_seed
    fi
fi

touch $CREATED_FLAG

python manage.py runserver 0.0.0.0:8000