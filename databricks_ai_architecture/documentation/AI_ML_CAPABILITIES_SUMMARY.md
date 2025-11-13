# Databricks AI/ML & GenAI Capabilities Summary

**Date**: November 13, 2025
**Purpose**: How to leverage Databricks for AI, ML Training, and Generative AI
**Associated Diagrams**:
- `../diagrams/04-databricks-ai-ml-deep-dive.drawio` - **AI/ML Deep-Dive Architecture** (NEW)
  * Section 1: ML Training & Development
  * Section 2: Generative AI & Foundation Models
  * Section 3: Deployment & Model Serving
  * Section 4: Use Cases & Applications
- `/architecture/diagrams/03-databricks-lakehouse-horizontal-with-databuck.drawio` - End-to-end lakehouse with ML lifecycle

**Strategic Context**: See `/databricks_ai_architecture/strategic/AI_Strategy_GenAI_Agentic.md` for business strategy and roadmap

---

## Executive Summary

Databricks provides a **unified AI/ML platform** that enables organizations to:
- Train machine learning models at scale using distributed computing
- Deploy and serve models with <100ms latency
- Build Generative AI applications using foundation models (DBRX, Llama 3.1, MPT)
- Implement RAG (Retrieval-Augmented Generation) systems
- Create multi-agent AI systems with orchestration
- Maintain data quality throughout the ML lifecycle with Databuck integration

This document explains how to leverage these capabilities effectively.

---

## Table of Contents

1. [AI/ML Platform Overview](#aiml-platform-overview)
2. [ML Training Pipeline](#ml-training-pipeline)
3. [Generative AI Capabilities](#generative-ai-capabilities)
4. [Model Deployment & Monitoring](#model-deployment--monitoring)
5. [Data Quality Integration (Databuck)](#data-quality-integration-databuck)
6. [Best Practices](#best-practices)
7. [Use Cases](#use-cases)

---

## AI/ML Platform Overview

### Unified Platform Benefits

Databricks provides a **single platform** for the entire AI/ML lifecycle:

```
┌─────────────────────────────────────────────────────────┐
│  DATABRICKS UNIFIED AI/ML PLATFORM                      │
├─────────────────────────────────────────────────────────┤
│  ✓ Data Engineering (ETL pipelines)                     │
│  ✓ Data Science (Collaborative notebooks)               │
│  ✓ Machine Learning (MLflow, model training)            │
│  ✓ Generative AI (Foundation models, RAG)               │
│  ✓ AI Applications (Model serving, APIs)                │
│  ✓ Data Quality (Databuck integration)                  │
└─────────────────────────────────────────────────────────┘
```

### Why Unified Platform Matters

- **No data movement**: Data stays in Delta Lake, eliminating ETL overhead
- **Distributed computing**: Train models on massive datasets using Spark
- **Built-in MLOps**: Automated workflows from training to production
- **Collaboration**: Data engineers, data scientists, and ML engineers work together
- **Governance**: Unity Catalog provides centralized access control and lineage

---

## ML Training Pipeline

### 10-Step ML Lifecycle Workflow

#### **Step 1: Data Preparation**
- **Source**: Delta Lake Gold tables (cleaned, processed data)
- **Validation**: Databuck Trust Score ≥ 80%
- **Purpose**: Ensure high-quality training data

```python
# Example: Load Gold layer data with Databuck validation
df = spark.table("gold.customer_features")

# Check Databuck Trust Score
trust_score = databuck.get_trust_score("gold.customer_features")
if trust_score >= 80:
    print(f"✓ Data quality validated: {trust_score}/100")
else:
    raise ValueError(f"⚠️ Low data quality: {trust_score}/100")
```

#### **Step 2: Feature Store**
- **Centralized feature management**: Reuse features across models
- **Point-in-time correctness**: Avoid data leakage
- **Online/Offline serving**: Features for training and real-time inference

```python
# Create feature table
from databricks import feature_store

fs = feature_store.FeatureStoreClient()
fs.create_table(
    name="ml.customer_features",
    primary_keys=["customer_id"],
    df=feature_df,
    description="Customer behavioral features"
)
```

#### **Step 3: Model Training**
- **Frameworks supported**: Spark ML, PyTorch, TensorFlow, Scikit-learn
- **Distributed training**: Scale training across multiple nodes
- **GPU acceleration**: Use GPUs for deep learning models

```python
# Example: PyTorch training on Databricks
import torch
from databricks.sdk import WorkspaceClient

# Distributed training using TorchDistributor
from pyspark.ml.torch.distributor import TorchDistributor

distributor = TorchDistributor(
    num_processes=4,
    local_mode=False,
    use_gpu=True
)

distributor.run(train_model, args=(train_data, model_config))
```

#### **Step 4: MLflow Tracking**
- **Experiment tracking**: Log parameters, metrics, artifacts
- **Hyperparameter tuning**: Compare multiple runs
- **Reproducibility**: Track code version, environment

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("n_estimators", 100)

    # Train model
    model = RandomForestClassifier(max_depth=10, n_estimators=100)
    model.fit(X_train, y_train)

    # Log metrics
    mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
    mlflow.log_metric("f1_score", f1_score(y_test, y_pred))

    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
```

#### **Step 5: Model Registry**
- **Version control**: Track model versions
- **Stage transitions**: Dev → Staging → Production
- **Model documentation**: Add descriptions, tags, metadata

```python
# Register model to MLflow Model Registry
model_uri = f"runs:/{run_id}/random_forest_model"
mlflow.register_model(model_uri, "customer_churn_model")

# Transition to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="customer_churn_model",
    version=3,
    stage="Production"
)
```

#### **Step 6: Model Validation**
- **A/B testing**: Compare new model against baseline
- **Champion/Challenger**: Run multiple models in parallel
- **Databuck validation**: Check model output quality

```python
# A/B test new model against champion
champion_model = mlflow.pyfunc.load_model("models:/customer_churn_model/Production")
challenger_model = mlflow.pyfunc.load_model("models:/customer_churn_model/Staging")

# Compare predictions
champion_pred = champion_model.predict(test_data)
challenger_pred = challenger_model.predict(test_data)

# Databuck quality check on predictions
databuck.validate_predictions(challenger_pred, threshold=0.8)
```

#### **Step 7: Staging Deployment**
- **Pre-production testing**: Test in staging environment
- **Integration tests**: Verify API contracts
- **Load testing**: Ensure performance under load

#### **Step 8: Production Serving**
- **Model Serving endpoints**: REST APIs with <100ms latency
- **Auto-scaling**: Handle variable traffic
- **Real-time inference**: Low-latency predictions

```python
# Deploy model to Model Serving
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ServedModelInput

w = WorkspaceClient()

w.serving_endpoints.create(
    name="customer_churn_endpoint",
    config={
        "served_models": [{
            "model_name": "customer_churn_model",
            "model_version": "3",
            "workload_size": "Small",
            "scale_to_zero_enabled": True
        }]
    }
)
```

#### **Step 9: Databuck Monitoring (RED EMPHASIS)**
- **Data drift detection**: Monitor input data distribution changes
- **Model quality tracking**: Track prediction quality over time
- **Performance metrics**: Latency, throughput, error rates

```python
# Databuck monitors predictions continuously
databuck.monitor_endpoint(
    endpoint_name="customer_churn_endpoint",
    alert_on_drift=True,
    drift_threshold=0.2,
    quality_threshold=0.8
)
```

#### **Step 10: Auto Retraining**
- **Drift-triggered**: Retrain when data drift detected
- **Scheduled**: Retrain on a regular cadence
- **Continuous improvement**: Improve models with new data

```python
# Auto-retrain workflow triggered by Databuck
if databuck.detect_drift() > 0.2:
    print("⚠️ Data drift detected. Triggering retraining...")
    dbutils.jobs.run(job_id=retrain_job_id)
```

---

## Generative AI Capabilities

### Foundation Model APIs

Databricks provides access to **state-of-the-art foundation models**:

| Model | Parameters | Use Case | Specialty |
|-------|-----------|----------|-----------|
| **DBRX** | 132B (MoE) | General-purpose LLM | Databricks' own MoE model |
| **Llama 3.1** | 8B, 70B, 405B | Open-source LLM | Meta's latest release |
| **MPT** | 7B, 30B | Mosaic Pretrained Transformer | Optimized for inference |
| **BGE Embeddings** | - | Text embeddings | For RAG systems |

### How to Use Foundation Models

```python
# Example: Using DBRX for text generation
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

w = WorkspaceClient()

response = w.serving_endpoints.query(
    name="databricks-dbrx-instruct",
    messages=[{
        "role": "user",
        "content": "Explain Databricks Lakehouse architecture"
    }]
)

print(response.choices[0].message.content)
```

### Fine-Tuning Foundation Models

Fine-tune models for domain-specific tasks:

#### **LoRA (Low-Rank Adaptation)**
- Efficient fine-tuning with fewer parameters
- Faster training, lower memory usage

```python
# Fine-tune Llama 3.1 with LoRA
from transformers import AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]
)

model = get_peft_model(model, lora_config)
# Train model with custom dataset
```

#### **Full Fine-Tuning**
- Update all model parameters
- Maximum customization for specific domains

### RAG (Retrieval-Augmented Generation)

Build RAG systems to ground LLMs with your enterprise data:

#### **RAG Workflow**
```
Documents → Chunking → Embeddings → Vector Search → Rerank → LLM + Context → Response
```

#### **Implementation Example**

```python
# Step 1: Document Chunking
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# Step 2: Generate Embeddings
from databricks.vector_search import VectorSearchClient

vsc = VectorSearchClient()
vsc.create_endpoint(name="my_vector_search_endpoint")

# Step 3: Create Vector Search Index
index = vsc.create_delta_sync_index(
    endpoint_name="my_vector_search_endpoint",
    index_name="docs_index",
    source_table_name="main.default.docs",
    pipeline_type="TRIGGERED",
    primary_key="doc_id",
    embedding_source_column="text",
    embedding_model_endpoint_name="bge-large-en"
)

# Step 4: Query with RAG
def rag_query(question):
    # Retrieve relevant docs
    results = index.similarity_search(
        query_text=question,
        columns=["doc_id", "text"],
        num_results=5
    )

    context = "\n\n".join([r["text"] for r in results["result"]["data_array"]])

    # Generate response with LLM + context
    prompt = f"""Context: {context}

    Question: {question}

    Answer:"""

    response = w.serving_endpoints.query(
        name="databricks-dbrx-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Use RAG
answer = rag_query("How do I configure Unity Catalog?")
print(answer)
```

#### **RAG Benefits**
- ✅ Reduces hallucinations from 20-30% to <5%
- ✅ Grounds LLM responses in factual enterprise data
- ✅ Provides source attribution for answers
- ✅ Keeps data fresh (no retraining needed)

### Agentic AI Framework

Build **multi-agent systems** that can:
- Execute complex multi-step tasks
- Use tools (SQL, APIs, Python functions)
- Collaborate between specialized agents

#### **Architecture**
```
┌────────────┐  ┌────────────┐  ┌────────────┐
│Data Agent  │  │ ML Agent   │  │Report Agent│
│(SQL Query) │  │(Training)  │  │(Viz/Docs)  │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │               │               │
      └───────────────┴───────────────┘
                      ↓
          ┌─────────────────────┐
          │ Coordinator Agent   │
          │   (Orchestrator)    │
          └─────────────────────┘
```

#### **Implementation with LangChain**

```python
from langchain.agents import AgentExecutor, create_databricks_agent
from langchain.tools import Tool

# Define specialized agents as tools
data_agent = Tool(
    name="DataQuery",
    func=lambda q: spark.sql(q).toPandas(),
    description="Query data using SQL"
)

ml_agent = Tool(
    name="MLPredict",
    func=lambda data: model.predict(data),
    description="Make predictions using ML model"
)

report_agent = Tool(
    name="GenerateReport",
    func=lambda results: create_visualization(results),
    description="Create visualizations and reports"
)

# Create coordinator agent
tools = [data_agent, ml_agent, report_agent]

coordinator = create_databricks_agent(
    llm=ChatDatabricks(endpoint="databricks-dbrx-instruct"),
    tools=tools,
    verbose=True
)

# Execute complex task
result = coordinator.invoke({
    "input": "Analyze customer churn, predict at-risk customers, and create a report"
})
```

---

## Model Deployment & Monitoring

### Production Serving

Deploy models as **REST API endpoints** with enterprise-grade capabilities:

#### **Key Features**
- **<100ms latency**: Optimized inference
- **Auto-scaling**: Scale from 0 to thousands of requests
- **A/B testing**: Test multiple models in production
- **Monitoring**: Track latency, throughput, errors

#### **Calling Deployed Models**

```python
import requests
import os

# Call Model Serving endpoint
url = "https://your-workspace.cloud.databricks.com/serving-endpoints/customer_churn_endpoint/invocations"
headers = {"Authorization": f"Bearer {os.environ['DATABRICKS_TOKEN']}"}

data = {
    "dataframe_records": [
        {"customer_id": 123, "tenure": 24, "monthly_charges": 89.99}
    ]
}

response = requests.post(url, headers=headers, json=data)
predictions = response.json()["predictions"]
```

### Monitoring with Databuck

**Databuck provides AI/ML-specific monitoring**:

#### **Data Drift Detection**
- Monitors input data distribution over time
- Alerts when data significantly changes
- **Trigger**: Retrain models when drift detected

```python
# Databuck drift monitoring
drift_score = databuck.check_drift(
    endpoint="customer_churn_endpoint",
    baseline_table="gold.customer_features",
    window="7 days"
)

if drift_score > 0.2:
    print(f"⚠️ Data drift detected: {drift_score:.2%}")
    # Trigger retraining workflow
```

#### **Model Quality Tracking**
- Track prediction quality metrics
- Compare against baseline performance
- Alert on quality degradation

```python
# Monitor model quality
quality_metrics = databuck.track_model_quality(
    endpoint="customer_churn_endpoint",
    metrics=["accuracy", "precision", "recall", "f1"],
    alert_threshold=0.1  # Alert if drops 10%
)
```

#### **Performance Metrics**
- Latency (p50, p95, p99)
- Throughput (requests per second)
- Error rates
- Resource utilization

---

## Data Quality Integration (Databuck)

### Why Data Quality Matters for AI/ML

**Poor data quality = Poor model performance**

| Issue | Impact | Example |
|-------|--------|---------|
| Missing values | Models can't predict | 20% of features are NULL |
| Outliers | Biased predictions | Customer age = 999 |
| Data drift | Model accuracy drops | Income distribution changes |
| Label errors | Wrong training signal | Mislabeled training data |

### Databuck Quality Gates

Databuck provides **quality checkpoints** throughout the ML lifecycle:

#### **1. Training Data Validation (Trust Score ≥80%)**
```python
# Before training, validate data quality
trust_score = databuck.validate_table("gold.customer_features")

if trust_score >= 80:
    print(f"✓ Training data validated: {trust_score}/100")
    # Proceed with training
else:
    print(f"⚠️ Poor data quality: {trust_score}/100")
    # Block training, fix data issues
```

#### **2. Model Output Validation**
```python
# Validate model predictions
databuck.validate_predictions(
    predictions=model_predictions,
    schema=expected_schema,
    rules=[
        "churn_probability BETWEEN 0 AND 1",
        "customer_id IS NOT NULL"
    ]
)
```

#### **3. Production Monitoring**
```python
# Continuous monitoring in production
databuck.monitor_endpoint(
    endpoint_name="customer_churn_endpoint",
    metrics=["drift", "quality", "performance"],
    alert_channels=["email", "slack"]
)
```

### Trust Score Components

Databuck Trust Score (0-100) is calculated from:
- **Completeness**: % of non-null values
- **Validity**: % of values passing validation rules
- **Consistency**: Cross-field validation
- **Timeliness**: Data freshness
- **Accuracy**: Compared to reference data

---

## Best Practices

### 1. Data Quality First

✅ **Always validate training data** with Databuck before training
✅ **Set quality thresholds**: Trust Score ≥ 80% for production models
✅ **Monitor data drift**: Retrain when input distribution changes
❌ **Don't ignore data issues**: They compound in model predictions

### 2. MLOps Automation

✅ **Use MLflow** for experiment tracking and model registry
✅ **Automate model validation**: A/B testing, champion/challenger
✅ **Set up monitoring**: Track performance in production
✅ **Enable auto-retraining**: Triggered by drift or schedule
❌ **Don't manually deploy models**: Use CI/CD pipelines

### 3. Feature Engineering

✅ **Use Feature Store**: Centralize features, avoid duplication
✅ **Point-in-time correctness**: Prevent data leakage
✅ **Document features**: Add descriptions, data types
❌ **Don't recreate features**: Reuse existing feature tables

### 4. Model Serving

✅ **Use Model Serving endpoints**: Built-in scaling, monitoring
✅ **Enable auto-scaling**: Handle variable traffic
✅ **Set up A/B testing**: Compare models in production
❌ **Don't host models outside Databricks**: Adds complexity

### 5. Generative AI

✅ **Use RAG for enterprise data**: Grounds LLM responses
✅ **Fine-tune for domain tasks**: Better than prompting alone
✅ **Monitor LLM outputs**: Check for hallucinations, quality
❌ **Don't use LLMs without RAG**: High risk of hallucinations

### 6. Security & Governance

✅ **Use Unity Catalog**: Centralized access control
✅ **Track lineage**: Know where data and models come from
✅ **Audit access**: Log who accesses models and data
❌ **Don't share credentials**: Use service principals

---

## Use Cases

### 1. Customer Churn Prediction (Traditional ML)

**Problem**: Predict which customers will cancel their subscription
**Solution**: Train classification model on Gold layer customer data

**Workflow**:
1. Load customer features from Delta Lake Gold
2. Validate with Databuck (Trust Score ≥ 80%)
3. Train Random Forest model with MLflow tracking
4. Register model to Model Registry
5. A/B test against baseline model
6. Deploy to Model Serving endpoint
7. Monitor with Databuck (drift, quality)
8. Auto-retrain when drift detected

**Business Impact**: Reduce churn by 15% through proactive retention

---

### 2. Document Q&A Chatbot (RAG + GenAI)

**Problem**: Answer employee questions about company policies
**Solution**: Build RAG system with Llama 3.1 and Vector Search

**Workflow**:
1. Ingest policy documents to Delta Lake
2. Chunk documents into 512-token segments
3. Generate embeddings with BGE model
4. Store in Vector Search index
5. Query: Retrieve relevant docs → Pass to Llama 3.1 → Generate answer
6. Monitor with Databuck (response quality)

**Business Impact**: 80% reduction in support tickets, <2s response time

---

### 3. Multi-Agent Data Analysis (Agentic AI)

**Problem**: Automate complex data analysis workflows
**Solution**: Build multi-agent system with coordinator

**Workflow**:
1. Data Agent: Query sales data from Gold tables
2. ML Agent: Run predictions on new customer leads
3. Report Agent: Generate visualizations and insights
4. Coordinator Agent: Orchestrates all agents, provides final report

**Business Impact**: Reduce analyst time by 60%, faster insights

---

### 4. Code Assistant (Fine-tuned LLM)

**Problem**: Help developers write Databricks-specific code
**Solution**: Fine-tune DBRX on Databricks documentation and code examples

**Workflow**:
1. Collect Databricks code examples and docs
2. Fine-tune DBRX with LoRA
3. Deploy to Model Serving endpoint
4. Integrate with IDE (VS Code extension)
5. Monitor usage and quality

**Business Impact**: 40% faster development, fewer errors

---

## Getting Started

### Prerequisites
- Databricks workspace (AWS, Azure, or GCP)
- Unity Catalog enabled
- Databuck integration configured

### Quick Start Guide

#### 1. Set Up Environment
```python
# Install required libraries
%pip install mlflow databricks-sdk langchain databricks-vectorsearch

# Configure workspace
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
```

#### 2. Train Your First Model
```python
import mlflow
from sklearn.ensemble import RandomForestClassifier

# Load data
df = spark.table("gold.training_data").toPandas()
X = df.drop("target", axis=1)
y = df["target"]

# Train with MLflow
with mlflow.start_run():
    model = RandomForestClassifier()
    model.fit(X, y)
    mlflow.sklearn.log_model(model, "rf_model")
```

#### 3. Deploy Model
```python
# Register and deploy
model_uri = f"runs:/{run_id}/rf_model"
mlflow.register_model(model_uri, "my_model")

# Deploy to serving
w.serving_endpoints.create(
    name="my_endpoint",
    config={"served_models": [{"model_name": "my_model", "model_version": "1"}]}
)
```

#### 4. Build RAG System
```python
from databricks.vector_search import VectorSearchClient

vsc = VectorSearchClient()
index = vsc.create_delta_sync_index(
    endpoint_name="vector_search_endpoint",
    index_name="docs_index",
    source_table_name="main.default.documents"
)

# Query with RAG
results = index.similarity_search("How do I...?")
```

---

## How to Choose: Classic ML vs GenAI

### Decision Framework

Use this decision tree to determine the best approach for your use case:

```
                    START: What problem are you solving?
                                    |
                    ┌───────────────┴───────────────┐
                    |                               |
            Is it predictive/analytical?     Is it generative/creative?
                    |                               |
                    ↓                               ↓
            CLASSIC ML APPROACH              GENERATIVE AI APPROACH

CLASSIC ML:                              GENERATIVE AI:
- Classification                         - Text generation
- Regression                             - Document Q&A
- Clustering                             - Code generation
- Anomaly detection                      - Summarization
- Recommendation                         - Translation
- Time series forecasting                - Creative content
- Tabular data                           - Conversational AI

FRAMEWORKS:                              MODELS:
✓ Spark ML                               ✓ DBRX
✓ XGBoost/LightGBM                       ✓ Llama 3.1
✓ PyTorch/TensorFlow                     ✓ MPT
✓ Scikit-learn                           ✓ GPT-4 (Azure)
                                         ✓ Claude (AWS)

WHEN TO USE:                             WHEN TO USE:
• Structured data                        • Unstructured text/code
• Clear labels/targets                   • No fixed output format
• Need explainability                    • Natural language required
• Lower cost per inference               • Context understanding needed
• <1ms latency required                  • Flexibility over precision
```

### Hybrid Approaches

Many production systems combine both:

**Example 1: Recommendation Engine with Explanations**
- Classic ML: XGBoost for recommendations (fast, accurate)
- GenAI: Llama 3.1 for generating natural language explanations

**Example 2: Fraud Detection with Investigation**
- Classic ML: Real-time fraud scoring (<10ms)
- GenAI: GPT-4 for fraud investigation summaries (post-detection)

**Example 3: Customer Support**
- Classic ML: Intent classification (route to right team)
- GenAI: RAG system for answering questions with context

---

## ML Training Framework Comparison

### Framework Selection Guide

| Framework | Best For | Training Speed | Inference Speed | Distributed | Complexity |
|-----------|----------|----------------|-----------------|-------------|------------|
| **Spark ML** | Tabular data, 100M+ rows | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast | ✅ Native | 🟢 Low |
| **XGBoost** | Structured data, competitions | ⚡⚡ Medium | ⚡⚡⚡ Fast | ✅ Yes | 🟢 Low |
| **LightGBM** | Large datasets, fast training | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast | ✅ Yes | 🟢 Low |
| **Scikit-learn** | Small-medium data, prototyping | ⚡⚡ Medium | ⚡⚡ Medium | ❌ Limited | 🟢 Low |
| **PyTorch** | Deep learning, research | ⚡ Slow | ⚡⚡ Medium | ✅ Horovod | 🔴 High |
| **TensorFlow** | Deep learning, production | ⚡ Slow | ⚡⚡ Medium | ✅ Strategy | 🟡 Medium |
| **Databricks AutoML** | Quick baselines, non-experts | ⚡⚡ Medium | ⚡⚡ Medium | ✅ Yes | 🟢 Low |

### When to Use Each Framework

#### Spark ML
**Use when:**
- Data > 100M rows
- Need native Spark integration
- Tabular data (classification, regression)
- Team familiar with Spark/Scala

```python
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler

# Spark ML for distributed training
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
lr = LogisticRegression(maxIter=100, regParam=0.01)

# Train on billions of rows
model = lr.fit(training_data)
```

#### XGBoost/LightGBM
**Use when:**
- Structured/tabular data
- Need high accuracy (competitions)
- Medium data size (1M-100M rows)
- Fast inference critical

```python
import xgboost as xgb

# XGBoost for structured data
dtrain = xgb.DMatrix(X_train, label=y_train)
params = {
    'max_depth': 6,
    'eta': 0.1,
    'objective': 'binary:logistic'
}
model = xgb.train(params, dtrain, num_boost_round=100)
```

#### PyTorch
**Use when:**
- Deep learning (NLP, computer vision)
- Research/experimentation
- Need flexibility
- Custom architectures

```python
import torch
import torch.nn as nn

# PyTorch for deep learning
class ChurnPredictor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.sigmoid(self.fc3(x))

model = ChurnPredictor(input_dim=50)
# Train with distributed Horovod on Databricks
```

#### Databricks AutoML
**Use when:**
- Quick baseline needed
- Team lacks ML expertise
- Exploratory analysis
- Want best practices automatically

```python
from databricks import automl

# AutoML automatically tries multiple algorithms
summary = automl.classify(
    dataset=training_df,
    target_col="churn",
    timeout_minutes=30
)

# Returns best model + code notebook
best_model = summary.best_trial.load_model()
```

---

## GenAI Deep Dive: Fine-Tuning & RAG

### Fine-Tuning Strategies

#### When to Fine-Tune vs RAG

| Approach | When to Use | Cost | Latency | Accuracy |
|----------|-------------|------|---------|----------|
| **Prompt Engineering** | Quick start, general tasks | $ | Fast | Good |
| **RAG** | Domain knowledge, documents | $$ | Medium | Very Good |
| **LoRA Fine-Tuning** | Task-specific, style adaptation | $$$ | Fast | Excellent |
| **Full Fine-Tuning** | Complete task specialization | $$$$ | Fast | Best |

#### LoRA Fine-Tuning Example

```python
# Fine-tune Llama 3.1 with LoRA on Databricks
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model

# Load base model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

# Configure LoRA (only trains 0.1% of parameters)
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA adapters
model = get_peft_model(model, lora_config)

# Fine-tune on your data (e.g., customer support tickets)
# Training is 10x faster than full fine-tuning
trainer.train()

# Register in MLflow
mlflow.transformers.log_model(model, "llama-customer-support")
```

#### RAG Implementation Patterns

**Pattern 1: Simple RAG (Single Retrieval)**
```python
# 1. Retrieve relevant documents
retrieved_docs = vector_search.similarity_search(query, k=5)

# 2. Augment prompt with context
context = "\n".join([doc.page_content for doc in retrieved_docs])
prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

# 3. Generate response
response = llm.generate(prompt)
```

**Pattern 2: Advanced RAG (Re-ranking + Filtering)**
```python
from databricks.vector_search import VectorSearchClient

# 1. Initial retrieval (get 20 candidates)
candidates = vector_search.similarity_search(query, k=20)

# 2. Re-rank with cross-encoder
reranked = reranker.score(query, candidates)
top_docs = reranked[:5]

# 3. Filter by Databuck quality score
quality_filtered = [
    doc for doc in top_docs
    if databuck.get_doc_quality(doc.id) >= 0.8
]

# 4. Generate with filtered context
response = llm.generate_with_context(query, quality_filtered)
```

**Pattern 3: Agentic RAG (Multi-Step Reasoning)**
```python
from langchain.agents import AgentExecutor
from databricks.agents import DatabricksAgent

# Create agent with tools
tools = [
    vector_search_tool,      # Retrieve documents
    databuck_quality_tool,   # Check data quality
    sql_query_tool,          # Query structured data
    web_search_tool          # External knowledge
]

agent = DatabricksAgent(
    llm=llm,
    tools=tools,
    verbose=True
)

# Agent reasons about which tools to use
response = agent.run(
    "What were our Q3 sales trends and how do they compare to industry benchmarks?"
)
# Agent will:
# 1. Query SQL for Q3 sales
# 2. Search vector DB for industry reports
# 3. Synthesize answer with both sources
```

---

## Production Deployment Patterns

### Deployment Strategy Selection

#### Blue-Green Deployment

**Use when:** Zero-downtime deployments required, easy rollback needed

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Step 1: Deploy new model (green) alongside old (blue)
w.serving_endpoints.create(
    name="churn_predictor_green",
    config={
        "served_models": [{
            "model_name": "customer_churn_v2",
            "model_version": "5",
            "workload_size": "Small"
        }]
    }
)

# Step 2: Test green endpoint
test_green_endpoint()

# Step 3: Switch traffic from blue → green (instant)
w.serving_endpoints.update_config(
    name="churn_predictor",
    served_models=[{
        "model_name": "customer_churn_v2",
        "model_version": "5",
        "workload_size": "Small"
    }]
)

# Step 4: Decommission blue after 24h monitoring
```

#### Canary Deployment

**Use when:** Risk mitigation needed, gradual rollout preferred

```python
# Canary: Route 10% traffic to new model, 90% to old

w.serving_endpoints.update_config(
    name="churn_predictor",
    served_models=[
        {
            "model_name": "customer_churn_v1",
            "model_version": "4",
            "workload_size": "Small",
            "scale_to_zero_enabled": False,
            "traffic_percentage": 90  # Old model gets 90%
        },
        {
            "model_name": "customer_churn_v2",
            "model_version": "5",
            "workload_size": "Small",
            "scale_to_zero_enabled": False,
            "traffic_percentage": 10  # New model gets 10%
        }
    ]
)

# Monitor canary performance
monitor_canary_metrics(hours=24)

# Gradually increase: 10% → 25% → 50% → 100%
if canary_success:
    increase_traffic_percentage(50)
```

#### A/B Testing Deployment

**Use when:** Need to compare model performance statistically

```python
# A/B: Split traffic 50/50 for statistical comparison

w.serving_endpoints.update_config(
    name="churn_predictor",
    served_models=[
        {
            "name": "model_a",
            "model_name": "customer_churn_xgboost",
            "model_version": "3",
            "traffic_percentage": 50
        },
        {
            "name": "model_b",
            "model_name": "customer_churn_neural_net",
            "model_version": "2",
            "traffic_percentage": 50
        }
    ]
)

# Track metrics by variant
metrics_a = track_metrics(variant="model_a", days=14)
metrics_b = track_metrics(variant="model_b", days=14)

# Statistical test
if is_statistically_significant(metrics_a, metrics_b):
    winner = get_winner(metrics_a, metrics_b)
    route_all_traffic(winner)
```

#### Shadow Mode Deployment

**Use when:** Testing without impacting users, risk-free validation

```python
# Shadow: New model processes all requests but results aren't used

# Production model (serves actual responses)
primary_model = load_model("churn_v1")

# Shadow model (logs predictions but doesn't serve)
shadow_model = load_model("churn_v2")

def predict(features):
    # Primary prediction (returned to user)
    primary_pred = primary_model.predict(features)

    # Shadow prediction (logged for analysis)
    shadow_pred = shadow_model.predict(features)

    # Log comparison
    log_predictions(
        primary=primary_pred,
        shadow=shadow_pred,
        features=features
    )

    return primary_pred  # Only primary is used

# After 1 week, analyze shadow performance
shadow_analysis = compare_predictions(days=7)
if shadow_analysis.better_than_primary:
    promote_shadow_to_primary()
```

### Monitoring & Alerting Setup

```python
# Comprehensive monitoring with Databuck

from databricks.monitoring import Monitor

# Create monitoring job
monitor = Monitor(
    endpoint_name="churn_predictor",
    baseline_table="gold.customer_features",

    # Data drift monitoring
    drift_threshold=0.2,
    drift_features=["age", "income", "tenure"],

    # Model quality monitoring
    quality_metrics=["accuracy", "precision", "recall"],
    quality_threshold=0.85,

    # Performance monitoring
    latency_threshold_ms=100,
    error_rate_threshold=0.01,

    # Databuck integration
    databuck_quality_check=True,
    databuck_trust_score_min=80
)

# Alert configuration
monitor.add_alert(
    name="High Data Drift",
    condition="drift_score > 0.2",
    action="trigger_retraining",
    notification_email="ml-team@company.com"
)

monitor.add_alert(
    name="Model Quality Degradation",
    condition="accuracy < 0.85",
    action="rollback_to_previous_version",
    notification_slack="#ml-alerts"
)

# Start monitoring
monitor.start()
```

---

## Additional Resources

### Databricks Documentation
- [Machine Learning Guide](https://docs.databricks.com/machine-learning/index.html)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Model Serving](https://docs.databricks.com/machine-learning/model-serving/index.html)
- [Vector Search](https://docs.databricks.com/generative-ai/vector-search.html)
- [Foundation Models](https://docs.databricks.com/machine-learning/foundation-models/index.html)

### Databuck Resources
- Databuck by FirstEigen: [https://www.firsteigen.com/](https://www.firsteigen.com/)
- Data Quality for ML white paper
- Trust Score calculation methodology

### Training & Certification
- Databricks ML Associate Certification
- Databricks ML Professional Certification
- Generative AI with Databricks course

---

## Conclusion

Databricks provides a **complete AI/ML platform** that enables you to:
- ✅ Train models at scale with distributed computing
- ✅ Deploy production-ready ML pipelines with MLOps automation
- ✅ Build Generative AI applications with foundation models
- ✅ Implement RAG systems grounded in your enterprise data
- ✅ Create multi-agent AI systems for complex workflows
- ✅ Maintain data quality throughout with Databuck integration

**Key Takeaway**: The unified platform eliminates data silos, speeds up development, and ensures governance and security at every step.

**Next Steps**:
1. Review the architecture diagrams in `diagrams/` folder
2. Set up your Databricks workspace with Unity Catalog
3. Configure Databuck integration for data quality
4. Start with a simple ML use case (e.g., classification)
5. Expand to GenAI (RAG, fine-tuning, agents)

---

**Questions or feedback?** Contact the Databricks AI/ML team.
