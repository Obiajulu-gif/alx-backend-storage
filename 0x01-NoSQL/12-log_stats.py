#!/usr/bin/env python3
"""Python function that returns the
list of school having a specific topic"""
from pymongo import MongoClient


def log_stats():
    """log stats"""

    client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = client.logs.nginx

    total_logs = log_collection.count_documents({})
    print("{} logs".format(total_logs))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        req_count = len(list(log_collection.find({"method": method})))
        print('\tmethod {}: {}'.format(method, req_count))

    status_check = len(list(log_collection.find(
        {"method": "GET", "path": "/status"})))
    print("{} status check".format(status_check))


if __name__ == "__main__":
    log_stats()
