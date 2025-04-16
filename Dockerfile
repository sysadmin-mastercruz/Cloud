# Imagem base
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copiar o ficheiro de dependências e instalar
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do projeto
COPY . .

# Definir variáveis de ambiente (podem também vir do Azure)
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expor a porta usada pelo Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
