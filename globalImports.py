from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

limiter = Limiter(key_func=get_remote_address)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})