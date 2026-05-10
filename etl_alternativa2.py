import json
import os
import time
import logging
import pandas as pd

from dotenv import load_dotenv
from google import genai

load_dotenv()

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Configuração ─────────────────────────────────────────────────────────────
INPUT_CSV   = "usuarios.csv"
OUTPUT_JSON = "output/usuarios_mensagens.json"
OUTPUT_CSV  = "output/usuarios_mensagens.csv"

# ─── Cliente Gemini ───────────────────────────────────────────────────────────
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# EXTRACT — lê o CSV

def extract(filepath: str) -> pd.DataFrame:
    """Lê o arquivo CSV e retorna um DataFrame."""
    log.info(f"[EXTRACT] Lendo arquivo: {filepath}")

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filepath}\n"
            "Crie o arquivo 'usuarios.csv' com as colunas: "
            "nome, saldo, limite_conta, limite_cartao, limite_cartao_utilizado"
        )

    df = pd.read_csv(filepath)
    log.info(f"[EXTRACT] {len(df)} usuários carregados. Colunas: {list(df.columns)}")
    return df


# TRANSFORM — Gemini AI gera mensagem para cada linha do DataFrame

def gerar_mensagem(row: pd.Series) -> str:
    """Gera uma mensagem personalizada para um usuário via Gemini AI."""
    percentual = (row["limite_cartao_utilizado"] / row["limite_cartao"] * 100) \
                 if row["limite_cartao"] > 0 else 0

    prompt = f"""
Você é um assistente financeiro do banco Santander.
Crie uma mensagem curta (máximo 3 frases) e personalizada para o cliente abaixo.
A mensagem deve ser amigável, positiva e dar uma dica financeira relevante.

Cliente: {row['nome']}
Saldo em conta: R$ {row['saldo']:,.2f}
Limite do cartão: R$ {row['limite_cartao']:,.2f}
Limite utilizado: R$ {row['limite_cartao_utilizado']:,.2f} ({percentual:.0f}%)

Responda apenas com a mensagem, sem saudação genérica.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
    )
    return response.text.strip()


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpeza e gera mensagens IA para cada usuário."""
    log.info("[TRANSFORM] Iniciando transformações...")

    # Limpeza básica
    df.columns = df.columns.str.strip().str.lower()
    df.dropna(how="all", inplace=True)
    df.drop_duplicates(inplace=True)

    # Garante tipos numéricos
    numeric_cols = ["saldo", "limite_conta", "limite_cartao", "limite_cartao_utilizado"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Gera mensagem para cada usuário
    mensagens = []
    for _, row in df.iterrows():
        log.info(f"[TRANSFORM] Gerando mensagem para: {row['nome']}")
        msg = gerar_mensagem(row)
        mensagens.append(msg)
        log.info(f"[TRANSFORM] ✓ {row['nome']} → {msg[:60]}...")
        time.sleep(5)  # evita estourar cota do free tier

    df["mensagem_ia"] = mensagens
    log.info(f"[TRANSFORM] {len(df)} mensagens geradas.")
    return df


# LOAD — salva CSV e JSON

def load(df: pd.DataFrame) -> None:
    """Salva o resultado em CSV e JSON."""
    os.makedirs("output", exist_ok=True)

    df.to_csv(OUTPUT_CSV, index=False)
    log.info(f"[LOAD] CSV salvo  → {OUTPUT_CSV}")

    records = df.to_dict(orient="records")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    log.info(f"[LOAD] JSON salvo → {OUTPUT_JSON}")


# PIPELINE

def run_pipeline():
    log.info("=" * 55)
    log.info("ETL — TOTVS Engenharia de Dados (Alternativa 2)")
    log.info("=" * 55)

    df = extract(INPUT_CSV)
    df = transform(df)
    load(df)

    log.info("=" * 55)
    log.info("PIPELINE CONCLUÍDO ✓")
    log.info("=" * 55)


if __name__ == "__main__":
    run_pipeline()