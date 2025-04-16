class Supermercado:
    def __init__(self, nome, distancia_loja, combustivel_loja, co2_loja):
        self.nome = nome
        self.distancia_loja = distancia_loja
        self.combustivel_loja = combustivel_loja
        self.co2_loja = co2_loja

    def calcular_impacto(self, frutas):
        impacto = {
            "consumo_agua": 0.0,
            "emissao_co2": 0.0,
            "consumo_combustivel": 0.0,
            "poluicao": 0.0
        }

        fatores_transporte = {
            "avião": {"combustivel_por_km": 0.75, "co2_por_km": 0.55},
            "navio": {"combustivel_por_km": 0.1, "co2_por_km": 0.15},
            "camião": {"combustivel_por_km": 0.35, "co2_por_km": 0.2},
            "local": {"combustivel_por_km": 0.05, "co2_por_km": 0.025}
        }

        for fruta, quantidade in frutas.items():
            impacto["consumo_agua"] += quantidade * fruta.impacto["consumo_agua_unidade"]
            impacto["emissao_co2"] += quantidade * fruta.impacto["emissao_co2"]

            transporte = fruta.transporte
            if transporte in fatores_transporte:
                fator = fatores_transporte[transporte]
                impacto["consumo_combustivel"] += (quantidade * fator["combustivel_por_km"] * fruta.distancia_portugal) / 100
                impacto["poluicao"] += (quantidade * fator["co2_por_km"] * fruta.distancia_portugal) / 100

        if self.nome == "Pingo Doce":
            impacto["consumo_agua"] *= 0.85
            impacto["emissao_co2"] *= 1.10
            impacto["consumo_combustivel"] *= 1.08
            impacto["poluicao"] *= 1.06
        elif self.nome == "Continente":
            impacto["consumo_agua"] *= 0.95
            impacto["emissao_co2"] *= 0.85
            impacto["consumo_combustivel"] *= 1.30
            impacto["poluicao"] *= 0.88
        elif self.nome == "Aldi":
            impacto["consumo_agua"] *= 1.00
            impacto["emissao_co2"] *= 0.92
            impacto["consumo_combustivel"] *= 0.84
            impacto["poluicao"] *= 0.97
        elif self.nome == "Lidl":
            impacto["consumo_agua"] *= 1.10
            impacto["emissao_co2"] *= 1.07
            impacto["consumo_combustivel"] *= 1.05
            impacto["poluicao"] *= 0.83
        elif self.nome == "Intermarché":
            impacto["consumo_agua"] *= 1.20
            impacto["emissao_co2"] *= 0.80
            impacto["consumo_combustivel"] *= 1.15
            impacto["poluicao"] *= 1.12

        return impacto

    def to_dict(self):
        return {
            "nome": self.nome,
            "distancia": self.distancia_loja,
            "combustivel": self.combustivel_loja,
            "emissao_co2": self.co2_loja
        }