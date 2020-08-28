# PyQS Mongo

A useful tool to parse the query string parameters on a resource into a 
MongoDB query object (compatible with PyMongo and MongoEngine).

Inspired by: https://github.com/Turistforeningen/node-mongo-querystring


## Features (Coming Soon)

* Aliased query parameters
* Blacklisted query parameters
* Whitelisted query parameters
* Geospatial operators
* Date comparision
* Basic operators to support
  * `$exists`
  * `$regex`


## Features
* Basic operators
  * `$eq`
  * `$gt`
  * `$gte`
  * `$lt`
  * `$lte`
  * `$ne`
  * `$in`
  * `$nin`


| operation | query string  | query object |
|-----------|---------------|--------------|
| equal     | `?foo=bar`    | `{ foo: "bar" }` |
| unequal   | `?foo=!bar`   | `{ foo: { $ne: "bar" }}` |
| greater than | `?foo=>10` | `{ foo: { $gt: 10 }}` |
| less than | `?foo=<10`    | `{ foo: { $lt: 10 }}` |
| greater than or equal to | `?foo=>=10` | `{ foo: { $gte: 10 }}` |
| less than or equal to | `?foo=<=10`    | `{ foo: { $lte: 10 }}` |
| in array  | `?foo=[]bar&foo=[]baz` | `{ foo: { $in: ['bar', 'baz'] }}` |
| not in array | `?foo=[!]bar&foo=[!]baz` | `{ foo: { $nin: ['bar', 'baz'] }}` |


## Install

```
pip install pyqs-mongo
```

## API

```python
from pyqs_mongo import parse

qs = 'name=ahmed&company=someCompany&age=>=20&age=<=50&username=[]ahmed&username=[]adh&username=[!]some'
query = parse(qs)
print(query)
```

## Tests
* Coming Soon


### Collaborators

* Ahmed Pyar Ali - @mrpycharm

## [MIT Licensed](https://raw.githubusercontent.com/Turistforeningen/node-mongo-querystring/master/LICENSE)