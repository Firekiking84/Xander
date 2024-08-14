import subprocess
import ast

from Class.Game import Game
from ScriptRebuilding import ScriptRebuilding
from Class.FunctionEnum import *


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
        

def get_a_getter(output_functions, target_time):
    for output_function in output_functions:
        if output_function.time == target_time and output_function.kind == FunctionKind.OUTPUT.value:
            return output_function
    return False


def get_the_getter(output_functions, target_time, var_name):
    output_function = get_a_getter(output_functions, target_time)
    while output_function:
        if output_function.return_value.name == var_name:
            return output_function
        target_time -= 1
        output_function = get_a_getter(output_functions, target_time)
    return False


def get_prev_value(output_functions, input_function, var_name):
    output_function = get_the_getter(output_functions, input_function.time - 1, var_name)
    if not output_function:
        return False
    return get_output_value(output_functions, output_function.time)

def get_next_prev_value(next_prev_value, input_function, output_functions, output_lines):
    if next_prev_value["n_var"] == 0 and input_function.kind == FunctionKind.INOUT.value:
        var_name = input_function.return_value.name
        next_prev_value["next"] = get_output_value(output_lines, input_function.time)
        next_prev_value["prev"] = get_prev_value(output_functions, input_function, var_name)
    else:
        if next_prev_value["n_var"] == 0:
            next_prev_value["n_var"] += 1
        output_function = get_a_getter(output_functions, input_function.time + next_prev_value["n_var"])
        if not output_function:
            return False
        var_name = output_function.return_value.name
        next_prev_value["next"] = get_output_value(output_functions, output_function.time)
        next_prev_value["prev"] = get_prev_value(output_functions, input_function, var_name)
    next_prev_value["n_var"] += 1
    return True


def define_function_operation(parsed_file, output_file):
    file = open(output_file, 'r')
    output_lines = file.readlines()
    output_functions = get_functions_by_type(parsed_file, FunctionKind.OUTPUT.value)
    input_functions = get_functions_by_type(parsed_file, FunctionKind.INPUT.value)
    index_input_functions = 0
    for input_function in input_functions:
        is_operation_find = False
        next_prev_value = {"n_var": 0, "next": None, "prev": None}
        while not get_next_prev_value(next_prev_value, input_function, output_functions, output_lines):
            # Maintenant qu'on a avant après. On teste les différentes possibilités d'interaction
            # Possibilités d'interactions codés en dur. Pas forcément ouf pour la suite
            if type(next_prev_value["prev"]) == type([]) and len(input_function.parameters) == 1:
                is_operation_find = test_operation_single_target_index(next_prev_value["prev"], next_prev_value["next"], input_function)
                if not is_operation_find:
                    is_operation_find = test_operation_single_target_name(next_prev_value["prev"], next_prev_value["next"], input_function)
            elif type(next_prev_value["prev"]) == type([]) and len(input_function.parameters) == 2:
                is_operation_find = test_operation_src_dest_target_index(next_prev_value["prev"], next_prev_value["next"], input_function)
                if not is_operation_find:
                    is_operation_find = test_operation_src_dest_target_name(next_prev_value["prev"], next_prev_value["next"], input_function)
            if not is_operation_find and type(next_prev_value["prev"]) == type(0) and len(input_function.parameters) == 1:
                is_operation_find = test_operation_quantity(next_prev_value["prev"], next_prev_value["next"], input_function)
            if not is_operation_find:
                input_function.operation = FunctionOperation.UNKNOWN.value
                print("Mode d'entrée inconnu !")
        index_input_functions += 1
    # Possibilité de définitions différentes pour des mêmes fonctions à cause de colision possible
    # Surtout sur Quantity_*
    # Alors on lisse tout
    uniform_function_operation(input_functions)
    print(output_lines)


def proceed_parsed_result(parsed_file):
    pool_test = "poolTest.py"
    output_file = "../output/output.txt"
    ScriptRebuilding(parsed_file, pool_test, output_file)
    subprocess.run(["python", pool_test])
    define_function_operation(parsed_file, output_file)
    game = Game()
    game.build_from_parsed_file(parsed_file)
    return game
