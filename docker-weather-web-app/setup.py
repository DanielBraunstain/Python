from flask_pymongo import PyMongo
import os

def configure_app(app):
    """
    configure the app based on the environment.
    """
    if os.path.exists('/.dockerenv'):# MongoDB Configuration
        app.config["MONGO_URI"] = os.getenv('MONGO_URI')
        mongo = PyMongo(app)
        return mongo
    else: #SQLite
        return get_db_path()

def get_db_path():
    """
    return the path to the SQLite database file.
    """
    return os.path.join(os.path.dirname(__file__), 'weather.db')
