class ContainsEmailError(Exception):
    pass

class WrongTypeError(Exception):
    def __init__(self, dict):
        types = {
            'dict': 'dictionary',
            'int': 'integer',
            'float': 'float',
            'list': 'list',
            'tuple': 'tuple'
        }
        self.dict = dict
        self.keys = [key for key in dict.keys() if type(dict[key]) != str]
        self.wrong_fields = [
            {key: types[type(dict[key]).__name__]} for key in self.keys
        ]