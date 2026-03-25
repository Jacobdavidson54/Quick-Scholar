# cache file

import time

cache_store = {}



def set_cache(key, value, TTL=None):
    
    if TTL is None:
        first_source = value[0]["source"].lower() if value and "source" in value[0] else "" 
        if first_source == "openalex":
            TTL = 86400 # 24 hours
        elif first_source == "crossref":
            TTL = 600 # 10 minutes
        else :
            TTL = 300 # default 5 minutes

        expiry_time = time.time() + TTL

        cache_store[key] = { 
                            "data" : value,
                            "expiry" : expiry_time
                           }
        
def get_cache(key):
    current_time = time.time()
    cached_entry = cache_store.get(key)
    if cached_entry:
        if current_time < cached_entry["expiry"]:
            return cached_entry["data"]
        else:
            del cache_store[key]

    return None
  




    