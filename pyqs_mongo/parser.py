"""
    Author: mrpycharm
    A URL query string parser that parses and converts the given query string into a MongoDB query.
    The resulting MongoDB query dict is a python `dict` object which is compatible with
    `pymongo` and `MongoEngine`.

    Supported MongoDB operators:
        - $eq
        - $gt
        - $gte
        - $lt
        - $ne
        - $in
        - $nin

    Operators to be supported in future:
        - $exists
        - $regex
        - Geospatial operators
        - Date comparision
"""

# --- system imports
from typing import Union, Tuple

# --- framework imports
from urllib import parse as ulib_parse

# --- local imports


class PyQSMongoParser:
    """
        The main parser class that initiates the parsing of a query string into
        a MongoDB query dict.

        :param qs: The query string to parse.
    """
    def __init__(self, qs: str):
        self.qs = qs
        self.query = {}
        self.operators = ['!', '>', '<']
        self.operator_map = {
            '!': '$ne',
            '>': '$gt',
            '>=': '$gte',
            '<': '$lt',
            '<=': '$lte',
            '[]': '$in',
            '[!]': '$nin'
        }

    @staticmethod
    def qs_to_dict(qs: str) -> dict:
        """
        Parses the query string into a python `dict`.
        Currently we use urllib's parse module to parse the query string.
        Later we might write our own parser, if needed.

        :param qs: The query string to parse.
        :return: The `dict` object. This `dict` object will have key-value-pairs
        where each value is an array of elements.
        """
        return ulib_parse.parse_qs(qs)

    def guess_operator(self, value) -> Tuple[Union[str, None], str]:
        """
        Parses the given value and try's to guess the relevant MongoDB operator for it.

        :param value: The value to parse.
        :return: Returns a tuple of the identified MongoDB operator and the value to apply the operator on.
         NOTE (mrpycharm): `None` is also returned in the position of operator in the returned tuple when
         no operator is intended to be applied onto the given value.
        """
        if value.startswith('<='):
            return '$lte', value[2:]

        if value.startswith('>='):
            return '$gte', value[2:]

        if value.startswith('<'):
            return '$lt', value[1:]

        if value.startswith('>'):
            return '$gt', value[1:]

        if value.startswith('!'):
            return '$ne', value[1: ]

        if value.startswith('[]'):
            return '$in', value[2: ]

        if value.startswith('[!]'):
            return '$nin', value[3: ]

        return None, value

    @staticmethod
    def finalize_sub_query(key: str, sub_query: dict) -> dict:
        """
        Finalizes (transforms the query) into a proper format.
        The sub-query is expected to be in the format where the key should be a MongoDB operator
        and the value should be an array of elements to apply the operator to.
        In case of MongoDB operators where arrays are required like `$in` and `$nin`, entire
        array would be set as the value of that operator. in the rest of the cases, only 1st
        element is chosen to tbe added (ideally should only be 1 element).

        :param key: The key to attach the sub-query with
        :param sub_query: The `dict` object that contains keys as MongoDB operators and values
         as a list of elements to add to the query.
        :return: Returns a `dict` object with key as an MongoDB operator and the value as the value
         to apply that operator to.
        """
        _sub_query = {}
        for _key, value in sub_query.items():
            if _key is None:
                return {key: value[-1]}

            elif _key not in ('$in', '$nin'):
                value = value[-1]

            _sub_query.update({_key: value})

        return {key: _sub_query}

    def parse(self) -> dict:
        """
        Parses the query string into a MongoDB query.
        If unable to parse the query string, raises an exception.
        :return: A python `dict` object which is essentially a MongoDB query `dict`,
        compatible with `PyMongo` and `MongoEngine`.
        """
        # parse qs into a dict
        parsed_qs = self.qs_to_dict(self.qs)

        # the resulting dict from the above operations will have its value in arrays
        # a value is a single element array if only found once in the query string, else an array of length > 1
        # for each element for a value in key-value pair of the quesry string, we try to "guess" the
        # operator that needs to be applied.
        # we align all the operators that need to applied on a given key and based on those operators
        # we finalize the query (different format for different operators like $nin, $in, $gte e.t.c)
        for key, value in parsed_qs.items():
            sub_query = {}

            for element in value:
                operator, _element = self.guess_operator(element)
                if not sub_query.get(operator, None):
                    sub_query[operator] = [_element]
                else:
                    sub_query[operator].append(_element)

            self.query.update(self.finalize_sub_query(key, sub_query))

        # parsed the query string, we can return now
        return self.query


def parse(qs: str) -> dict:
    """
    This function is the entry point for parsing the query string into a MongoDB query dict.
    :param qs: The query string to parse into a MongoDB query dict.
    :return: Returns a query dict which is compatible with the MongoDB driver and MongoEngine.
    An exception is raise if unable to parse the query string.
    """
    parser = PyQSMongoParser(qs)
    return parser.parse()
