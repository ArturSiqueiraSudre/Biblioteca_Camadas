
from flask import Flask

# A única coisa que o app.py precisa conhecer é o Controller.
# Ele não importa Serviços, não importa Repositórios e não importa Domínio.
from Controller.biblioteca_controller import biblioteca_bp

def create_app():
    # Instancia a aplicação Flask
    app = Flask(__name__, template_folder='Template')
    
    # Configuração vital para usar o sistema de Flash Messages do Flask
    # Em produção, isso JAMAIS deve ficar exposto no código. Deve vir de um .env
    app.secret_key = 'chave_super_secreta_para_desenvolvimento'

    # Registra as rotas que definimos no Controller
    app.register_blueprint(biblioteca_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    # O debug=True reinicia o servidor automaticamente se você alterar o código
    app.run(debug=True, port=5000)