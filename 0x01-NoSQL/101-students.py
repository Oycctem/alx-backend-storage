#!/usr/bin/env python3
"""Top students"""
import pymongo


def top_students(mongo_collection):
    """
    returns all students sorted by average score:
    """
    pipeline = [
        {
            '$project': {
                'name': '$name',
                'averageScore': {'$avg': '$scores.score'}
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
