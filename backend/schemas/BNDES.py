BNDES_SCHEMA = {
    "type": "object",
    "properties": {
        "razao_social": {"type": "string"},
        "cnpj": {"type": "string"},
        "subcredito_financeiro": {"type": "string"},
        "sistema": {"type": "string"},
        "unidade_monetaria": {"type": "string"},
        "identificador": {"type": "string"},
        "data_emissao": {"type": "string"},
        "pagina": {"type": "string"},
        "detalhes": {
            "type": "object",
            "properties": {
                "modalidade_juros": {"type": "string"},
                "tipo_amortizacao": {"type": "string"},
                "data_contratacao": {"type": "string"},
            },
        },
        "custo": {
            "type": "object",
            "properties": {
                "custo_financeiro": {"type": "string"},
                "taxa_bndes": {"type": "string"},
                "taxa_agente": {"type": "string"},
                "custo_adicional": {"type": "string"},
            },
        },
        "carencia": {
            "type": "object",
            "properties": {
                "prazo": {"type": "string"},
                "periodicidade": {"type": "string"},
                "inicio": {"type": "string"},
                "fim": {"type": "string"},
            },
        },
        "amortizacao": {
            "type": "object",
            "properties": {
                "prazo": {"type": "string"},
                "periodicidade": {"type": "string"},
                "inicio": {"type": "string"},
                "fim": {"type": "string"},
            },
        },
        "saldos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "data": {"type": "string"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "saldo": {"type": "string"},
                                "valor": {"type": "string"},
                            },
                            "required": ["saldo", "valor"],
                        },
                    },
                },
                "required": ["data", "items"],
            },
        },
    },
    "required": ["razao_social", "subcredito_financeiro", "identificador", "saldos"],
}
