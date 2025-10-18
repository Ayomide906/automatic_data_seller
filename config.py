# config.py
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Configuration management class"""

    # Base directory
    BASE_DIR = Path(__file__).parent

    # WhatsApp Configuration
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN', '')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', '')

    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/storage/databases/data_business.db')

    # Bank API Configuration
    BANK_API_KEY = os.getenv('BANK_API_KEY', '')
    BANK_API_SECRET = os.getenv('BANK_API_SECRET', '')

    # Data Purchase Website Configuration
    DATA_WEBSITE_URL = os.getenv('DATA_WEBSITE_URL', '')
    DATA_WEBSITE_USERNAME = os.getenv('DATA_WEBSITE_USERNAME', '')
    DATA_WEBSITE_PIN = os.getenv('DATA_WEBSITE_PIN', '')

    # Image Processing Configuration
    TESSERACT_PATH = os.getenv('TESSERACT_PATH', '/usr/bin/tesseract')

    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # File Storage Paths
    @property
    def RECEIPTS_DIR(self):
        return self.BASE_DIR / 'storage' / 'receipts'

    @property
    def LOGS_DIR(self):
        return self.BASE_DIR / 'storage' / 'logs'

    @property
    def DATABASES_DIR(self):
        return self.BASE_DIR / 'storage' / 'databases'

# Create configuration instance
config = Config()

# Ensure storage directories exist
config.RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
config.DATABASES_DIR.mkdir(parents=True, exist_ok=True)