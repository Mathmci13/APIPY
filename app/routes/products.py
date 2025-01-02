from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import httpx

router = APIRouter()

# Rota para criar um novo produto
@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Chama a função CRUD para criar o produto no banco de dados
    return crud.create_product(db=db, product=product)

# Rota para listar todos os produtos
@router.get("/products/")
def get_products(db: Session = Depends(get_db)):
    # Chama a função CRUD para obter todos os produtos
    products = crud.get_products(db)
    return products

# Rota para buscar um produto por ID
@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    # Chama a função CRUD para obter um produto pelo ID
    product = crud.get_product_by_id(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

# Rota para atualizar um produto
@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Chama a função CRUD para atualizar o produto
    updated_product = crud.update_product(db, product_id=product_id, product=product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_product

# Rota para excluir um produto
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Chama a função CRUD para excluir o produto
    result = crud.delete_product(db, product_id=product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto excluído com sucesso"}



# BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory="app/templates")

@router.get("/productsNoJinja", response_class=HTMLResponse)
async def get_products_no_jinja(request: Request):
    try:
        # Consumindo a API existente para obter a lista de produtos
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/products/")
            products = response.json()  # Obtemos os produtos em formato JSON
    except Exception as e:
        products = []  # Em caso de erro, enviamos uma lista vazia
        print(f"Erro ao obter os produtos: {e}")

    # Renderizando o template com os produtos
    context = {"request": request, "products": products}
    return templates.TemplateResponse("index.html", context)