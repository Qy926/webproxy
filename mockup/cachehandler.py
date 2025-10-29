import logging
import time
import random


cache_dict = {}

def sleep_random_time(long_sleep=False):
    if long_sleep:
        sleep_time = random.uniform(0.300, 2.000)
    else:
        sleep_time = random.uniform(0.003, 0.008)

    time.sleep(sleep_time)


class CacheHandler:

    def __init__(self, fqdn, port, ttl):
        self._fqdn = fqdn
        self._port = port
        self._ttl = ttl

    def check_cache_key_exist(self, key, extra=None, trace_id=None):
        global cache_dict
        sleep_random_time()
        if key in cache_dict:
            logging.info("the key:%s exists in the cache service", key, extra=extra)
            return True

        logging.warning("the key:%s does not exist in the cache service", key, extra=extra)
        return False

    def get_cache_key_value(self, key, extra=None, trace_id=None):
        global cache_dict
        sleep_random_time()
        if key in cache_dict:
            value = cache_dict[key]
            logging.info("succeed to get the key:%s from the cache service, value:%r", key, value, extra=extra)
            return value

        logging.warning("the key:%s does not exist in the cache service", key, extra=extra)
        return None

    def set_cache_key_value(self, key, value, extra=None, trace_id=None, ttl=0):
        global cache_dict
        sleep_random_time()
        if not ttl:
            ttl = self._ttl

        cache_dict[key] = value
        logging.info("succeed to set the key:%s to the cache service, value:%r, ttl:%d", key, value, ttl, extra=extra)