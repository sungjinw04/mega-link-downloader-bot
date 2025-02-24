import ast
import redis
import os
from urllib.parse import urlparse

# Import config
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Parse Redis URI properly
parsed_redis_url = urlparse(Config.REDIS_URI)

REDIS_HOST = parsed_redis_url.hostname
REDIS_PORT = parsed_redis_url.port
REDIS_PASS = parsed_redis_url.password

# Initialize Redis connection
DB = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
    charset="utf-8",
    decode_responses=True,
)

def get_stuff(WHAT):
    cha = DB.get(WHAT)
    if not cha:
        return {}  # Return an empty dictionary instead of a list with a dictionary
    return ast.literal_eval(cha)

