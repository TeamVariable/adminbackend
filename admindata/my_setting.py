from typing import Dict

MY_SECRET: Dict = {
    "SECRET_KEY": r'django-insecure-_1#f(vf6%obd4h!+3kzv3a6x2e+me2=e**2uvz0-!_*2w*k@p2'
}

MY_DATABASES: Dict = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admindata',
        'USER': 'root',
        'PASSWORD': '123456789',
        'HOST': 'sql',
        'PORT': '3306'
    }
}