from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from facilibras.rotas import autenticacao, exercicios, perfil, ranking

# Cria a API o middleware para liberar comunicação com frontend
app = FastAPI(title="Facilibras", summary="Facilitando o aprendizado de Libras")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclue todos os roteadores no principal
app.include_router(autenticacao.router)
app.include_router(exercicios.router)
app.include_router(ranking.router)
app.include_router(perfil.router)
