from barbados.settings import Setting, Settings

elasticsearch_settings = Settings(
    scheme=Setting(path='/index/elasticsearch/scheme', env='AMARI_ELASTICSEARCH_SCHEME', default='http', type_=str),
    hosts=Setting(path='/index/elasticsearch/hosts', env='AMARI_ELASTICSEARCH_HOSTS', default=['localhost'], type_=list),
    port=Setting(path='/index/elasticsearch/port', env='AMARI_ELASTICSEARCH_PORT', default=9200, type_=int),
)
