class Origin:
    UNKNOWN = 'UNKNOWN'

    def __init__(self, creator=UNKNOWN, venue=UNKNOWN, location=UNKNOWN, year=UNKNOWN, story=UNKNOWN, era=UNKNOWN):
        self.creator = creator
        self.venue = venue
        self.location = location
        self.year = year
        self.story = story
        self.era = era

    # def __iter__(self):
    #     keys = ['creator', 'venue', 'location', 'year', 'story']
    #
    #     output = []
    #     for key in keys:
    #         if hasattr(self, key):
    #             output.append(str(getattr(self, key)))
    #
    #     if len(output) == 0:
    #         output.append('Origin Unknown')
    #
    #     print(output)
    #     return iter(output)

    def __repr__(self):
        if hasattr(self, 'location'):
            return "<Object:Origin::location=%s>" % self.location
        else:
            return "<Object:Origin::unknown>"

    def serialize(self):
        keys = ['creator', 'venue', 'location', 'year', 'story', 'era']
        ser = {}

        for key in keys:
            if getattr(self, key) != Origin.UNKNOWN:
                ser[key] = getattr(self, key)

        return ser
