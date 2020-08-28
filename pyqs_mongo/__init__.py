"""
    Author: mrpycharm
    The PyQSMongo package is a parser that parses a given URL query string into a MongoDB
    query. The resulting query object is a python `dict` which is compatible with `PyMongo`
    and `MongoEngine`.
"""
# --- system imports
# --- framework imports
# --- local imports
from .parser import parse
