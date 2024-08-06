class Variable:
    def __init__(self, kind="", size=0, name=""):
        self.kind = kind
        self.size = size
        self.name = name
        if len(kind) == 0 or len(name) == 0:
            self.is_empty = True
        else:
            self.is_empty = False

    def __cmp__(self, other):
        if self.name == other.name:
            return True
        return False

    def __str__(self):
        return_str = f"Variable's Name : {self.name}\n"
        return_str += f"Type : {self.kind}\n"
        if self.kind == "array":
            return_str += f"Size : {self.size}"
        return return_str
