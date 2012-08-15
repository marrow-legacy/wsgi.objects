# encoding: utf-8

class MockObject(object):
    def __init__(self):
        self._data = dict()

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name] = value

    def __delitem__(self, name):
        del self._data[name]

    def __contains__(self, name):
        return name in self._data
    
    def __iter__(self):
        return iter(self._data)

    def get(self, name, default=None):
        return self._data.get(name, default)
