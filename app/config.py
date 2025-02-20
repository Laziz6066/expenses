import os

from dotenv import load_dotenv

load_dotenv()
ADMINS = list(map(int, os.getenv('ADMINS', '').split(',')))\
    if os.getenv('ADMINS') else []
