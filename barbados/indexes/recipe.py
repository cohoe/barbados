from elasticsearch_dsl import Document, Text


class RecipeIndex(Document):
    slug = Text()

    class Index:
        name = 'recipe'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
