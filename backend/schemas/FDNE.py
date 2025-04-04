FDNE_SCHEMA = {
    "type": "object",
    "properties": {
        "tabelas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Empresa": {
                        "type": "string",
                        "example": "VENTOS DE SAO JOAQUIM ENERGIAS RENOVAVEIS S.A.",
                    },
                    "CNPJ": {
                        "type": "string",
                        "example": "35.874.355/0001-94",
                    },
                    "DataReferencia": {
                        "type": "string",
                        "example": "31/12/2024",
                    },
                    "Dados": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "LINHA": {
                                    "type": "string",
                                    "example": "FDNE FUNDO DE DESENVOLVIMENTO",
                                },
                                "OPERAÇÃO Nº": {
                                    "type": "string",
                                    "example": "191.101.324",
                                },
                                "SALDO CAPITALIZADO": {
                                    "type": "string",
                                    "example": "214.594.362,59",
                                },
                                "JUROS": {
                                    "type": "string",
                                    "example": "7.171.595,78",
                                },
                                "SALDO DEVEDOR": {
                                    "type": "string",
                                    "example": "221.765.958,37",
                                },
                            },
                            "required": [
                                "LINHA",
                                "OPERAÇÃO Nº",
                                "SALDO CAPITALIZADO",
                                "JUROS",
                                "SALDO DEVEDOR",
                            ],
                        },
                    },
                    "Total": {
                        "type": "string",
                        "example": "221.765.958,37",
                    },
                },
                "required": ["Empresa", "CNPJ", "DataReferencia", "Dados", "Total"],
            },
        }
    },
    "required": ["tabelas"],
}
