import json

class Log:
    """
    """
    def __init__(self):
        self.history = []

    def get_log(self, toString = True):
        if toString:
            return json.dumps(self.history)
        else:
            return self.history