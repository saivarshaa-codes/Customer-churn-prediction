# Customer Retention Intelligence System

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB.svg)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5%2B-E25A1C.svg)](https://spark.apache.org/)
[![Anthropic Claude](https://img.shields.io/badge/Claude%20AI-Sonnet%20%7C%20Haiku-D97706.svg)](https://www.anthropic.com/)

An enterprise-grade, end-to-end customer intelligence and predictive retention platform engineered for telecommunications providers. Built on the canonical **IBM Telco Customer Churn dataset** (7,043 subscriber records, 26.54% churn baseline), this platform features an integrated architecture spanning automated preprocessing, star-schema relational data warehousing, PySpark ETL pipelines, high-recall machine learning classification, high-throughput REST APIs, an executive React dashboard, and an autonomous Claude-powered AI retention assistant.

---

## Architectural Workflow

```text
                                 CUSTOMER DATA INGESTION
                     [WA_Fn-UseC_-Telco-Customer-Churn.csv]
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │ Phase 1: Python Core    │
                           │ Clean & Feature Engine  │
                           └────────────┬────────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
         ┌─────────────────────────────┐  ┌─────────────────────────────┐
         │ Phase 2: MySQL DB Layer     │  │ Phase 5: Data Engineering   │
         │ - dim_contract, dim_payment │  │ - PySpark ETL Ingestion     │
         │ - customers, fact_account   │  │ - Incremental Upserts       │
         │ - customer_ml_features      │  │ - Quality Gates (de7)       │
         └──────────────┬──────────────┘  └──────────────┬──────────────┘
                        │                                │
                        └───────────────┬────────────────┘
                                        ▼
                           ┌─────────────────────────┐
                           │ Phase 6: ML Pipeline    │
                           │ - Lab_ML/ml1.py         │
                           │ - DecisionTree (F1:0.62)│
                           │ - models/feature_columns│
                           └────────────┬────────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
         ┌─────────────────────────────┐  ┌─────────────────────────────┐
         │ Phase 3: FastAPI Backend    │  │ Phase 7 & 8: Claude AI      │
         │ - /customer/{id}            │  │ - Schema Contract (CL1)     │
         │ - /churn/summary            │  │ - Secret Leak Guard (CL2)   │
         │ - /customers/high-risk      │  │ - 4 JSON Schema Tools (AI2) │
         │ - /predict-churn            │  │ - Headless CI Review (AI4)  │
         └──────────────┬──────────────┘  │ - Benchmark Suite (AI5)     │
                        │                 └──────────────┬──────────────┘
                        ▼                                │
         ┌───────────────────────────────────────────────▼──────────────┐
         │ Phase 4: Modern React 19 UI Dashboard                         │
         │ 📊 Churn Analytics  🔍 Customer Search  ⚠️ High-Risk Queue   │
         │ 🔮 ML Churn Predictor                   🤖 Retention AI      │
         └──────────────────────────────────────────────────────────────┘
```

---

## Engineering Breakdown by Phase

### Phase 1: Python Core & Data Preprocessing (`Lab_CP`)
- **`customer_cleaner.py`**: Modular `CustomerCleaner` class performing programmatic standardization to `snake_case`, numeric coercion of `total_charges` with zero-tenure imputation, and binary normalization.
- **`customer_pipeline.py`**: Automated end-to-end pipeline generating production-ready feature matrices (`cleaned_file_*.csv`, `feature_file_*.csv`).
- **Feature Engineering (`lab_cp1.py` – `lab_cp4.py`)**: Derivation of high-value predictive signals including `high_charge_flag`, `is_long_term_customer`, `auto_pay_flag`, and `has_streaming_bundle`.

### Phase 2: Relational Data Warehouse & Star Schema (`Lab_SQL1`, `Lab_SQL2_3`)
- **Star Schema Architecture**: Normalized relational tables in MySQL (`telecom_db`):
  - `dim_contract`: Standardized contract tiers (`Month-to-month`, `One year`, `Two year`).
  - `dim_payment`: Payment channel classifications (`Electronic check`, `Mailed check`, `Bank transfer`, `Credit card`).
  - `customers`: Core subscriber demographic table.
  - `fact_customer_account`: Central account fact table linking tenure, recurring charges, and churn indicators.
  - `customer_ml_features`: Dedicated table storing engineered ML feature vectors.
  - `v_high_risk_customers`: Real-time view isolating month-to-month accounts with tenure under 12 months and above-average charges.

### Phase 3: High-Performance FastAPI Backend (`Lab_API`)
- **Production REST Microservices (`main.py`)**:
  - `GET /customer/{customer_id}`: High-speed profile lookup via SQLAlchemy ORM.
  - `GET /churn/summary`: Global retention metrics and segment aggregations.
  - `GET /customers/high-risk`: Prioritized worklist for customer success outreach.
  - `GET /customer/{customer_id}/features`: Feature vector retrieval for external model consumers.
  - `POST /predict-churn`: Real-time inference endpoint executing model predictions.
  - Comprehensive CORS support, typed Pydantic models, and structured exception handlers.

### Phase 4: Interactive React Dashboard (`customer-dashboard`)
- Built with React 19 and Vite:
  - **📊 Churn Analytics**: Global KPIs and proportional CSS distribution bars across contract types and internet service tiers.
  - **🔍 Customer Profile Search**: Instant lookup card displaying tenure, billing figures, and active/churn status.
  - **⚠️ High-Risk Queue**: Prioritized retention worklist with tenure-based sorting and incremental pagination ("Load More").
  - **🔮 ML Churn Predictor**: Real-time what-if scenario evaluator with color-coded risk indicators.
  - **🤖 Retention AI Assistant**: Conversational assistant interface featuring visible backend tool execution badges and retry logic.

### Phase 5: Production Data Engineering & PySpark (`data`)
- **Scalable Ingestion & Quality Gates**:
  - `de2_ingestion.py`: Schema validation with execution logging to `ingestion_log`.
  - `de3_cleaning.py`: Production ETL applying automated data transformations.
  - `de4_features.py`: Feature engineering pipeline stage populating `customer_ml_features`.
  - `de5_pyspark.py`: Distributed PySpark aggregation job analyzing multi-segment retention metrics.
  - `de6_upsert.py`: Incremental `ON DUPLICATE KEY UPDATE` upsert flow for daily extracts.
  - `de7_quality_checks.py`: Comprehensive automated quality gate enforcing null rates, value bounds, primary key uniqueness, row count thresholds, and distribution consistency.

### Phase 6: Machine Learning Pipeline (`Lab_ML`)
- **Model Training & Comparison (`Lab_ML/ml1.py`)**:
  - Trains and evaluates Logistic Regression and Decision Tree classifiers using stratified 5-fold cross-validation.
  - Prioritizes **Recall (63.10%)** and **F1-Score (0.6154)** on the Decision Tree to effectively identify churn candidates.
  - Persists production artifacts to `models/tree_churn.pkl` and `models/logistic_churn.pkl`.
  - Serializes the formal feature schema to `models/feature_columns.json`.
- **Inference & Batch Scoring**:
  - `Lab_ML/predict.py`: Real-time inference engine serving `POST /predict-churn`.
  - `Lab_ML/batch_score.py`: Daily automated batch scoring job generating `customer_risk_table.csv`.

### Phase 7: Claude AI Feature Synchronization & Security Boundaries (`Lab_CL`)
- **`audit_defect.py`**: Automated schema auditing using Claude API forced `tool_choice` (`report_defect_findings`), verifying full parity between training pipelines (`Lab_ML/ml1.py`) and runtime inference.
- **`predict_fixed.py`**: Calibrated multi-factor inference engine dynamically bound to `models/feature_columns.json`.
- **`run_cl1_experiment.py`**: Empirical validation confirming risk calibration across the full subscriber base:
  - Calibrated Model Churn Rate: **28.10%** *(aligned with ground truth: **26.54%**)*.
- **`project_context.py`**: Compact (<200 lines) durable enterprise memory prepended to LLM system prompts.
- **`prompt_loader.py`**: Secure template loader equipped with an automated **Secret-Leakage Guard** preventing environment variables from entering prompts, plus strict argument validation.
- **`security_review.py`**: Isolated human-directed code security auditing module.
- **`test_cl2_security.py`**: Automated test suite verifying template loading, bounds checks, and secret leakage prevention.

### Phase 8: Autonomous Retention AI Assistant (`Lab_AI`)
- **`assistant_api.py`**: Dedicated FastAPI service (`/assistant/chat`) featuring prompt caching (reducing input token costs by ~90%), bounded conversational history (last 8 turns), and cost-optimized model routing.
- **`tools.py`**: Four JSON Schema tools with analyst-level descriptions (`get_customer_profile`, `get_churn_summary`, `get_high_risk_customers`, `predict_customer_churn`) dispatched to backend logic within a 5-iteration bounded loop.
- **`daily_retention_brief.py`**: Headless pipeline automation generating executive daily retention briefings from aggregated segment deltas (zero PII exposure).
- **`code_review.py`**: Automated pre-push CI code auditor reading diffs from `stdin` and enforcing coding standards.
- **`eval_assistant.py`**: 15-question evaluation suite measuring factual accuracy, tool selection, and safe boundary refusal. Outputs `assistant_audit_log.json` and `evaluation_report.json`.

---

## Machine Learning Performance

| Model | Test Accuracy | Precision (Churned) | Recall (Churned) | F1-Score (Churned) | 5-Fold CV F1 | Production Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Decision Tree (Max Depth = 5)** | **79.06%** | **60.05%** | **63.10%** | **0.6154** | **0.5710** | **Primary Classifier** |
| **Logistic Regression** | 77.71% | 60.42% | 46.52% | 0.5257 | 0.5663 | Baseline Comparison |

> **Selection Rationale**: In telecom retention operations, missing a customer who is about to churn (False Negative) is significantly more costly than proactively reaching out to a customer who stays (False Positive). The Decision Tree was selected for production because it maximizes Recall (63.10%).

---

## AI Assistant Evaluation Benchmark

Evaluated using [`Lab_AI/eval_assistant.py`](Lab_AI/eval_assistant.py) across 15 standardized queries categorized into Single Checkable, Multi-Tool Reasoning, and Boundary Refusal cohorts:

```text
======================================================================
EVALUATION BENCHMARK RESULTS (Model: Claude 3.5 Sonnet)
======================================================================
Factual Accuracy Rate:         73.3%
Tool Selection Accuracy:        66.7%
Correct Refusal Rate:           60.0%
Cost per Conversation:          $0.0016
Projected Monthly Cost:         $35.97 (for 22,000 queries)
Prompt Caching Savings:         ~90% on input tokens
======================================================================
Audit Log: Lab_AI/assistant_audit_log.json
Report:    Lab_AI/evaluation_report.json
```

---

## Repository Structure

```text
Prodapt_Labs/
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment configuration template
├── .gitignore                        # Git ignore patterns
├── README.md                         # Project documentation
│
├── models/                           # TRAINED ML MODELS & SCHEMA CONTRACT
│   ├── logistic_churn.pkl            # Logistic Regression classifier
│   ├── tree_churn.pkl                # Decision Tree classifier (Primary)
│   └── feature_columns.json          # Persisted ML feature contract
│
├── Lab_CP/                           # PHASE 1: PYTHON CORE
│   ├── customer_cleaner.py           # Reusable data cleaner class
│   ├── customer_pipeline.py          # End-to-end data pipeline
│   ├── lab_cp1.py - lab_cp4.py       # EDA, business insights, and feature engineering
│   └── cutomer_cleaner_test.py       # Cleaner verification test
│
├── Lab_SQL1/                         # PHASE 2: DATABASE SETUP
│   └── table_creation.py             # DDL script creating relational schema
│
├── Lab_SQL2_3/                       # PHASE 2: ETL & ANALYTICAL SQL
│   ├── sql2.py                       # Data loading into staging tables
│   └── sql3.py                       # Analytical aggregations and views
│
├── Lab_API/                          # PHASE 3: FASTAPI BACKEND
│   ├── main.py                       # Core FastAPI application & endpoints
│   └── models.py                     # SQLAlchemy ORM models
│
├── customer-dashboard/               # PHASE 4: REACT 19 UI
│   ├── src/
│   │   ├── App.jsx                   # Main layout with 5-tab navigation
│   │   ├── App.css                   # Responsive styling & status colors
│   │   ├── api.js                    # API client configuration
│   │   └── pages/
│   │       ├── ChurnSummary.jsx      # Churn KPIs & distribution bars
│   │       ├── CustomerSearch.jsx    # Profile search card
│   │       ├── HighRiskCustomers.jsx # High-risk worklist table
│   │       ├── ChurnPrediction.jsx   # Real-time ML prediction form
│   │       └── AssistantPage.jsx     # Claude AI retention assistant
│   ├── package.json                  # Frontend dependencies
│   └── vite.config.js                # Vite build configuration
│
├── data/                             # PHASE 5: DATA ENGINEERING & PYSPARK
│   ├── connection.py                 # SQLAlchemy engine provider
│   ├── de2_ingestion.py              # Ingestion flow and logging
│   ├── de3_cleaning.py               # Automated cleaning flow
│   ├── de4_features.py               # Feature generation pipeline
│   ├── de5_pyspark.py                # PySpark aggregation job
│   ├── de6_upsert.py                 # Incremental upsert logic
│   └── de7_quality_checks.py         # Automated data quality gate
│
├── Lab_ML/                           # PHASE 6: MACHINE LEARNING
│   ├── ml1.py                        # Model training, CV comparison, and feature export
│   ├── predict.py                    # Real-time inference logic
│   └── batch_score.py                # Daily batch scoring job
│
├── Lab_CL/                           # PHASE 7: CLAUDE AI & SECURITY BOUNDARIES
│   ├── audit_defect.py               # Lab CL1: Automated schema parity auditor
│   ├── predict_fixed.py              # Lab CL1: Calibrated multi-factor inference engine
│   ├── run_cl1_experiment.py         # Lab CL1: Full-dataset empirical validation
│   ├── project_context.py            # Lab CL2: Durable project memory (<200 lines)
│   ├── prompt_loader.py              # Lab CL2: Template loader & secret guard
│   ├── security_review.py            # Lab CL2: Human-isolated security auditor
│   ├── test_cl2_security.py          # Lab CL2: Security test suite
│   └── prompts/                      # Lab CL2: Versioned prompt templates
│       ├── dataset_profiling_v1.txt
│       ├── scaffold_api_endpoint_v1.txt
│       └── security_review_v1.txt
│
└── Lab_AI/                           # PHASE 8: THE RETENTION AI ASSISTANT
    ├── assistant_api.py              # Lab AI1: Assistant backend (/assistant/chat)
    ├── tools.py                      # Lab AI2: 4 JSON Schema tools & request loop
    ├── ui/AssistantPage.jsx          # Lab AI3: Standalone React assistant page
    ├── daily_retention_brief.py      # Lab AI4: Headless daily pipeline briefing
    ├── code_review.py                # Lab AI4: Pre-push git diff auditor
    ├── install_git_hook.py           # Lab AI4: Git pre-push hook installer
    ├── eval_assistant.py             # Lab AI5: 15-question benchmark suite
    ├── assistant_audit_log.json      # Lab AI5: Execution audit log
    └── evaluation_report.json        # Lab AI5: Metrics report
```

---

## Executive UI Interface

The unified React 19 dashboard provides clean, focused views across five operational tabs:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  CUSTOMER RETENTION INTELLIGENCE SYSTEM                                                │
│  Enterprise Telecom Analytics · Machine Learning · AI Assistant                        │
│                                                                                        │
│  [ 📊 Churn Analytics ] [ 🔍 Customer Search ] [ ⚠️ High-Risk Queue ]                 │
│  [ 🔮 ML Churn Predictor ] [ 🤖 Retention AI Assistant ]                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  1. 📊 Churn Analytics:                                                                │
│     Total Customers: 7,043  │  Total Churned: 1,869  │  Churn Rate: 26.5%              │
│     • Month-to-month: [████████████████████                    ] 42.7%                 │
│     • One year:       [████                                    ] 11.3%                 │
│     • Two year:       [█                                       ]  2.8%                 │
│                                                                                        │
│  2. 🔍 Customer Search:                                                                │
│     Input: [ 7590-VHVEG ] [ Search ]                                                   │
│     Card: Tenure: 1 month | Contract: Month-to-month | Monthly: $29.85 | Status: Active │
│                                                                                        │
│  3. ⚠️ High-Risk Queue:                                                                │
│     Prioritized worklist with interactive sorting on Tenure, Charges, and Risk Reason  │
│                                                                                        │
│  4. 🔮 ML Churn Predictor:                                                             │
│     Inputs: Tenure: 2 | Monthly: $85 | Contract: Month-to-month | Services: 1          │
│     Result Badge: [ High Risk: 72.1% — Likely to churn ]                               │
│                                                                                        │
│  5. 🤖 Retention AI Assistant:                                                         │
│     Chat conversation window with prompt suggestions, bounded history (8 turns),       │
│     and visible backend tool badges:                                                   │
│     [ Tools Executed: get_customer_profile({"customer_id": "7590-VHVEG"}) ]            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quickstart Guide

### 1. Environment Installation
```bash
# Clone the repository and navigate to root
cd Prodapt_Labs

# Create and activate Python virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```
Ensure `.env` contains your Anthropic API key:
```env
ANTHROPIC_API_KEY=sk-ant-api...
```

### 3. Model Training & Schema Serialization
Train models, evaluate cross-validation metrics, and serialize feature metadata:
```bash
python Lab_ML/ml1.py
```

### 4. Launch Backend Services
Start the core FastAPI service:
```bash
uvicorn Lab_API.main:app --host 127.0.0.1 --port 8000 --reload
```

In a second terminal, start the AI Assistant service:
```bash
python Lab_AI/assistant_api.py
```
*(Interactive API documentation available at `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8001/docs`)*.

### 5. Launch React Dashboard
```bash
cd customer-dashboard
npm install
npm run dev
```
Navigate to `http://localhost:5173` to explore all five views.

### 6. Run Verification & Test Suites
```bash
# Phase 7: Automated schema audit & empirical calibration experiment
python Lab_CL/audit_defect.py
python Lab_CL/run_cl1_experiment.py

# Phase 7: Security checklist & secret-leakage guard test suite
python Lab_CL/test_cl2_security.py
python Lab_CL/security_review.py Lab_CL/predict_fixed.py

# Phase 8: Pipeline brief, CI review & 15-question evaluation suite
python Lab_AI/daily_retention_brief.py
python Lab_AI/code_review.py
python Lab_AI/eval_assistant.py

# Phase 5: Automated data quality checks
python -c "import sys; sys.path.insert(0, 'data'); from de7_quality_checks import *"

# Frontend: ESLint verification & production build
cd customer-dashboard
npm run lint
npm run build
```

---

## Enterprise Security & Data Governance

1. **Automated Secret-Leakage Guard**: `Lab_CL/prompt_loader.py` programmatically intercepts prompt compilations to guarantee that environment variables and credentials (`ANTHROPIC_API_KEY`, `API_KEY`) never enter prompt texts.
2. **Type Safety & Bounds Enforcement**: All endpoint and tool arguments undergo strict Pydantic schema validation before executing queries or running inference.
3. **Bounded Execution Loops**: Conversational LLM loops are capped at 5 iterations with bounded history (last 8 turns) to ensure predictable context and budget consumption.
4. **Human-in-the-Loop Isolation**: The security code auditor is strictly isolated in `Lab_CL/security_review.py` and cannot be triggered by automated pipelines.
5. **PII Protection**: Aggregated daily pipeline briefings operate exclusively on cohort-level metrics, preventing personal identifying information from transmitting over external networks.
