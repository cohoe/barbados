from elasticsearch import Elasticsearch


class ElasticsearchConnector:
    def __init__(self, scheme='http', hosts=None, port=9200):
        if hosts is None:
            hosts = ['localhost']
        self.scheme = scheme
        self.hosts = hosts
        self.port = port

    def _connect(self):
        if not hasattr(self, 'client'):
            self.client = Elasticsearch(hosts=self.hosts, scheme=self.scheme, port=self.port)

    def insert(self, index, id, body):
        self._connect()
        result = self.client.index(index=index, id=id, body=body)
        return result['result']

    def get(self, index, id):
        self._connect()
        result = self.client.get(index=index, id=id)
        return result

    def search(self, index, body):
        self._connect()
        results = self.client.search(index=index, body=body)
        return results
