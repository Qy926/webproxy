import logging
import time
import random

import conf


def sleep_random_time(long_sleep=False):
    if long_sleep:
        sleep_time = random.uniform(0.300, 2.000)
    else:
        sleep_time = random.uniform(0.010, 0.050)

    time.sleep(sleep_time)


class DomainHandler:

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_company_id(self, domain, timeout = None, extra = None, trace_id=None):
        logging.info("call domain service to get company id, domain:%s", domain, extra=extra)
        try:
            sleep_random_time(True)
            if domain not in conf.domain_company_mapping:
                logging.error("failed to get the company id from domain service, domain:%s not found", domain, extra=extra)
                return None

            company_id = conf.domain_company_mapping.get(domain)
            logging.info("succeed to get the company id from domain service, domain:%s, company id:%s", domain, company_id, extra=extra)
            return company_id
        except Exception as e:
            logging.error("exception occurred when getting the company id from domain service, domain:%s, exception[%r]", domain, e, extra=extra)
            return None