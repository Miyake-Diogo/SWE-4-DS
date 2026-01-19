---
titulo: "Aula 07 – Parte 02: Estratégias de Deploy - Batch vs. Tempo Real, Blue-Green e Canary"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "FastAPI configurado"
  - "CI básico configurado"
tags: ["deploy", "batch", "real-time", "blue-green", "canary"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos falar sobre **estratégias de deploy** para projetos de Data Science.

Você já tem uma API FastAPI funcionando. Agora precisamos decidir **como** colocar esse modelo em produção. É um job agendado em batch? É uma API de inferência em tempo real? E como atualizar versões sem derrubar o serviço?

Vamos explorar estratégias clássicas como **Blue-Green** e **Canary Release**, além de comparar deploy batch vs. tempo real. Tudo conectado com a nossa API que consome o modelo da pasta Consumer_API.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você treina um novo modelo e sobe direto para produção. Alguns usuários começam a ter respostas inconsistentes.

**Agitação**: Não dá para saber se o problema é o modelo novo ou o tráfego. Você precisa fazer rollback rápido, mas não há estratégia definida.

**Solução**: Planejar o deploy. Usar batch quando o problema permite processamento em lotes, tempo real quando latência é crítica, e estratégias como Blue-Green e Canary para atualizar versões com segurança. Tudo isso integrado à evolução incremental da API.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Distinguir** deploy batch e tempo real
2. **Explicar** Blue-Green e Canary Release
3. **Simular** duas versões da API em paralelo
4. **Planejar** deploy seguro para a API de ML

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- FastAPI em execução
- Docker opcional (para simular múltiplas versões)

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar API local
uv run uvicorn src.main:app --reload
```

**Checklist de setup:**
- [ ] API rodando localmente
- [ ] Endpoint /health funcionando
- [ ] Acesso ao modelo em Consumer_API

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual esperado:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   │   └── predict.py
│   └── services/
├── Consumer_API/        # Modelo e artefatos
└── tests/
```

**O que será alterado nesta parte:**
- Adição de um script batch
- Simulação de duas versões da API

# 6. Passo a passo (comandos + código)

## Passo 1: Comparar batch vs tempo real (Excalidraw: Slide 2)

**Intenção:** Entender quando cada modo é mais adequado.

### Exemplo de script batch

Arquivo: `scripts/batch_predict.py` (novo)

```python
"""Executa predições em lote a partir de um CSV."""

import pandas as pd
from src.services.model_service import load_model, predict

MODEL = load_model()


def run_batch(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    preds = predict(MODEL, df)
    df["prediction"] = preds
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    run_batch("data/input.csv", "data/output.csv")
```

**CHECKPOINT:** Ao rodar o script, você deve ver o arquivo `data/output.csv` criado.

```bash
uv run python scripts/batch_predict.py
```

---

## Passo 2: API em tempo real

**Intenção:** Reforçar quando latência baixa é necessária.

Arquivo: `src/routes/predict.py` (trecho existente)

```python
from fastapi import APIRouter
from pydantic import BaseModel
from src.services.model_service import load_model, predict_one

router = APIRouter()
MODEL = load_model()

class PredictRequest(BaseModel):
    age: int
    limit: float
    history: str

@router.post("/predict")
def predict_endpoint(payload: PredictRequest):
    result = predict_one(MODEL, payload.model_dump())
    return {"prediction": result}
```

**CHECKPOINT:** Requisição POST em `/predict` retorna JSON com predição.

---

## Passo 3: Estratégia Blue-Green (Excalidraw: Slide 2)

**Intenção:** Simular duas versões rodando lado a lado.

### Simulação com portas diferentes

```bash
# Versão blue
uv run uvicorn src.main:app --port 8000

# Versão green (nova)
uv run uvicorn src.main:app --port 8001
```

Troque o tráfego manualmente apontando o cliente para a porta 8001.

**CHECKPOINT:** Ambas versões respondem em portas diferentes.

---

## Passo 4: Estratégia Canary

**Intenção:** Direcionar só parte do tráfego para a versão nova.

Simulação simples em cliente:

```python
import random
import requests

url_blue = "http://localhost:8000/predict"
url_green = "http://localhost:8001/predict"

payload = {"age": 30, "limit": 2000, "history": "good"}

# 10% do tráfego vai para green
if random.random() < 0.1:
    r = requests.post(url_green, json=payload)
else:
    r = requests.post(url_blue, json=payload)

print(r.json())
```

**CHECKPOINT:** A maior parte das requisições vai para blue, algumas para green.

# 7. Testes rápidos e validação

```bash
# Testar endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"age\": 30, \"limit\": 2000, \"history\": \"good\"}"
```

Resposta esperada (exemplo):
```json
{"prediction": "approved"}
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Planejamento de deploy**: evita downtime. Trade-off: mais etapas no release.
2. **Separar batch e real-time**: performance e custo equilibrados. Trade-off: dois fluxos de execução.
3. **Estratégias de rollout**: Blue-Green e Canary reduzem risco. Trade-off: duplicar infraestrutura temporariamente.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Porta já em uso | Outra instância rodando | Trocar `--port` |
| Batch lento | CSV muito grande | Processar em chunks |
| Canary inconsistente | Modelos diferentes demais | Ajustar testes A/B |
| API responde 500 | Modelo não carregou | Validar caminho do modelo |

# 10. Exercícios (básico e avançado)

**Básico 1:** Criar um script que roteia 20% do tráfego para a versão green.
- Concluído com sucesso: script envia requisições com distribuição aproximada.

**Básico 2:** Comparar outputs do batch e da API para o mesmo input.
- Concluído com sucesso: outputs equivalentes.

**Avançado:** Escrever um mini relatório com critérios para escolher batch ou real-time no seu projeto.
- Concluído com sucesso: relatório com critérios claros (latência, custo, volume).

# 11. Resultados e Lições

**Resultados (como medir):**
- Latência média (medir com `time` ou logs)
- Taxa de erro (contar respostas não-2xx)
- Diferença entre versões (comparar outputs)

**Lições:**
- Batch é ótimo para volume, real-time para latência
- Blue-Green reduz risco de downtime
- Canary permite detectar problemas cedo

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu a escolher entre deploy batch e tempo real e a aplicar estratégias Blue-Green e Canary para atualizar sua API de ML com segurança.

Na próxima parte, vamos mergulhar em **observabilidade e monitoramento**: métricas de sistema, métricas de aplicação e métricas específicas de modelos como drift e acurácia. Você vai entender como manter a qualidade do modelo em produção.
