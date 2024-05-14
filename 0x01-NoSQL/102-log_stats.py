#!/usr/bin/env python3

"""
MongoDB class
"""


from pymongo import MongoClient


class MongoDB:
    """ MongoDB class """

    def __init__(self):
        """ Initialize MongoDB connection """
        self.client = MongoClient('mongodb://127.0.0.1:27017')
        self.collection_logs = self.client.logs.nginx

    def count_logs(self):
        """ Count logs """
        return self.collection_logs.count_documents({})

    def count_methods(self, methods):
        """ Count methods """
        method_counts = {
            method: self.collection_logs.count_documents({"method": method})
            for method in methods
        }
        return method_counts

    def top_ips(self):
        """ Get top 10 IPs """
        pipeline = [
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        top_ips = self.collection_logs.aggregate(pipeline)
        return {ip["_id"]: ip["count"] for ip in top_ips}


if __name__ == "__main__":
    mongo = MongoDB()
    total_logs = mongo.count_logs()
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = mongo.count_methods(methods)
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")

    top_ips = mongo.top_ips()
    print("IPs:")
    for ip, count in top_ips.items():
        print(f"    {ip}: {count}")
