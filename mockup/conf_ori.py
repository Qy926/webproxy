#!/usr/bin/env python
# -*- coding:utf-8 -*-


domain_company_mapping = {
    "163.com": "28d31999-a5b8-46af-a32b-e7af050adaa2",
    "hotmail.com": "0783bede-409c-4a75-b488-9ee86e8e63ec",
    "trendmicro.com": "e0bac94a-6559-49fd-a5e2-84f4f93af166"
}

company_policy_mapping = {
    "28d31999-a5b8-46af-a32b-e7af050adaa2": {
        "max_user_billing": 1000,
        "max_group_billing": 5000,
        "max_company_billing": 10000
    },
    "0783bede-409c-4a75-b488-9ee86e8e63ec": {
        "max_user_billing": 2000,
        "max_group_billing": 10000,
        "max_company_billing": 20000
    },
    "e0bac94a-6559-49fd-a5e2-84f4f93af166": {
        "max_user_billing": 3000,
        "max_group_billing": 15000,
        "max_company_billing": 30000
    }
}

company_users_mapping = {
    ("28d31999-a5b8-46af-a32b-e7af050adaa2", "alice@163.com"): "dd4facb4-ca9e-4b1a-891a-7c69e79d0f9a",
    ("28d31999-a5b8-46af-a32b-e7af050adaa2", "bob@163.com"): "756eb564-27c5-4f86-a6e3-e70065dcaeb8",
    ("0783bede-409c-4a75-b488-9ee86e8e63ec", "dave@hotmail.com"): "28720977-ff43-4d6e-ae20-68ba80ab9a77",
    ("0783bede-409c-4a75-b488-9ee86e8e63ec", "eve@hotmail.com"): "49e25fe6-b39b-401c-9a1d-ff3fd0b55cb9",
    ("0783bede-409c-4a75-b488-9ee86e8e63ec", "frank@hotmail.com"): "ef505d50-744b-44be-b5ba-b84414cc291f",
    ("e0bac94a-6559-49fd-a5e2-84f4f93af166", "grace@trendmicro.com"): "cd5bb77f-5487-4db2-99e0-d9295cd94ee9",
    ("e0bac94a-6559-49fd-a5e2-84f4f93af166", "heidi@trendmicro.com"): "3d8ef549-30ec-4986-ac21-dbd23dc89fb5",
    ("e0bac94a-6559-49fd-a5e2-84f4f93af166", "ivan@trendmicro.com"): "7c9b3688-d897-4806-835a-5411f175ee63",
    ("e0bac94a-6559-49fd-a5e2-84f4f93af166", "kyle@trendmicro.com"): "0a1625ab-0776-43dd-8e9b-a81cd90ac4c9"
}

group_users_mapping = {
    ("28d31999-a5b8-46af-a32b-e7af050adaa2", "engineering"): [
        {
            "username":"alice@163.com",
            "user_id": "dd4facb4-ca9e-4b1a-891a-7c69e79d0f9a"
        },
        {
            "username":"bob@163.com",
            "user_id": "756eb564-27c5-4f86-a6e3-e70065dcaeb8"
        }
    ],
    ("0783bede-409c-4a75-b488-9ee86e8e63ec", "marketing"): [
        {
            "username": "dave@hotmail.com",
            "user_id": "28720977-ff43-4d6e-ae20-68ba80ab9a77"
        },
        {
            "username": "eve@hotmail.com",
            "user_id": "49e25fe6-b39b-401c-9a1d-ff3fd0b55cb9"
        },
        {
            "username": "frank@hotmail.com",
            "user_id": "ef505d50-744b-44be-b5ba-b84414cc291f"
        }
    ],  
    ("e0bac94a-6559-49fd-a5e2-84f4f93af166", "sales"): [
        {
            "username": "grace@trendmicro.com",
            "user_id": "cd5bb77f-5487-4db2-99e0-d9295cd94ee9"
        },
        {
            "username": "heidi@trendmicro.com",
            "user_id": "3d8ef549-30ec-4986-ac21-dbd23dc89fb5"
        },
        {
            "username": "ivan@trendmicro.com",
            "user_id": "7c9b3688-d897-4806-835a-5411f175ee63"
        },
        {
            "username": "kyle@trendmicro.com",
            "user_id": "0a1625ab-0776-43dd-8e9b-a81cd90ac4c9"
        }
    ]
}

company_traffic_mapping = {
    "28d31999-a5b8-46af-a32b-e7af050adaa2": {
        "international_traffic": 7000,
        "domestic_traffic": 3000
    },
    "0783bede-409c-4a75-b488-9ee86e8e63ec": {
        "international_traffic": 8000,
        "domestic_traffic": 4000
    },
    "e0bac94a-6559-49fd-a5e2-84f4f93af166": {
        "international_traffic": 9000,
        "domestic_traffic": 5000
    }
}

user_traffic_mapping = {
    "dd4facb4-ca9e-4b1a-891a-7c69e79d0f9a": {
        "international_traffic": 700,
        "domestic_traffic": 300
    },
    "756eb564-27c5-4f86-a6e3-e70065dcaeb8": {
        "international_traffic": 800,
        "domestic_traffic": 400
    },
    "28720977-ff43-4d6e-ae20-68ba80ab9a77": {
        "international_traffic": 900,
        "domestic_traffic": 500
    },
    "49e25fe6-b39b-401c-9a1d-ff3fd0b55cb9": {
        "international_traffic": 1000,
        "domestic_traffic": 600
    },
    "ef505d50-744b-44be-b5ba-b84414cc291f": {
        "international_traffic": 1100,
        "domestic_traffic": 700
    },
    "cd5bb77f-5487-4db2-99e0-d9295cd94ee9": {
        "international_traffic": 1200,
        "domestic_traffic": 800
    },
    "3d8ef549-30ec-4986-ac21-dbd23dc89fb5": {
        "international_traffic": 1300,
        "domestic_traffic": 900
    },
    "7c9b3688-d897-4806-835a-5411f175ee63": {
        "international_traffic": 1400,
        "domestic_traffic": 1000
    },
    "0a1625ab-0776-43dd-8e9b-a81cd90ac4c9": {
        "international_traffic": 1500,
        "domestic_traffic": 1100
    }
}

company_billing_mapping = {
    "28d31999-a5b8-46af-a32b-e7af050adaa2": 8000,
    "0783bede-409c-4a75-b488-9ee86e8e63ec": 12000,
    "e0bac94a-6559-49fd-a5e2-84f4f93af166": 18000
}

user_billing_mapping = {
    "dd4facb4-ca9e-4b1a-891a-7c69e79d0f9a": 800,
    "756eb564-27c5-4f86-a6e3-e70065dcaeb8": 900,
    "28720977-ff43-4d6e-ae20-68ba80ab9a77": 1000,
    "49e25fe6-b39b-401c-9a1d-ff3fd0b55cb9": 1100,
    "ef505d50-744b-44be-b5ba-b84414cc291f": 1200,
    "cd5bb77f-5487-4db2-99e0-d9295cd94ee9": 1300,
    "3d8ef549-30ec-4986-ac21-dbd23dc89fb5": 1400,
    "7c9b3688-d897-4806-835a-5411f175ee63": 1500,
    "0a1625ab-0776-43dd-8e9b-a81cd90ac4c9": 1600
}