from flask import Blueprint, request, jsonify
from models import Product
from database import db

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'quantity': p.quantity
    } for p in products])

@product_routes.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201

@product_routes.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Produto não encontrado!'}), 404

    data = request.json
    product.name = data['name']
    product.description = data.get('description', product.description)
    product.price = data['price']
    product.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Produto atualizado com sucesso!'})

@product_routes.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Produto não encontrado!'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Produto removido com sucesso!'})
