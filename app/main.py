from fastapi import FastAPI
from app.routes import router as api_router
from app.database import engine
from app.models import Base
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Inicializar o banco de dados
Base.metadata.create_all(bind=engine)

# Instanciar o FastAPI
app = FastAPI()

# Adicionar o middleware CORS para permitir solicitações do frontend (React)
origins = [
    "http://localhost:3000",  # Permitir que o React no localhost:3000 acesse a API
    "http://127.0.0.1:"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Configuração de templates
templates = Jinja2Templates(directory="app/templates")

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registrar as rotas
app.include_router(api_router)

# Rota de homepage
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
