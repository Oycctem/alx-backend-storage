#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    col = client.logs.nginx
    total_logs = col.estimated_document_count()
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = col.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check = col.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")
