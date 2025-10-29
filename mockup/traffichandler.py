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


class TrafficHandler:

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_company_international_traffic(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get company international traffic, company id:%s", company_id, extra=extra)
        try:
            sleep_random_time() 
            if company_id not in conf.company_traffic_mapping:
                logging.error("failed to get the company international traffic from traffic service, company id:%s not found", company_id, extra=extra)
                return None

            traffic_info = conf.company_traffic_mapping.get(company_id)
            traffic = traffic_info.get('international_traffic', 0)
            logging.info("succeed to get the company international traffic from traffic service, company id:%s, value:%d", company_id, traffic, extra=extra)
            return traffic
        except Exception as e:
            logging.error("exception occurred when getting the company international traffic from traffic service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None

    def get_company_domestic_traffic(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get company domestic traffic, company id:%s", company_id, extra=extra)
        try:
            sleep_random_time() 
            if company_id not in conf.company_traffic_mapping:
                logging.error("failed to get the company domestic traffic from traffic service, company id:%s not found", company_id, extra=extra)
                return None

            traffic_info = conf.company_traffic_mapping.get(company_id)
            traffic = traffic_info.get('domestic_traffic', 0)
            logging.info("succeed to get the company domestic traffic from traffic service, company id:%s, value:%d", company_id, traffic, extra=extra)
            return traffic
        except Exception as e:
            logging.error("exception occurred when getting the company domestic traffic from traffic service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None

    def get_user_international_traffic(self, user_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get user international traffic, user id:%s", user_id, extra=extra)
        try:
            sleep_random_time() 
            if user_id not in conf.user_traffic_mapping:
                logging.error("failed to get the user international traffic from traffic service, user id:%s not found", user_id, extra=extra)
                return None

            traffic_info = conf.user_traffic_mapping.get(user_id)
            traffic = traffic_info.get('international_traffic', 0)
            logging.info("succeed to get the user international traffic from traffic service, user id:%s, value:%d", user_id, traffic, extra=extra)
            return traffic
        except Exception as e:
            logging.error("exception occurred when getting the user international traffic from traffic service, user id:%s, exception[%r]", user_id, e, extra=extra)
            return None

    def get_user_domestic_traffic(self, user_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get user domestic traffic, user id:%s", user_id, extra=extra)
        try:
            sleep_random_time()
            if user_id not in conf.user_traffic_mapping:
                logging.error("failed to get the user domestic traffic from traffic service, user id:%s not found", user_id, extra=extra)
                return None

            traffic_info = conf.user_traffic_mapping.get(user_id)
            traffic = traffic_info.get('domestic_traffic', 0)
            logging.info("succeed to get the user domestic traffic from traffic service, user id:%s, value:%d", user_id, traffic, extra=extra)
            return traffic
        except Exception as e:
            logging.error("exception occurred when getting the user domestic traffic from traffic service, user id:%s, exception[%r]", user_id, e, extra=extra)
            return None