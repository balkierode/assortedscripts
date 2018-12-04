"""
A simple wrapper around aws dynamodb table that lets you use as a persistent dict/hashmap. 
The table should have two fields 'mapkey' (primary), 'value'
Though not explicitly tested, should work with most python3 versions

Usage:
>>> d = DynamoDict(mytable)
>>> d["mykey"] = "myvalue"
>>> val = d["mykey"]
>>> if "mykey" in d:
>>>     print("Good!")

Note: Currently supports only the above functionality as that is what I needed. Feel free to implement/improve further and send a pull request
"""

import collections


class DynamoDictKeyError(KeyError):
    pass


class DynamoDict(collections.abc.MutableMapping):
    def __init__(self, table):
        self.table = table

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def get(self, k):
        resp = self.table.get_item(Key=dict(mapkey=k))
        if 'Item' in resp:
            return resp['Item']['value']

    def __getitem__(self, k):
        val = self.get(k)
        if not val:
            raise DynamoDictKeyError(k)
        return val

    def __contains__(self, item):
        val = self.get(item)
        if val:
            return True
        else:
            return False

    def __delitem__(self, v):
        raise NotImplementedError

    def __setitem__(self, k, v):
        self.table.put_item(Item=dict(mapkey=k, value=v))

