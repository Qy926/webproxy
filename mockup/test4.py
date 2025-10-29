#!/usr/bin/env python
# -*- coding:utf-8 -*-


import uuid
import requests

import conf


SERVICE_PORT                = '8080'
DEFAULT_REQUEST_TIMEOUT     = 30


if __name__ == '__main__':

    print("===Test Get Group Traffic Usage===")
    REQUEST_GET_GROUP_TRAFFIC_USAGE_URL = "http://127.0.0.1:{port}/api/v1/getgrouptrafficusage?companyid={company_id}&groupname={group_name}&traceid={trace_id}"
    for (company_id, group_name) in conf.group_users_mapping:
        trace_id = str(uuid.uuid4())
        url = REQUEST_GET_GROUP_TRAFFIC_USAGE_URL.format(port=SERVICE_PORT, company_id=company_id, group_name=group_name, trace_id=trace_id)
        response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
        print("Request URL:", url)
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)