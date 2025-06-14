import os
import google.generativeai as genai
from dotenv import load_dotenv # Importa para carregar variáveis de ambiente do arquivo .env

class TextToSQLConverter:
    """
    Uma classe para converter perguntas em linguagem natural para queries SQL
    usando a API do Google Gemini.
    """
    def __init__(self, schema: dict, model_name: str = "gemini-pro"):
        """
        Inicializa o conversor TextToSQL.

        Args:
            schema (dict): Um dicionário que descreve o esquema do banco de dados.
                           Ex: {"tabela_nome": ["coluna1", "coluna2"]}
            model_name (str): O nome do modelo Gemini a ser usado (ex: "gemini-pro", "gemini-1.5-flash").
        """
        self.schema = schema
        self.model_name = model_name

        # Carrega as variáveis de ambiente do arquivo .env
        # Certifique-se de que GOOGLE_API_KEY está definido no seu .env
        load_dotenv()

        # Configura a chave da API Gemini
        # A chave será lida da variável de ambiente GOOGLE_API_KEY
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Inicializa o modelo Gemini com o nome especificado
        self.model = genai.GenerativeModel(self.model_name)

    def format_schema(self) -> str:
        """
        Formata o esquema do banco de dados em uma string legível para o modelo de IA.
        """
        schema_text = ""
        for table, columns in self.schema.items():
            schema_text += f"Tabela {table} ({', '.join(columns)})\n"
        return schema_text

    def generate_sql(self, user_question: str) -> str | None:
        """
        Gera uma query SQL a partir de uma pergunta em linguagem natural usando o modelo Gemini.

        Args:
            user_question (str): A pergunta do usuário em linguagem natural.

        Returns:
            str | None: A query SQL gerada ou None se ocorrer um erro.
        """
        prompt = (
            "Você é um assistente que converte linguagem natural para SQL.\n"
            "Sempre que gerar uma consulta SQL, adicione um ponto e vírgula no final.\n"
            "Esquema do banco de dados:\n"
            f"{self.format_schema()}\n"
            "Pergunta:\n"
            f"{user_question}\n"
            "Responda apenas com a query SQL completa, sem explicações:"
        )

        try:
            # Chama a API do Gemini para gerar conteúdo
            response = self.model.generate_content(
                prompt,
                # Define a temperatura para 0.0 para respostas mais determinísticas (menos criativas)
                generation_config=genai.GenerationConfig(temperature=0.0)
            )
            # Retorna o texto da resposta, removendo espaços em branco extras
            return response.text.strip()
        except Exception as e:
            # Captura e imprime quaisquer erros que ocorram durante a chamada da API
            print(f"❌ Erro ao gerar SQL: {e}")
            return None
