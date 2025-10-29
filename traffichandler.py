import requests
import uuid
import json
import logging


class TrafficHandler:
    REQUEST_GET_COMPANY_INTERNATIONAL_TRAFFIC_URL = "http://{fqdn}:{port}/v1/getcompanyinternationaltraffic?companyid={company_id}&traceId={trace_id}"
    REQUEST_GET_COMPANY_DOMESTIC_TRAFFIC_URL      = "http://{fqdn}:{port}/v1/getcompanydomestictraffic?companyid={company_id}&traceId={trace_id}"
    REQUEST_GET_USER_INTERNATIONAL_TRAFFIC_URL    = "http://{fqdn}:{port}/v1/getuserinternationaltraffic?userid={user_id}&traceId={trace_id}"
    REQUEST_GET_USER_DOMESTIC_TRAFFIC_URL         = "http://{fqdn}:{port}/v1/getuserdomestictraffic?userid={user_id}&traceId={trace_id}"
    SUCCEED_GET_STATUS_CODE                       = 200

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_company_international_traffic(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get company international traffic, company id:%s", company_id, extra=extra)
        get_url = TrafficHandler.REQUEST_GET_COMPANY_INTERNATIONAL_TRAFFIC_URL.format(fqdn=self._fqdn, port=self._port, company_id=company_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != TrafficHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the company international traffic from traffic service, company id:%s, status code:%d", company_id, response.status_code, extra=extra)
                return None

            traffic_info = response.json().get('data', {})
            international_traffic = traffic_info.get('traffic', 0)
            logging.info("succeed to get the company international traffic from traffic service, company id:%s, value:%d", company_id, international_traffic, extra=extra)
            return international_traffic
        except Exception as e:
            logging.error("exception occurred when getting the company international traffic from traffic service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None

    def get_company_domestic_traffic(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get company domestic traffic, company id:%s", company_id, extra=extra)
        get_url = TrafficHandler.REQUEST_GET_COMPANY_DOMESTIC_TRAFFIC_URL.format(fqdn=self._fqdn, port=self._port, company_id=company_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != TrafficHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the company domestic traffic from traffic service, company id:%s, status code:%d", company_id, response.status_code, extra=extra)
                return None

            traffic_info = response.json().get('data', {})
            domestic_traffic = traffic_info.get('traffic', 0)
            logging.info("succeed to get the company domestic traffic from traffic service, company id:%s, value:%d", company_id, domestic_traffic, extra=extra)
            return domestic_traffic
        except Exception as e:
            logging.error("exception occurred when getting the company domestic traffic from traffic service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None

    def get_user_international_traffic(self, user_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get user international traffic, user id:%s", user_id, extra=extra)
        get_url = TrafficHandler.REQUEST_GET_USER_INTERNATIONAL_TRAFFIC_URL.format(fqdn=self._fqdn, port=self._port, user_id=user_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != TrafficHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the user international traffic from traffic service, user id:%s, status code:%d", user_id, response.status_code, extra=extra)
                return None

            traffic_info = response.json().get('data', {})
            international_traffic = traffic_info.get('traffic', 0)
            logging.info("succeed to get the user international traffic from traffic service, user id:%s, value:%d", user_id, international_traffic, extra=extra)
            return international_traffic
        except Exception as e:
            logging.error("exception occurred when getting the user international traffic from traffic service, user id:%s, exception[%r]", user_id, e, extra=extra)
            return None

    def get_user_domestic_traffic(self, user_id, timeout = None, extra = None, trace_id=None):
        logging.info("call traffic service to get user domestic traffic, user id:%s", user_id, extra=extra)
        get_url = TrafficHandler.REQUEST_GET_USER_DOMESTIC_TRAFFIC_URL.format(fqdn=self._fqdn, port=self._port, user_id=user_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != TrafficHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the user domestic traffic from traffic service, user id:%s, status code:%d", user_id, response.status_code, extra=extra)
                return None

            traffic_info = response.json().get('data', {})
            domestic_traffic = traffic_info.get('traffic', 0)
            logging.info("succeed to get the user domestic traffic from traffic service, user id:%s, value:%d", user_id, domestic_traffic, extra=extra)
            return domestic_traffic
        except Exception as e:
            logging.error("exception occurred when getting the user domestic traffic from traffic service, user id:%s, exception[%r]", user_id, e, extra=extra)
            return None