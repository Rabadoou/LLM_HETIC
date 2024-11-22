import os
from dotenv import load_dotenv

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

if DROPBOX_ACCESS_TOKEN is None:
    raise ValueError("La variable d'environnement DROPBOX_ACCESS_TOKEN n'est pas définie.")

DEFAULT_TEMPERATURE = 37   
