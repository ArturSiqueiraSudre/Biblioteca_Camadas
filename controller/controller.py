from flask import Flask, render_template, request
from model.model import SistemaAlocacao

app = Flask(__name__)
sistema = SistemaAlocacao()

@app.route("/", methods=["GET", "POST"])
def portal_cliente():
    usuario_logado = "Artur" 
    
    if request.method == "POST":
        id_livro_escolhido = request.form.get("livro_id")
        if id_livro_escolhido:
            sistema.alocar_livro(id_livro_escolhido, usuario_logado)
            
    catalogo_disponivel = sistema.listar_catalogo()
    meus_livros = sistema.listar_alocacoes_usuario(usuario_logado)
    
    return render_template("index.html", 
                           catalogo=catalogo_disponivel, 
                           meus_livros=meus_livros, 
                           usuario=usuario_logado)

if __name__ == "__main__":
    app.run(debug=True)