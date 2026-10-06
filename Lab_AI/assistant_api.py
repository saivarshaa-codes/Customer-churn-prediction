"""
Lab_AI/assistant_api.py — FastAPI Endpoint for Claude-Powered Retention Assistant
Lab AI1: Backend integration with Claude, Anthropic client, prompt caching, model comparison.
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure project root is in path
sys.path.insert(0, os.path.abspath("."))

from Lab_CL.project_context import get_system_context
from Lab_AI.tools import run_assistant_request

load_dotenv()

# Module-level Anthropic Client Construction
api_key = os.getenv("ANTHROPIC_API_KEY")
client = None
if api_key and api_key != "your_claude_api_key_here":
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        print(f"Warning: Anthropic client failed to initialize: {e}")

# Base System Prompt incorporating durable project memory
BASE_SYSTEM_PROMPT = f"""
{get_system_context()}

## Retention Assistant Operating Guidelines:
1. You are the AI Customer Retention Analyst for this telecom operator.
2. Ground all answers in tool data. NEVER state a customer churn percentage, status, or prediction without running the corresponding tool.
3. If a customer is not found, state clearly that the customer does not exist in the record.
4. When explaining churn risk, highlight actionable factors: contract duration, payment method, tenure, and internet service type.
"""

# Model Selection & Cost Matrix
MODEL_COMPARISON_TABLE = [
    {
        "model": "claude-3-5-sonnet-20241022",
        "input_cost_per_mtok": "$3.00",
        "output_cost_per_mtok": "$15.00",
        "cache_write_per_mtok": "$3.75",
        "cache_read_per_mtok": "$0.30",
        "context_window": "200,000 tokens",
        "recommended_role": "Primary interactive retention assistant, complex tool orchestration, multi-step queries."
    },
    {
        "model": "claude-3-haiku-20240307",
        "input_cost_per_mtok": "$0.25",
        "output_cost_per_mtok": "$1.25",
        "cache_write_per_mtok": "$0.30",
        "cache_read_per_mtok": "$0.03",
        "context_window": "200,000 tokens",
        "recommended_role": "High-throughput batch jobs, daily brief delta summaries, simple classification."
    },
    {
        "model": "claude-3-opus-20240229",
        "input_cost_per_mtok": "$15.00",
        "output_cost_per_mtok": "$75.00",
        "cache_write_per_mtok": "$18.75",
        "cache_read_per_mtok": "$1.50",
        "context_window": "200,000 tokens",
        "recommended_role": "Strategic executive analysis and long-form synthesis."
    }
]

app = FastAPI(
    title="Customer Retention AI Assistant API",
    description="Claude-powered retention assistant with tool use, prompt caching, and guardrails",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Customer Retention AI Assistant API",
        "endpoints": {
            "chat": "POST /assistant/chat",
            "models": "GET /assistant/models",
            "docs": "/docs"
        }
    }

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: list[dict] = Field(default=[], description="Previous conversation turns (max 8)")

class ChatResponse(BaseModel):
    reply: str
    tools_called: list[dict]
    usage: dict
    iterations: int

@app.get("/assistant/models")
def get_model_matrix():
    """Returns the pricing, token limits, and task-fit comparison table for Claude models."""
    return {
        "models": MODEL_COMPARISON_TABLE,
        "recommended_production_model": "claude-3-5-sonnet-20241022",
        "caching_benefit": "Prompt caching reduces input token cost by ~90% on repeated system prompts."
    }

@app.post("/assistant/chat", response_model=ChatResponse)
def assistant_chat(request: ChatRequest):
    """
    POST /assistant/chat
    Interacts with the Retention AI Assistant, executing tools as needed.
    """
    # 1. Bounded conversation history (last 8 turns)
    bounded_history = request.history[-8:] if len(request.history) > 8 else list(request.history)
    bounded_history.append({"role": "user", "content": request.message})

    # 2. Execute assistant loop
    result = run_assistant_request(
        messages=bounded_history,
        system_prompt=BASE_SYSTEM_PROMPT,
        client=client,
        model="claude-3-5-sonnet-20241022"
    )

    return result

if __name__ == "__main__":
    import uvicorn
    print("Starting Assistant API server on http://localhost:8001...")
    uvicorn.run("Lab_AI.assistant_api:app", host="127.0.0.1", port=8001, reload=True)
