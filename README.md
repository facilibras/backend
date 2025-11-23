# Facilibras (Backend)

Gerencia autenticação, exercícios, categorias de sinais, registro de desempenho e o processamento necessário para avaliar os sinais realizados pelo usuário.

## Bibliotecas Utilizadas
- FastAPI (Framework Web)
- MediaPipe (Reconhecimento dos Gestos)
- SQLAlchemy (ORM)
- Alembic (Migrações)

## Como Iniciar o Backend
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Crie um banco de dados PostgreSQL
    ```sql
    CREATE DATABASE facilibras; -- apenas exemplo
    ```

3. Configure as variáveis de ambiente:
   - Copie o arquivo de exemplo `.env.example` para um novo arquivo `.env`:  
     ```bash
     cp .env.example .env
     ```
   - Editar o arquivo `.env` conforme necessário.

4. Inicie o banco de dados:
   ```bash
   python -m scripts.iniciar_db
   ```
5. Inicie o servidor FastAPI:
   ```bash
   python -m fastapi dev facilibras/main.py
   ```
## Executar pela linha de comando
```bash
# Reconhece o sinal referente à letra G utiliza a webcam
python -m facilibras letra G

# Reconhece o sinal referente ao alimento 'Bolacha' a partir de um vídeo
python -m facilibras alimento bolacha --video caminho_video.mp4

# Lista todas os sinais que podem ser reconhecidos
python -m facilibras sinais

# Validar interativamente um sinal
python -m facilibras interativo -o FRENTE -d POLEGAR_CIMA -d INDICADOR_BAIXO

# Para ver todos os comandos
python -m facilibras --help
```
