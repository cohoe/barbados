from elasticsearch_dsl import connections
from barbados.services.logging import LogService
from barbados.settings.search import elasticsearch_settings


# @TODO this doesn't resemble the other connectors :/
class ElasticsearchConnector:

    @staticmethod
    def connect():
        hosts = elasticsearch_settings.get('hosts')
        scheme = elasticsearch_settings.get('scheme')
        port = elasticsearch_settings.get('port')

        LogService.info("Using ElasticSearch hosts: \"%s\" via %s/%i" % (hosts, scheme, port))
        connections.create_connection(scheme=scheme, hosts=hosts, port=port)
