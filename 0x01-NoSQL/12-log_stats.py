#!/usr/bin/env python3


"""
Provides some stats about Nginx logs stored in MongoDB
"""


def log_stats(logs_collection):
    """
    Provides stats about Nginx logs

    Args:
        logs_collection: pymongo collection object for Nginx logs

    Returns:
        None
    """
    # Total number of logs
    total_logs_count = logs_collection.count_documents({})

    # Methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: logs_collection.count_documents({"method": method})
                     for method in methods}

    # Number of status checks
    status_check_count = logs_collection.count_documents({"method": "GET",
                                                          "path": "/status"})

    # Display stats
    print(f"{total_logs_count} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    from pymongo import MongoClient

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    logs_collection = db.nginx

    # Call log_stats function
    log_stats(logs_collection)
