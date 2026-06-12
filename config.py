import os
from datetime import datetime

class Config:
    """Base configuration"""
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'scholarship.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = False
    TESTING = False

    # File upload
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Email (mocked for testing)
    MAIL_MODE = 'mock'  # 'mock' or 'smtp'
    MAIL_LOG_FILE = os.path.join(BASEDIR, 'email_log.txt')

    # Data sources
    SCHOLARSHIP_MASTER_FILE = os.path.join(BASEDIR, 'MASTER Scholarship Spreadsheet 2025-2026.xlsx')
    AVAILABLE_FUNDS_FILE = os.path.join(BASEDIR, 'FY26 Available Funds for Committee.xlsx')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

get_config = lambda env='development': config.get(env, DevelopmentConfig)
