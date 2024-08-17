#!/usr/bin/env python3
"""a Python function that returns
all students sorted by average score"""


def top_students(mongo_collection):
    """
    Return all students sorted by average score.
    Each document in the collection will have an added field 'avergescore'
    the students will be sorted in descending order by 'averagescore'
    """
    return list(mongo_collection.aggregate([
        {"$project": {
            "name": 1,
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]))
