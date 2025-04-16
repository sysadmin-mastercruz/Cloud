class Produto:
    def __init__(
        self,
        nome,
        consumo_agua_unidade,
        emissao_co2,
        pais_origem,
        distancia_portugal,
        transporte,
        combustivel_por_km,
        emissao_co2_por_km
    ):
        self.nome = nome
        self.pais_origem = pais_origem
        self.distancia_portugal = distancia_portugal
        self.transporte = transporte
        self.combustivel_por_km = combustivel_por_km
        self.emissao_co2_por_km = emissao_co2_por_km
        self.impacto = {
            "consumo_agua_unidade": consumo_agua_unidade,
            "emissao_co2": emissao_co2
        }

    def to_dict(self):
        return {
            "nome": self.nome,
            "pais_origem": self.pais_origem,
            "distancia": self.distancia_portugal,
            "transporte": self.transporte,
            "combustivel_por_km": self.combustivel_por_km,
            "emissao_co2_por_km": self.emissao_co2_por_km,
            "impacto": self.impacto
        }