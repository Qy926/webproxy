#!/usr/bin/env python
# -*- coding:utf-8 -*-


import uuid
import requests

import conf


SERVICE_PORT                = '8080'
DEFAULT_REQUEST_TIMEOUT     = 2


if __name__ == '__main__':
    print("===Test Get Policy===")
    users = [
        {"username": "aa@sina.com"},
        {"username": "bb@sina.comm"},
        {"username": "cc@sina.com"},
        {"username": "dd@sina.com"},
        {"username": "ee@sina.com"},
    ]
    REQUEST_GET_POLICY_URL = "http://127.0.0.1:{port}/api/v1/getpolicy?username={username}&traceid={trace_id}"
    for user in users:
        trace_id = str(uuid.uuid4())
        url = REQUEST_GET_POLICY_URL.format(port=SERVICE_PORT, username=user['username'], trace_id=trace_id)
        response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
        print("Request URL:", url)
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)
