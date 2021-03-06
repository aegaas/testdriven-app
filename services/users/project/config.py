""" services/users/project/config.py """

import os


class BaseConfig:
    """Base Configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    TESTING = True
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class StagingConfig(BaseConfig):
    """Staging Configuration"""
    ENV = 'staging'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
