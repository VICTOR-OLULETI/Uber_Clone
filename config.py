import os

# config.py (production configuration)
class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_URI = os.environ.get('MONGODB_URI')