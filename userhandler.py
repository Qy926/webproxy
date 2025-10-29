import requests
import uuid
import json
import logging


class UserHandler:
    REQUEST_GET_USER_ID_URL          = "http://{fqdn}:{port}/v1/getuserid?companyid={company_id}&username={username}&traceId={trace_id}"
    REQUEST_GET_ALL_GROUP_USERS_URL  = "http://{fqdn}:{port}/v1/getallgroupusers?companyid={company_id}&groupname={group_name}&traceId={trace_id}"
    SUCCEED_GET_STATUS_CODE          = 200
    NOT_FOUND_STATUS_CODE            = 404


    def __init__(self, fqdn, port, request_timeout):
        self._fqdn = fqdn
        self._port = port
        self._request_timeout = request_timeout

    def get_user_id(self, company_id, username, timeout = None, extra = None, trace_id=None):
        logging.info("call user service to get user id, company id:%s, username:%s", company_id, username, extra=extra)
        get_url = UserHandler.REQUEST_GET_USER_ID_URL.format(fqdn=self._fqdn, port=self._port, company_id=company_id, username=username, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code == UserHandler.SUCCEED_GET_STATUS_CODE:
                user_info = response.json().get('data', {})
                user_id = user_info.get('userId')
                logging.info("succeed to get the user id from user service, company id:%s, username:%s, user id:%s", company_id, username, user_id, extra=extra)
                return user_id

            if response.status_code == UserHandler.NOT_FOUND_STATUS_CODE:
                logging.warning("the user service could not find the user id for the company id:%s, username:%s", company_id, username, extra=extra)
                return None

            logging.error("failed to get the user id from user service, company id:%s, username:%s, status code:%d", company_id, username, response.status_code, extra=extra)
            return None
        except Exception as e:
            logging.error("exception occurred when getting the user id from user service, company id:%s, username:%s, exception[%r]", company_id, username, e, extra=extra)
            return None

    def get_all_group_users(self, company_id, group_name, timeout = None, extra = None, trace_id=None):
        logging.info("call user service to get all group users, company id:%s, group name:%s", company_id, group_name, extra=extra)
        get_url = UserHandler.REQUEST_GET_ALL_GROUP_USERS_URL.format(fqdn=self._fqdn, port=self._port, company_id=company_id, group_name=group_name, trace_id=trace_id or str(uuid.uuid4()))
        try:
            response = requests.get(url=get_url, timeout=timeout or self._request_timeout)
            if response.status_code != UserHandler.SUCCEED_GET_STATUS_CODE:
                logging.error("failed to get all group users from user service, company id:%s, group name:%s, status code:%d", company_id, group_name, response.status_code, extra=extra)
                return None

            group_users_info = response.json().get('data', {})
            users = group_users_info.get('users', [])
            logging.info("succeed to get all group users from user service, company id:%s, group name:%s, group users info:%r", company_id, group_name, group_users_info, extra=extra)
            return users
        except Exception as e:
            logging.error("exception occurred when getting all group users from user service, company id:%s, group name:%s, exception[%r]", company_id, group_name, e, extra=extra)
            return None