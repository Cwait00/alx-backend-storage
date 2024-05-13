#!/usr/bin/env python3

"""
8-all: Python function to list all documents in a collection
"""


def list_all(mongo_collection):
    """
    Lists all documents in the specified collection
    """

    documents = []
    for doc in mongo_collection.find():
        documents.append(doc)
    return documents


if __name__ == "__main__":
    from pymongo import MongoClient

    def main():
        client = MongoClient('mongodb://127.0.0.1:27017')
        school_collection = client.my_db.school
        schools = list_all(school_collection)
        for school in schools:
            print("[{}] {}".format(school.get('_id'), school.get('name')))

    main()
