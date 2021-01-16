import logging

logging.basicConfig(level=logging.INFO)

LogService = logging.getLogger('barbados')

logging.getLogger('kazoo.client').setLevel(logging.WARN)
