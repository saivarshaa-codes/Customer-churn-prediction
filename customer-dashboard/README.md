# Customer Retention Intelligence — Frontend Dashboard

A modern React 19 single-page application built with Vite, serving as the interactive user interface for the **Customer Retention Intelligence System**.

## Features & Modules

The dashboard provides a unified navigation interface across five primary business modules:

1. **📊 Churn Analytics Overview** (`ChurnSummary.jsx`):
   - Real-time KPIs: Total Customer Volume (7,043), Total Churned (1,869), and Baseline Churn Rate (26.54%).
   - Interactive churn rate distribution bars segmented by Contract Type and Internet Service.
2. **🔍 Customer Profile Search** (`CustomerSearch.jsx`):
   - On-demand customer lookup by ID (e.g., `7590-VHVEG`).
   - Displays tenure, contract type, monthly charges, and active/churn status badge.
3. **⚠️ High-Risk Customer Queue** (`HighRiskCustomers.jsx`):
   - Prioritized worklist for customer success and retention outreach.
   - Interactive sorting by customer tenure, monthly charges, and highlighted risk drivers.
   - Incremental pagination ("Load More").
4. **🔮 Machine Learning Churn Predictor** (`ChurnPrediction.jsx`):
   - Real-time what-if scenario evaluator powered by the trained Decision Tree classifier.
   - Interactive inputs: tenure, monthly recurring charges, contract type, and subscribed service count.
   - Displays predicted risk percentage, categorization, and confidence level.
5. **🤖 Retention AI Assistant** (`AssistantPage.jsx`):
   - Autonomous conversational assistant powered by Claude 3.5 Sonnet and verified backend tools.
   - Features visible tool execution audit badges under every response.
   - Bounded conversation history (last 8 turns) and automatic retry mechanism on failure.

## Getting Started

### Prerequisites
- Node.js 18+ and npm

### Installation
```bash
npm install
```

### Environment Configuration
Copy `.env.example` to `.env`:
```bash
VITE_API_URL=http://localhost:8000
VITE_ASSISTANT_API_URL=http://localhost:8001/assistant/chat
```

### Development Server
```bash
npm run dev
```
The dashboard will be available at `http://localhost:5173`.

### Production Build & Linting
```bash
# Verify code quality with ESLint
npm run lint

# Compile production bundle
npm run build
```
