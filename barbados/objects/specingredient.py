

class SpecIngredient:
    def __init__(self, name, quantity=None, unit=None):
        self.name = name
        self.quantity = quantity
        self.unit = unit

        if isinstance(self.name, str):
            if len(self.name) <= 1:
                raise KeyError("Got single character or less for name. Probably a data problem. Got '%s'" % self.name)

    def __repr__(self):
        return "<Object:SpecIngredient::name=%s>" % self.name

    def serialize(self):
        keys = ['name', 'quantity', 'unit']
        ser = {}
        for key in keys:
            if getattr(self, key) is not None:
                ser[key] = getattr(self, key)
        return ser

    # Old code for doing pretty quantity conversion:
    #
    # if type(quantity) == float:
    #     for fraction in pretty_fractions:
    #         quantity = str(quantity).replace(fraction, pretty_fractions[fraction])
    #     quantity = quantity.lstrip('0')
    #     ingredient['quantity'] = quantity
