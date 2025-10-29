#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import uuid
import requests
import logging
import logging.config
from datetime import datetime
import time
import logging.handlers
from flask import Flask, request, jsonify

from domainhandler import DomainHandler
from userhandler import UserHandler
from policyhandler import PolicyHandler
from traffichandler import TrafficHandler
from billinghandler import BillingHandler
from cachehandler import CacheHandler


default_trace_id = 'accb07dd-9a73-4fa9-8092-161eaf093ded'
reponame = 'webproxy'


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'reponame'):
            record.reponame = reponame
        if not hasattr(record, 'trace_id'):
            record.trace_id = default_trace_id
        return super().format(record)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('flask').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
handler = logging.handlers.TimedRotatingFileHandler(
    '/var/log/webproxy.log', when='midnight', interval=1, backupCount=5
)
handler.setLevel(logging.INFO)
formatter = CustomFormatter(
    fmt='%(asctime)s.%(msecs)03d  %(levelname)s  trace_id=%(trace_id)s  %(reponame)s:%(filename)s:%(funcName)s:#%(lineno)d  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


DOMAIN_SERVICE_FQDN         = 'domain.webproxy.com'
USER_SERVICE_FQDN           = 'user.webproxy.com'
POLICY_SERVICE_FQDN         = 'policy.webproxy.com'
TRAFFIC_SERVICE_FQDN        = 'traffic.webproxy.com'
BILLING_SERVICE_FQDN        = 'billing.webproxy.com'
CACHE_SERVICE_FQDN          = 'cache.webproxy.com'
SERVICE_PORT                = '8080'
DEFAULT_REQUEST_TIMEOUT     = 30
DEFAULT_CACHE_TTL           = 7200
SHORT_CACHE_TTL             = 300
LONG_CACHE_TTL              = 86400

global_domain_handler = DomainHandler(DOMAIN_SERVICE_FQDN, SERVICE_PORT, DEFAULT_REQUEST_TIMEOUT)
global_user_handler = UserHandler(USER_SERVICE_FQDN, SERVICE_PORT, DEFAULT_REQUEST_TIMEOUT)
global_policy_handler = PolicyHandler(POLICY_SERVICE_FQDN, SERVICE_PORT, DEFAULT_REQUEST_TIMEOUT)
global_traffic_handler = TrafficHandler(TRAFFIC_SERVICE_FQDN, SERVICE_PORT, DEFAULT_REQUEST_TIMEOUT)
global_billing_handler = BillingHandler(BILLING_SERVICE_FQDN, SERVICE_PORT, DEFAULT_REQUEST_TIMEOUT)
global_cache_handler = CacheHandler(CACHE_SERVICE_FQDN, SERVICE_PORT, DEFAULT_CACHE_TTL)


app = Flask(__name__)

@app.route('/api/v1/getpolicy', methods=['GET'])
def get_policy_info():
    start = datetime.now()
    user_name = request.args.get('username')
    trace_id = request.args.get('traceid')
    extra = {'trace_id': trace_id, 'reponame': reponame}
    logging.info("Received request for getting the user policy info, username:%s", user_name, extra=extra)

    if not user_name or "@" not in user_name:
        err_msg = "Invalid username"
        logging.error("%s:%s", err_msg, user_name, extra=extra)
        return jsonify({"error": err_msg}), 400

    domain = user_name.split("@")[-1]
    cache_domain_exists_key = domain.lower() + "_exists"
    company_id = global_cache_handler.get_cache_key_value(cache_domain_exists_key, extra=extra, trace_id=trace_id)
    if not company_id:
        company_id = global_domain_handler.get_company_id(domain, extra=extra, trace_id=trace_id)
        if not company_id:
            cost_time = (datetime.now() - start).total_seconds() * 1000
            err_msg = "User not found"
            logging.error("End request for getting the user policy info, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
            return jsonify({"error": err_msg}), 404
        else:
            global_cache_handler.set_cache_key_value(cache_domain_exists_key, company_id, extra=extra, trace_id=trace_id, ttl=LONG_CACHE_TTL)

    policy_info = global_policy_handler.get_policy(company_id, extra=extra, trace_id=trace_id)
    cost_time = (datetime.now() - start).total_seconds() * 1000
    if not policy_info:
        err_msg = "Policy not found"
        logging.error("End request for getting the user policy info, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
        return jsonify({"error": err_msg}), 404
    else:
        logging.info("End request for getting the user policy info, username:%s, cost time:%.3fms, result:%r", user_name, cost_time, policy_info)
        return jsonify({"policy": policy_info}), 200

@app.route('/api/v1/getusertrafficusage', methods=['GET'])
def get_user_traffic_usage():
    start = datetime.now()
    user_name = request.args.get('username')
    trace_id = request.args.get('traceid')
    extra = {'trace_id': trace_id, 'reponame': reponame}
    logging.info("Received request for getting the user traffic usage, username:%s", user_name, extra=extra)

    if not user_name or "@" not in user_name:
        err_msg = "Invalid username"
        logging.error("%s:%s", err_msg, user_name, extra=extra)
        return jsonify({"error": err_msg}), 400

    domain = user_name.split("@")[-1]
    cache_domain_exists_key = domain.lower() + "_exists"
    company_id = global_cache_handler.get_cache_key_value(cache_domain_exists_key, extra=extra, trace_id=trace_id)
    if not company_id:
        company_id = global_domain_handler.get_company_id(domain, extra=extra, trace_id=trace_id)
        if not company_id:
            err_msg = "User not found"
            cost_time = (datetime.now() - start).total_seconds() * 1000
            logging.error("End request for getting the user traffic usage, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
            return jsonify({"error": err_msg}), 404
        else:
            global_cache_handler.set_cache_key_value(cache_domain_exists_key, company_id, extra=extra, trace_id=trace_id, ttl=LONG_CACHE_TTL)

    cache_user_exists_key = user_name.lower() + "_" + company_id + "_exists"
    user_id = global_cache_handler.get_cache_key_value(cache_user_exists_key, extra=extra, trace_id=trace_id)
    if not user_id:
        user_id = global_user_handler.get_user_id(company_id, user_name, extra=extra, trace_id=trace_id)
        if not user_id:
            err_msg = "User not found"
            cost_time = (datetime.now() - start).total_seconds() * 1000
            logging.error("End request for getting the user traffic usage, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
            return jsonify({"error": err_msg}), 404
        else:
            global_cache_handler.set_cache_key_value(cache_user_exists_key, user_id, extra=extra, trace_id=trace_id, ttl=LONG_CACHE_TTL)

    company_total_traffic = 0
    company_international_traffic = global_traffic_handler.get_company_international_traffic(company_id, extra=extra, trace_id=trace_id)
    if company_international_traffic:
        company_total_traffic += company_international_traffic
    company_domestic_traffic = global_traffic_handler.get_company_domestic_traffic(company_id, extra=extra, trace_id=trace_id)
    if company_domestic_traffic:
        company_total_traffic += company_domestic_traffic

    user_total_traffic = 0
    user_international_traffic = global_traffic_handler.get_user_international_traffic(user_id, extra=extra, trace_id=trace_id)
    if user_international_traffic:
        user_total_traffic += user_international_traffic
    user_domestic_traffic = global_traffic_handler.get_user_domestic_traffic(user_id, extra=extra, trace_id=trace_id)
    if user_domestic_traffic:
        user_total_traffic += user_domestic_traffic

    traffic_info = {
        "companyTotalTraffic": company_total_traffic,
        "userTotalTraffic": user_total_traffic,
        "usagePercentage": (user_total_traffic / company_total_traffic * 100) if company_total_traffic > 0 else 0
    }

    cost_time = (datetime.now() - start).total_seconds() * 1000
    logging.info("End request for getting the user traffic usage, username:%s, cost time:%.3fms, result:%r", user_name, cost_time, traffic_info, extra=extra)
    return jsonify({"traffic": traffic_info}), 200

@app.route('/api/v1/getgrouptrafficusage', methods=['GET'])
def get_group_traffic_usage():
    start = datetime.now()
    trace_id = request.args.get('traceid')
    company_id = request.args.get('companyid')
    group_name = request.args.get('groupname')
    extra = {'trace_id': trace_id, 'reponame': reponame}
    logging.info("Received request for getting the group traffic usage, company id:%s, group name:%s", company_id, group_name, extra=extra)

    if not company_id or not group_name:
        err_msg = "Invalid company id or group name"
        logging.error("%s, company id:%s, group name:%s", err_msg, company_id, group_name, extra=extra)
        return jsonify({"error": err_msg}), 400

    users = global_user_handler.get_all_group_users(company_id, group_name, extra=extra, trace_id=trace_id)
    if not users:
        err_msg = "Group not found"
        cost_time = (datetime.now() - start).total_seconds() * 1000
        logging.error("End request for getting the group traffic usage, company id:%s, group name:%s, cost time:%.3fms, result:%s", company_id, group_name, cost_time, err_msg, extra=extra)
        return jsonify({"error": err_msg}), 404

    company_total_traffic = 0
    company_international_traffic = global_traffic_handler.get_company_international_traffic(company_id, extra=extra, trace_id=trace_id)
    if company_international_traffic:
        company_total_traffic += company_international_traffic
    company_domestic_traffic = global_traffic_handler.get_company_domestic_traffic(company_id, extra=extra, trace_id=trace_id)
    if company_domestic_traffic:
        company_total_traffic += company_domestic_traffic

    group_total_traffic = 0
    for user in users:
        user_id = user.get('user_id')
        user_total_traffic = 0
        user_international_traffic = global_traffic_handler.get_user_international_traffic(user_id, extra=extra, trace_id=trace_id)
        if user_international_traffic:
            user_total_traffic += user_international_traffic
        user_domestic_traffic = global_traffic_handler.get_user_domestic_traffic(user_id, extra=extra, trace_id=trace_id)
        if user_domestic_traffic:
            user_total_traffic += user_domestic_traffic
        group_total_traffic += user_total_traffic

    traffic_info = {
        "companyTotalTraffic": company_total_traffic,
        "groupTotalTraffic": group_total_traffic,
        "usagePercentage": (group_total_traffic / company_total_traffic * 100) if company_total_traffic > 0 else 0
    }

    cost_time = (datetime.now() - start).total_seconds() * 1000
    logging.info("End request for getting the group traffic usage, company id:%s, group name:%s, cost time:%.3fms, result:%r", company_id, group_name, cost_time, traffic_info, extra=extra)
    return jsonify({"traffic": traffic_info}), 200

@app.route('/api/v1/getuserbillingusage', methods=['GET'])
def get_user_billing_usage():
    start = datetime.now()
    user_name = request.args.get('username')
    trace_id = request.args.get('traceid')
    extra = {'trace_id': trace_id, 'reponame': reponame}
    logging.info("Received request for getting the user billing info, username:%s", user_name, extra=extra)

    if not user_name or "@" not in user_name:
        err_msg = "Invalid username"
        logging.error("%s, username:%s", err_msg, user_name, extra=extra)
        return jsonify({"error": err_msg}), 400

    domain = user_name.split("@")[-1]
    cache_domain_exists_key = domain.lower() + "_exists"
    company_id = global_cache_handler.get_cache_key_value(cache_domain_exists_key, extra=extra, trace_id=trace_id)
    if not company_id:
        company_id = global_domain_handler.get_company_id(domain, extra=extra, trace_id=trace_id)
        if not company_id:
            err_msg = "User not found"
            cost_time = (datetime.now() - start).total_seconds() * 1000
            logging.error("End request for getting the user billing info, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
            return jsonify({"error": err_msg}), 404
        else:
            global_cache_handler.set_cache_key_value(cache_domain_exists_key, company_id, extra=extra, trace_id=trace_id, ttl=LONG_CACHE_TTL)

    cache_user_exists_key = user_name.lower() + "_" + company_id + "_exists"
    user_id = global_cache_handler.get_cache_key_value(cache_user_exists_key, extra=extra, trace_id=trace_id)
    if not user_id:
        user_id = global_user_handler.get_user_id(company_id, user_name, extra=extra, trace_id=trace_id)
        if not user_id:
            err_msg = "User not found"
            cost_time = (datetime.now() - start).total_seconds() * 1000
            logging.error("End request for getting the user billing info, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
            return jsonify({"error": err_msg}), 404
        else:
            global_cache_handler.set_cache_key_value(cache_user_exists_key, user_id, extra=extra, trace_id=trace_id, ttl=LONG_CACHE_TTL)

    company_billing_info = global_billing_handler.get_company_billing_info(company_id, extra=extra, trace_id=trace_id)
    if company_billing_info is None:
        err_msg = "No company billing info found"
        cost_time = (datetime.now() - start).total_seconds() * 1000
        logging.error("End request for getting the user billing info, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
        return jsonify({"error": err_msg}), 404

    user_billing_info = global_billing_handler.get_user_billing_info(user_id, extra=extra, trace_id=trace_id)
    if user_billing_info is None:
        err_msg = "No user billing info found"
        cost_time = (datetime.now() - start).total_seconds() * 1000
        logging.error("End request for getting the user billing info, username:%s, cost time:%.3fms, result:%s", user_name, cost_time, err_msg, extra=extra)
        return jsonify({"error": err_msg}), 404

    billing_info = {
        "companyBilling": company_billing_info,
        "userBilling": user_billing_info,
        "usagePercentage": (user_billing_info / company_billing_info * 100) if company_billing_info > 0 else 0
    }

    cost_time = (datetime.now() - start).total_seconds() * 1000
    logging.info("End request for getting the user billing info, username:%s, cost time:%.3fms, result:%r", user_name, cost_time, billing_info, extra=extra)
    return jsonify({"billing": billing_info}), 200

@app.route('/api/v1/getgroupbillingusage', methods=['GET'])
def get_group_billing_usage():
    start = datetime.now()
    trace_id = request.args.get('traceid')
    company_id = request.args.get('companyid')
    group_name = request.args.get('groupname')
    extra = {'trace_id': trace_id, 'reponame': reponame}
    logging.info("Received request for getting the group billing usage, company id:%s, group name:%s", company_id, group_name, extra=extra)

    if not company_id or not group_name:
        err_msg = "Invalid company id or group name"
        logging.error("%s, company id:%s, group name:%s", err_msg, company_id, group_name, extra=extra)
        return jsonify({"error": err_msg}), 400

    users = global_user_handler.get_all_group_users(company_id, group_name, extra=extra, trace_id=trace_id)
    if not users:
        err_msg = "Group not found"
        cost_time = (datetime.now() - start).total_seconds() * 1000
        logging.error("End request for getting the group billing usage, company id:%s, group name:%s, cost time:%.3fms, result:%s", company_id, group_name, cost_time, err_msg, extra=extra)
        return jsonify({"error": err_msg}), 404

    company_billing_info = global_billing_handler.get_company_billing_info(company_id, extra=extra, trace_id=trace_id)
    if company_billing_info is None:
        err_msg = "No company billing info found"
        cost_time = (datetime.now() - start).total_seconds() * 1000
        logging.error("End request for getting the group billing usage, company id:%s, group name:%s, cost time:%.3fms, result:%s", company_id, group_name, cost_time, err_msg, extra=extra)
        return jsonify({"error": err_msg}), 404

    group_total_billing = 0
    for user in users:
        user_id = user.get('user_id')
        user_billing_info = global_billing_handler.get_user_billing_info(user_id, extra=extra, trace_id=trace_id)
        if user_billing_info:
            group_total_billing += user_billing_info

    billing_info = {
        "companyBilling": company_billing_info,
        "groupBilling": group_total_billing,
        "usagePercentage": (group_total_billing / company_billing_info * 100) if company_billing_info > 0 else 0
    }

    cost_time = (datetime.now() - start).total_seconds() * 1000
    logging.info("End request for getting the group billing usage, company id:%s, group name:%s, cost time:%.3fms, result:%r", company_id, group_name, cost_time, billing_info, extra=extra)
    return jsonify({"billing": billing_info}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVICE_PORT)
