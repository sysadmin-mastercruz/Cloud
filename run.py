from app import create_app
from flask_cors import CORS
from flask import request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Summary
import time

# Criar a app Flask
app = create_app()
CORS(app)

# Métricas Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Contagem total de pedidos HTTP',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Summary(
    'http_request_duration_seconds', 
    'Latência dos pedidos HTTP',
    ['method', 'endpoint']
)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time

    endpoint = request.path
    method = request.method
    status = response.status_code

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(request_latency)

    return response

# Função para listar todas as rotas disponíveis
def listar_rotas():
    print("\n📌 Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} ➜ {rule}")

if __name__ == '__main__':
    listar_rotas()
    app.run(debug=True, host='0.0.0.0')
