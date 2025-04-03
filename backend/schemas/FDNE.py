FDNE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "Empresa": {"type": "string"},
            "CNPJ": {"type": "string"},
            "DataReferencia": {"type": "string"},
            "Dados": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "LINHA": {"type": "string"},
                        "OPERAÇÃO Nº": {"type": "string"},
                        "SALDO CAPITALIZADO": {"type": "string"},
                        "JUROS": {"type": "string"},
                        "SALDO DEVEDOR": {"type": "string"},
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
            "Total": {"type": "string"},
        },
        "required": ["Empresa", "CNPJ", "DataReferencia", "Dados", "Total"],
    },
}
