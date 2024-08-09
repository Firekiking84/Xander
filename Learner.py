import subprocess
import ast

from ParseExample import ParseExample
from ScriptRebuilding import ScriptRebuilding
from FunctionEnum import *


def get_functions_by_type(parsed_file, value1, value2=FunctionKind.INOUT.value):
    res = []
    for i in range(len(parsed_file.players_name)):
        for n_function in range(len(parsed_file.players[parsed_file.players_name[i]].functions_used)):
            if parsed_file.players[parsed_file.players_name[i]].functions_used[n_function].kind == value1 or \
                    parsed_file.players[parsed_file.players_name[i]].functions_used[n_function].kind == value2:
                res.append(parsed_file.players[parsed_file.players_name[i]].functions_used[n_function])
    res.sort(key=lambda function: function.time)
    return res


def get_output_value(output_lines, index):
    for line in output_lines:
        split_line = line.split(" ", 2)
        if (int(split_line[0])) == index:
            return ast.literal_eval(split_line[2])


def define_function_operation(parsed_file, output_file):
    file = open(output_file, 'r')
    output_lines = file.readlines()
    output_functions = get_functions_by_type(parsed_file, FunctionKind.OUTPUT.value)
    input_functions = get_functions_by_type(parsed_file, FunctionKind.INPUT.value)
    index_output_functions = 0
    for input_function in input_functions:
        next = get_output_value(output_lines, input_function.time)
        while index_output_functions < len(output_functions) and output_functions[
            index_output_functions].time < input_function.time:
            index_output_functions += 1
        if index_output_functions == len(output_functions):
            raise Exception("Error in the output file, no value before operation !")
        output_function = output_functions[index_output_functions]
        prev = get_output_value(output_lines, output_function.time)
        # Maintenant qu'on a avant après. On teste les différentes possibilités d'interaction
        is_operation_find = False;
        if type(prev) == type([]) and len(input_function.parameters) == 1:
            test_index = int(input_function.parameters[0])
            index = 0
            for prev_elem in prev:
                if index != test_index and prev_elem != next[index]:
                    break
                if index == test_index and prev_elem == next[index]:
                    break
                index += 1
            if index == len(prev):
                input_function.operation = FunctionOperation.SINGLE_TARGET_INDEX.value
                is_operation_find = True
        if not is_operation_find:
            input_function.operation = FunctionOperation.UNKNOWN.value
            print("Mode d'entrée inconnu !")
    print(output_lines)


def start_player_creation(parsed_file, player_name):
    pool_test = "poolTest.py"
    output_file = "output.txt"
    ScriptRebuilding(parsed_file, pool_test, output_file)
    subprocess.run(["python", pool_test])
    define_function_operation(parsed_file, output_file)


#    build_player(parsed_file, player_name, pool_test, output_file)


def learner(example_file, player_name):
    parsed_file = ParseExample(example_file)
    if len(parsed_file.players) == 0:
        raise Exception("Error in the example file ! No player detected !")
    start_player_creation(parsed_file, player_name)


learner("exampleMorpion.py", "morpionPlayer")
