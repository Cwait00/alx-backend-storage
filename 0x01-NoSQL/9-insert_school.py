#!/usr/bin/env python3

"""
Inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in the collection

    Args:
        mongo_collection: pymongo collection object
        **kwargs: key-value pairs for the document to be inserted

    Returns:
        new _id of the inserted document, or None if insertion fails
    """
    existing_doc = mongo_collection.find_one(kwargs)
    if existing_doc:
        return None
    else:
        new_doc_id = mongo_collection.insert_one(kwargs).inserted_id
        return new_doc_id


if __name__ == "__main__":
    pass  # No code should be executed when imported
