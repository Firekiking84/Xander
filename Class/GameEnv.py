class GameEnv:
    def __init__(self, name=None, getter=None, setter=None):
        self.name = name
        self.getter = getter
        self.setter = setter

    def __str__(self):
        return self.name

    def __cmp__(self, other):
        return self.name == other.name
