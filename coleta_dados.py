"""Coleta e tratamento de cotacoes financeiras com yfinance."""

from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd
import yfinance as yf

from config import ATIVOS


COLUNAS_RELATORIO = [
    "Ativo",
    "Ticker",
    "Moeda",
    "Preco Atual",
    "Variacao Diaria (%)",
    "Maxima",
    "Minima",
    "Volume",
    "Ultima Atualizacao",
]


def _obter_moeda(ticker: yf.Ticker, simbolo: str) -> str:
    """Tenta identificar a moeda sem impedir a coleta em caso de falha."""
    try:
        moeda = ticker.fast_info.get("currency")
        if moeda:
            return str(moeda)
    except Exception:
        pass

    if simbolo in {"BRL=X", "EURBRL=X", "^BVSP"} or simbolo.endswith(".SA"):
        return "BRL"
    return "USD"


def _coletar_ativo(simbolo: str, nome: str) -> dict[str, object]:
    """Coleta os ultimos pregoes e calcula os indicadores do ativo."""
    ticker = yf.Ticker(simbolo)
    historico = ticker.history(
        period="7d",
        interval="1d",
        auto_adjust=False,
        actions=False,
    )

    if historico.empty:
        raise ValueError("nenhuma cotacao retornada")

    historico = historico.dropna(subset=["Close"])
    if historico.empty:
        raise ValueError("historico sem precos de fechamento")

    ultimo = historico.iloc[-1]
    preco_atual = float(ultimo["Close"])
    fechamento_anterior = (
        float(historico.iloc[-2]["Close"]) if len(historico) > 1 else preco_atual
    )
    variacao = (
        ((preco_atual / fechamento_anterior) - 1) * 100
        if fechamento_anterior
        else 0.0
    )

    data_cotacao = historico.index[-1]
    if hasattr(data_cotacao, "to_pydatetime"):
        data_cotacao = data_cotacao.to_pydatetime()
    if not isinstance(data_cotacao, datetime):
        data_cotacao = datetime.now()

    volume = ultimo.get("Volume")
    volume_tratado = int(volume) if pd.notna(volume) else None

    return {
        "Ativo": nome,
        "Ticker": simbolo,
        "Moeda": _obter_moeda(ticker, simbolo),
        "Preco Atual": preco_atual,
        "Variacao Diaria (%)": variacao,
        "Maxima": float(ultimo["High"]),
        "Minima": float(ultimo["Low"]),
        "Volume": volume_tratado,
        "Ultima Atualizacao": data_cotacao.replace(tzinfo=None),
    }


def coletar_dados(
    ativos: dict[str, str] | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    """
    Coleta todos os ativos configurados.

    Retorna o DataFrame e uma lista de avisos. Uma falha isolada nao cancela
    o relatorio dos demais ativos.
    """
    ativos = ativos or ATIVOS
    registros: list[dict[str, object]] = []
    avisos: list[str] = []

    for simbolo, nome in ativos.items():
        try:
            registros.append(_coletar_ativo(simbolo, nome))
            logging.info("Cotacao coletada: %s", simbolo)
        except Exception as erro:
            mensagem = f"{nome} ({simbolo}): {erro}"
            avisos.append(mensagem)
            logging.warning("Falha na coleta de %s", mensagem)

    if not registros:
        raise RuntimeError(
            "Nao foi possivel coletar nenhum ativo. Verifique a conexao "
            "com a internet e tente novamente."
        )

    dataframe = pd.DataFrame(registros, columns=COLUNAS_RELATORIO)
    dataframe = dataframe.sort_values("Ativo").reset_index(drop=True)
    return dataframe, avisos
