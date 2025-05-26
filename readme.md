## 🌍 API Azure – Plataforma Logística  
### 📚 Módulo 7
### 📅 Maio de 2025


---

## 📖 Descrição do Projeto

Este projeto simula uma plataforma logística baseada em microserviços, onde uma API Flask expõe endpoints relacionados com encomendas, fornecedores e consumidores de fruta.  
A aplicação está preparada para produção com **Docker**, **Kubernetes**, **Prometheus/Grafana**, e pipelines de **CI/CD com análise de segurança** (Trivy e OWASP ZAP).

---

# 📁 Estrutura do Projeto

```
projeto7/
├── .github/
│   └── workflows/
│       └── github-pipeline.yml
├── app/
│   ├── logic/
│   │   ├── consumidor.py
│   │   ├── encomendas.py
│   │   ├── fornecedor.py
│   │   ├── impacto.py
│   │   └── produto.py
│   ├── utils/
│   │   ├── data_loader.py
│   │   └── __init__.py
│   └── api_routes.py
├── k8s/
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── api-servicemonitor.yaml
│   ├── azure-pipelines.yml
│   ├── azure.yml
│   ├── grafana-deployment.yaml
│   ├── grafana-service.yaml
│   ├── kube-state-metrics.yaml
│   ├── monitor.py
│   ├── namespace.yaml
│   ├── prometheus-configmap.yaml
│   ├── prometheus-deployment.yaml
│   └── prometheus-service.yaml
├── .env
├── deploy.sh
├── deploy_aci.sh
├── docker-compose.yml
├── Dockerfile
├── readme.md
├── requirements.txt
├── run.py
├── swagger.yaml
├── teste_endpoints.py
└── teste_postman.json

```



# 📊 Monitorização da API `api-azure` com Prometheus e Grafana

## 🎯 Objetivo
Implementar a monitorização de uma API Flask (`api-azure`) usando Prometheus e Grafana, com métricas personalizadas expostas no endpoint `/metrics`. O ambiente Kubernetes está no namespace onde corre a aplicação e  está instalada a stack de monitorização com Prometheus Operator

---

## 🧩 Visão Geral do Processo

1. Preparar a aplicação Flask para expor métricas via `prometheus_client`
2. Atualizar a imagem Docker e publicá-la no Azure Container Registry (ACR)
3. Atualizar os deployments em Kubernetes nos dois namespaces
4. Criar um `Service` com nome de porta e labels corretos
5. Criar um `ServiceMonitor` no namespace do Prometheus Stack
6. Verificar que o Prometheus está a scrapar métricas com sucesso
7. Visualizar métricas no Grafana

---

## 🛠️ Etapas detalhadas

### 1. Instrumentação da aplicação Flask

Foi adicionado ao `run.py` suporte para métricas Prometheus com os seguintes elementos:

- `http_requests_total`: contador total de pedidos HTTP
- `http_request_duration_seconds`: latência dos pedidos por método e endpoint

```python
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Summary

REQUEST_COUNT = Counter('http_requests_total', 'Total de pedidos HTTP', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Summary('http_request_duration_seconds', 'Duração dos pedidos HTTP', ['method', 'endpoint'])

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(duration)
    return response
```

---

### 2. Atualização do `requirements.txt`

Adição da biblioteca `prometheus_client` para permitir exportar métricas:

```
prometheus_client
```

---

### 3. Construção e publicação da imagem Docker no ACR

```bash
docker build -t acrgrupo1.azurecr.io/api-azure:v3 .
docker push acrgrupo1.azurecr.io/api-azure:v3
```

---

### 4. Atualização do deployment da aplicação no Kubernetes

```bash
kubectl set image deployment/api-azure api-azure=acrgrupo1.azurecr.io/api-azure:v3 -n master-cruz
```

---

### 5. Configuração do Service da API

Foi criado um Service com o nome de porta `http` (necessário para o ServiceMonitor) e label `app=api-azure`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-azure
  namespace: grupo1
  labels:
    app: api-azure
spec:
  selector:
    app: api-azure
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

---

### 6. Criação do ServiceMonitor no namespace `master-cruz`

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-azure-monitor
  namespace: master-cruz
  labels:
    release: prometheus-stack
spec:
  selector:
    matchLabels:
      app: api-azure
  namespaceSelector:
    matchNames:
      - master-cruz
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

Utilizámos o recurso `ServiceMonitor` do Prometheus para permitir encontrar o serviço `api-azure` no namespace `master-cruz`, na porta `http`, no path `/metrics`.

O Prometheus procura o serviço api-azure com a label app:api-azure e escuta na porta http no path /metrics a cada 15 segundos.

Isto permite que o Prometheus recolha as métricas expostas pela aplicação automáticamente.

---

### 7. Verificação no Prometheus e Grafana

Após aplicação de todas as configurações:

- O Prometheus detectou automaticamente o target `api-azure-monitor`
- Estado `UP` confirmado no dashboard Prometheus (Status → Targets)
- As métricas `http_requests_total` e `http_request_duration_seconds` tornaram-se visíveis no Grafana

---

## ✅ Resultado final

- A API está a exportar métricas completas de tráfego e performance
- A interface do Prometheus fica acessível no browser e permite vizualizar o estado dos containers
- A interface do Grafana fica acessível no browser e permite visualizar os gráficos das métricas pretendidas
- Concluindo: a stack de observabilidade Prometheus + Grafana monitoriza a API em tempo real

🟢 Endereço do Prometheus
```bash 
http://172.211.209.38/targets
```
📊 Link direto para o dashboard Grafana (grupo1)
```bash Grafana:
http://132.220.61.62/d/6581e46e4e5c7ba40a07646395ef7b29/grupo1?orgId=1&from=now-1h&to=now&timezone=utc&var-datasource=default&var-cluster=&var-namespace=master-cruz&var-pod=api-azure-746b55858-cttzr&refresh=10s
```

---

## 📝 Considerações finais

Este processo permite escalar a monitorização facilmente:
- Adicionando novas aplicações com métricas Prometheus
- Automatizando ServiceMonitors via Helm ou CI/CD
- Configurando alertas via Alertmanager ou Grafana


---


# 🔐 Análise de Segurança com Trivy

**Trivy** é uma ferramenta de análise de vulnerabilidades usada neste projeto para:

* Verificar falhas de segurança na imagem Docker
* Identificar problemas no código-fonte (pacotes, libs)
* Integrar segurança no CI/CD (GitHub Actions)

### 🧪 Testes Locais com Trivy

#### 1. Instalar Trivy localmente (Linux)

```bash
wget https://github.com/aquasecurity/trivy/releases/download/v0.62.1/trivy_0.62.1_Linux-64bit.deb
sudo dpkg -i trivy_0.62.1_Linux-64bit.deb
```

#### 2. Construir a imagem Docker

```bash
sudo docker build -t api-azure:v1 .
```

#### 3. Fazer scan à imagem Docker

```bash
trivy image api-azure:v1
```

#### 4. Fazer scan ao código-fonte (dependências e ficheiros)

```bash
trivy fs .
```

#### 5. Verificar configuração do Dockerfile

```bash
trivy config Dockerfile
```

#### (Opcional) 6. Verificar segurança no Kubernetes (se aplicável)

```bash
trivy k8s sysadmin-cluster --report summary --include-namespaces master-cruz -f json -o relatorio.json
```

### 🛠 Exemplo de integração no GitHub Actions

```yaml
- name: Instalar Trivy
  run: |
    wget https://github.com/aquasecurity/trivy/releases/download/v0.62.1/trivy_0.62.1_Linux-64bit.deb
    sudo dpkg -i trivy_0.62.1_Linux-64bit.deb

- name: Scan da imagem Docker
  run: |
    docker build -t api-azure:v1 .
    trivy image api-azure:v1 || true

- name: Scan do código
  run: trivy fs . || true
```

### 🔎 Notas importantes

* Scans no CI/CD não bloqueiam o pipeline (`|| true`), mas devem ser monitorizados
* Trivy usa uma base de dados de vulnerabilidades que é atualizada automaticamente
* Para melhores resultados, executa os comandos com frequência e antes de cada deploy

---

# 🧪 Pipeline de Análise de Segurança com OWASP ZAP via GitLab CI/CD

Este projeto implementa uma pipeline CI/CD que utiliza o OWASP ZAP para realizar uma análise de segurança automatizada sempre que é feito um push para o repositório remoto. A análise de segurança é feita a uma API em execução numa máquina virtual (VM) do Azure, utilizando o endpoint `/api/supermercados`. O relatório gerado é guardado como artefacto no GitLab.

---

## 🔧 Pré-requisitos

* Projeto com aplicação Python (ex: Flask) com `python3 run.py` e `requirements.txt`
* API acessível externamente (ex: `http://51.124.96.205:5000/api/supermercados`)
* GitLab Runner configurado na VM Azure
* Permissões de escrita adequadas no sistema de ficheiros para o GitLab Runner

---

## 🚀 Comandos Git para dar trigger à pipeline:

```bash
git add .gitlab-ci.yml
git commit --allow-empty -m "Trigger pipeline"
git push origin RodasAzure
```

---

## 📄 Estrutura do `.gitlab-ci.yml`

```yaml
zap_scan:
  stage: test
  script:
    - apt-get update && apt-get install -y python3-venv curl unzip default-jre
    - python3 -m venv venv
    - source venv/bin/activate
    - pip install --upgrade pip
    - pip install -r requirements.txt
    - nohup python3 run.py > app.log 2>&1 &
    - sleep 10

    # Instalar ZAP
    - curl -L -o zap.sh https://github.com/zaproxy/zaproxy/releases/download/v2.15.0/ZAP_2_15_0_unix.sh
    - chmod +x zap.sh
    - mkdir zap_install
    - ./zap.sh -q -dir zap_install
    - chmod -R 777 zap_install

    # Fazer scan e gerar relatório em JSON
    - export ZAP_JSON="$(pwd)/zap-report.json"
    - ./zap_install/zap.sh -cmd -quickurl http://51.124.96.205:5000/api/supermercados -quickout "$ZAP_JSON" -quickprogress

    # Verificar se há vulnerabilidades no JSON
    - python3 -c "import json; data=open('$ZAP_JSON').read(); print('❌ Vulnerabilidades encontradas!') if 'riskdesc' in data else print('✅ Sem vulnerabilidades!'); exit(1) if 'riskdesc' in data else exit(0)"

  artifacts:
    when: always
    paths:
      - zap-report.json
```

📄 [Ver zap-report.html](https://gitlab.com/sysadmin-modulo5/projeto5/-/raw/RodasAzure/zap-report.html)

---

## 🛡️ Principais Alertas Identificados pelo OWASP ZAP

| Alerta                                                                               | Descrição e Solução                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Médio - Content Security Policy (CSP) Header Not Set**                             | **Descrição:** CSP é uma camada adicional de segurança que ajuda a detetar e mitigar ataques como XSS e injeção de dados, controlando as fontes de conteúdo que o browser pode carregar. <br> **Solução:** Configurar o servidor web (ou load balancer, etc.) para incluir o header `Content-Security-Policy`.         |
| **Baixo - Server Leaks Version Information via "Server" HTTP Response Header Field** | **Descrição:** O servidor web/aplicação está a expor informações sobre a versão no header HTTP `Server`, o que pode facilitar ataques. <br> **Solução:** Configurar o servidor para ocultar o header `Server` ou mostrar apenas informações genéricas.                                                                 |
| **Baixo - X-Content-Type-Options Header Missing**                                    | **Descrição:** A ausência do header `X-Content-Type-Options: nosniff` permite que browsers antigos façam "MIME sniffing", podendo interpretar o conteúdo de forma errada e insegura. <br> **Solução:** Garantir que o servidor define corretamente o header `Content-Type` e também `X-Content-Type-Options: nosniff`. |

---




---

## ✍️ **Equipa**

- Ricardo Cruz
- Rodrigo Almeida
- José Cardoso
- Rui Maciel


## 📌 Observações

- Projeto modular e preparado para produção
- Monitorização e segurança integradas no ciclo DevSecOps
- Estrutura de pastas clara e padronizada
- Documentação Swagger disponível para testes interativos

> Última alteração: maio 2025
