import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'WQ-GAmL5ipzcOYafMH7wzA'
    DATABASE_HOST = os.environ.get('DATABASE_HOST') or 'mychatappservice-server.mysql.database.azure.com'
    DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME') or 'rxalspiqjj'
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or '96$WOUAb4Z9dWVtV'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'mychatappservice-database'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False