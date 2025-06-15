from sqlalchemy import create_engine, inspect, text, Result
from sqlalchemy.exc import SQLAlchemyError

class DatabaseManager:
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = ""
        self.engine = None

    def connect_server(self) -> bool:
        """
        Conecta ao servidor MySQL sem escolher um banco de dados.
        """
        try:
            url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/"
            self.engine = create_engine(url)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Conexão com o servidor MySQL estabelecida.")
            return True
        except SQLAlchemyError as e:
            print("Erro ao conectar ao servidor:", e)
            return False

    def list_databases(self) -> str | None:
        """
        Lista os bancos disponíveis e retorna o nome escolhido pelo usuário.
        """
        if not self.engine:
            print("Erro: conexão ao servidor ainda não foi feita.")
            return None

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SHOW DATABASES;"))
                databases = [row[0] for row in result]

            if not databases:
                print("Nenhum banco de dados encontrado.")
                return None

            print("\nBancos de dados disponíveis:")
            for i, db_name in enumerate(databases):
                print(f"{i + 1}. {db_name}")

            while True:
                escolha = input("Digite o número do banco que deseja usar: ").strip()
                if escolha.isdigit() and 1 <= int(escolha) <= len(databases):
                    return databases[int(escolha) - 1]
                else:
                    print("Escolha inválida. Tente novamente.")
        except SQLAlchemyError as e:
            print("Erro ao listar bancos de dados:", e)
            return None

    def connect_database(self, database_name: str) -> bool:
        """
        Conecta a um banco de dados específico.
        """
        try:
            self.database = database_name
            url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(url)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"Conectado ao banco de dados: {self.database}")
            return True
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao banco '{database_name}':", e)
            return False

    def get_tables_and_columns(self):
        """
        Retorna um dicionário com tabelas e colunas do banco conectado.
        """
        if not self.engine:
            print("Erro: nenhuma conexão ativa.")
            return

        inspector = inspect(self.engine)
        schema = {}
        for table in inspector.get_table_names():
            columns = inspector.get_columns(table)
            schema[table] = [col['name'] for col in columns]
        return schema

    def run_query(self, sql):
        """
        Executa uma query SQL. Retorna linhas e colunas se for SELECT, ou apenas confirma execução.
        """
        if not self.engine:
            print("Erro: nenhuma conexão ativa.")
            return None, None

        try:
            with self.engine.begin() as conn:
                result: Result = conn.execute(text(sql))

                if result.returns_rows:
                    rows = result.fetchall()
                    cols = result.keys()
                    return rows, cols
                else:
                    return [], []
        except SQLAlchemyError as e:
            print("Erro ao executar a query:", e)
            return None, None
