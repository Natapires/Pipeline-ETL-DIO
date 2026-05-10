# 📊 Formação em Engenharia de Dados — Python, ETL, Cloud & Machine Learning

Repositório de projetos desenvolvidos durante a **Formação em Engenharia de Dados**, uma trilha completa e alinhada ao mercado que cobre desde os fundamentos de Python e bancos de dados até Machine Learning e integração de LLMs em pipelines de dados.

> **61 horas** de aulas aplicadas · **Mentorias ao vivo**

---

## 🎯 Sobre a Formação

A trilha foi desenhada para quem quer atuar com **Engenharia de Dados** no mercado real. O foco está em aplicar cada conceito em projetos que simulam desafios reais de empresas — do tratamento e transformação de dados até a geração de insights que orientam decisões de negócio.

A formação cobre:

- Fundamentos sólidos de **Python** para dados
- **Bancos de dados** relacionais e não-relacionais
- Fundamentos de **ETL** e pipelines de dados
- **Cloud** para engenharia de dados
- **Machine Learning** aplicado a dados reais
- **IA Generativa** e integração de **LLMs** em pipelines

---

## 🗂️ Projetos do Portfólio

### 📁 Pipeline ETL com Python e IA Generativa

Pipeline ETL completo que extrai dados de usuários, aplica transformações com Pandas e utiliza a **API da Anthropic (Claude AI)** para gerar mensagens financeiras personalizadas via LLM.

**Conceitos aplicados:** ETL · Pandas · Integração de LLMs · JSON · CSV

```
etl_alternativa1.py   → ETL com lista Python + Claude AI
etl_alternativa2.py   → ETL com CSV + Claude AI
usuarios.csv          → Dados de entrada
output/               → Resultados: .csv e .json
```

**Fluxo:**
```
[Extract]            [Transform]                  [Load]
Lista Python   →   Limpeza + Validação   →   output/
ou CSV             Geração de msg (LLM)       ├── .csv
                   Timestamp                  └── .json
```

---

## 🧭 Trilha de Conhecimento

```
Fundamentos          Intermediário            Avançado
──────────────       ──────────────────       ──────────────────────
Python para dados    ETL e Pipelines          Machine Learning
Bancos de Dados      Cloud para Dados         IA Generativa
SQL                  Orquestração             Integração de LLMs
```

---

## 🛠️ Tecnologias da Formação

| Categoria | Tecnologias |
|-----------|-------------|
| Linguagem | Python 3.9+ |
| Dados | Pandas, SQL |
| ETL | Scripts Python, Pipelines |
| Cloud | AWS / GCP / Azure |
| IA & LLMs | Anthropic Claude, IA Generativa |
| Versionamento | Git, GitHub |

---

## ▶️ Como executar o Projeto 1 (ETL)

### Pré-requisitos

- Python 3.9+
- API Key da [Anthropic](https://console.anthropic.com)

### Instalação

```bash
git clone https://github.com/SEU_USUARIO/formacao-engenharia-dados.git
cd formacao-engenharia-dados
pip install anthropic pandas
```

### Configuração da API Key

```bash
# Linux / macOS
export ANTHROPIC_API_KEY="sk-ant-sua-chave-aqui"

# Windows CMD
set ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
```

### Execução

```bash
# Alternativa 1 — dados em lista Python
python etl_alternativa1.py

# Alternativa 2 — leitura de CSV
python etl_alternativa2.py
```

---

## 📄 Exemplo de saída do Pipeline ETL

```json
{
  "nome": "Ana Silva",
  "saldo": 1250.0,
  "limite_cartao": 2000.0,
  "limite_cartao_utilizado": 350.0,
  "mensagem_ia": "Ana, seu cartão está com apenas 17% do limite utilizado — ótima gestão! Que tal aproveitar esse equilíbrio para criar uma reserva de emergência com parte do seu saldo?"
}
```

---

## 📚 Aprendizados da Formação

- Construção de pipelines ETL do zero com Python
- Boas práticas de tratamento e validação de dados
- Integração de LLMs em pipelines de dados reais
- Adaptação de soluções quando fontes de dados falham
- Geração de outputs estruturados para consumo por sistemas e pessoas
- Versionamento de projetos de dados com Git e GitHub

---

## 🎓 Sobre

Formação desenvolvida pela **DIO (Digital Innovation One)** com **61h de conteúdo aplicado**, mentorias ao vivo e projetos que preparam para os desafios reais da Engenharia de Dados.

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar e modificar.