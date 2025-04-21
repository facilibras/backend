# Facilibras (Backend)

Backend do Facilibras

## Bibliotecas utilizadas: 
- FastAPI
- MediaPipe

## Como Iniciar o Backend  
1. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```
2. Configure as variáveis de ambiente:  
   - Copie o arquivo de exemplo `.env.example` para um novo arquivo `.env`:  
     ```bash
     cp .env.example .env
     ```
   - Editar o arquivo `.env` conforme necessário.

3. Inicie o banco de dados:
   ```bash
   python iniciar_db.py
   ```
4. Inicie o servidor FastAPI:  
   ```bash
   fastapi dev facilibras/main.py
   ```
