import sqlite3
import os

# Novamente, simulando a entidade de Domínio que você pulou.
# Em uma arquitetura limpa, isso seria importado de 'domain.livro'
class Livro:
    def __init__(self, id, titulo, livraria):
        self.id = id
        self.titulo = titulo
        self.livraria = livraria

class CatalogoRepository:
    def __init__(self):
        self.db_name = "app_cliente.db"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, '..', self.db_name)

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def listar_todos(self):
        """
        Busca todos os livros no banco e os devolve como Objetos de Domínio.
        O Repositório não filtra regras de negócio (ex: 'esconder livros da Cultura').
        Ele apenas busca os dados; o Serviço decide o que fazer com eles.
        """
        query = "SELECT id, titulo, livraria FROM catalogo"
        livros = []
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                linhas = cursor.fetchall()
                
                # Hidratação: transformando a tupla burra do SQLite em um objeto inteligente.
                for linha in linhas:
                    livro = Livro(id=linha[0], titulo=linha[1], livraria=linha[2])
                    livros.append(livro)
                    
        except sqlite3.Error as e:
            print(f"Erro ao buscar catálogo (DB): {e}")
            
        return livros

    def buscar_por_id(self, livro_id):
        """
        Busca um único livro pelo ID. Retorna o objeto Livro ou None se não existir.
        """
        query = "SELECT id, titulo, livraria FROM catalogo WHERE id = ?"
        livro = None
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (livro_id,))
                linha = cursor.fetchone()
                
                if linha:
                    livro = Livro(id=linha[0], titulo=linha[1], livraria=linha[2])
                    
        except sqlite3.Error as e:
            print(f"Erro ao buscar livro por ID (DB): {e}")
            
        return livro