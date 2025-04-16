import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    print("GET /")
    r = requests.get(f"{BASE_URL}/")
    print(f"Status: {r.status_code}\n")


def test_produtos():
    print("GET /api/produtos")
    r = requests.get(f"{BASE_URL}/api/produtos")
    print(f"Status: {r.status_code}")
    print("Resposta:", r.json(), "\n")


def test_supermercados():
    print("GET /api/supermercados")
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
    r = requests.post(f"{BASE_URL}/api/encomendas", json=payload)
    print(f"Status: {r.status_code}")
    try:
        print("Resposta:", r.json(), "\n")
    except Exception:
        print("Resposta não é JSON:", r.text, "\n")


def test_impacto():
    print("GET /api/impacto")
    r = requests.get(f"{BASE_URL}/api/impacto")
    print(f"Status: {r.status_code}")
    print("Resposta:", r.json(), "\n")


if __name__ == "__main__":
    test_home()
    test_produtos()
    test_supermercados()
    test_post_encomenda()
    test_impacto()