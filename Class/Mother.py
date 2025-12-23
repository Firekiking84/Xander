from Class.ParseExample import ParseExample

class Mother:
    def __init__(self):
        print("Starting Mother !")

    def createSon(self, name: str, example_path: str):
        parsed_file = ParseExample(example_path)
        if len(parsed_file.players) == 0:
            raise Exception("Error in the example file ! No player detected !")
