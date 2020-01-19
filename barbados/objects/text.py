class Text:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Object:Text>"

    def serialize(self):
        return self.text
