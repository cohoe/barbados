from barbados.factories.base import BaseFactory
from barbados.factories.parser import FactoryParser
from barbados.objects.user import User
from barbados.models.user import UserModel


class UserFactory(BaseFactory):
    _model = UserModel
    _validator = None
    _index = None

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        # Parse fields
        raw_obj.pop('password')

        return User(**raw_obj)
