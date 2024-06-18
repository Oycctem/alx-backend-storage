#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


def log_stats():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    colcs = db.nginx
    total_logs = colcs.count_docs({})
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = colcs.count_docs({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check_count = colcs.count_docs({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
