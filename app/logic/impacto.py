def exibir_resumo_impacto(impactos_mercados):
    # Encontrar o supermercado com melhor impacto para cada parâmetro
    melhor_agua = min(impactos_mercados, key=lambda x: impactos_mercados[x]["consumo_agua"])
    melhor_co2 = min(impactos_mercados, key=lambda x: impactos_mercados[x]["emissao_co2"])
    melhor_combustivel = min(impactos_mercados, key=lambda x: impactos_mercados[x]["consumo_combustivel"])
    melhor_poluicao = min(impactos_mercados, key=lambda x: impactos_mercados[x]["poluicao"])

    return {
        "melhor_consumo_agua": melhor_agua,
        "melhor_emissao_co2": melhor_co2,
        "melhor_consumo_combustivel": melhor_combustivel,
        "melhor_poluicao": melhor_poluicao
    }