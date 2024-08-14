from ParseExample import ParseExample
from Proceed_parsed_result import proceed_parsed_result
from src.Build_player import build_player


def learner(example_file, player_name):
    parsed_file = ParseExample(example_file)
    if len(parsed_file.players) == 0:
        raise Exception("Error in the example file ! No player detected !")
    game = proceed_parsed_result(parsed_file)
    build_player(game, player_name)


learner("../res/exampleMorpion.py", "morpionPlayer")
