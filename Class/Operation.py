from Class.FunctionEnum import FunctionOperation

class Operation:
    def __init__(self, kind=FunctionOperation.UNKNOWN.value, variable=None):
        self.kind = kind
        self.variable = variable