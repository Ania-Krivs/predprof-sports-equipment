from os import getenv

from dotenv import load_dotenv

load_dotenv()

MONGO_DSN = getenv("MONGO_DSN")
ENVIRONMENT = getenv("ENVIRONMENT")

ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES") 
ALGORITHM = getenv("ALGORITHM")
SECURITY_KEY = getenv("SECURITY_KEY")
SECURITY_KEY_USER = getenv("SECURITY_KEY_USER")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_HOST = getenv("REDIS_HOST")
ACCESS_TOKEN_EXPIRE_MINUTES_REDIS = getenv("ACCESS_TOKEN_EXPIRE_MINUTES_REDIS")
