from flask import Flask
from config import Config
from database import db
from routes import init_routes
from flask_cors import CORS

# Configuração do app Flask
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicialização do banco de dados
db.init_app(app)

# Registro das rotas
init_routes(app)

# Criando o banco de dados
with app.app_context():
    db.create_all()

# Execução do app
if __name__ == '__main__':
    app.run(debug=True)
