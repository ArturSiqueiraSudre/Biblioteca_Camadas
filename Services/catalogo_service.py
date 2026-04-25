# Acesso a dados via Repositório, mantendo o Serviço limpo
from Repositories.catalogo_repository import CatalogoRepository

class CatalogoService:
    def __init__(self):
        # O Serviço confia no Repositório para buscar os dados brutos
        self.catalogo_repo = CatalogoRepository()

    def listar_todos_disponiveis(self):
        """
        Retorna todos os livros que estão atualmente no catálogo.
        No futuro, regras como "não mostrar livros esgotados" entrariam aqui.
        """
        livros_brutos = self.catalogo_repo.listar_todos()
        
        # Aqui o Serviço poderia aplicar regras de formatação ou filtragem.
        # Por exemplo, se tivéssemos um campo 'ativo' no banco de dados.
        livros_filtrados = []
        for livro in livros_brutos:
            # Exemplo de regra de negócio: ignorar livros de certas livrarias em manutenção
            # if livro.livraria == "Livraria em Reforma": continue
            livros_filtrados.append(livro)
            
        return livros_filtrados

    def buscar_livro_por_id(self, livro_id):
        """Busca um livro específico e aplica regras caso não seja encontrado."""
        if not livro_id or str(livro_id).strip() == "":
            return None, "ID do livro é inválido."
            
        livro = self.catalogo_repo.buscar_por_id(livro_id)
        
        if not livro:
            return None, "Livro não encontrado no catálogo atual."
            
        return livro, "Livro encontrado."