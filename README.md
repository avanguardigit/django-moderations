# django-moderations


aggiungere al file settings


INSTALLED_APPS = [
    ...
    'moderations'
    ...
]

#custom backend autentication
AUTHENTICATION_BACKENDS = [
    'moderations.autenticationbackend.BlockBannedUserBackend'
]


MIDDLEWARE = [
    ....
    'moderations.middleware.BanManagement',
    ....
]
