class ScriptRebuilding:
    def next_player(self):
        for i in range(len(self.parsed_file.players_name)):
            if self.parsed_file.players_name[i] == self.current_player:
                i += 1
                if i == len(self.parsed_file.players_name):
                    self.current_player = self.parsed_file.players_name[0]
                    return
                self.current_player = self.parsed_file.players_name[i]
                return
        self.current_player = self.parsed_file.players_name[0]

    def next_function(self):
        find = False
        start_research = self.current_player
        while not find:
            function_index = self.parsed_file.players[self.current_player].get_time_function(self.time)
            if function_index == -1:
                self.next_player()
                if self.current_player == start_research:
                    return None
            else:
                self.time += 1
                return self.parsed_file.players[self.current_player].functions_used[function_index]

    def write_function(self, file, function):
        return_value = function.return_value
        if not return_value.is_empty:
            file.write(return_value.name)
            file.write(" = ")
        file.write(f"{function.name}(")
        for i in range(len(function.parameters)):
            file.write(f"{function.parameters[i]}")
            if (i + 1) < len(function.parameters):
                file.write(", ")
        file.write(")\n")
        if not return_value.is_empty and return_value.kind != "game":
            write_content = f"output.write(f\"{function.time} {return_value.name} " + \
                            "{" + \
                            f"{return_value.name}" + \
                            "}\\n\")\n"
            file.write(write_content)

    def write_functions(self, file, functions):
        for function in functions:
            self.write_function(file, function)
            self.time += 1

    def __init__(self, parsed_file, pool_test, output_file):
        self.parsed_file = parsed_file
        self.current_player = parsed_file.players_name[0]
        self.time = 0
        file = open(pool_test, "w+")
        for line in parsed_file.imports:
            file.write(line)
        file.write(f"\noutput = open(\"{output_file}\", \"w+\")\n")
        self.write_functions(file, parsed_file.init_functions)
        current_function = self.next_function()
        while current_function is not None:
            self.write_function(file, current_function)
            current_function = self.next_function()
        file.write("output.close()")
        file.close()
