class BasePreparation:
    @property
    def slug(self):
        raise NotImplementedError

    def __str__(self):
        return self.slug


class DiscardedPreparation(BasePreparation):
    slug = 'discarded'


class FlamedPreparation(BasePreparation):
    slug = 'flamed'


class DehydratedPreparation(BasePreparation):
    slug = 'dehydrated'


class TwistedPreparation(BasePreparation):
    slug = 'twisted'


class GratedPreparation(BasePreparation):
    slug = 'grated'


class PickPreparation(BasePreparation):
    slug = 'pick'


class SidePreparation(BasePreparation):
    slug = 'side'


class FlagPreparation(BasePreparation):
    slug = 'flag'


class NullPreparation(BasePreparation):
    slug = None


class PreparationFactory:
    def __init__(self):
        self._preparations = {}
    
    def register_class(self, preparation):
        self._preparations[preparation.slug] = preparation
    
    def get_preparation(self, slug):
        p = self._preparations.get(slug)
        if not p:
            raise KeyError("Invalid preparation '%s'" % slug)
        return p


Preparations = PreparationFactory()
Preparations.register_class(DiscardedPreparation)
Preparations.register_class(FlamedPreparation)
Preparations.register_class(DehydratedPreparation)
Preparations.register_class(NullPreparation)
Preparations.register_class(TwistedPreparation)
Preparations.register_class(GratedPreparation)
Preparations.register_class(PickPreparation)
Preparations.register_class(SidePreparation)
Preparations.register_class(FlagPreparation)
