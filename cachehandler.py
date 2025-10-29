import requests
import time
import uuid
import json
import logging
import random


class CacheHandler:
    REQUEST_CACHE_DAEMON_GET_CACHE_URL    = "http://{fqdn}:{port}/v1/cacheproxy?key={key}&traceId={trace_id}"
    REQUEST_CACHE_DAEMON_SET_CACHE_URL    = "http://{fqdn}:{port}/v1/cacheproxy?traceId={trace_id}"

    CACHE_MAX_RETRY_TIMES                 = 3
    CACHE_BASE_SLEEP_TIME                 = 2
    CACHE_TIMEOUT                         = 60

    SUCCEED_GET_STATUS_CODE               = 200
    SUCCEED_POST_STATUS_CODE              = 201
    NOT_FOUND_STATUS_CODE                 = 404

    def __init__(self, fqdn, port, ttl):
        self._fqdn = fqdn
        self._port = port
        self._ttl = ttl

    def check_cache_key_exist(self, key, extra=None, trace_id=None):
        get_url = CacheHandler.REQUEST_CACHE_DAEMON_GET_CACHE_URL.format(fqdn=self._fqdn, port=self._port, key=key, trace_id=trace_id or str(uuid.uuid4()))
        for retry in range(CacheHandler.CACHE_MAX_RETRY_TIMES):
            sleep_time = random.random() * (CacheHandler.CACHE_BASE_SLEEP_TIME ** retry)
            try:
                response = requests.head(url=get_url)
                if response.status_code == CacheHandler.SUCCEED_GET_STATUS_CODE:
                    return True

                if response.status_code == CacheHandler.NOT_FOUND_STATUS_CODE:
                    logging.info("the key does not exist in cache, key:%s", key, extra=extra)
                    return False

                logging.warning("failed to check the cache key exist, key:%s, status code:%d, retry:%d", key, response.status_code, retry, extra=extra)
            except Exception as e:
                logging.error("failed to check the cache key exist, key:%s, retry:%d, exception[%r]", key, retry, e, extra=extra)

            time.sleep(sleep_time)

        logging.error("failed to check the cache key exist, key:%s", key, extra=extra)
        return False

    def get_cache_key_value(self, key, extra=None, trace_id=None):
        get_url = CacheHandler.REQUEST_CACHE_DAEMON_GET_CACHE_URL.format(fqdn=self._fqdn, port=self._port, key=key, trace_id=trace_id or str(uuid.uuid4()))
        for retry in range(CacheHandler.CACHE_MAX_RETRY_TIMES):
            sleep_time = random.random() * (CacheHandler.CACHE_BASE_SLEEP_TIME ** retry)
            try:
                response = requests.get(url=get_url)
                if response.status_code == CacheHandler.SUCCEED_GET_STATUS_CODE:
                    return response.json().get('data', {}).get(key)

                if response.status_code == CacheHandler.NOT_FOUND_STATUS_CODE:
                    logging.info("the key does not exist in cache, key:%s", key)
                    return None

                logging.warning("failed to get the cache key, key:%s, status code:%d, retry:%d", key, response.status_code, retry, extra=extra)
            except Exception as e:
                logging.error("failed to get the cache key, key:%s, retry:%d, exception[%r]", key, retry, e, extra=extra)

            time.sleep(sleep_time)

        logging.error("failed to get the cache key, key:%s", key, extra=extra)
        return None

    def set_cache_key_value(self, key, value, extra=None, trace_id=None, ttl=0):
        if not ttl:
            ttl = self._ttl

        post_url = CacheHandler.REQUEST_CACHE_DAEMON_SET_CACHE_URL.format(fqdn=self._fqdn, port=self._port, trace_id=trace_id or str(uuid.uuid4()))
        param = json.dumps(
            {
                "ttl": ttl,
                "data": {
                    key: value
                }
            }
        )

        kwargs = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'timeout': CacheHandler.CACHE_TIMEOUT,
            'data': param
        }
 
        for retry in range(CacheHandler.CACHE_MAX_RETRY_TIMES):
            sleep_time = random.random() * (CacheHandler.CACHE_BASE_SLEEP_TIME ** retry)
            try:
                response = requests.post(url=post_url, **kwargs)
                if response.status_code == CacheHandler.SUCCEED_POST_STATUS_CODE:
                    return

                logging.warning("failed to set the cache, key:%s, value:%s, status code:%d, retry:%d", key, value, response.status_code, retry, extra=extra)
            except Exception as e:
                logging.error("failed to set the cache, key:%s, value:%s, retry:%d, exception[%r]", key, value, retry, e, extra=extra)

            time.sleep(sleep_time)

        logging.error("failed to set the cache, key:%s, value:%s", key, value, extra=extra)