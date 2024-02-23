from dotenv import load_dotenv
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

path = os.path.join(BASEDIR, '.env')

load_dotenv(path)

def load_env_config():
    return {
        'server': os.getenv("DATABASE_SERVER"),
        'database': os.getenv("DATABASE"),
        'database_user': os.getenv("DATABASE_USERNAME"),
        'database_pass': os.getenv("DATABASE_PASSWORD"),
        'cleardb_database_url': os.getenv("CLEARDB_DATABASE_URL"),
        'secret_key': os.getenv("ACCESS_SECRET_KEY"),
        'password_salt': os.getenv("ACCESS_SALT"),
        'algorithm': os.getenv('ALGORITHM'),
        'access_token_expiry_minutes': os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'),
        'storage_directory': os.getenv('STORAGE_DIRECTORY'),
    }

