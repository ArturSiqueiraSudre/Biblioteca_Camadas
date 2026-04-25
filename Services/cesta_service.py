# Importamos as interfaces de acesso a dados (Repositories). 
# O Service confia que o Repository sabe falar com o banco.
from Repositories.cesta_repository import CestaRepository
from Repositories.catalogo_repository import CatalogoRepository

class CestaService:
    def __init__(self):
        # Injeção de dependência clássica. 
        self.cesta_repo = CestaRepository()
        self.catalogo_repo = CatalogoRepository()
        
        # Regra de negócio explícita: limite máximo de livros na cesta
        self.LIMITE_LIVROS = 3

    def obter_cesta_usuario(self, usuario):
        """Retorna os itens atuais na cesta do usuário."""
        return self.cesta_repo.buscar_itens_por_usuario(usuario)

    def adicionar_item(self, usuario, livro_id):
        """
        Tenta adicionar um livro à cesta. 
        Retorna uma tupla (Sucesso: bool, Mensagem: str)
        """
        # REGRA 1: O livro realmente existe no catálogo da biblioteca?
        livro = self.catalogo_repo.buscar_por_id(livro_id)
        if not livro:
            return False, "Operação negada: Livro não encontrado no catálogo."

        itens_atuais = self.cesta_repo.buscar_itens_por_usuario(usuario)

        # REGRA 2: O usuário já estourou o limite de empréstimos?
        if len(itens_atuais) >= self.LIMITE_LIVROS:
            return False, f"Limite atingido: Você só pode ter {self.LIMITE_LIVROS} livros na cesta."

        # REGRA 3: O usuário está tentando adicionar o mesmo livro duas vezes?
        # (Assumindo que 'itens_atuais' traz objetos da nossa camada Domain)
        for item in itens_atuais:
            if str(item.id) == str(livro_id):
                return False, f"O livro '{livro.titulo}' já está na sua cesta."

        # Se passou por todas as barreiras de segurança, autorizamos o Repository a salvar.
        sucesso = self.cesta_repo.adicionar(usuario, livro_id)
        
        if sucesso:
            return True, f"'{livro.titulo}' adicionado à cesta com sucesso!"
        else:
            return False, "Erro interno de sistema ao tentar salvar a cesta."

    def remover_item(self, usuario, livro_id):
        """Remove um item da cesta do usuário."""
        # Poderíamos colocar regras aqui (ex: logar quem removeu), mas por hora apenas delegamos.
        return self.cesta_repo.remover(usuario, livro_id)