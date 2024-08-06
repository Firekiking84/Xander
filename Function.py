from Variable import Variable
from FunctionEnum import FunctionKind


class Function:
    def __init__(self, name="", return_value=None, parameters=None, time=0, kind=None, operation=None):
        if parameters is None:
            parameters = []
        self.name = name
        self.return_value = return_value
        self.parameters = parameters
        self.time = time
        if kind is not None:
            self.kind = kind
        else:
            if len(self.parameters) > 0 and self.return_value is not None:
                self.kind = FunctionKind.INOUT.value
            elif len(self.parameters) > 0:
                self.kind = FunctionKind.INPUT.value
            elif self.return_value is not None:
                self.kind = FunctionKind.OUTPUT.value
            else:
                self.kind = FunctionKind.NONE.value
        self.operation = operation

    def __cmp__(self, other):
        if self.name == other.name:
            return True
        return False

    def __str__(self):
        return_str = f"Function's Name : {self.name}\n"
        return_str += f"Return Value : [{self.return_value}]\n"
        return_str += f"Parameters : {self.parameters}\n"
        return_str += f"Used at : {self.time}\n"
        return return_str
