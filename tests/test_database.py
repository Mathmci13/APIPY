# def test_add_product_to_database(db_session):
#     from app.models import Product  # Importa o modelo de produto
#     new_product = Product(name="Produto Teste", description="Teste", price=50.0, quantity=5)
#     db_session.add(new_product)
#     db_session.commit()
#     db_session.refresh(new_product)
#
#     assert new_product.id is not None
#     assert new_product.name == "Produto Teste"
