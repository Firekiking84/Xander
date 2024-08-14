class Player:
    def __init__(self, number, functions_used=None):
        if functions_used is None:
            functions_used = []
        self.number = number
        self.functions_used = functions_used

    def __str__(self):
        return_str = f"Player n°{self.number} has used :"
        for function in self.functions_used:
            return_str += str(function) + '\n'
        return return_str

    def get_time_function(self, time):
        for i in range(len(self.functions_used)):
            if self.functions_used[i].time == time:
                return i
        return -1

