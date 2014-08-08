class attrdict(dict):
    def __init__(self, *args, **kwargs) :
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
    def retrieve(self, key, value) :
        if key in self :
            return self[key]
        else :
            self[key] = value
            return value

class attrdict_const(dict):
    class ConstError(TypeError) : pass
    def __init__(self, *args, **kwargs) :
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
    def __setattr__(self, name, value) :
        if self.has_key(name) :
            raise self.ConstError, "Can't rebind const(%s)"%name
        super(attrdict_const, self).__setattr__(name, value)
    def retrieve(self, key, value) :
        if key in self :
            return self[key]
        else :
            self[key] = value
            return value