#!/usr/bin/env python3


"""
Module: 101-students
Contains: top_students
Function: top_students
"""


from pymongo import collection


def top_students(mongo_collection):
    """
    Function that returns all students sorted by average score.

    Args:
        mongo_collection: pymongo collection object

    Returns:
        List of dictionaries, each containing student information with
        an additional 'averageScore' key representing the average score
        of the student.
    """
    students = list(mongo_collection.find())

    for student in students:
        total_score = 0
        num_topics = 0

        for topic in student['topics']:
            total_score += topic['score']
            num_topics += 1

        student['averageScore'] = total_score / num_topics

    return sorted(students, key=lambda x: x['averageScore'], reverse=True)


if __name__ == "__main__":
    pass  # No code should be executed when imported
