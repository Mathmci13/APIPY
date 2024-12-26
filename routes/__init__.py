from flask import Blueprint
from routes.product_routes import product_routes

# Inicializa o blueprint para as rotas
def init_routes(app):
    app.register_blueprint(product_routes)
