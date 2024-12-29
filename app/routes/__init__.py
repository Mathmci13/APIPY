from fastapi import APIRouter
from .products import router as products_router

# Criação do roteador principal para agregar todos os sub-roteadores
router = APIRouter()

# Inclusão das rotas no roteador principal
router.include_router(products_router)
