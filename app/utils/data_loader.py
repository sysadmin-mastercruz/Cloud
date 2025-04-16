import csv
import io
import os
from azure.storage.blob import BlobServiceClient
from app.logic.produto import Produto
from app.logic.fornecedor import Supermercado
from dotenv import load_dotenv

load_dotenv()

CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

def _ler_csv_blob(blob_name):
    blob_service = BlobServiceClient.from_connection_string(CONN_STR)
    blob_client = blob_service.get_blob_client(container=CONTAINER, blob=blob_name)
    stream = blob_client.download_blob()
    content = stream.readall().decode("utf-8")
    return list(csv.DictReader(io.StringIO(content)))

def carregar_produtos():
    dados = _ler_csv_blob("produtos.csv")
    produtos = []
    for row in dados:
        p = Produto(
            row["nome"],
            float(row["preco"]),
            float(row["peso"]),
            row["pais_origem"],
            int(row["distancia"]),
            row["transporte"],
            float(row["emissoes"]),
            float(row["impacto"]),
        )
        produtos.append(p)
    return produtos

def carregar_supermercados():
    dados = _ler_csv_blob("supermercados.csv")
    supermercados = {}
    for row in dados:
        s = Supermercado(
            row["nome"],
            float(row["consumo_energia"]),
            float(row["eficiencia"]),
            int(row["distancia"]),
        )
        supermercados[row["nome"]] = s
    return supermercados
