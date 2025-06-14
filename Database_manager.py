from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

class DatabaseManager:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = None

    def connect(self) -> bool:
        try:
            url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(url)
            # Testa a conexão
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            print("✅ Conexão com MySQL estabelecida!")
            return True
        except SQLAlchemyError as e:
            print("❌ Erro ao conectar ao banco:", e)
            return False

    def get_tables_and_columns(self):
        if not self.engine:
            print("❌ Sem conexão ativa.")
            return

        inspector = inspect(self.engine)
        schema = {}
        for table in inspector.get_table_names():
            columns = inspector.get_columns(table)
            schema[table] = [col['name'] for col in columns]
        return schema

    def run_query(self, sql):
        if not self.engine:
            print("❌ Sem conexão ativa.")
            return
        try:
            with self.engine.connect() as conn:
                result = conn.execute(sql)
                return result.fetchall(), result.keys()
        except SQLAlchemyError as e:
            print("❌ Erro ao executar query:", e)
            return None, None
