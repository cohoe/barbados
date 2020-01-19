import requests


class ElasticsearchConnector:
    def __init__(self, protocol='http', host='localhost', port=9200):
        self.protocol = protocol
        self.host = host
        self.port = port

    # @TODO maybe make this take an object instead?
    def upload_doc(self, index, id, obj):
        url = "%s://%s:%i/%s/_doc/%s" % (self.protocol, self.host, self.port, index, id)

        # headers = {
        #     'Content-Type': 'application/json'
        # }

        req = requests.put(url, json=obj.serialize())

        if req.status_code == 200:
            print('Updated index')
        elif req.status_code == 201:
            print('Created key in index')
        else:
            raise Exception("Web request failed! Resp: %i: %s" % (req.status_code, req.text))
