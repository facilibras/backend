# Facilibras (Backend)

Backend do Facilibras

## Bibliotecas Utilizadas
- FastAPI (Framework Web)
- MediaPipe (Reconhecimento dos Gestos)

## Como Iniciar o Backend
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Crie o banco de dados PostgreSQL
    ```sql
    CREATE DATABASE facilibras;
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

# Validar interativamente um sinal
python -m facilibras interativo -o FRENTE -d POLEGAR_CIMA -d INDICADOR_BAIXO
```
