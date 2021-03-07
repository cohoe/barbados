from barbados.settings import Setting, Settings

redis_settings = Settings(
    host=Setting(path='/cache/redis/host', env='AMARI_REDIS_HOST', default='127.0.0.1', type_=str),
    port=Setting(path='/cache/redis/port', env='AMARI_REDIS_PORT', default=6379, type_=int),
    # username=EmptySetting(path='/cache/redis/username'),
    # password=EmptySetting(path='/cache/redis/password'),
    username=None,
    password=None,
    ssl=Setting(path='/cache/redis/ssl', env='AMARI_REDIS_SSL', default=False, type_=bool),
    request_timeout=Setting(path='/cache/redis/request_timeout', env='AMARI_REDIS_REQUEST_TIMEOUT', default=18000, type_=int),
    flask_database_id=Setting(path='/cache/redis/flask_database_id', env='AMARI_REDIS_FLASK_DATABASE_ID', default=2, type_=int),
)
