import os
from elasticsearch_dsl import connections
from barbados.services.logging import LogService


class ElasticsearchConnector:
    @staticmethod
    def connect():
        scheme = os.getenv('AMARI_ELASTICSEARCH_SCHEME', default='http')
        hosts = os.getenv('AMARI_ELASTICSEARCH_HOSTS', default=['localhost'])
        port = int(os.getenv('AMARI_ELASTICSEARCH_PORT', default=9200))

        LogService.info("Using ElasticSearch hosts: \"%s\" via %s/%i" % (hosts, scheme, port))

        connections.create_connection(scheme=scheme, hosts=hosts, port=port)
