from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from dotenv import load_dotenv
from pathlib import Path
import os


def mongodb():
    db = connect().get_database(os.getenv('MONGO_CLUSTER'))
    return db


def check_connection():
    try:
        if connect().admin.command('ismaster')['ismaster']:
            print("connected")
    except OperationFailure:
        print("Database not found")
    except ServerSelectionTimeoutError:
        print("MongoDB Server is down.")


def connect():
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)
    client = MongoClient(
        'mongodb+srv://' + os.getenv('MONGO_USER') + ':' + os.getenv(
            'MONGO_PASSWORD') + '@' + os.getenv('MONGO_IDENTIFIER') + '.mongodb.net/?retryWrites=true&w=majority')
    return client
