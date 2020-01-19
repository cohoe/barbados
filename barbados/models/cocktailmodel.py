from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, JSONAttribute, NumberAttribute


class CocktailModel(Model):
    class Meta:
        table_name = 'cocktails'
        host = 'http://127.0.0.1:8000'
        read_capacity_units = 1
        write_capacity_units = 1

    slug = UnicodeAttribute(hash_key=True)
    display_name = UnicodeAttribute(null=False)
    spec = JSONAttribute(null=False)
    status = UnicodeAttribute(null=False)
    citations = JSONAttribute(null=True)
    notes = UnicodeSetAttribute(null=True)
    origin = JSONAttribute(null=True)
    spec_count = NumberAttribute(null=False)