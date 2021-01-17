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
