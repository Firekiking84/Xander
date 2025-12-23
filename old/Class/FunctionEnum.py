from enum import Enum

class FunctionKind(Enum):
    NONE = 0
    OUTPUT = 1
    INPUT = 2
    INOUT = 3
