1. run rabbitmq server

2. run these commands
    
    `python3 manage.py runserver`

    `celery -A WarPigs worker -l INFO`

    `celery -A WarPigs beat -l INFO`