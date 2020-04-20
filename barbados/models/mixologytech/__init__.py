from barbados.models.base import MixologyTechModel
from sqlalchemy import Column, Integer, JSON, String, TIMESTAMP, Boolean, ForeignKey


class IngredientModel(MixologyTechModel):
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


class IngredientAlternateSpellingModel(MixologyTechModel):
    __tablename__ = 'ZINGREDIENTALTERNATESPELLING'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    ingredient_id = Column(Integer, ForeignKey('IngredientModel.id'), name='ZINGREDIENT', doc='Primary Key of the Ingredient this references.')
    alternative_spelling = Column(String, name='ZCONTENT', doc='The alternative spelling')
    fok_ingredient = Column(Integer, name='Z_FOK_INGREDIENT', doc='????????')


class IngredientCategoryModel(MixologyTechModel):
    __tablename__ = 'ZINGREDIENTCATEGORY'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    ingredients_count = Column(Integer, name='ZINGREDIENTSCOUNT', doc='Count of ingredients in the category')
    position = Column(Integer, name='ZPOSITION', doc='Sort order for categories.')
    annotation = Column(String, name='ZANNOTATION', doc='Tagline in the "By Category" view.')
    display_name = Column(String, name='ZDISPLAYNAME', doc='Display name of the category.')
    remote_id = Column(String, name='ZREMOTEID', doc='???????')


class IngredientCategoryMappingModel(MixologyTechModel):
    __tablename__ = 'Z_1CATEGORIES'

    ingredient_id = Column(Integer, primary_key=True, name='Z_1INGREDIENTS1', doc='Ingredient ID')
    category_id = Column(Integer, primary_key=True, name='Z_3CATEGORIES', doc='Category ID')
    fok_3categories = Column(Integer, name='Z_FOK_3CATEGORIES', doc='???????')


class IngredientDependencyModel(MixologyTechModel):
    __tablename__ = 'ZINGREDIENTDEPENDENCY'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    position = Column(Integer, name='ZPOSITION', doc='???????') # @TODO this might be the small ingredient text below each recipe?
    recipe = Column(Integer, name='ZRECIPE', doc='Primary Key of Recipe.')

    # status = Column(Integer, name='ZSTATUS')
    # satisfied_ingredient = Column(Integer, name='ZSATISFIEDINGREDIENT')
    # satisfier = Column(Integer, name='ZSATISFIER')


class IngredientSynonymModel(MixologyTechModel):
    __tablename__ = 'ZINGREDIENTSYNONYM'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    ingredient_id = Column(Integer, ForeignKey('IngredientModel.id'), name='ZINGREDIENT', doc='Foreign ID of the base ingredient.')
    fok_ingredient = Column(Integer, name='Z_FOK_INGREDIENT', doc='????')
    synonym = Column(String, name='ZCONTENT', doc='The synonym')


class RecipeModel(MixologyTechModel):
    __tablename__ = 'ZRECIPE'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    # flagged, disliked, favorited, liked aren't used?
    is_ingredient = Column(Boolean, name='ZISINGREDIENT', doc='Is this a custom ingredient recipe.')
    missing_ingredients_count = Column(Integer, name='ZMISSINGINGREDIENTSCOUNT', doc='Number of missing ingredients based on inventory.')
    # zservings.... now that's an idea.
    synonymous_ingredient_id = Column(Integer, name='ZSYNONYMOUSINGREDIENT', doc='Primary Key of Ingredient if this is a Custom recipe.')
    citation_year = Column(String, name='ZCITATIONYEAR', doc='Drink citation year (or "????"), likely used for era')
    detail_json = Column(JSON, name='ZDETAILJSON', doc='Detail view JSON')
    ingredient_dependencies_json = Column(JSON, name='ZINGREDIENTDEPENDENCIESJSON', doc='List of Lists of ingredent remote IDs that this recipe needs')
    original_title = Column(String, name='ZORIGTITLE')
    # zpresentation == 'pdt2', wonder if thats different per-app?
    remote_id = Column(String, name='ZREMOTEID')
    sort_key = Column(String, name='ZSORTKEY')
    sort_key_initial = Column(String, name='ZSORTKEYINITIAL')
    summary = Column(String, name='ZSUMMARY', doc='Summary description of ingredients under the list item.')
    title = Column(String, name='ZTITLE', doc='Drink title')


class RecipeFactoidModel(MixologyTechModel):
    __tablename__ = 'ZRECIPEFACTOID'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    recipe_id = Column(Integer, ForeignKey('RecipeModel.id'), name='ZRECIPE', doc='Recipe ID')
    fok_recipe = Column(Integer, name='Z_FOK_RECIPE', doc='Parameter kind ID ?????')
    name = Column(String, name='ZNAME', doc='Key')
    content = Column(String, name='ZCONTENT', doc='Value')


class RecipeKeywordGroup(MixologyTechModel):
    __tablename__ = 'ZRECIPEKEYWORDGROUP'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    position = Column(Integer, name='ZPOSITION', doc='Sort order for group.')
    show_in_menu = Column(Boolean, name='ZSHOULDSHOWINMENU')
    remote_id = Column(String, name='ZREMOTEID', doc='Keyword Group')


class RecipeKeywordModel(MixologyTechModel):
    __tablename__ = 'ZRECIPEKEYWORD'

    id = Column(Integer, name='Z_PK', primary_key=True, doc='Table primary key ID.')
    recipes_count = Column(Integer, name='ZRECIPESCOUNT', doc='Count of recipes????')
    group_id = Column(Integer, ForeignKey('RecipeKeywordGroup.id'), name='ZGROUP')
    fok_group = Column(Integer, name='Z_FOK_GROUP')
    remote_id = Column(String, name='ZREMOTEID', doc='Keyword value')
    shortname = Column(String, name='ZSHORTNAME', doc='Keyword Display Name')
