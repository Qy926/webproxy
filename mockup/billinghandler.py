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


class BillingHandler:

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_user_billing_info(self, user_id, timeout = None, extra = None, trace_id=None):
        logging.info("call billing service to get user billing info, user id:%s", user_id, extra=extra)
        try:
            if user_id not in conf.user_billing_mapping:
                logging.error("failed to get the user billing info from billing service, user id:%s not found", user_id, extra=extra)
                return None

            sleep_random_time()
            billing = conf.user_billing_mapping.get(user_id)
            logging.info("succeed to get the user billing info from billing service, user id:%s, billing:%d", user_id, billing, extra=extra)
            return billing
        except Exception as e:
            logging.error("exception occurred when getting the user billing info from billing service, user id:%s, exception[%r]", user_id, e, extra=extra)
            return None

    def get_company_billing_info(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call billing service to get company billing info, company id:%s", company_id, extra=extra)
        try:
            if company_id not in conf.company_billing_mapping:
                logging.error("failed to get the company billing info from billing service, company id:%s not found", company_id, extra=extra)
                return None

            sleep_random_time()
            billing = conf.company_billing_mapping.get(company_id)
            logging.info("succeed to get the company billing info from billing service, company id:%s, billing:%d", company_id, billing, extra=extra)
            return billing
        except Exception as e:
            logging.error("exception occurred when getting the company billing info from billing service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None