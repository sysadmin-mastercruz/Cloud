from app import create_app
from flask_cors import CORS  # Importar suporte a CORS

# Criar a app Flask
app = create_app()

# Ativar CORS para permitir chamadas de qualquer origem (útil para Swagger UI, por exemplo)
CORS(app)

# Função para listar todas as rotas disponíveis na API
def listar_rotas():
    print("\n📌 Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} ➜ {rule}")

# Iniciar a aplicação
if __name__ == '__main__':
    listar_rotas()
    app.run(debug=True, host='0.0.0.0')
