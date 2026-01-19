---
titulo: "Aula 08 – Parte 01: Detectando 'Bad Smells' - Diagnóstico de Código em Projetos DS"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Projeto FastAPI em andamento"
  - "Conhecimento básico de testes"
tags: ["refatoracao", "code-smells", "qualidade", "fastapi", "ds"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos aprender a **diagnosticar problemas de qualidade** no código de projetos de Data Science.

Em DS é muito comum termos notebooks e scripts que funcionam, mas são difíceis de manter. O problema é que, quando o projeto cresce, esse “funciona” vira um risco: bugs escondidos, dependências implícitas e código impossível de reutilizar.

Hoje vamos identificar **bad smells** — sinais de alerta no código — e entender por que a refatoração contínua é essencial para manter nossa API FastAPI saudável enquanto ela evolui.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: O time tem vários notebooks duplicados, cada um com pequenas variações do mesmo pipeline.

**Agitação**: Uma correção precisa ser aplicada em 5 lugares diferentes. Um notebook é atualizado, outro não. A API passa a usar dados inconsistentes.

**Solução**: Detectar bad smells cedo, padronizar o código e refatorar continuamente. Assim, seguimos com a construção incremental da API sem acumular dívidas técnicas.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Identificar** bad smells em notebooks e scripts de DS
2. **Explicar** impactos desses smells na manutenção e colaboração
3. **Priorizar** quais smells refatorar primeiro
4. **Relacionar** smells com riscos na API FastAPI

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- uv instalado
- Projeto FastAPI em execução

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar testes para garantir baseline
uv run pytest -q
```

**Checklist de setup:**
- [ ] Ambiente virtual ativo
- [ ] Testes rodando
- [ ] Código atual versionado no Git

# 5. Visão geral do que já existe no projeto (continuidade)

Estado esperado do projeto:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   └── services/
├── tests/
└── Consumer_API/
```

**O que será alterado nesta parte:**
- Não vamos alterar arquivos ainda. Vamos **diagnosticar** o estado atual.

# 6. Passo a passo (comandos + código)

## Passo 1: Mapear duplicações (Excalidraw: Slide 1)

**Intenção:** Encontrar lógica repetida nos scripts/notebooks.

Comando de busca simples:

```bash
# Procurar por blocos duplicados
Get-ChildItem -Recurse -Filter "*.py" | Select-String "predict" -Context 2,2
```

**CHECKPOINT:** Se deu certo, você verá ocorrências repetidas de lógica similar.

---

## Passo 2: Identificar funções monolíticas

**Intenção:** Detectar funções que fazem “tudo” ao mesmo tempo.

Critérios simples:
- Funções com mais de 30–40 linhas
- Funções que fazem leitura, validação e predição juntas

Exemplo típico:

```python
# SMELL: Função faz tudo
def process_and_predict(input_path: str) -> dict:
    df = pd.read_csv(input_path)
    # limpeza
    # feature engineering
    # predição
    # salvar saída
    return result
```

**CHECKPOINT:** Liste 1 ou mais funções longas no seu projeto.

---

## Passo 3: Variáveis globais e dependências implícitas

**Intenção:** Ver onde o código depende de ordem de execução.

Exemplo de smell comum:

```python
# SMELL: Dependência implícita
MODEL = None

if MODEL is None:
    MODEL = load_model()

def predict(data):
    return MODEL.predict(data)
```

Problema: a função depende de um estado global oculto.

**CHECKPOINT:** Identifique pelo menos 1 variável global crítica.

---

## Passo 4: Impacto prático nos projetos de DS

**Intenção:** Conectar smells com problemas reais.

Impactos:
- Dificuldade de colaboração (ninguém entende o fluxo)
- Bugs difíceis de rastrear
- Reuso quase impossível
- Deploy arriscado

**CHECKPOINT:** Liste 2 impactos que você já viu na prática.

# 7. Testes rápidos e validação

Teste simples para validar comportamento antes da refatoração:

```bash
uv run pytest -q
```

Exemplo de resposta:
```json
{"status": "ok"}
```

Teste automatizado (exemplo em `tests/test_health.py`):

```python
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Identificação contínua de smells**: reduz dívidas técnicas. Trade-off: demanda tempo de revisão.
2. **Testes como rede de segurança**: garante refatoração segura. Trade-off: esforço inicial.
3. **Modularização gradual**: facilita evolução. Trade-off: mais arquivos para organizar.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Código duplicado não aparece em busca simples | Variações pequenas | Use buscas por padrões ou diff manual |
| Função longa ignorada | Pressão por entrega | Defina limite de linhas no time |
| Variáveis globais escondidas | Notebook “funcionou” | Mova estado para funções/serviços |

# 10. Exercícios (básico e avançado)

**Básico 1:** Encontre 3 duplicações no projeto.
- Concluído com sucesso: lista com local e motivo da duplicação.

**Básico 2:** Liste 2 funções com mais de 30 linhas e descreva o que fazem.
- Concluído com sucesso: lista com arquivo e responsabilidade.

**Avançado:** Criar um relatório curto de smells do projeto e priorizar 3 para refatorar.
- Concluído com sucesso: relatório com prioridade justificada.

# 11. Resultados e Lições

**Resultados (como medir):**
- Número de funções longas (contagem manual)
- Quantidade de duplicações (inspeção ou ferramenta)
- Cobertura de testes antes de refatorar (pytest --cov)

**Lições:**
- Smells são sinais, não bugs
- Diagnóstico cedo evita dívidas grandes
- Refatorar é parte do ciclo de vida

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu a **diagnosticar bad smells** em projetos de Data Science e entendeu por que eles impactam diretamente a evolução da nossa API FastAPI.

Na próxima aula, vamos aprender **técnicas de refatoração graduais**: Extract Function, Rename e Move/Rearrange. Você verá como aplicar essas mudanças passo a passo, sempre com testes garantindo que a API continue correta.
