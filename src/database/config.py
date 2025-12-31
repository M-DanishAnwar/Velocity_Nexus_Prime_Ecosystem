class DBConfig:
    # SQL Server Config - Using Local Express
    SERVER = r'(local)\SQLEXPRESS'
    DATABASE = 'VelocityNexusPrime'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    TRUSTED_CONNECTION = 'yes'

    @staticmethod
    def get_connection_string():
        return (
            f"DRIVER={{{DBConfig.DRIVER}}};"
            f"SERVER={DBConfig.SERVER};"
            f"DATABASE={DBConfig.DATABASE};"
            f"Trusted_Connection={DBConfig.TRUSTED_CONNECTION};"
        )