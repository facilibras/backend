# Facilibras (Backend)

Backend do Facilibras

## Bibliotecas Utilizadas
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
   python -m scripts.iniciar_db
   ```
4. Inicie o servidor FastAPI:
   ```bash
   fastapi dev facilibras/main.py
   ```
## Executar pela linha de comando
```bash
# Reconhece a letra G utiliza a webcam
python -m facilibras letra G

# Reconhece a letra Y a partir de um video
python -m facilibras letra Y --video exemplo.mp4

# Lista todas os sinais que podem ser reconhecidos
python -m facilibras sinais

# Lista todas os sinais da categoria ALFABETO
python -m facilibras sinais --categoria alfabeto
```