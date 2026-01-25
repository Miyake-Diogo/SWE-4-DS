---
titulo: "Aula 08 – Parte 04: Reorganização de Projeto DS - Estrutura de Pastas e Boas Práticas"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "Aula 08 - Parte 03 concluída"
  - "Git e organização básica de projeto"
tags: ["estrutura-projeto", "cookiecutter", "organizacao", "ds", "fastapi"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos falar sobre **organização profissional de projetos de Data Science**.

Depois de refatorar código, o próximo passo natural é organizar a estrutura do projeto para facilitar colaboração e transição para produção. Vamos usar o **Cookiecutter Data Science** como referência e encaixar nossa API FastAPI dentro dessa estrutura, mantendo o modelo da pasta Consumer_API bem localizado.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: O projeto cresceu e virou um conjunto de scripts soltos, dados espalhados e notebooks sem padrão.

**Agitação**: Ninguém sabe onde colocar novos módulos, e o time perde tempo procurando arquivos. O deploy da API fica confuso.

**Solução**: Estruturar o projeto com uma organização clara de pastas (dados, notebooks, src, artefatos). Isso facilita colaboração, versionamento e produção, mantendo nossa API evoluindo de forma incremental.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Explicar** a estrutura Cookiecutter Data Science
2. **Mapear** scripts e notebooks para pastas corretas
3. **Integrar** a API FastAPI dentro da estrutura
4. **Descrever** benefícios da organização para produção

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- Projeto com API FastAPI funcionando

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar testes
uv run pytest -q
```

**Checklist de setup:**
- [ ] API funcionando
- [ ] Testes rodando
- [ ] Backup/commit antes de reorganizar

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual (simplificado):
```
swe4ds-credit-api/
├── src/
├── tests/
├── Consumer_API/
└── notebooks/
```

**O que será alterado nesta parte:**
- Criar estrutura baseada em Cookiecutter
- Mover scripts e notebooks para locais adequados

# 6. Passo a passo (comandos + código)

## Passo 1: Estrutura de referência (Excalidraw: Slide 6)

**Intenção:** Conhecer o template Cookiecutter DS.

Estrutura base:

```
project/
├── data/
│   ├── raw/
│   ├── processed/
├── notebooks/
├── src/
├── models/
├── reports/
└── README.md
```

**CHECKPOINT:** Entenda as pastas principais e seus propósitos.

---

## Passo 2: Criar estrutura no projeto

**Intenção:** Preparar diretórios necessários.

```bash
mkdir data
mkdir data\raw
mkdir data\processed
mkdir models
mkdir reports
```

**CHECKPOINT:** Pastas criadas na raiz do projeto.

---

## Passo 3: Migrar scripts e notebooks (Excalidraw: Slide 7)

**Intenção:** Colocar cada artefato no lugar correto.

Diff lógico de movimentação:

```diff
- notebooks/analysis_credit.ipynb
+ notebooks/analysis_credit.ipynb   # permanece em notebooks

- Consumer_API/model.pkl
+ models/model.pkl                  # mover artefatos de modelo
```

Movimentação prática (exemplo):

```bash
Move-Item Consumer_API\model.pkl models\model.pkl
```

**CHECKPOINT:** Notebooks em `notebooks/`, modelos em `models/`.

---

## Passo 4: Atualizar caminhos no código

**Intenção:** Ajustar referências para nova estrutura.

Exemplo de ajuste em `src/services/model_service.py`:

```diff
- MODEL_PATH = "Consumer_API/model.pkl"
+ MODEL_PATH = "models/model.pkl"
```

Abra e edite o arquivo:

```bash
code src/services/model_service.py
```

**CHECKPOINT:** API continua carregando o modelo corretamente.

---

## Passo 5: Onde ficam pipelines e features (Excalidraw: Slide 7)

**Intenção:** Definir destino de código de pré-processamento.

Sugestão:
```
src/
├── services/
│   ├── preprocessing.py
│   └── model_service.py
```

**CHECKPOINT:** Código de domínio fica em `src/services`.

---

## Passo 6: Benefícios e próximos passos (Excalidraw: Slide 8)

**Intenção:** Conectar organização com produção.

Benefícios:
- Colaboração facilitada
- Versionamento claro
- Integração com pipelines (Airflow/Prefect) mais simples

**CHECKPOINT:** Estrutura pronta para produção e escalabilidade.

---

## Passo 7: Validar tudo na prática

**Intenção:** Garantir que a reorganização não quebrou a API.

```bash
uv run pytest -q
uv run uvicorn src.main:app --reload
```

**CHECKPOINT:** `/health` responde e testes passam.

# 7. Testes rápidos e validação

```bash
# Rodar testes após mover arquivos
uv run pytest -q

# Subir API para validar modelo
uv run uvicorn src.main:app --reload
```

Exemplo de resposta:
```json
{"status": "ok"}
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Estrutura padronizada**: acelera onboarding. Trade-off: reorganização inicial.
2. **Separar dados e código**: facilita versionamento. Trade-off: mais disciplina.
3. **Caminhos configuráveis**: evita hardcode. Trade-off: mais configuração.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| API não encontra modelo | Caminho antigo | Atualizar `MODEL_PATH` |
| Notebook quebrou | Caminho relativo mudou | Ajustar importações |
| Dados misturados com código | Falta de padrão | Usar `data/raw` e `data/processed` |

# 10. Exercícios (básico e avançado)

**Básico 1:** Criar pasta `reports/` e gerar um relatório simples.
- Concluído com sucesso: arquivo salvo em `reports/`.

**Básico 2:** Mover um script solto para `src/services/`.
- Concluído com sucesso: importações funcionando.

**Avançado:** Definir uma estrutura de pipeline com Airflow/Prefect (descrição, não implementação).
- Concluído com sucesso: diagrama simples do fluxo.

# 11. Resultados e Lições

**Resultados (como medir):**
- Tempo para encontrar arquivos (observação do time)
- Redução de erros de caminho
- Facilidade de onboarding (feedback do time)

**Lições:**
- Estrutura de projeto é parte da engenharia
- Organização reduz bugs ocultos
- Facilita integração com produção

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu a reorganizar um projeto de Data Science com uma estrutura profissional, integrando a API FastAPI e o modelo em um padrão claro.

Com isso encerramos o módulo de refatoração. A partir daqui, você tem base sólida para escalar o projeto e integrar com pipelines de orquestração como Airflow ou Prefect.
