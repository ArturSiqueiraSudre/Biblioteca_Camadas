import sqlite3
import os

# Simulando a entidade de Domínio (O ideal é que isso estivesse em domain/livro.py)
class Livro:
    def __init__(self, id, titulo, livraria):
        self.id = id
        self.titulo = titulo
        self.livraria = livraria

class CestaRepository:
    def __init__(self):
        # A configuração do banco deve idealmente vir de variáveis de ambiente (.env)
        # Por enquanto, chumbamos o nome para manter a compatibilidade com seu código base.
        self.db_name = "app_cliente.db"
        
        # Garante que o banco está no caminho correto, mesmo rodando de pastas diferentes
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, '..', self.db_name)

    def _get_connection(self):
        """Método privado para garantir que a conexão sempre seja feita corretamente."""
        # Se o banco de dados mudar (ex: para Postgres), você muda o driver aqui.
        return sqlite3.connect(self.db_path)

    def buscar_itens_por_usuario(self, usuario):
        """
        Retorna uma lista de objetos Livro (Entidade de Domínio) que estão na cesta do usuário.
        """
        query = '''
            SELECT c.id, c.titulo, c.livraria 
            FROM alocacoes a 
            JOIN catalogo c ON a.livro_id = c.id 
            WHERE a.usuario = ?
        '''
        itens_cesta = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (usuario,))
                linhas = cursor.fetchall()
                
                # O Repositório "hidrata" (transforma tuplas do banco em Objetos de Domínio)
                for linha in linhas:
                    # linha[0] = id, linha[1] = titulo, linha[2] = livraria
                    livro = Livro(id=linha[0], titulo=linha[1], livraria=linha[2])
                    itens_cesta.append(livro)
                    
        except sqlite3.Error as e:
            # Em um ambiente real, você usaria o módulo 'logging' do Python aqui.
            print(f"Erro ao buscar cesta no banco: {e}")
            
        return itens_cesta

    def adicionar(self, usuario, livro_id):
        """
        Salva um novo item na cesta. Retorna True se sucesso, False se falha.
        As validações de regra de negócio (limites, duplicatas) JÁ FORAM FEITAS no Service.
        """
        query = "INSERT INTO alocacoes (livro_id, usuario) VALUES (?, ?)"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (livro_id, usuario))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao adicionar na cesta (DB): {e}")
            return False

    def remover(self, usuario, livro_id):
        """Remove um item específico da cesta do usuário."""
        query = "DELETE FROM alocacoes WHERE usuario = ? AND livro_id = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (usuario, livro_id))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover da cesta (DB): {e}")
            return False