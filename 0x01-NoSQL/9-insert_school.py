#!/usr/bin/env python3
"""Python function that inserts a new document
in a collection based on kwargs"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    insert a new document in a collection based on kwargs
     Args:
        mongo_collection: A pymongo collection object.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        The new _id of the inserted document.

    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
