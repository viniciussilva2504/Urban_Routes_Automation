import os

from dotenv import load_dotenv

load_dotenv()

URBAN_ROUTES_URL = os.getenv(
    "URBAN_ROUTES_URL",
    "https://cnt-6c0a83b5-8f45-4d4b-ae50-0537ddd748f7.containerhub.tripleten-services.com/?lng=pt",
).strip()
ADDRESS_FROM = os.getenv("ADDRESS_FROM", "East 2nd Street, 601")
ADDRESS_TO = os.getenv("ADDRESS_TO", "1300 1st St")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+11231231212")
CARD_NUMBER = os.getenv("CARD_NUMBER", "1234 5678 9100")
CARD_CODE = os.getenv("CARD_CODE", "1111")
MESSAGE_FOR_DRIVER = os.getenv("MESSAGE_FOR_DRIVER", "Please, stop in the Juices bar")
