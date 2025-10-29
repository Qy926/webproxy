import requests
import uuid
import json
import logging


class BillingHandler:
    REQUEST_GET_USER_BILLING_URL    = "http://{fqdn}:{port}/v1/getuserbilling?userid={user_id}&traceId={trace_id}"
    REQUEST_GET_COMPANY_BILLING_URL = "http://{fqdn}:{port}/v1/getcompanybilling?companyid={company_id}&traceId={trace_id}"
    SUCCEED_GET_STATUS_CODE         = 200

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_user_billing_info(self, user_id, timeout = None, extra = None, trace_id=None):
        logging.info("call billing service to get user billing info, user id:%s", user_id, extra=extra)
        get_url = BillingHandler.REQUEST_GET_USER_BILLING_URL.format(fqdn=self._fqdn, port=self._port, user_id=user_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != BillingHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the user billing info from billing service, user id:%s, status code:%d", user_id, response.status_code, extra=extra)
                return None

            billing_info = response.json().get('data', {})
            billing = billing_info.get('billing')
            logging.info("succeed to get the user billing info from billing service, user id:%s, billing:%d", user_id, billing, extra=extra)
            return billing
        except Exception as e:
            logging.error("exception occurred when getting the user billing info from billing service, user id:%s, exception[%r]", user_id, e, extra=extra)
            return None

    def get_company_billing_info(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call billing service to get company billing info, company id:%s", company_id, extra=extra)
        get_url = BillingHandler.REQUEST_GET_COMPANY_BILLING_URL.format(fqdn=self._fqdn, port=self._port, company_id=company_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != BillingHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the company billing info from billing service, company id:%s, status code:%d", company_id, response.status_code, extra=extra)
                return None

            billing_info = response.json().get('data', {})
            billing = billing_info.get('billing')
            logging.info("succeed to get the company billing info from billing service, company id:%s, billing:%d", company_id, billing, extra=extra)
            return billing
        except Exception as e:
            logging.error("exception occurred when getting the company billing info from billing service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None