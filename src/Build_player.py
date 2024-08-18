def build_get_env(game, file):
    print("Coming Soon")

def build_blank_rule(game, file):
    print("Coming Soon")


def build_player(game, player_name):
    file = open(f"AI/{player_name}", "w+")
    build_get_env(game, file)
    build_blank_rule(game, file)
    file.close()
