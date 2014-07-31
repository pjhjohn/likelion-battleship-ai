import json

class Log:
    """
    """
    def __init__(self, fleet):
        self.history = []
        self.fleet = fleet

    def get_log(self):
        log = { "fleet" : self.fleet, "history" : self.history }
        return json.dumps(log)