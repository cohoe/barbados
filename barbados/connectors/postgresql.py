import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import event
from barbados.models.base import BarbadosModel
from barbados.services.logging import LogService
from barbados.settings import Setting
from contextlib import contextmanager


class PostgresqlConnector:
    """
    Connector to PostgreSQL.
    Unfortunately I didn't write down all of the various StackOverflow
    and tutorial posts that certainly got this code to work.
    """

    def __init__(self):
        self.username = Setting(path='/database/postgres/username', env='AMARI_DATABASE_USERNAME', default='amari', type_=str).get_value()
        self.password = Setting(path='/database/postgres/password', env='AMARI_DATABASE_PASSWORD', default='s3krAt', type_=str).get_value()
        self.host = Setting(path='/database/postgres/host', env='AMARI_DATABASE_HOST', default='127.0.0.1', type_=str).get_value()
        self.port = Setting(path='/database/postgres/port', env='AMARI_DATABASE_PORT', default=5432, type_=int).get_value()
        self.database = Setting(path='/database/postgres/database', env='AMARI_DATABASE_NAME', default='amari', type_=str).get_value()
        self.debug_sql = Setting(path='/database/postgres/debug_sql', env='AMARI_DATABASE_DEBUG_SQL', default=False, type_=bool).get_value()

        connection_string = "postgres://%s:%s@%s:%i/%s" % (self.username, self.password, self.host, self.port, self.database)

        # https://stackoverflow.com/questions/48995979/how-to-replace-all-characters-in-a-string-with-one-character/48996018
        masked_connection_string = connection_string.replace(self.password, '*' * len(self.password))
        LogService.info("Postgres string: %s" % masked_connection_string)
        LogService.warn('Starting PostgreSQL connection!')

        self.engine = sqlalchemy.create_engine(connection_string, echo=self.debug_sql)
        self.Session = sessionmaker(bind=self.engine)
        self.ScopedSession = scoped_session(self.Session)

        self._setup_events()

    def _setup_events(self):
        """
        Setup some testing event handlers to report when things happen in SQLAlchemy.
        :return:
        """

        def event_new_session(session, transaction, connection):
            LogService.info("Opening new database session: %s" % session)

        def event_end_session(session, transaction):
            LogService.info("Closing database session: %s" % session)

        event.listen(self.Session, "after_begin", event_new_session)
        event.listen(self.Session, "after_transaction_end", event_end_session)

    def create_all(self):
        BarbadosModel.metadata.create_all(self.engine)

    def drop_all(self):
        BarbadosModel.metadata.drop_all(self.engine)

    @contextmanager
    def get_session(self):
        """
        Provide a valid SQLAlchemy Session for use in a context.
        Example:
          with get_session() as session:
            result = session.query(CocktailModel).get('mai-tai')
        :return: None
        """
        session, commit = self._build_session()

        try:
            yield session
            if commit:
                session.commit()
        except Exception:
            session.rollback()
            raise

        finally:
            LogService.info("Database with() context complete.")
            # This is disabled since the only place this is called is in Factories where
            # they are responsible for commit control.
            # session.commit()

    def _build_session(self):
        """
        Construct a SQLAlchemy Session() context object. To avoid having to pass session
        objects around between Barbados (backend) and Jamaica (frontend) this function
        will attempt to determine if we're running inside of a Flask context at the time of
        call (scoped session per-request) and use that session. If we're not then generate
        one 'cause we're probably running in a script or something weird like that.
        Flask sessions will close at the end of the request or when explicitly told to
        so to prevent double-committing (which isn't a problem, it just resets the session
        an extra time) this will feed back into the caller.
        https://docs.sqlalchemy.org/en/13/orm/session_basics.html#closing
        :return: Session context object, Boolean of whether to trigger a commit or not.
        """
        commit = False
        try:
            from flask_sqlalchemy_session import current_session as session
            if not session:
                raise RuntimeError
            LogService.info("Using Flask session")
        except RuntimeError as e:
            session = self.ScopedSession()
            commit = True
            LogService.info("Using thread scoped session")

        return session, commit
