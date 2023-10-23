import os
from dotenv import load_dotenv
from configparser import ConfigParser

load_dotenv()

def dbconfig(filename='database.ini', section='postgresql'):
    db = {}
    try:
        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    except(Exception) as err:
        print(err)

    return db

class Settings: 
    LOG_FILENAME = os.environ.get('LOG_FILENAME')
    EXIT_MSG_INCLOG= os.environ.get('EXIT_MSG_INCLOG')
    IN_METADATA_FILE = os.environ.get('IN_METADATA_FILE')
    
settings = Settings()