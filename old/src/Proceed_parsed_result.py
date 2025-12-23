import subprocess

from old.Class.Game import Game
from ScriptRebuilding import ScriptRebuilding
from old.Class.FunctionEnum import *


def assign_setters(parsed_file, output_lines):
    for player in parsed_file.players:
        for function in player.functions_used:
            if function.kind is FunctionKind.NONE or  function.kind is FunctionKind.INPUT or function.kind is FunctionKind.INOUT:



def assign_getters(parsed_file):

def define_function_operation(parsed_file, output_file):
    file = open(output_file, 'r')
    output_lines = file.readlines()
    assign_setters(parsed_file, output_lines)
    assign_getters(parsed_file)


def proceed_parsed_result(parsed_file):
    pool_test = "../output/poolTest.py"
    output_file = "output.txt"
    ScriptRebuilding(parsed_file, pool_test, output_file)
    subprocess.run(["python3", pool_test])
    define_function_operation(parsed_file, output_file)
    game = Game()
    game.build_from_parsed_file(parsed_file)
    return game
