from enum import Enum


class FunctionKind(Enum):
    NONE = 0
    OUTPUT = 1
    INPUT = 2
    INOUT = 3


class FunctionOperation(Enum):
    UNKNOWN = 0
    SINGLE_TARGET_INDEX = 1
