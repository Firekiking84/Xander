from enum import Enum


class FunctionKind(Enum):
    NONE = 0
    OUTPUT = 1
    INPUT = 2
    INOUT = 3


class FunctionOperation(Enum):
    UNKNOWN = 0
    SINGLE_TARGET_INDEX = 1
    SINGLE_TARGET_NAME = 2
    SRC_DEST_TARGET_INDEX = 3
    SRC_DEST_TARGET_NAME = 4
    QUANTITY_SET = 5
    QUANTITY_RM = 6
    QUANTITY_ADD = 7
