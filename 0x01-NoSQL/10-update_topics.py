#!/usr/bin/env python3

"""
Changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name

    Args:
        mongo_collection: pymongo collection object
        name: name of the school to update
        topics: list of strings containing topics

    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})


if __name__ == "__main__":
    pass  # No code should be executed when imported
