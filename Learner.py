import subprocess

from ParseExample import ParseExample
from ScriptRebuilding import ScriptRebuilding
from FunctionEnum import *


def define_output_operation(parsed_file, output_file):
    file = open(output_file, 'r')
    output_lines = file.readlines()
    print(output_lines)
    for i in range(len(parsed_file.players_name)):
        for n_function in range(len(parsed_file.players[parsed_file.players_name[i]].functions_used)):
            if parsed_file.players[parsed_file.players_name[i]].functions_used[n_function].kind == FunctionKind.OUTPUT.value or parsed_file.players[parsed_file.players_name[i]].functions_used[n_function].kind == FunctionKind.INOUT.value:
                print("Cacahuètes")


def start_player_creation(parsed_file, player_name):
    pool_test = "poolTest.py"
    output_file = "output.txt"
    ScriptRebuilding(parsed_file, pool_test, output_file)
    subprocess.run(["python", pool_test])
    define_output_operation(parsed_file, output_file)


#    build_player(parsed_file, player_name, pool_test, output_file)


def learner(example_file, player_name):
    parsed_file = ParseExample(example_file)
    if len(parsed_file.players) == 0:
        raise Exception("Error in the example file ! No player detected !")
    start_player_creation(parsed_file, player_name)


learner("exampleMorpion.py", "morpionPlayer")
