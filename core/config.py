import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    LOG_FILENAME = os.environ.get('LOG_FILENAME')
    EXIT_MSG_INCLOG = os.environ.get('EXIT_MSG_INCLOG')

settings = Settings()
