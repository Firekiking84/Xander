import subprocess
import ast

from Class.Game import Game
from Class.Operation import Operation
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


def test_operation_single_target_index(prev, next_value, input_function, operation):
    test_index = int(input_function.parameters[0])
    index = 0
    for prev_elem in prev:
        if index != test_index and prev_elem != next_value[index]:
            break
        if index == test_index and prev_elem == next_value[index]:
            break
        index += 1
    if index == len(prev):
        operation.kind = FunctionOperation.SINGLE_TARGET_INDEX.value
        input_function.operations.append(operation)
        return True
    return False


def test_operation_single_target_name(prev, next_value, input_function, operation):
    test_name = input_function.parameters[0]
    index = 0
    for prev_elem in prev:
        if test_name != prev_elem and prev_elem != next_value[index]:
            break
        if test_name == prev_elem and prev_elem == next_value[index]:
            break
        index += 1
    if index == len(prev):
        operation.kind = FunctionOperation.SINGLE_TARGET_NAME.value
        input_function.operations.append(operation)
        return True
    return False


def test_operation_quantity(prev, next_value, input_function, operation):
    test_quantity = input_function.parameters[0]
    if (prev - test_quantity) == next_value:
        operation.kind = FunctionOperation.QUANTITY_RM.value
        input_function.operations.append(operation)
        return True
    if (prev + test_quantity) == next_value:
        operation.kind = FunctionOperation.QUANTITY_ADD.value
        input_function.operations.append(operation)
        return True
    if next_value == test_quantity:
        operation.kind = FunctionOperation.QUANTITY_SET.value
        input_function.operations.append(operation)
        return True
    return False


def test_operation_src_dest_target_index(prev, next_value, input_function, operation):
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
        operation.kind = FunctionOperation.SRC_DEST_TARGET_INDEX.value
        input_function.operations.append(operation)
        return True
    return False


def test_operation_src_dest_target_name(prev, next_value, input_function, operation):
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
        operation.kind = FunctionOperation.SRC_DEST_TARGET_NAME.value
        input_function.operations.append(operation)
        return True
    return False


def get_once_all_functions(input_functions):
    single_functions = []
    for input_function in input_functions:
        if input_function not in single_functions:
            single_functions.append(input_function)
    return single_functions


def mistake_operations_filter(single_function, input_functions):
    operations = {}
    for input_function in input_functions:
        if input_function == single_function:
            for input_operation in input_function.operations:
                if operations.get(input_operation) is not None:
                    operations[input_operation] += 1
                else:
                    operations[input_operation] = 1
    # 50 % de marge d'erreur
    limit = len(input_functions) / 2
    for key in operations.keys():
        if operations.get(key) < limit:
            operations.pop(key)
    return operations.keys()


def apply_main_operation(target_function, input_functions, operations):
    for input_function in input_functions:
        if input_function == target_function:
            input_function.operations = operations


def uniform_function_operation(input_functions):
    #  On récupère toutes les fonctions une fois
    single_functions = get_once_all_functions(input_functions)
    #  On récupère l'opération majoritaire et on l'applique partout
    for single_function in single_functions:
        apply_main_operation(single_function, input_functions, mistake_operations_filter(single_function, input_functions))
        

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


def get_prev_value(output_functions, input_function, var_name, output_lines):
    output_function = get_the_getter(output_functions, input_function.time - 1, var_name)
    if not output_function:
        return False
    return get_output_value(output_lines, output_function.time)


def get_next_prev_value(next_prev_value, input_function, output_functions, output_lines):
    if next_prev_value["n_var"] == 0 and input_function.kind == FunctionKind.INOUT.value:
        var_name = input_function.return_value.name
        next_prev_value["variable"] = input_function.return_value
        next_prev_value["next"] = get_output_value(output_lines, input_function.time)
        next_prev_value["prev"] = get_prev_value(output_functions, input_function, var_name, output_lines)
    else:
        if next_prev_value["n_var"] == 0:
            next_prev_value["n_var"] += 1
        output_function = get_a_getter(output_functions, input_function.time + next_prev_value["n_var"])
        if not output_function:
            return False
        var_name = output_function.return_value.name
        next_prev_value["variable"] = output_function.return_value
        next_prev_value["next"] = get_output_value(output_functions, output_function.time)
        next_prev_value["prev"] = get_prev_value(output_functions, input_function, var_name, output_lines)
    next_prev_value["n_var"] += 1
    return True


def define_var_getter(variable, output_functions):
    passed_functions = []
    for function in output_functions:
        if function.name not in passed_functions:
            passed_functions.append(function.name)
            if function.return_value.name == variable.name:
                variable.getters.append(function)


def define_var_setter(variable, input_functions):
    passed_functions = []
    for function in input_functions:
        if function.name not in passed_functions:
            passed_functions.append(function.name)
            for operation in function.operations:
                if operation.variable.name == variable.name:
                    variable.setters.append(function)


def define_var_getter_setter(parsed_file, output_functions, input_functions):
    passed_variables = {}
    index = 0
    for variable in parsed_file.variables:
        ref_index = passed_variables.get(variable.name)
        # Si c'est une variable qui n'est pas déjà passé on lui attribut les setters et getters
        if ref_index is None:
            passed_variables[variable.name] = index
            define_var_getter(variable, output_functions)
            define_var_setter(variable, input_functions)
        else: # Sinon on lui attribut celle de la fonction identique déjà traité
            variable.getters = parsed_file.variables[ref_index].getters
            variable.setters = parsed_file.variables[ref_index].setters
        index += 1


def define_function_operation(parsed_file, output_file):
    file = open(output_file, 'r')
    output_lines = file.readlines()
    output_functions = get_functions_by_type(parsed_file, FunctionKind.OUTPUT.value)
    input_functions = get_functions_by_type(parsed_file, FunctionKind.INPUT.value)
    index_input_functions = 0
    for input_function in input_functions:
        is_operation_find = False
        next_prev_value = {"n_var": 0, "next": None, "prev": None, "variable": None}
        while not get_next_prev_value(next_prev_value, input_function, output_functions, output_lines):
            # Maintenant qu'on a avant après. On teste les différentes possibilités d'interaction
            # Possibilités d'interactions codés en dur. Pas forcément ouf pour la suite
            operation = Operation(variable=next_prev_value["variable"])
            if type(next_prev_value["prev"]) == type([]) and len(input_function.parameters) == 1:
                is_operation_find = test_operation_single_target_index(next_prev_value["prev"], next_prev_value["next"], input_function, operation)
                if not is_operation_find:
                    is_operation_find = test_operation_single_target_name(next_prev_value["prev"], next_prev_value["next"], input_function, operation)
            elif type(next_prev_value["prev"]) == type([]) and len(input_function.parameters) == 2:
                is_operation_find = test_operation_src_dest_target_index(next_prev_value["prev"], next_prev_value["next"], input_function, operation)
                if not is_operation_find:
                    is_operation_find = test_operation_src_dest_target_name(next_prev_value["prev"], next_prev_value["next"], input_function, operation)
            if not is_operation_find and type(next_prev_value["prev"]) == type(0) and len(input_function.parameters) == 1:
                is_operation_find = test_operation_quantity(next_prev_value["prev"], next_prev_value["next"], input_function, operation)
            if not is_operation_find:
                print("Mode d'entrée inconnu !")
        index_input_functions += 1
    # Possibilité de définitions différentes pour des mêmes fonctions à cause de colision possible
    # Surtout sur Quantity_*
    # Alors on lisse tout
    uniform_function_operation(input_functions)
    # On applique ensuite les changements sur les variables

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
