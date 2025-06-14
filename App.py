import os
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from Database_manager import DatabaseManager
from TextToSQLConverter import TextToSQLConverter

class TextToSQLApp:
    """
    Classe para gerenciar o aplicativo de conversão de linguagem natural para SQL.
    """
    def __init__(self, db_manager: DatabaseManager, converter: TextToSQLConverter):
        self.db_manager = db_manager
        self.converter = converter
        self.db_connected = False
        self.schema_loaded = False

    def conectar_banco(self):
        print("\n🔌 Conectando ao banco de dados...")
        self.db_connected = self.db_manager.connect()
        if not self.db_connected:
            print("❌ Conexão falhou. Verifique as credenciais.")
        else:
            print("✅ Banco conectado com sucesso!")

    def carregar_esquema(self):
        if not self.db_connected:
            print("⚠️ Conecte-se ao banco primeiro.")
            return
        print("\n📦 Carregando esquema...")
        schema = self.db_manager.get_tables_and_columns()
        if schema:
            self.converter.schema = schema
            self.schema_loaded = True
            print("✅ Esquema carregado com sucesso:\n")
            print(self.converter.format_schema())
        else:
            print("❌ Erro ao carregar o esquema.")

    def perguntar_e_executar(self):
        if not self.db_connected or not self.schema_loaded:
            print("⚠️ Conecte-se ao banco e carregue o esquema primeiro.")
            return

        pergunta = input("\n🧠 Pergunta em linguagem natural: ").strip()
        if not pergunta:
            print("⚠️ Nenhuma pergunta fornecida.")
            return

        print("📡 Enviando para o Gemini...")
        sql = self.converter.generate_sql(pergunta)

        if sql:
            print("🚀 Executando...")
            rows, cols = self.db_manager.run_query(sql)
            if rows is not None:
                if cols:
                    print("\n📊 Resultado:")
                    print(f"Colunas: {', '.join(cols)}")
                    for row in rows:
                        print(row)
                else:
                    print("✅ Query executada com sucesso.")
            else:
                print("❌ Erro ao executar a query.")
        else:
            print("❌ O Gemini não conseguiu gerar a query.")

    def exibir_menu(self):
        print("\n====== MENU PRINCIPAL ======")
        print("1. Conectar ao Banco de Dados")
        print("2. Carregar Esquema do Banco")
        print("3. Fazer Pergunta e Executar SQL")
        print("4. Sair")
        print("============================")

    def run(self):
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            match opcao:
                case '1':
                    self.conectar_banco()
                case '2':
                    self.carregar_esquema()
                case '3':
                    self.perguntar_e_executar()
                case '4':
                    print("👋 Saindo do programa.")
                    break
                case _:
                    print("❌ Opção inválida. Tente novamente.")

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    load_dotenv() # Carrega as variáveis de ambiente novamente para o escopo global

    # Carrega as credenciais do banco de dados do arquivo .env
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 3306)) # Porta padrão para MySQL é 3306
    DB_DATABASE = os.getenv("DB_DATABASE")

    db_manager = DatabaseManager(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)

    try:
        text_to_sql_converter = TextToSQLConverter(schema={})
    except ValueError as e:
        print(f"Erro de inicialização do Gemini: {e}")
        print("Não será possível usar a funcionalidade de geração de SQL.")
        text_to_sql_converter = None

    if text_to_sql_converter:
        # Instancia e executa o menu
        app_menu = TextToSQLApp(db_manager, text_to_sql_converter)
        app_menu.run()
    else:
        print("\nO programa não pode iniciar sem a configuração correta da API do Gemini.")
