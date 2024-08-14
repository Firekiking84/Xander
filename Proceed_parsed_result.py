import subprocess
import ast

from Game import Game
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


def test_operation_single_target_index(prev, next_value, input_function):
    test_index = int(input_function.parameters[0])
    index = 0
    for prev_elem in prev:
        if index != test_index and prev_elem != next_value[index]:
            break
        if index == test_index and prev_elem == next_value[index]:
            break
        index += 1
    if index == len(prev):
        input_function.operation = FunctionOperation.SINGLE_TARGET_INDEX.value
        return True
    return False


def test_operation_single_target_name(prev, next_value, input_function):
    test_name = input_function.parameters[0]
    index = 0
    for prev_elem in prev:
        if test_name != prev_elem and prev_elem != next_value[index]:
            break
        if test_name == prev_elem and prev_elem == next_value[index]:
            break
        index += 1
    if index == len(prev):
        input_function.operation = FunctionOperation.SINGLE_TARGET_NAME.value
        return True
    return False


def test_operation_quantity(prev, next_value, input_function):
    test_quantity = input_function.parameters[0]
    if (prev - test_quantity) == next_value:
        input_function.operation = FunctionOperation.QUANTITY_RM.value
        return True
    if (prev + test_quantity) == next_value:
        input_function.operation = FunctionOperation.QUANTITY_ADD.value
        return True
    if next_value == test_quantity:
        input_function.operation = FunctionOperation.QUANTITY_SET.value
        return True
    return False


def test_operation_src_dest_target_index(prev, next_value, input_function):
    test_index1 = int(input_function.parameters[0])
    test_index2 = int(input_function.parameters[1])
    index = 0
    for prev_elem in prev:
        if (index != test_index1 or index != test_index2) and prev_elem != next_value[index]:
            break
        if (index == test_index1 or index == test_index2) and prev_elem == next_value[index]:
            break
        index += 1
    if index == len(prev):
        input_function.operation = FunctionOperation.SRC_DEST_TARGET_INDEX.value
        return True
    return False


def test_operation_src_dest_target_name(prev, next_value, input_function):
    test_name1 = input_function.parameters[0]
    test_name2 = input_function.parameters[0]
    index = 0
    for prev_elem in prev:
        if (test_name1 != prev_elem or test_name2 != prev_elem) and prev_elem != next_value[index]:
            break
        if (test_name1 == prev_elem or test_name2 == prev_elem) and prev_elem == next_value[index]:
            break
        index += 1
    if index == len(prev):
        input_function.operation = FunctionOperation.SRC_DEST_TARGET_NAME.value
        return True
    return False


def get_once_all_functions(input_functions):
    single_functions = []
    for input_function in input_functions:
        if input_function not in single_functions:
            single_functions.append(input_function)
    return single_functions


def get_main_operation(single_function, input_functions):
    operations = {}
    for input_function in input_functions:
        if input_function == single_function:
            if operations.get(input_function.operation) is not None:
                operations[input_function.operation] += 1
            else:
                operations[input_function.operation] = 1
    main_operation = None
    biggest_score = 0
    for key in operations.keys():
        score = operations.get(key)
        if score > biggest_score:
            biggest_score = score
            main_operation = key
    return main_operation


def apply_main_operation(target_function, input_functions, operation):
    for input_function in input_functions:
        if input_function == target_function:
            input_function.operation = operation


def uniform_function_operation(input_functions):
    #  On récupère toutes les fonctions une fois
    single_functions = get_once_all_functions(input_functions)
    #  On récupère l'opération majoritaire et on l'applique partout
    for single_function in single_functions:
        apply_main_operation(single_function, input_functions, get_main_operation(single_function, input_functions))


def define_function_operation(parsed_file, output_file):
    file = open(output_file, 'r')
    output_lines = file.readlines()
    output_functions = get_functions_by_type(parsed_file, FunctionKind.OUTPUT.value)
    input_functions = get_functions_by_type(parsed_file, FunctionKind.INPUT.value)
    index_output_functions = 0
    for input_function in input_functions:
        next_value = get_output_value(output_lines, input_function.time)
        while index_output_functions < len(output_functions) and output_functions[
            index_output_functions].time < input_function.time:
            index_output_functions += 1
        if index_output_functions == len(output_functions):
            raise Exception("Error in the output file, no value before operation !")
        output_function = output_functions[index_output_functions]
        prev = get_output_value(output_lines, output_function.time)
        # Maintenant qu'on a avant après. On teste les différentes possibilités d'interaction
        # Possibilités d'interactions codés en dur. Pas forcément ouf pour la suite
        is_operation_find = False
        if type(prev) == type([]) and len(input_function.parameters) == 1:
            is_operation_find = test_operation_single_target_index(prev, next_value, input_function)
            if not is_operation_find:
                is_operation_find = test_operation_single_target_name(prev, next_value, input_function)
        elif type(prev) == type([]) and len(input_function.parameters) == 2:
            is_operation_find = test_operation_src_dest_target_index(prev, next_value, input_function)
            if not is_operation_find:
                is_operation_find = test_operation_src_dest_target_name(prev, next_value, input_function)
        if not is_operation_find and type(prev) == type(0) and len(input_function.parameters) == 1:
            is_operation_find = test_operation_quantity(prev, next_value, input_function)
        if not is_operation_find:
            input_function.operation = FunctionOperation.UNKNOWN.value
            print("Mode d'entrée inconnu !")
    # Possibilité de définitions différentes pour des mêmes fonctions à cause de colision possible
    # Surtout sur Quantity_*
    # Alors on lisse tout
    uniform_function_operation(input_functions)
    print(output_lines)


def proceed_parsed_result(parsed_file):
    pool_test = "poolTest.py"
    output_file = "output.txt"
    ScriptRebuilding(parsed_file, pool_test, output_file)
    subprocess.run(["python", pool_test])
    define_function_operation(parsed_file, output_file)
    game = Game()
    game.build_from_parsed_file(parsed_file)
    return game
