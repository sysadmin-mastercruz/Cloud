from app import create_app

app = create_app()

def listar_rotas():
    print("\n📌 Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} ➜ {rule}")


if __name__ == '__main__':
    listar_rotas()
    app.run(debug=True, host='0.0.0.0')
