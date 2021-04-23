# -*- coding: utf-8 -*-
# default config

import os
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = b'\xfaF;X\x83:u\x1fW\xac9\xd1v\xf3o\xef+\x16{a\x81\xeb\xc7>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
    
class ProductionConfig(BaseConfig):
    DEBUG = False
    