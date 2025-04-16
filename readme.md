## 🌍 API Azure – Plataforma Logística  
### 📚 Módulo 6 - Projeto 3  
### 📅 Abril de 2025


🚀 API desenvolvida com Flask que simula uma cadeia logística de venda de frutas.

📦 O principal objetivo é permitir que os utilizadores façam encomendas personalizadas e recebam um cálculo do impacto ambiental, com base nas frutas selecionadas e no supermercado escolhido.

---


🧾 Funcionalidades da API

✅ Listar frutas disponíveis → /produtos

✅ Listar supermercados disponíveis → /supermercados

✅ Criar uma nova encomenda → /encomendas

✅ Calcular o impacto ambiental de uma encomenda → /impactos

📘 A documentação completa encontra-se no ficheiro swagger.yml, no formato OpenAPI (Swagger).

---

📁 Estrutura do Projeto

```
api-azure/
├── app/
│   ├── api_routes.py         # Rotas da API
│   ├── init.py               # Inicialização da app
│   ├── logic/                # Lógica de negócio (frutas, encomendas, etc.)
│   └── utils/                # Utilitários e carregamento de dados
├── run.py                    # Ponto de entrada da aplicação
├── requirements.txt          # Dependências do projeto
├── teste_endpoints.py        # Testes com mock
├── teste_postman.py          # Testes com dados do Postman
├── .env                      # Variáveis de ambiente
├── Dockerfile                # Dockerfile da aplicação
├── docker-compose.yml        # Orquestração com Docker Compose
├── azure-pipelines.yml       # Pipeline CI/CD (Azure)
├── azure.yml                 # Configuração YAML para o Azure App Service
└── README.md                 # Documentação do projeto
```

---

## 🛠️ Tecnologias Usadas

- **Linguagem**: Python
- **Framework**: Flask
- **Testes**: pytest, unittest.mock, Postman
- **Linting**: flake8
- **CI/CD**: Azure DevOps (YAML pipeline)
- **Containerização**: Docker + Docker Compose
- **Infraestrutura**: VM com agente self-hosted


---


## 🚀 **Como Executar Localmente**

### **Clonar o repositório:**

```bash
git clone https://github.com/sysadmin-mastercruz/Cloud
cd api-azure
```

### **Criar e ativar ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # (Windows: .\venv\Scripts\activate)
```

### **Instalar dependências:**

```bash
pip install -r requirements.txt
```

### **Iniciar a aplicação Flask:**

```bash
python run.py
```

### **Aceder à API:**

```bash
http://localhost:5000
Ou em produção: http://<IP_DA_VM>:5000
```

---

## 🧪 **Testes Automatizados**

A API foi validada com três abordagens:

- ✔️ **Testes unitários** com pytest
- ✔️ **Testes de integração** com Postman (`teste_postman.py`)
- ✔️ **Testes simulados** com mock (`teste_endpoints.py`) – permite testar respostas sem ligação ativa ao servidor

---

## 🔁 **CI/CD com Azure DevOps**

Este guia explica os componentes e configurações essenciais para correr uma pipeline no Azure DevOps.

---

## 📁 Repositório de Código

O ficheiro YAML da pipeline deve estar num repositório de código.  
Neste caso, o repositório utilizado é o **GitHub**.

---

## 📦 Projeto no Azure DevOps

Foi criado um projeto no Azure DevOps onde a pipeline será executada.  
Este projeto pode contem:

- Pipelines
- Repositórios
- Artefactos

---

## 🔐 Permissões Necessárias

A conta que configura a pipeline precisa de:

- Permissões de leitura no repositório
- Permissões para criar/editar pipelines
- Permissões para aceder ao **Agent Pool** (ex: ao usar um *self-hosted agent*)

---

## 🛠️ Pipeline Criada

A pipeline utiliza um ficheiro YAML (por exemplo: `azure-pipelines.yml`) que define os passos a executar automaticamente:

- Instalação de dependências e ferramentas (`flake8`, `pytest`)
- Validação do código com `flake8`
- Testes simulados com `mock`
- Testes unitários com `pytest`
- Construção da imagem Docker


## Executar a imagem Docker criada através da pipeline
```bash
docker images
docker ps -a
docker run -d --name api-projeto-test meuacrprojeto/api-projeto:v1
```


---

## 👷 Agente de Build (Agent)

A pipeline precisa de um agente para correr os jobs definidos:

- **Self-hosted agent**: Instalado e configurado manualmente (ex: `selfhostedagent`)
  - Corre numa VM sob controlo total do utilizador

---

## 🧰 Agent Pool

A pipeline deve estar associada a um **Agent Pool**.  
Ao usar um agente *self-hosted*, é necessário:

- Criar o Agent Pool
- Associá-lo à pipeline

```bash
mkdir myagent && cd myagent  #criar diretório para o agent

curl -O https://vstsagentpackage.azureedge.net/agent/4.254.0/vsts-agent-linux-x64-4.254.0.tar.gz  # download dos ficheiros para instalar o agent

tar zxvf vsts-agent-linux-x64-4.254.0.tar.gz # desencriptar os ficheiros

./config.sh  # script de configuração da pool e nome do agente

./run.py  # script que coloca o agente em execução
```


---

## ⏱️ Triggers (Opcional mas útil)

Define *triggers* no ficheiro YAML para correr a pipeline automaticamente quando há alterações no repositório (main e pr):

### 🔁 *Triggers no ficheiro YAML*

```yaml
trigger:
- main
- pr

pool:
  name: selfhostedagent

variables:
  IMAGE_NAME: api-projeto
  IMAGE_TAG: v1
  REGISTRY_NAME: meuacrprojeto
  DOCKERFILE_PATH: Dockerfile
  variables:
  AZURE_STORAGE_CONNECTION_STRING: 'DefaultEndpointsProtocol=https;AccountName=meuarmazenamento;AccountKey=XXXXX;EndpointSuffix=core.windows.net'


steps:
- script: |
    echo "Versão do Python:"
    python3 --version

    echo "Instalar dependências e ferramentas..."
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install flake8
    pip install pytest
  displayName: 'Instalar dependências, flake8 e pytest'

- script: |
    echo "Testar estilo de código com flake8..."
    flake8 app/
  displayName: 'Testar linting com flake8 (pode falhar mas continua)'
  continueOnError: true

- script: |
    echo "Executar testes funcionais simulados com mock..."
    python3 teste_endpoints.py
  displayName: 'Testes funcionais simulados com servidor mockado'

- script: |
    echo "Executar testes unitários com pytest..."
    pytest || echo "Sem testes pytest definidos."
  displayName: 'Testes unitários com pytest'
  continueOnError: true

- task: Docker@2
  displayName: 'Construir imagem Docker'
  inputs:
    command: build
    repository: $(REGISTRY_NAME)/$(IMAGE_NAME)
    dockerfile: $(DOCKERFILE_PATH)
    tags: $(IMAGE_TAG)

```

### 📦 *Dockerfile & Docker Compose*

#### **Dockerfile:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

#### **Construir Docker Image:**

```bash
docker build -t api-azure .
docker run -p 5000:5000 api-azure
```

---

### **Levantar com Docker Compose:**

```bash
docker-compose up --build
```

- A aplicação ficará disponível em: `http://localhost:5000`

- Ou em: http://<IP_DA_VM>:5000


---


## 📘 **Documentação Swagger** (OpenAPI)

A documentação da API está no ficheiro `swagger.yml`, com:

- Exemplos de resposta
- Esquemas de dados (Produto, Supermercado, Encomenda, Impacto)
- Descrição completa dos endpoints
- Compatível com Swagger UI

---

## 📌 **Notas Finais:**

- A API é modular e extensível
- Os dados de impacto ambiental são realistas e simulados
- O ambiente Docker e a pipeline CI/CD garantem portabilidade e integração contínua

**Potencial para expansão com:**

- Autenticação de utilizadores
- Dashboard de impacto ambiental
- Histórico de encomendas


---

## ✍️ **Autores**

- Ricardo Cruz
- Rodrigo Almeida
- José Cardoso
- Rui Maciel


