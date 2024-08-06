from Function import Function
from Player import Player
from Variable import Variable


class ParseExample:

    @staticmethod
    def check_kind(word):
        if "array" in word:
            return "array"
        elif "string" in word:
            return "string"
        elif "integer" in word:
            return "integer"
        elif "bool" in word:
            return "bool"
        elif "game" in word:
            return "game"
        else:
            raise Exception(f"Error in the example file ! Unknow Type only 'array', 'string' and 'integer' not {word}")

    @staticmethod
    def check_size(word):
        word = word.strip()
        if word.isdigit():
            return int(word)
        else:
            raise Exception("Size must be an integer !")

    def get_var_spe(self, line):
        word = ""
        size = 1
        is_kind = False
        has_kind = False
        is_size = False
        i = 0
        while i < len(line):
            if line[i] == '#':
                is_kind = True
                i += 1
            elif is_kind and line[i] == ' ':
                kind = self.check_kind(word)
                is_size = True
                is_kind = False
                has_kind = True
                word = ""
            elif is_size and line[i] == ' ' and len(word) > 0:
                return kind, self.check_size(word)
            elif is_kind or is_size:
                word += line[i]
            i += 1
        if is_kind:
            return self.check_kind(word), size
        elif len(word) > 0 and is_size and has_kind:
            return kind, self.check_size(word)
        else:
            raise Exception("Error in the example file ! Maybe type is missing !")

    def parse_line(self, line, mode):
        word = ""
        is_function = False
        has_return_value = False
        function_name = ""
        function_time = 0
        function_return_value = None
        function_parameters = []
        i = 0
        while i < len(line) and line[i] != '#':
            if line[i] == ' ':
                if is_function:
                    if has_return_value:
                        function_return_value = self.variables[-1]
                    else:
                        function_return_value = None
                    new_function = Function(function_name, function_return_value, function_parameters, function_time)
                    if mode == -2:
                        self.init_functions.append(new_function)
                    else:
                        self.players[mode].functions_used.append(new_function)
                    function_parameters = []
                else:
                    kind, size = self.get_var_spe(line)
                    self.variables.append(Variable(kind, size, word))
                    has_return_value = True
                while line[i] == ' ' or line[i] == '=':
                    i += 1
                word = ""
            elif line[i] == '(':
                if is_function:
                    raise Exception("Case not programmed ! ")
                is_function = True
                function_name = word
                if self.time >= 0:
                    function_time = self.time
                    self.time += 1
                word = ""
                i += 1
            elif line[i] == ',':
                function_parameters.append(word)
                word = ""
                i += 2
            elif line[i] == ')':
                if len(word) > 0:
                    function_parameters.append(word)
                word = ""
                i += 1
            else:
                word += line[i]
                i += 1

    def __init__(self, example_file):
        self.imports = []
        self.variables = []
        self.init_functions = []
        self.players = {}
        self.players_name = []
        self.winner = ""
        self.time = 0  # for chronology of calls during game
        # mode values -> -1: include; -2: init; x>0: n°x player
        mode = -1
        example = open(example_file, 'r')
        lines = example.readlines()
        example.close()
        for line in lines:
            if line[0] == '#':
                if "# include" in line:
                    mode = -1
                elif "# init" in line:
                    mode = -2
                elif "# end" in line:
                    self.winner = line[len("# end ")]
                elif "# player" in line:
                    mode = line[len("# player "):].strip()
            elif line[0] != '\n':
                if mode == -1:
                    self.imports.append(line)
                elif mode == -2:
                    self.parse_line(line, mode)
                else:
                    if mode not in self.players:
                        self.players[mode] = Player(mode)
                        self.players_name.append(mode)
                    self.parse_line(line, mode)
