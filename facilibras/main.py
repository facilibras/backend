from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Carrega as variáveis de ambiente
load_dotenv()

# Cria a API o middleware para liberar comunicação com frontend
app = FastAPI(title="Facilibras")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return "teste"
