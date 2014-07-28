import json

class Log:
    """
    """
    def __init__(self):
        self.history = []

    def get_log(self):
        return json.dumps(self.history)