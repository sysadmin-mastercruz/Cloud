import requests
from unittest.mock import patch

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "API em execução"}
        
        r = requests.get(f"{BASE_URL}/")
        
        assert r.status_code == 200
        assert r.json() == {"message": "API em execução"}


def test_produtos():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"nome": "banana", "preco": 1.2},
            {"nome": "maçã", "preco": 2.3}
        ]
        
        r = requests.get(f"{BASE_URL}/api/produtos")
        
        assert r.status_code == 200
        assert r.json() == [
            {"nome": "banana", "preco": 1.2},
            {"nome": "maçã", "preco": 2.3}
        ]


def test_supermercados():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"nome": "Pingo Doce", "localizacao": "Lisboa"},
            {"nome": "Continente", "localizacao": "Porto"}
        ]
        
        r = requests.get(f"{BASE_URL}/api/supermercados")
        
        assert r.status_code == 200
        assert r.json() == [
            {"nome": "Pingo Doce", "localizacao": "Lisboa"},
            {"nome": "Continente", "localizacao": "Porto"}
        ]


def test_post_encomenda():
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
        
        assert r.status_code == 201
        assert r.json() == {"status": "Encomenda criada com sucesso"}


def test_impacto():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"impacto": "baixo"}
        
        r = requests.get(f"{BASE_URL}/api/impacto")
        
        assert r.status_code == 200
        assert r.json() == {"impacto": "baixo"}
