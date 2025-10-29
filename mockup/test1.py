#!/usr/bin/env python
# -*- coding:utf-8 -*-


import uuid
import requests

import conf


SERVICE_PORT                = '8080'
DEFAULT_REQUEST_TIMEOUT     = 2


if __name__ == '__main__':
    print("===Test Get Policy===")
    REQUEST_GET_POLICY_URL = "http://127.0.0.1:{port}/api/v1/getpolicy?username={username}&traceid={trace_id}"
    for (company_id, group_name) in conf.group_users_mapping:
        users = conf.group_users_mapping.get((company_id, group_name))
        for user in users:
            username = user.get('username')
            trace_id = str(uuid.uuid4())
            url = REQUEST_GET_POLICY_URL.format(port=SERVICE_PORT, username=username, trace_id=trace_id)
            response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
            print("Request URL:", url)
            print("Response Code:", response.status_code)
            print("Response Body:", response.text)

    print("===Test Get User Traffic Usage===")
    REQUEST_GET_USER_TRAFFIC_USAGE_URL = "http://127.0.0.1:{port}/api/v1/getusertrafficusage?username={username}&traceid={trace_id}"
    for (company_id, group_name) in conf.group_users_mapping:
        users = conf.group_users_mapping.get((company_id, group_name))
        for user in users:
            username = user.get('username')
            trace_id = str(uuid.uuid4())
            url = REQUEST_GET_USER_TRAFFIC_USAGE_URL.format(port=SERVICE_PORT, username=username, trace_id=trace_id)
            response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
            print("Request URL:", url)
            print("Response Code:", response.status_code)
            print("Response Body:", response.text)

    print("===Test Get Group Traffic Usage===")
    REQUEST_GET_GROUP_TRAFFIC_USAGE_URL = "http://127.0.0.1:{port}/api/v1/getgrouptrafficusage?companyid={company_id}&groupname={group_name}&traceid={trace_id}"
    for (company_id, group_name) in conf.group_users_mapping:
        trace_id = str(uuid.uuid4())
        url = REQUEST_GET_GROUP_TRAFFIC_USAGE_URL.format(port=SERVICE_PORT, company_id=company_id, group_name=group_name, trace_id=trace_id)
        response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
        print("Request URL:", url)
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

    print("===Test Get User Billing Usage===")
    REQUEST_GET_USER_BILLING_USAGE_URL = "http://127.0.0.1:{port}/api/v1/getuserbillingusage?username={username}&traceid={trace_id}"
    for (company_id, group_name) in conf.group_users_mapping:
        users = conf.group_users_mapping.get((company_id, group_name))
        for user in users:
            username = user.get('username')
            trace_id = str(uuid.uuid4())
            url = REQUEST_GET_USER_TRAFFIC_USAGE_URL.format(port=SERVICE_PORT, username=username, trace_id=trace_id)
            response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
            print("Request URL:", url)
            print("Response Code:", response.status_code)
            print("Response Body:", response.text)

    print("===Test Get Group Billing Usage===")
    REQUEST_GET_GROUP_BILLING_USAGE_URL = "http://127.0.0.1:{port}/api/v1/getgroupbillingusage?companyid={company_id}&groupname={group_name}&traceid={trace_id}"
    for (company_id, group_name) in conf.group_users_mapping:
        trace_id = str(uuid.uuid4())
        url = REQUEST_GET_GROUP_BILLING_USAGE_URL.format(port=SERVICE_PORT, company_id=company_id, group_name=group_name, trace_id=trace_id)
        response = requests.get(url=url, timeout=DEFAULT_REQUEST_TIMEOUT)
        print("Request URL:", url)
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)