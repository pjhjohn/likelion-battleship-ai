import json

class Log:
    """
    """
    def __init__(self, fleet):
        self.history = []
        self.fleet = fleet

    def get_log(self, toString = True):
        log = { "fleet" : self.fleet, "history" : self.history }
        if toString:
            return json.dumps(log)
        else:
            return log