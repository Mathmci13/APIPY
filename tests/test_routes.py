from tests.conftest import add_sample_products


def test_create_product(test_client):
    new_product = {
        # "id": "1",
        "name": "Produto Teste",
        "description": "Descrição do produto de teste",
        "price": 100.0,
        "quantity": 10
    }
    response = test_client.post("/products/", json=new_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_product["name"]

def test_get_products(test_client, add_sample_products):
    # Cria os produtos de exemplo no banco
    add_sample_products()

    # Chama o endpoint
    response = test_client.get("/products/")
    assert response.status_code == 200
    products = response.json()

    # Exibe a lista no console
    print("Produtos retornados pela API:", products)
    assert len(products) == 2  # Verifica se dois produtos foram retornados

    for product in products:
        assert "id" in product
        assert isinstance(product["id"], int)



def test_delete_product(test_client,add_sample_products):
    add_sample_products()
    product_id = 2  # Substitua pelo ID de um produto existente ou crie um para teste
    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 200
