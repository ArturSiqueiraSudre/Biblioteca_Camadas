import sqlite3

class SistemaAlocacao:
    def __init__(self):
        self.db_name = "app_cliente.db"
        self._preparar_banco()

    def _preparar_banco(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Tabela 1: O catálogo
            cursor.execute('''CREATE TABLE IF NOT EXISTS catalogo (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                titulo TEXT, 
                                livraria TEXT)''')
            
            # Tabela 2: O que o usuário alocou
            cursor.execute('''CREATE TABLE IF NOT EXISTS alocacoes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                livro_id INTEGER, 
                                usuario TEXT)''')
            
            # Injeta dados iniciais se o banco for novo
            cursor.execute("SELECT COUNT(*) FROM catalogo")
            if cursor.fetchone()[0] == 0:
                livros_iniciais = [
                    ("O Nome do Vento", "Livraria Cultura - Centro"),
                    ("Engenharia de Software", "Biblioteca Universitaria"),
                    ("Padroes de Projeto", "Saraiva Mega Store")
                ]
                cursor.executemany("INSERT INTO catalogo (titulo, livraria) VALUES (?, ?)", livros_iniciais)
            conn.commit()

    def listar_catalogo(self):
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT id, titulo, livraria FROM catalogo").fetchall()

    def alocar_livro(self, livro_id, usuario):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO alocacoes (livro_id, usuario) VALUES (?, ?)", (livro_id, usuario))
            conn.commit()

    def listar_alocacoes_usuario(self, usuario):
        with sqlite3.connect(self.db_name) as conn:
            query = '''SELECT c.titulo, c.livraria 
                       FROM alocacoes a 
                       JOIN catalogo c ON a.livro_id = c.id 
                       WHERE a.usuario = ?'''
            return conn.execute(query, (usuario,)).fetchall()