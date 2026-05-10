import json
import os
import logging
import time

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

# ─── Cliente Gemini ───────────────────────────────────────────────────────────
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

OUTPUT_FILE = "output/usuarios_mensagens.json"

# EXTRACT — cria a lista de usuários fictícios

def extract() -> list[dict]:
    """Retorna uma lista de usuários fictícios (substitui a chamada à API)."""
    log.info("[EXTRACT] Carregando usuários fictícios...")

    usuarios = [
        {
            "nome": "Ana Silva",
            "conta": {"saldo": 1250.00, "limite": 500.00},
            "cartao": {"limite": 2000.00, "limite_utilizado": 350.00},
        },
        {
            "nome": "Carlos Mendes",
            "conta": {"saldo": 320.50, "limite": 200.00},
            "cartao": {"limite": 1000.00, "limite_utilizado": 980.00},
        },
        {
            "nome": "Beatriz Costa",
            "conta": {"saldo": 8750.00, "limite": 1000.00},
            "cartao": {"limite": 5000.00, "limite_utilizado": 120.00},
        },
    ]

    log.info(f"[EXTRACT] {len(usuarios)} usuários carregados.")
    return usuarios

# TRANSFORM — Gemini AI gera mensagem personalizada para cada usuário

def gerar_mensagem(usuario: dict) -> str:
    """Chama a API do Gemini e retorna uma mensagem financeira personalizada."""
    nome              = usuario["nome"]
    saldo             = usuario["conta"]["saldo"]
    limite_cartao     = usuario["cartao"]["limite"]
    usado_cartao      = usuario["cartao"]["limite_utilizado"]
    percentual_cartao = (usado_cartao / limite_cartao * 100) if limite_cartao else 0

    prompt = f"""
Você é um assistente financeiro do banco Santander.
Crie uma mensagem curta (máximo 3 frases) e personalizada para o cliente abaixo.
A mensagem deve ser amigável, positiva e dar uma dica financeira relevante com base nos dados.

Cliente: {nome}
Saldo em conta: R$ {saldo:,.2f}
Limite do cartão: R$ {limite_cartao:,.2f}
Limite utilizado: R$ {usado_cartao:,.2f} ({percentual_cartao:.0f}%)

Responda apenas com a mensagem, sem saudação genérica.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
    )

    return response.text.strip()


def transform(usuarios: list[dict]) -> list[dict]:
    """Adiciona uma mensagem personalizada a cada usuário."""
    log.info("[TRANSFORM] Gerando mensagens com Gemini AI...")

    for usuario in usuarios:
        log.info(f"[TRANSFORM] Gerando mensagem para: {usuario['nome']}")
        usuario["mensagem_ia"] = gerar_mensagem(usuario)
        log.info(f"[TRANSFORM] ✓ {usuario['nome']} → {usuario['mensagem_ia'][:60]}...")
        time.sleep(5)

    log.info(f"[TRANSFORM] {len(usuarios)} mensagens geradas.")
    return usuarios

# LOAD — salva o resultado em JSON

def load(usuarios: list[dict]) -> None:
    """Salva a lista de usuários com mensagens em um arquivo JSON."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

    log.info(f"[LOAD] Resultado salvo em: {OUTPUT_FILE}")

# PIPELINE

def run_pipeline():
    log.info("=" * 55)
    log.info("ETL — Santander Dev Week (Alternativa 1)")
    log.info("=" * 55)

    usuarios = extract()
    usuarios = transform(usuarios)
    load(usuarios)

    log.info("=" * 55)
    log.info("PIPELINE CONCLUÍDO ✓")
    log.info("=" * 55)


if __name__ == "__main__":
    run_pipeline()