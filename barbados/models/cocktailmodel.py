import barbados.config
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, JSONAttribute, NumberAttribute


class CocktailNameIndex(GlobalSecondaryIndex):
    class Meta:
        projection = IncludeProjection(['display_name'])

    slug = UnicodeAttribute(hash_key=True)


class CocktailModel(Model):
    class Meta:
        table_name = 'cocktails'
        host = barbados.config.database.dynamodb_endpoint
        read_capacity_units = 1
        write_capacity_units = 1

    slug = UnicodeAttribute(hash_key=True)
    display_name = UnicodeAttribute(null=False)
    specs = JSONAttribute(null=False)
    status = UnicodeAttribute(null=False)
    citations = JSONAttribute(null=True)
    notes = UnicodeSetAttribute(null=True)
    origin = JSONAttribute(null=True)
    spec_count = NumberAttribute(null=False)

    name_index = CocktailNameIndex()
