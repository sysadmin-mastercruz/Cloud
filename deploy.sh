#!/bin/bash

# Parâmetros
RESOURCE_GROUP="projeto-api-rg"
ACR_NAME="meuacrprojeto"
APP_NAME="pi-encomendas-webapp"
PLAN_NAME="api-plan"
IMAGE_NAME="api-projeto"
IMAGE_TAG="v1"
LOCATION="westeurope"

# Função para verificar se o comando anterior falhou devido a MFA ou outros erros
verificar_erro() {
    if [[ $? -ne 0 ]]; then
        echo "❌ ERRO: O comando anterior falhou. Verifica a mensagem acima."
        echo "👉 SUGESTÃO: Confirma se fizeste login corretamente com MFA."
        echo "⚠️ A execução do script foi interrompida."
        exit 1
    fi
}

# Login no Azure
echo "🔐 A fazer login no Azure..."
az account show &>/dev/null
if [[ $? -ne 0 ]]; then
    az login --use-device-code
    verificar_erro
else
    echo "✅ Já estás autenticado no Azure."
fi

# Verificar subscrições disponíveis
SUB_COUNT=$(az account list --query "length([?state=='Enabled'])")
if [[ "$SUB_COUNT" -eq 0 ]]; then
    echo "🚫 Não foram encontradas subscrições ativas."
    echo "👉 Verifica se tens uma subscrição associada à tua conta no portal do Azure."
    exit 1
fi

# Criar Resource Group
echo "📦 A criar resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION
verificar_erro

# Criar Azure Container Registry
echo "📦 A criar Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
verificar_erro

# Ativar modo admin no ACR (necessário para obter credenciais)
echo "🔧 A ativar o modo admin no ACR..."
az acr update -n $ACR_NAME --admin-enabled true
verificar_erro

# Login no ACR
echo "🔐 A fazer login no ACR..."
az acr login --name $ACR_NAME
verificar_erro

# Construir imagem Docker
echo "🐳 A construir imagem Docker..."
docker build -t $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG .
verificar_erro

# Push da imagem para o ACR
echo "📤 A fazer push da imagem para o ACR..."
docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG
verificar_erro

# Criar App Service Plan
echo "☁️ A criar App Service Plan..."
az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --is-linux --sku B1
verificar_erro

# Criar Web App for Containers
echo "🌐 A criar Web App com container..."
az webapp create --resource-group $RESOURCE_GROUP \
                 --plan $PLAN_NAME \
                 --name $APP_NAME \
                 --deployment-container-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG
verificar_erro

# Obter credenciais do ACR
echo "🔑 A obter credenciais do ACR..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

if [[ -z "$ACR_PASSWORD" ]]; then
  echo "❌ ERRO: A password do ACR veio vazia. Verifica se o modo admin está ativo com:"
  echo "   az acr update -n $ACR_NAME --admin-enabled true"
  exit 1
fi

# Configurar container no Web App (novas opções Azure CLI)
echo "⚙️ A configurar container no Web App..."
az webapp config container set --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --container-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --container-registry-url https://$ACR_NAME.azurecr.io \
  --container-registry-user $ACR_USERNAME \
  --container-registry-password $ACR_PASSWORD
verificar_erro

echo "✅ Deploy completo! A tua app está disponível em:"
echo "   �� https://$APP_NAME.azurewebsites.net/"

