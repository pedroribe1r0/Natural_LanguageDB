import os
from src.Database_manager import DatabaseManager
from src.TextToSQLConverter import TextToSQLConverter
from config.settings import get_db_data

class TextToSQLApp:
    def __init__(self, db_manager: DatabaseManager, converter: TextToSQLConverter):
        self.db_manager = db_manager
        self.converter = converter
        self.db_connected = False
        self.schema_loaded = False

    def limpar_terminal(self):
        os.system("clear")

    def pausar(self):
        input("\nPressione Enter para continuar...")

    def conectar_banco(self):
        self.limpar_terminal()
        if self.db_manager.connect_server():
            nome = self.db_manager.list_databases()
            self.db_connected = True
            if nome and self.db_manager.connect_database(nome):
                schema = self.db_manager.get_tables_and_columns()
                self.converter.schema = schema
                print(self.converter.format_schema())
                self.schema_loaded = True
        if not self.db_connected:
            print("Conexão falhou. Verifique as credenciais.")
        else:
            print("Banco conectado com sucesso.")
        self.pausar()

    def perguntar_e_executar(self):
        self.limpar_terminal()

        if not self.db_connected or not self.schema_loaded:
            print("Conecte-se ao banco e carregue o esquema primeiro.")
            self.pausar()
            return

        pergunta = input("Pergunta em linguagem natural: ").strip()
        if not pergunta:
            print("Nenhuma pergunta fornecida.")
            self.pausar()
            return

        print("Enviando para o Gemini...")
        sql = self.converter.generate_sql(pergunta)
        print(f"\nSQL Gerado:\n{sql}")

        if sql:
            print("\nExecutando...")
            result = self.db_manager.run_query(sql)

            if result is not None:
                rows, cols = result

                if rows and cols:
                    print("\nResultado:")
                    print(f"Colunas: {', '.join(cols)}")
                    for row in rows:
                        print(row)
                else:
                    print("Query executada com sucesso.")
            else:
                print("Erro ao executar a query.")
        else:
            print("O Gemini não conseguiu gerar a query.")
        self.pausar()

    def exibir_menu(self):
        self.limpar_terminal()
        print("==================== MENU PRINCIPAL ====================")
        print("1. Conectar ao Banco de Dados")
        print("2. Fazer Pergunta e Executar SQL")
        print("3. Sair")
        print("========================================================")

    def run(self):
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            match opcao:
                case '1':
                    self.conectar_banco()
                case '2':
                    self.perguntar_e_executar()
                case '3':
                    print("Saindo do programa.")
                    break
                case _:
                    print("Opção inválida. Tente novamente.")
                    self.pausar()

# --- Execução principal ---
if __name__ == "__main__":
    DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT = get_db_data()
    print(f"Usuário: {DB_USERNAME}")
    print(f"Senha: {DB_PASSWORD}")
    print(f"Host: {DB_HOST}")
    print(f"Porta: {DB_PORT} ({type(DB_PORT)})")

    db_manager = DatabaseManager(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT)

    try:
        text_to_sql_converter = TextToSQLConverter(schema={})
    except ValueError as e:
        print(f"Erro de inicialização do Gemini: {e}")
        print("Não será possível usar a funcionalidade de geração de SQL.")
        text_to_sql_converter = None

    if text_to_sql_converter:
        app_menu = TextToSQLApp(db_manager, text_to_sql_converter)
        app_menu.run()
    else:
        print("O programa não pode iniciar sem a configuração correta da API do Gemini.")
