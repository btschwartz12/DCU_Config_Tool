

from collections import OrderedDict
from dataclasses import dataclass, fields


def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def toStr(data) -> str:
    _str = ""
    if isinstance(data, list):
        for val in data:
            _str += str(val) + ','
        _str = _str[:len(_str)-1]
    elif isinstance(data, int):
        _str = str(data)
    elif isinstance(data, str):
        _str = data
    else:
        _str = ""
    return _str


@dataclass
class StepData:

    def validate(self):
        for field in fields(self):
            val = getattr(self, field.name)
            if val is None: ############ 
                raise Exception(type(self).__name__+": "+field.name+" is not initialized")

    def getOrderedDict(self) -> OrderedDict:
        data = OrderedDict()
        for field in fields(self):
            val = getattr(self, field.name)
            data[field.name] = val
        return data



class EntryException(Exception):
    def __init__(self, name, msg):
        self.entry_name = name
        self.error_msg = msg
