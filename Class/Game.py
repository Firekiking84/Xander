class Game:
    def __init__(self, game=None, back_function=None, env=None, nb_players=0, players_names=None, nb_action_per_turn=0):
        if players_names is None:
            players_names = []
        if env is None:
            env = []
        # Contient le jeu,
        self.game = game
        # Contient la fonction qui permet de revenir en arrière
        self.back_function = back_function
        # Contient toutes les variables disponibles dans le jeu
        self.env = env
        # Contient le nombre d'actions que peut/doit faire l'IA
        self.nb_actions_per_turn = nb_action_per_turn
        # Contient le nombres de joueurs
        self.nb_players = nb_players
        # Contient le nom des joueurs imposé par le jeu
        self.players_names = players_names

    @staticmethod
    def get_game_from_parsed_file(parsed_file):
        for variable in parsed_file.variables:
            if variable.kind == "game":
                return variable
        return None

    @staticmethod
    def get_env_from_parsed_file(parsed_file):
        env = []
        used_variables = []
        for variable in parsed_file.variables:
            if variable != "game" and variable.name not in used_variables:
                used_variables.append(variable.name)
                env.append(variable)
        return env


    @staticmethod
    def get_nb_actions_per_turn(parsed_file):
        intervales = {}
        for player in parsed_file.players.values():
            i = 0
            while i < len(player.functions_used):
                intervale = 0
                while i < len(player.functions_used) and (player.functions_used[i].time + 1) != player.functions_used[i + 1].time:
                    intervale += 1
                if intervales.get(intervale) is not None:
                    intervales[intervale] += 1
                else:
                    intervales[intervale] = 0
        biggest_score = 0
        best_intervale = 0
        for key in intervales.keys():
            score = intervales.get(key)
            if score > biggest_score:
                biggest_score = score
                best_intervale = key
        return best_intervale


    def build_from_parsed_file(self, parsed_file):
        self.game = self.get_game_from_parsed_file(parsed_file)
        self.back_function = parsed_file.back_function
        self.env = self.get_env_from_parsed_file(parsed_file)
        self.nb_players = len(parsed_file.players)
        self.players_names = parsed_file.players_name
        self.nb_actions_per_turn = self.get_nb_actions_per_turn(parsed_file)