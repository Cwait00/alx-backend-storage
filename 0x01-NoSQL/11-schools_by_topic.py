#!/usr/bin/env python3

"""
Returns the list of schools having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic

    Args:
        mongo_collection: pymongo collection object
        topic (string): Topic to search for

    Returns:
        List of unique schools with the specified topic
    """
    cursor = mongo_collection.find({"topics": topic})
    unique_schools = {}
    for school in cursor:
        if school["name"] not in unique_schools:
            unique_schools[school["_id"]] = school
    return list(unique_schools.values())


if __name__ == "__main__":
    pass  # No code should be executed when imported
