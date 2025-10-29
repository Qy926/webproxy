import requests
import uuid
import json
import logging


class DomainHandler:
    REQUEST_GET_COMPANY_ID_URL    = "http://{fqdn}:{port}/v1/getcompanyid?domain={domain}&traceId={trace_id}"
    SUCCEED_GET_STATUS_CODE       = 200
    NOT_FOUND_STATUS_CODE         = 404

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_company_id(self, domain, timeout = None, extra = None, trace_id=None):
        logging.info("call domain service to get company id, domain:%s", domain, extra=extra)
        get_url = DomainHandler.REQUEST_GET_COMPANY_ID_URL.format(fqdn=self._fqdn, port=self._port, domain=domain, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code == DomainHandler.SUCCEED_GET_STATUS_CODE:
                company_info = response.json().get('data', {})
                company_id = company_info.get('companyId')
                logging.info("succeed to get the company id from domain service, domain:%s, company id:%s", domain, company_id, extra=extra)
                return company_id

            if response.status_code == DomainHandler.NOT_FOUND_STATUS_CODE:
                logging.error("the domain service could not find the company id for the domain:%s", domain, extra=extra)
                return None

            logging.error("failed to get the company id from domain service, domain:%s, status code:%d", domain, response.status_code, extra=extra)
            return None
        except Exception as e:
            logging.error("exception occurred when getting the company id from domain service, domain:%s, exception[%r]", domain, e, extra=extra)
            return None