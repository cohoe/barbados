from elasticsearch_dsl import connections
from barbados.services.logging import LogService
from barbados.settings import Setting


class ElasticsearchConnector:

    @staticmethod
    def connect():
        scheme = Setting(path='/index/elasticsearch/scheme', env='AMARI_ELASTICSEARCH_SCHEME', default='http', type_=str).get_value()
        hosts = Setting(path='/index/elasticsearch/hosts', env='AMARI_ELASTICSEARCH_HOSTS', default=['localhost'], type_=list).get_value()
        port = Setting(path='/index/elasticsearch/port', env='AMARI_ELASTICSEARCH_PORT', default=9200, type_=int).get_value()

        LogService.info("Using ElasticSearch hosts: \"%s\" via %s/%i" % (hosts, scheme, port))

        connections.create_connection(scheme=scheme, hosts=hosts, port=port)
