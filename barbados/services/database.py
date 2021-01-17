from barbados.connectors.postgresql import PostgresqlConnector


class DatabaseService:
    """
    Generic database service class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * PostgreSQL
    * SQLite
    * DynamoDB
    """

    database_connector = PostgresqlConnector()
