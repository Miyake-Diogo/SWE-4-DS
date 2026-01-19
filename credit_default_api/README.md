# Credit Card Default Prediction API

Uma API completa e Dockerizada que expõe um modelo de **Árvore de Decisão** treinado sobre o **UCI Credit Card Default Dataset**. O projeto utiliza **MLflow** para rastreamento de experimentos e **BentoML** para servir o modelo em produção.

## Visão Geral

Este projeto demonstra boas práticas de Engenharia de Software para Data Science, incluindo:

- ✅ **Gerenciamento de Dependências**: `pyproject.toml` com **UV** (10-100x mais rápido que pip)
- **Rastreamento de Experimentos**: MLflow para logging de métricas e modelos
- **Containerização**: Docker e Docker Compose para ambientes reprodutíveis
- **API REST**: BentoML para servir o modelo com validação de schemas
- **Código Modular**: Separação clara entre treinamento, servir e utilitários
- **Testes**: Script de testes automatizados para validar a API

## Arquitetura

```
┌─────────────────┐
│  Cliente HTTP   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐       ┌──────────────┐
│  BentoML API    │◄──────┤ Modelo + Scaler
│  (Port 3000)    │       │  (MLflow)    │
└────────┬────────┘       └──────────────┘
         │
         ▼
┌─────────────────┐
│  MLflow UI      │
│  (Port 5000)    │
└─────────────────┘
```

## Estrutura do Projeto

```
Consumer_API/
├── train.py              # Pipeline de treinamento com MLflow
├── service.py            # Serviço BentoML
├── data_loader.py        # Carregamento e preprocessamento de dados
├── test_api.py           # Testes da API
├── requirements.txt      # Dependências Python
├── bentofile.yaml        # Configuração do BentoML
├── Dockerfile.mlflow     # Dockerfile para MLflow server
├── docker-compose.yml    # Orquestração de containers
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Este arquivo
```

## Início Rápido

### Pré-requisitos

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) - Gerenciador de dependências moderno
- Docker e Docker Compose
- Git

### 1️⃣ Instalação de Dependências

**Instalar UV (se ainda não tiver):**
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Instalar dependências do projeto:**
```bash
cd Consumer_API
uv sync
```

Ou, se preferir usar um ambiente virtual tradicional:
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
uv pip install -e .
```

### Treinamento do Modelo

Execute o pipeline de treinamento que automaticamente:
- Carrega o dataset UCI Credit Card Default
- Treina um modelo de Árvore de Decisão
- Registra métricas e artefatos no MLflow

```bash
python train.py
```

**Saída esperada:**
```
================================================================================
CREDIT CARD DEFAULT PREDICTION - DECISION TREE MODEL
================================================================================

1. Loading dataset...
   Dataset shape: (30000, 23)
   Default rate: 22.12%

2. Preprocessing data...
   Train samples: 24000
   Test samples: 6000

3. Training Decision Tree model...
   Training complete!

4. Evaluating model...

================================================================================
MODEL PERFORMANCE METRICS
================================================================================
   train_accuracy      : 0.8245
   test_accuracy       : 0.8156
   test_precision      : 0.6834
   test_recall         : 0.4523
   test_f1             : 0.5442
   test_roc_auc        : 0.7289
...
```

### Visualizar Experimentos no MLflow

```bash
mlflow ui --backend-store-uri file:./mlruns
```

Abra no navegador: http://localhost:5055

### Construir a Imagem BentoML

```bash
bentoml build
```

Isso cria uma imagem Docker otimizada com o modelo e suas dependências.

**Identifique a tag da imagem gerada:**
```bash
bentoml list
```

### Containerizar o Modelo

Após construir a imagem com `bentoml build`, identifique a tag gerada:

```bash
bentoml list
# Exemplo de saída:
# Tag: credit_default_classifier:abc123def
```

Depois, crie uma tag local para uso no Docker Compose:

```bash
bentoml containerize credit_default_classifier:abc123def -t credit_default_classifier:latest
```

### Iniciar os Serviços

```bash
docker-compose up -d
```

Isso inicia:
- **MLflow Server** em http://localhost:5055
- **BentoML API** em http://localhost:3033

### Testar a API

```bash
python test_api.py
```

## Endpoints da API

### 1. Health Check
```bash
curl -X POST http://localhost:3033/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true,
  "n_features": 23
}
```

### 2. Predição Individual
```bash
curl -X POST http://localhost:3033/predict \
  -H "Content-Type: application/json" \
  -d '{
    "LIMIT_BAL": 200000,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 35,
    "PAY_0": 0,
    "PAY_2": 0,
    "PAY_3": 0,
    "PAY_4": 0,
    "PAY_5": 0,
    "PAY_6": 0,
    "BILL_AMT1": 15000,
    "BILL_AMT2": 14000,
    "BILL_AMT3": 13000,
    "BILL_AMT4": 12000,
    "BILL_AMT5": 11000,
    "BILL_AMT6": 10000,
    "PAY_AMT1": 2000,
    "PAY_AMT2": 2000,
    "PAY_AMT3": 2000,
    "PAY_AMT4": 2000,
    "PAY_AMT5": 2000,
    "PAY_AMT6": 2000
  }'
```

**Resposta:**
```json
{
  "prediction": 0,
  "probability": 0.15,
  "risk_level": "low"
}
```

### 3. Predição em Lote
```bash
curl -X POST http://localhost:3033/predict_batch \
  -H "Content-Type: application/json" \
  -d '[{...}, {...}]'
```

### 4. Importância de Features
```bash
curl -X POST http://localhost:3033/feature_importance
```

**Resposta:**
```json
{
  "PAY_0": 0.2345,
  "PAY_2": 0.1678,
  "LIMIT_BAL": 0.1234,
  ...
}
```

## Configuração

### Parâmetros do Modelo

Edite os parâmetros em `train.py`:

```python
train_decision_tree(
    max_depth=10,              # Profundidade máxima da árvore
    min_samples_split=20,      # Mínimo de amostras para split
    min_samples_leaf=10,       # Mínimo de amostras em folha
    criterion='gini',          # Critério de divisão
    random_state=42            # Seed para reprodutibilidade
)
```

### Recursos do BentoML

Ajuste em `service.py`:

```python
@bentoml.service(
    resources={
        "cpu": "2",           # Número de CPUs
        "memory": "2Gi",      # Memória RAM
    },
)
```

## Dataset

O projeto usa o **UCI Credit Card Default Dataset**:
- **Fonte**: UCI Machine Learning Repository
- **ID**: 350
- **Amostras**: 30,000
- **Features**: 23 (limite de crédito, dados demográficos, histórico de pagamento)
- **Target**: Default no próximo mês (0=Não, 1=Sim)

**Features principais:**
- `LIMIT_BAL`: Limite de crédito
- `SEX`, `EDUCATION`, `MARRIAGE`, `AGE`: Dados demográficos
- `PAY_0` a `PAY_6`: Status de pagamento (Setembro a Abril)
- `BILL_AMT1` a `BILL_AMT6`: Valores das faturas
- `PAY_AMT1` a `PAY_AMT6`: Valores pagos

## Comandos Docker

```bash
# Construir e iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Rebuild completo
docker-compose up -d --build

# Ver status
docker-compose ps
```

## Desenvolvimento

### Gerenciamento de Dependências com UV

```bash
# Adicionar nova dependência
uv add <package-name>

# Adicionar dependência de desenvolvimento
uv add --dev <package-name>

# Atualizar dependências
uv lock --upgrade

# Sincronizar ambiente com pyproject.toml
uv sync

# Executar comandos no ambiente UV
uv run python train.py
uv run python test_api.py
```

### Treinar Novamente o Modelo

```bash
uv run python train.py
# ou, se estiver no ambiente virtual ativado
python train.py
```

### Testar Localmente (sem Docker)

```bash
# Terminal 1: Servir com BentoML
uv run bentoml serve service:CreditDefaultService

# Terminal 2: Testar
uv run python test_api.py
```

### Rebuild do Bento

```bash
bentoml build
bentoml containerize credit_default_classifier:latest
docker-compose up -d bentoml
```

## Métricas do Modelo

Métricas típicas após treinamento:

| Métrica | Valor |
|---------|-------|
| Accuracy | ~82% |
| Precision | ~68% |
| Recall | ~45% |
| F1-Score | ~54% |
| ROC-AUC | ~73% |

**Nota**: O modelo prioriza precisão sobre recall para minimizar falsos positivos em aprovação de crédito.

## Troubleshooting

### Erro: "Model not loaded"
- Certifique-se de executar `python train.py` antes de servir
- Verifique se a pasta `mlruns/` existe e contém experimentos

### Porta já em uso
```bash
# Alterar portas no docker-compose.yml
ports:
  - "3034:3000"  # BentoML
  - "5056:5000"  # MLflow
```

### Problemas com Docker
```bash
# Limpar containers e volumes
docker-compose down -v
docker system prune -a
```

## Referências

- [UV Documentation](https://docs.astral.sh/uv/) - Gerenciador de dependências moderno
- [BentoML Documentation](https://docs.bentoml.org/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients)
- [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

## Licença

Este projeto é um exemplo educacional para o as aulas de Engenharia de Software para Data Science da pós graduação de Engenharia de Machine Learning.

## Autor

Desenvolvido por Diogo Miyake Com auxilio de IA para material didático para POSTECH FIAP - Machine Learning Engineering.

---

