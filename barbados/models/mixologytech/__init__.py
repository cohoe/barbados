from barbados.models.base import BarbadosModel
from sqlalchemy import Column, Integer, JSON, String, TIMESTAMP, Boolean, ForeignKey


class IngredientModel(BarbadosModel):
    __tablename__ = 'ZINGREDIENT'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    derivative = Column(Boolean, name='ZDERIVATIVE', doc='Is this ingredient made from something else (ie, lemon wheels). Not included in ingredients list but is in search.')
    potential_recipes_count = Column(Integer, name='ZPOTENTIALRECIPESCOUNT', doc='??????????????')
    recipes_count = Column(Integer, name='ZRECIPESCOUNT', doc='Number of recipes that call for this specific ingredient.')
    uses_count = Column(Integer, name='ZUSESCOUNT', doc='Number of recipes this can be used in.')
    derivation_source_id = Column(Integer, name='ZDERIVATIONSOURCE', doc='Primary Key of the base of this derivation.')
    generic_id = Column(Integer, name='ZGENERIC', doc='Primary Key of the generic parent of this ingredient.')
    synonymous_recipe_id = Column(Integer, name='ZSYNONYMOUSRECIPE', doc='ID of the recipe for this custom ingredient.')
    canonical_name = Column(String, name='ZCANONICALNAME', doc='Common name of the ingredient.')
    canonical_name_initial = Column(String, name='ZCANONICALNAMEINITIAL', doc='First letter of the ingredient canonical name.')
    detail_json = Column(JSON, name='ZDETAILJSON', doc='All information displayed when viewing the ingredient details.')
    inventory_annotation = Column(String, name='ZINVENTORYANNOTATION', doc='Tagline in the inventory list.')
    remote_id = Column(String, name='ZREMOTEID')

    # Empty Columns
    # inventorysoftequivalentsjson = Column(JSON, name='ZINVENTORYSOFTEQUIVALENTSJSON')
    # synctime = Column(TIMESTAMP, name='ZSYNCTIME')
    # onhandupdatedat = Column(TIMESTAMP, name='ZONHANDUPDATEDAT')
    # lastchosenforrecipefilterat = Column(TIMESTAMP, name='ZLASTCHOSENFORRECIPEFILTERAT')

    # onhand = Column(Integer, name='ZONHAND')
    # onhanddefacto = Column(Integer, name='ZONHANDDEFACTO')
    # syncstate = Column(Integer, name='ZSYNCSTATE')


class IngredientAlternateSpellingModel(BarbadosModel):
    __tablename__ = 'ZINGREDIENTALTERNATESPELLING'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    ingredient_id = Column(Integer, ForeignKey('IngredientModel.id'), name='ZINGREDIENT', doc='Primary Key of the Ingredient this references.')
    alternative_spelling = Column(String, name='ZCONTENT', doc='The alternative spelling')
    fok_ingredient = Column(Integer, name='Z_FOK_INGREDIENT', doc='????????')


class IngredientCategoryModel(BarbadosModel):
    __tablename__ = 'ZINGREDIENTCATEGORY'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    ingredients_count = Column(Integer, name='ZINGREDIENTSCOUNT', doc='Count of ingredients in the category')
    position = Column(Integer, name='ZPOSITION', doc='Sort order for categories.')
    annotation = Column(String, name='ZANNOTATION', doc='Tagline in the "By Category" view.')
    display_name = Column(String, name='ZDISPLAYNAME', doc='Display name of the category.')
    remote_id = Column(String, name='ZREMOTEID', doc='???????')


class IngredientDependencyModel(BarbadosModel):
    __tablename__ = 'ZINGREDIENTDEPENDENCY'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    position = Column(Integer, name='ZPOSITION', doc='???????') # @TODO this might be the small ingredient text below each recipe?
    recipe = Column(Integer, name='ZPOSITION', doc='Primary Key of Recipe.')

    # status = Column(Integer, name='ZSTATUS')
    # satisfied_ingredient = Column(Integer, name='ZSATISFIEDINGREDIENT')
    # satisfier = Column(Integer, name='ZSATISFIER')


class IngredientSynonymModel(BarbadosModel):
    __tablename__ = 'ZINGREDIENTSYNONYM'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    ingredient_id = Column(Integer, ForeignKey('IngredientModel.id'), name='ZINGREDIENT', doc='Foreign ID of the base ingredient.')
    fok_ingredient = Column(Integer, name='Z_FOK_INGREDIENT', doc='????')
    synonym = Column(String, name='ZCONTENT', doc='The synonym')
