BNB_SCHEMA = {
    "type": "object",
    "properties": {
        "nome_banco": {"type": "string"},
        "titulo_documento": {"type": "string"},
        "agencia": {"type": "string"},
        "page_info": {
            "type": "object",
            "properties": {
                "current_page": {"type": "string"},
                "total_pages": {"type": "string"},
            },
        },
        "report_datetime": {
            "type": "object",
            "properties": {"data": {"type": "string"}, "hora": {"type": "string"}},
        },
        "info_cliente": {
            "type": "object",
            "properties": {"nome": {"type": "string"}, "endereço": {"type": "string"}},
            "required": ["nome", "endereço"],
        },
        "dados_operacao": {
            "type": "object",
            "properties": {
                "periodo": {
                    "type": "object",
                    "properties": {
                        "data_inicio": {"type": "string"},
                        "data_fim": {"type": "string"},
                    },
                },
                "area_de_credito": {"type": "string"},
                "codigo_da_operacao": {"type": "string"},
                "valor_da_operacao": {"type": "string"},
                "data_do_contrato": {"type": "string"},
                "vencimento_final": {"type": "string"},
                "moeda_da_operacao": {"type": "string"},
                "moeda_indexadora": {"type": "string"},
                "programa": {"type": "string"},
            },
            "required": ["programa"],
        },
        "saldo_inicial": {
            "type": "object",
            "properties": {
                "saldo_normal": {"type": "string"},
                "saldo_atraso": {"type": "string"},
                "saldo_prejuizo": {"type": "string"},
            },
        },
        "transacoes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "data_lancamento": {"type": "string"},
                    "data_valorizacao": {"type": "string"},
                    "d/c": {"type": "string"},
                    "historico": {"type": "string"},
                    "valor_normal": {"type": "string"},
                    "saldo_normal": {"type": "string"},
                    "valor_atraso": {"type": "string"},
                    "saldo_atraso": {"type": "string"},
                    "valor_prejuizo": {"type": "string"},
                    "saldo_prejuizo": {"type": "string"},
                },
            },
            "required": [
                "data_lancamento",
                "data_valorizacao",
                "d/c",
                "historico",
                "valor_normal",
                "saldo_normal",
            ],
        },
        "saldo_final": {
            "type": "object",
            "properties": {
                "principal": {"type": "string"},
                "jus_bas_var": {"type": "string"},
            },
        },
        "totais": {
            "type": "object",
            "properties": {
                "total_cliente_operacao": {
                    "type": "object",
                    "properties": {
                        "valor_normal": {"type": "string"},
                        "valor_atraso": {"type": "string"},
                        "valor_prejuizo": {"type": "string"},
                    },
                },
                "total_cliente_ficha": {
                    "type": "object",
                    "properties": {
                        "valor_normal": {"type": "string"},
                        "valor_atraso": {"type": "string"},
                        "valor_prejuizo": {"type": "string"},
                    },
                },
                "total_geral_pago": {"type": "string"},
            },
        },
        "banco_emissor": {"type": "string"},
    },
    "required": [
        "nome_banco",
        "info_cliente",
        "dados_operacao",
        "transacoes",
        "saldo_final",
        "banco_emissor",
    ],
}
