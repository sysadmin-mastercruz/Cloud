import requests
from unittest.mock import patch

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    print("GET /")
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "API em execução"}
        
        r = requests.get(f"{BASE_URL}/")
        print(f"Status: {r.status_code}\n")
        print("Resposta:", r.json(), "\n")


def test_produtos():
    print("GET /api/produtos")
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"nome": "banana", "preco": 1.2},
            {"nome": "maçã", "preco": 2.3}
        ]
        
        r = requests.get(f"{BASE_URL}/api/produtos")
        print(f"Status: {r.status_code}")
        print("Resposta:", r.json(), "\n")


def test_supermercados():
    print("GET /api/supermercados")
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"nome": "Pingo Doce", "localizacao": "Lisboa"},
            {"nome": "Continente", "localizacao": "Porto"}
        ]
        
        r = requests.get(f"{BASE_URL}/api/supermercados")
        print(f"Status: {r.status_code}")
        print("Resposta:", r.json(), "\n")


def test_post_encomenda():
    print("POST /api/encomendas")
    payload = {
        "supermercado": "Continente",
        "produtos": [
            {"nome": "banana", "quantidade": 2},
            {"nome": "maçã", "quantidade": 1}
        ]
    }
    
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"status": "Encomenda criada com sucesso"}
        
        r = requests.post(f"{BASE_URL}/api/encomendas", json=payload)
        print(f"Status: {r.status_code}")
        try:
            print("Resposta:", r.json(), "\n")
        except Exception:
            print("Resposta não é JSON:", r.text, "\n")


def test_impacto():
    print("GET /api/impacto")
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"impacto": "baixo"}
        
        r = requests.get(f"{BASE_URL}/api/impacto")
        print(f"Status: {r.status_code}")
        print("Resposta:", r.json(), "\n")


if __name__ == "__main__":
    test_home()
    test_produtos()
    test_supermercados()
    test_post_encomenda()
    test_impacto()
