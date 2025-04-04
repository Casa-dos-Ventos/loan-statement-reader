from .BNB import BNB_SCHEMA
from .BNDES import BNDES_SCHEMA
from .FDNE import FDNE_SCHEMA
from .classifier import CLASSIFIER_SCHEMA

SCHEMAS = {
    "BNB": BNB_SCHEMA,
    "BNDES": BNDES_SCHEMA,
    "FDNE": FDNE_SCHEMA,
    "classifier": CLASSIFIER_SCHEMA,
}

LIST_KEYS = {
    "BNDES": ["saldos", "saldos.items"],
    "BNB": ["transacoes"],
    "FDNE": ["tabelas", "tabelas.Dados"],
}
