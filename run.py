from app import create_app
from flask_cors import CORS
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Summary
import time

# Criar a app Flask
app = create_app()
CORS(app)

# Métricas Prometheus
REQUEST_COUNT = Counter('api_requests_total', 'Número total de pedidos à API')
REQUEST_LATENCY = Summary('api_request_latency_seconds', 'Latência dos pedidos à API')

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.before_request
def before_request():
    REQUEST_COUNT.inc()
    app.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - app.start_time
    REQUEST_LATENCY.observe(duration)
    return response

# Função para listar todas as rotas disponíveis
def listar_rotas():
    print("\n📌 Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} ➜ {rule}")

if __name__ == '__main__':
    listar_rotas()
    app.run(debug=True, host='0.0.0.0')
