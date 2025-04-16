#!/bin/bash

# Parâmetros
RESOURCE_GROUP="projeto-api-rg"
ACI_NAME="api-container-instance"
ACI_LOCATION="westeurope"
ACR_NAME="meuacrprojeto"
IMAGE_NAME="api-projeto"
IMAGE_TAG="v1"
DNS_LABEL="api-container-demo"  # <-- personaliza se quiseres

# Obter credenciais do ACR
echo "🔑 A obter credenciais do ACR..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Criar container instance
echo "🚀 A criar Azure Container Instance..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $ACI_NAME \
  --image $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --cpu 1 \
  --memory 1 \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports 5000 \
  --dns-name-label $DNS_LABEL \
  --location $ACI_LOCATION \
  --os-type Linux

echo "🌐 A API ficará acessível em:"
echo "👉 http://$DNS_LABEL.$ACI_LOCATION.azurecontainer.io:5000"
