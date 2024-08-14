from GameEnv import GameEnv


class Game:
    def __init__(self, game=None, back_function=None, game_env=None, nb_players=0, players_name=[]):
        if game_env is None:
            game_env = []
        self.game = game
        self.back_function = back_function
        self.game_env = game_env
        self.nb_players = nb_players
        self.players_name = players_name

    @staticmethod
    def get_game_from_parsed_file(parsed_file):
        for variable in parsed_file.variables:
            if variable.kind == "game":
                return variable
        return None

    @staticmethod
    def get_game_env_from_parsed_file(parsed_file):
        game_envs = []
        used_variables = []
        for variable in parsed_file.variables:
            if variable != "game" and variable.name not in used_variables:
                used_variables.append(variable.name)
                game_env = GameEnv()
                game_env.name = variable.name
                for
        return game_envs

    def build_from_parsed_file(self, parsed_file):
        self.game = self.get_game_from_parsed_file(parsed_file)
        self.back_function = parsed_file.back_function
        self.game_env = self.get_game_env_from_parsed_file(parsed_file)
