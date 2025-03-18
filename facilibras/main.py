from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from facilibras.rotas import autenticacao

# Cria a API o middleware para liberar comunicação com frontend
app = FastAPI(title="Facilibras")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclue todos os roteadores no principal
app.include_router(autenticacao.router)
