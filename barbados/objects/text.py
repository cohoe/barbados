class Text:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "Barbados::Object::Text[]"

    def serialize(self, serializer):
        serializer.add_property('text', self.text)
