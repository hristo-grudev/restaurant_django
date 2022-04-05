import os


def is_production():
    return os.getenv('APP_ENV') == 'Production'


def is_development():
    return os.getenv('APP_ENV') == 'Development'
