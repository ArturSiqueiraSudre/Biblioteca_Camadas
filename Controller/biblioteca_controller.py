from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importações das camadas de Serviço (que você ainda precisará construir)
# Observe que o Controller não importa o BD nem o Model diretamente.
from Services.catalogo_service import CatalogoService
from Services.cesta_service import CestaService

# Definição do Blueprint para o módulo da biblioteca
biblioteca_bp = Blueprint('biblioteca', __name__)

# Instanciação dos serviços
catalogo_service = CatalogoService()
cesta_service = CestaService()

@biblioteca_bp.route("/", methods=["GET"])
def index():
    # Simulando a sessão do usuário logado por enquanto
    usuario_logado = "Artur"
    
    # O Controller não faz queries. Ele pede os dados prontos ao Service.
    livros_disponiveis = catalogo_service.listar_todos_disponiveis()
    itens_cesta = cesta_service.obter_cesta_usuario(usuario_logado)
    
    return render_template(
        "index.html", 
        catalogo=livros_disponiveis, 
        cesta=itens_cesta, 
        usuario=usuario_logado
    )

@biblioteca_bp.route("/cesta/adicionar", methods=["POST"])
def adicionar_a_cesta():
    usuario_logado = "Artur"
    livro_id = request.form.get("livro_id")
    
    if not livro_id:
        flash("Erro: Livro inválido ou não selecionado.", "error")
        return redirect(url_for('biblioteca.index'))

    # Delegação total da regra de negócio para a camada de Serviço
    sucesso, mensagem = cesta_service.adicionar_item(usuario_logado, livro_id)
    
    if sucesso:
        flash(mensagem, "success")
    else:
        flash(mensagem, "error") # Ex: "Livro esgotado" ou "Limite da cesta atingido"
        
    return redirect(url_for('biblioteca.index'))

@biblioteca_bp.route("/cesta/remover", methods=["POST"])
def remover_da_cesta():
    usuario_logado = "Artur"
    livro_id = request.form.get("livro_id")
    
    if livro_id:
        cesta_service.remover_item(usuario_logado, livro_id)
        
    return redirect(url_for('biblioteca.index'))