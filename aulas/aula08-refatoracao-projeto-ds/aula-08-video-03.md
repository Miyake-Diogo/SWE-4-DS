---
titulo: "Aula 08 – Parte 03: Hands-on - Refatorando um Código de Data Science (Antes e Depois)"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 30
prerequisitos:
  - "Python 3.12+"
  - "Aula 08 - Parte 02 concluída"
  - "Testes automatizados básicos"
tags: ["hands-on", "refatoracao", "fastapi", "tests", "clean-code"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos fazer uma refatoração **na prática**.

Vamos pegar um código de Data Science com problemas típicos: duplicação, funções longas e mistura de responsabilidades. E vamos transformá-lo em um código organizado, testável e pronto para produção, sem alterar o comportamento.

Tudo isso integrado à nossa API FastAPI, que continua consumindo o modelo da pasta Consumer_API.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: O endpoint de predição funciona, mas a lógica de validação e pré-processamento está duplicada em vários lugares.

**Agitação**: Uma pequena mudança no pré-processamento quebra um endpoint, mas não o outro. O time perde confiança na API.

**Solução**: Refatorar passo a passo, extraindo funções reutilizáveis e reorganizando o código em módulos claros. A API continua estável, mas o design melhora drasticamente.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Refatorar** um trecho real de código de DS
2. **Extrair** funções reutilizáveis
3. **Reorganizar** módulos mantendo testes verdes
4. **Comparar** estrutura original e refatorada

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- uv instalado
- Testes configurados

**Setup:**

```bash
.\.venv\Scripts\Activate.ps1
uv run pytest -q
```

**Checklist de setup:**
- [ ] Ambiente virtual ativo
- [ ] Testes passando
- [ ] Git limpo

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual:
```
swe4ds-credit-api/
├── src/
│   ├── routes/predict.py
│   ├── services/model_service.py
│   └── services/preprocessing.py   # será criado
├── tests/
└── Consumer_API/
```

**O que será alterado nesta parte:**
- Refatorar `predict.py`
- Criar `services/preprocessing.py`
- Ajustar testes

# 6. Passo a passo (comandos + código)

## Passo 1: Código “ruim” inicial (Excalidraw: Slide 3)

**Intenção:** Ver o problema antes da refatoração.

Abra o arquivo e confirme o trecho (ou cole se necessário):

```bash
code src/routes/predict.py
```

Trecho em `src/routes/predict.py` (antes):

```python
# ANTES
@router.post("/predict")
def predict_endpoint(payload: PredictRequest):
    data = payload.model_dump()
    if data["age"] < 18:
        return {"error": "underage"}
    if data["limit"] <= 0:
        return {"error": "invalid_limit"}
    # pré-processamento duplicado
    data["score"] = data["limit"] * 0.01
    result = predict_one(MODEL, data)
    return {"prediction": result}
```

**CHECKPOINT:** Código funciona, mas tem duplicação e validação embutida no endpoint.

---

## Passo 2: Extract Function para validação (Excalidraw: Slide 3)

**Intenção:** Mover validação para função reutilizável.

Crie o arquivo e adicione a função (diff lógico):

```bash
New-Item src/services/preprocessing.py -ItemType File
code src/services/preprocessing.py
```

```diff
+ def validate_payload(data: dict) -> str | None:
+     if data["age"] < 18:
+         return "underage"
+     if data["limit"] <= 0:
+         return "invalid_limit"
+     return None
```

Atualizar `predict.py`:

```diff
- if data["age"] < 18:
-     return {"error": "underage"}
- if data["limit"] <= 0:
-     return {"error": "invalid_limit"}
+ if error := validate_payload(data):
+     return {"error": error}
```

**CHECKPOINT:** Endpoint continua funcionando, validação agora centralizada.

---

## Passo 3: Extract Function para pré-processamento (Excalidraw: Slide 4)

**Intenção:** Evitar duplicação de lógica de features.

Adicionar em `preprocessing.py` (diff lógico):

```diff
+ def build_features(data: dict) -> dict:
+     data = data.copy()
+     data["score"] = data["limit"] * 0.01
+     return data
```

Atualizar `predict.py`:

```diff
- data["score"] = data["limit"] * 0.01
- result = predict_one(MODEL, data)
+ features = build_features(data)
+ result = predict_one(MODEL, features)
```

**CHECKPOINT:** O endpoint usa funções reutilizáveis.

---

## Passo 4: Reorganizar módulos (Excalidraw: Slide 4)

**Intenção:** Separar HTTP de lógica de domínio.

Diff lógico:

```diff
# src/routes/predict.py
- from src.services.model_service import load_model, predict_one
+ from src.services.model_service import load_model, predict_one
+ from src.services.preprocessing import validate_payload, build_features
```

**CHECKPOINT:** Router apenas orquestra fluxo, sem lógica pesada.

---

## Passo 5: Testes unitários para o novo módulo

**Intenção:** Garantir que validação e features funcionam isoladamente.

Crie `tests/test_preprocessing.py`:

```bash
New-Item tests/test_preprocessing.py -ItemType File
code tests/test_preprocessing.py
```

```python
from src.services.preprocessing import build_features, validate_payload


def test_validate_payload_ok():
    data = {"age": 30, "limit": 1000}
    assert validate_payload(data) is None


def test_validate_payload_error():
    data = {"age": 15, "limit": 1000}
    assert validate_payload(data) == "underage"


def test_build_features_adds_score():
    data = {"age": 30, "limit": 1000}
    features = build_features(data)
    assert features["score"] == 10.0
```

```bash
uv run pytest tests/test_preprocessing.py -q
```

**CHECKPOINT:** Testes do módulo passam.

---

## Passo 6: Comparação final (Excalidraw: Slide 5)

**Intenção:** Visualizar ganhos de qualidade.

Antes:
- Validação e features dentro do endpoint
- Repetição em outros endpoints

Depois:
- Validação centralizada
- Features reutilizáveis
- Endpoints menores e mais legíveis

**CHECKPOINT:** Código mais modular e pronto para testes isolados.

# 7. Testes rápidos e validação

```bash
# Rodar testes
uv run pytest -q
```

Exemplo de teste em `tests/test_preprocessing.py`:

```python
from src.services.preprocessing import validate_payload


def test_validate_payload_ok():
    data = {"age": 30, "limit": 1000}
    assert validate_payload(data) is None
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Funções pequenas**: facilitam testes e manutenção. Trade-off: mais arquivos.
2. **Separação de camadas**: endpoints só orquestram. Trade-off: exige disciplina.
3. **Testes unitários rápidos**: garantem refatoração segura. Trade-off: escrita de testes.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Import falhou após mover função | Caminho errado | Revisar imports |
| Endpoint retornou 500 | Função nova com bug | Rodar testes unitários |
| Feature engineering duplicado | Função não usada | Substituir uso no endpoint |

# 10. Exercícios (básico e avançado)

**Básico 1:** Criar teste unitário para `build_features`.
- Concluído com sucesso: teste valida saída esperada.

**Básico 2:** Refatorar outro endpoint para usar `validate_payload`.
- Concluído com sucesso: duplicação removida.

**Avançado:** Criar módulo `services/validation.py` com regras mais completas e testes.
- Concluído com sucesso: validação centralizada em módulo próprio.

# 11. Resultados e Lições

**Resultados (como medir):**
- Redução de linhas no endpoint
- Número de funções reutilizáveis criadas
- Testes unitários adicionados

**Lições:**
- Refatoração reduz duplicação
- Funções pequenas facilitam evolução
- Separação de responsabilidades melhora confiabilidade

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você realizou uma refatoração prática, transformando um endpoint pesado em funções pequenas e reutilizáveis, mantendo a API estável.

Na próxima parte, vamos aprender a **reorganizar um projeto de Data Science** com uma estrutura profissional, como o Cookiecutter Data Science, e discutir benefícios de colaboração e produção.
