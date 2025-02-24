import ast
import redis
import os
from urllib.parse import urlparse

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Parse Redis URI properly
parsed_redis_url = urlparse(Config.REDIS_URI)

REDIS_HOST = parsed_redis_url.hostname or "localhost"
REDIS_PORT = parsed_redis_url.port or 6379  # Default Redis port
REDIS_PASS = parsed_redis_url.password or None

# Initialize Redis connection
DB = redis.StrictRedis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),  # Ensure port is an integer
    password=REDIS_PASS,
    charset="utf-8",
    decode_responses=True,
)

def get_stuff(WHAT):
    cha = DB.get(WHAT)
    if not cha:
        return {}  
    return ast.literal_eval(cha)

