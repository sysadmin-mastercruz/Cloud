from prometheus_client import start_http_server, Summary, Counter, Gauge
import time
import random

# Metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')
IN_PROGRESS = Gauge('app_inprogress_requests', 'Number of in-progress requests')

@REQUEST_TIME.time()
def process_request():
    with IN_PROGRESS.track_inprogress():
        REQUEST_COUNT.inc()
        time.sleep(random.random())

if __name__ == '__main__':
    start_http_server(8000)  # Exposes metrics at http://localhost:8000
    while True:
        process_request()
