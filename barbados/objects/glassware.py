class Glassware:
    def __init__(self, name=None):
        self.name = name
        if name is None:
            self.name = 'UNKNOWN'

    def __repr__(self):
        return "<Object:Glassware::name=%s>" % self.name

    def serialize(self):
        return self.name