import logging
import time
import random

import conf


def sleep_random_time(long_sleep=False):
    if long_sleep:
        sleep_time = random.uniform(1.000, 2.000)
    else:
        sleep_time = random.uniform(0.010, 0.050)

    time.sleep(sleep_time)


class UserHandler:

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_user_id(self, company_id, username, timeout = None, extra = None, trace_id=None):
        logging.info("call user service to get user id, company id:%s, username:%s", company_id, username, extra=extra)
        try:
            if (company_id, username) not in conf.company_users_mapping:
                logging.error("failed to get the user id from user service, company id:%s, username:%s not found", company_id, username, extra=extra)
                return None

            sleep_random_time()
            user_id = conf.company_users_mapping.get((company_id, username))
            logging.info("succeed to get the user id from user service, company id:%s, username:%s, user id:%s", company_id, username, user_id, extra=extra)
            return user_id
        except Exception as e:
            logging.error("exception occurred when getting the user id from user service, company id:%s, username:%s, exception[%r]", company_id, username, e, extra=extra)
            return None

    def get_all_group_users(self, company_id, group_name, timeout = None, extra = None, trace_id=None):
        logging.info("call user service to get all group users, company id:%s, group name:%s", company_id, group_name, extra=extra)
        try:
            sleep_random_time()
            if (company_id, group_name) not in conf.group_users_mapping:
                logging.error("failed to get all group users from user service, company id:%s, group name:%s not found", company_id, group_name, extra=extra)
                return None

            group_users = conf.group_users_mapping.get((company_id, group_name))
            logging.info("succeed to get all group users from user service, company id:%s, group name:%s, group users:%r", company_id, group_name, group_users, extra=extra)
            return group_users
        except Exception as e:
            logging.error("exception occurred when getting all group users from user service, company id:%s, group name:%s, exception[%r]", company_id, group_name, e, extra=extra)
            return None