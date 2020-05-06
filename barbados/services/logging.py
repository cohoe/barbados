import logging

logging.basicConfig(level=logging.INFO)

Log = logging.getLogger('barbados')

logging.getLogger('kazoo.client').setLevel(logging.WARN)
