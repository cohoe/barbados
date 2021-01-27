from barbados.connectors.postgresql import PostgresqlConnector


class DatabaseService:
    """
    Generic database service class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * PostgreSQL
    * SQLite
    * DynamoDB

    Since everything in database-land operates via a connection object that's all
    this class really creates.
    """

    connector = PostgresqlConnector()

    @staticmethod
    def get_session():
        """
        Retrieve a SQLAlchemy Session context from the connector.
        :return: SQLAlchemy Session object.
        """
        return DatabaseService.connector.get_session()

    @staticmethod
    def drop_all():
        """
        Drop all tables from the database.
        :return: None
        """
        DatabaseService.connector.drop_all()

    @staticmethod
    def create_all():
        """
        Create all tables in the database.
        :return: None
        """
        DatabaseService.connector.create_all()
