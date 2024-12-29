from sqlalchemy.orm import Session
from app import models, schemas

# Função para criar um produto
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        description=product.description,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Função para obter todos os produtos
def get_products(db: Session):
    return db.query(models.Product).all()

# Função para obter um produto pelo ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

# Função para atualizar um produto
def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.description = product.description
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

# Função para excluir um produto
def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
