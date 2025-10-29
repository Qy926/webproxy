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


class PolicyHandler:

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_policy(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call policy service to get the policy, company id:%s", company_id, extra=extra)
        try:
            sleep_random_time(True)
            if company_id not in conf.company_policy_mapping:
                logging.error("failed to get the policy from policy service, company id:%s not found", company_id, extra=extra)
                return None

            policy = conf.company_policy_mapping.get(company_id)
            logging.info("succeed to get the policy from policy service, company id:%s, policy:%r", company_id, policy, extra=extra)
            return policy
        except Exception as e:
            logging.error("exception occurred when getting the policy from policy service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None