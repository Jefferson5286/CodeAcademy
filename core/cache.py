from cachetools import TTLCache

user_registration_cache = TTLCache(maxsize=100, ttl=900)
magic_link_cache = TTLCache(maxsize=1000, ttl=900)
