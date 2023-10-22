import os
from dotenv import load_dotenv
load_dotenv()

class Settings: 
    logfile = os.environ.get('LOG_FILENAME')
    exitmsginclog =  os.environ.get('EXIT_MSG_INCLOG')
    LOG_FILENAME = r'C:\lenisson\UFFS\bd2\trabalho log undo\BD2-Log-Undo\input_case\in.in' if logfile is None else logfile
    EXIT_MSG_INCLOG = '' if exitmsginclog is None else exitmsginclog
    
settings = Settings()
