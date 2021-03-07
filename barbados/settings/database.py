from barbados.settings import Setting, Settings

postgresql_settings = Settings(
    username=Setting(path='/database/postgres/username', env='AMARI_DATABASE_USERNAME', default='amari', type_=str),
    password=Setting(path='/database/postgres/password', env='AMARI_DATABASE_PASSWORD', default='s3krAt', type_=str),
    host=Setting(path='/database/postgres/host', env='AMARI_DATABASE_HOST', default='127.0.0.1', type_=str),
    port=Setting(path='/database/postgres/port', env='AMARI_DATABASE_PORT', default=5432, type_=int),
    database=Setting(path='/database/postgres/database', env='AMARI_DATABASE_NAME', default='amari', type_=str),
    debug_sql=Setting(path='/database/postgres/debug_sql', env='AMARI_DATABASE_DEBUG_SQL', default=False, type_=bool),
)
