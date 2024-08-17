#!/usr/bin/env python3
"""Python function that lists all documents in a collection"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection.

    Args:
        mongo_collection: A pymongo collection object.

    Returns:
        a list of all document in the collection.
    """
    if mongo_collection.find():
        return list(mongo_collection.find())

    return []
