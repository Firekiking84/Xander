from Class.FunctionEnum import FunctionOperation

class Operation:
    def __init__(self, kind=FunctionOperation.UNKNOWN.value, variable=None):
        self.kind = kind
        self.variable = variable

    def __cmp__(self, other):
        return self.kind == other.kind and self.variable.name == other.variable.name