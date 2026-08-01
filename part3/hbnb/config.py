#!/usr/bin/python3
"""Configuration classes for the HBnB application."""
import os


class Config:
    """Base configuration shared by every environment."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-jwt-secret-key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development: SQLite file database."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///development.db')


class ProductionConfig(Config):
    """Production: MySQL."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+mysqlconnector://hbnb_user:hbnb_pwd@localhost/hbnb_prod'
    )


class TestingConfig(Config):
    """Testing: in-memory SQLite."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
