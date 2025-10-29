import requests
import uuid
import json
import logging


class PolicyHandler:
    REQUEST_GET_POLICY_ID_URL    = "http://{fqdn}:{port}/v1/getpolicy?companyid={company_id}&traceId={trace_id}"
    SUCCEED_GET_STATUS_CODE       = 200

    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_policy(self, company_id, timeout = None, extra = None, trace_id=None):
        logging.info("call policy service to get the policy, company id:%s", company_id, extra=extra)
        get_url = PolicyHandler.REQUEST_GET_POLICY_ID_URL.format(fqdn=self._fqdn, port=self._port, company_id=company_id, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != PolicyHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get the policy from policy service, company id:%s, status code:%d", company_id, response.status_code, extra=extra)
                return None

            policy_info = response.json().get('data', {})
            logging.info("succeed to get the policy from policy service, company id:%s, policy:%r", company_id, policy_info, extra=extra)
            return policy_info
        except Exception as e:
            logging.error("exception occurred when getting the policy from policy service, company id:%s, exception[%r]", company_id, e, extra=extra)
            return None