import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent
TEMP_DIR = BASE_DIR / os.getenv('TEMP_DIR', 'temp')
OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'output')

# Create directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Application settings
APP_NAME = os.getenv('APP_NAME', 'PDF Tools')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# File upload settings
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 200))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Security settings
ENCRYPTION_STRENGTH = int(os.getenv('ENCRYPTION_STRENGTH', 256))
DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD', '')

# OCR settings
TESSERACT_PATH = os.getenv('TESSERACT_PATH', '')
OCR_LANGUAGE = os.getenv('OCR_LANGUAGE', 'eng')

# Compression settings
DEFAULT_COMPRESSION_QUALITY = int(os.getenv('DEFAULT_COMPRESSION_QUALITY', 85))

# Supported formats
SUPPORTED_FORMATS = {
    'pdf': ['.pdf'],
    'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'],
    'word': ['.doc', '.docx'],
    'excel': ['.xls', '.xlsx'],
    'powerpoint': ['.ppt', '.pptx'],
    'html': ['.html', '.htm']
}
