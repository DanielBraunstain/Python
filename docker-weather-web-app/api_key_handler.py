import os
from dotenv import load_dotenv

def get_api_key():
    """
    handles getting api key from .env file
    :return: api key to weather server
    """
    load_dotenv()
    api_key = os.getenv('MY_API_KEY')
    if api_key is None:
        raise EnvironmentError("API KEY NOT FOUND, PLEASE SET ONE IN .env FILE")
    return api_key
