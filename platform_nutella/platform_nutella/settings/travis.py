from . import *

# SECRET_KEY = 's)@1Z*\x0cF\rAHQ}2\n$VQzX76[d'
SECRET_KEY = 's)@1Z*\x0cF\rAHQ}2\n$VQzX95[d'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': '', # le nom de notre base de données créée précédemment
        'USER': 'postgres', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
