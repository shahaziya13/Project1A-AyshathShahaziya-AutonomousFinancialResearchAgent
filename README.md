# Autonomous Financial Research Agent (ARA-1)

## Project Overview

The Autonomous Financial Research Agent (ARA-1) is an agentic AI system designed to perform multi-step financial research using planning, tool execution, evidence collection, verification, memory, and report generation.

The project follows a hybrid **Plan-and-Execute + ReAct** architecture. The agent is designed to receive a financial research query, create a research plan, select appropriate tools, collect information from multiple sources, resolve conflicting evidence, verify important claims, and produce a structured financial research report.

## Core Features

- Hybrid Plan-and-Execute + ReAct agent architecture
- Registry of 12 financial research tools
- JSON-schema-based tool validation
- Mock tools for safe development and testing
- LLM abstraction layer
- Automatic LLM retry handling
- LLM token usage tracking
- Persistent ChromaDB vector database
- Environment-based configuration management
- Agent, tool-call, observation, and error logging
- Multi-source financial research architecture
- Three-layer memory architecture
- Conflict resolution and fact-verification design
- Automated testing with pytest

## Current Development Status

Completed:

- Day 1 — Agent Architecture Specification
- Day 2 — Tool Registry Design and Implementation
- Day 3 — Environment Setup and LLM Integration

The project currently supports mock LLM operation so that development and testing can continue without requiring paid API access.

## Technology Stack

- Python 3.12
- OpenAI Python SDK
- ChromaDB
- Pydantic
- Tenacity
- HTTPX
- Tiktoken
- python-dotenv
- Rich
- Pytest

## Project Structure

```text
Project1A-AyshathShahaziya-AutonomousFinancialResearchAgent/
│
├── agent/
│   ├── __init__.py
│   └── llm_client.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── logging_config.py
│   └── vector_db.py
│
├── docs/
│   ├── architecture_diagram.md
│   └── architecture_diagram.png
│
├── tools/
│   ├── __init__.py
│   ├── mock_tools.py
│   ├── tool_registry.py
│   └── schemas/
│       ├── __init__.py
│       └── tool_schemas.py
│
├── tests/
│   ├── __init__.py
│   └── test_tools.py
│
├── memory/
├── synthesis/
├── evaluation/
├── results/
│
├── architecture_specification.md
├── ERROR_LOG.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Project1A-AyshathShahaziya-AutonomousFinancialResearchAgent
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Environment Configuration

Copy the example environment configuration:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

The project defaults to mock LLM mode:

```text
LLM_PROVIDER=mock
```

This allows the project to run without an API key.

To use an OpenAI model, configure:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_name
```

Never commit the `.env` file or real API keys to GitHub.

## LLM Integration

The LLM client is located at:

```text
agent/llm_client.py
```

It provides:

- Mock LLM mode
- OpenAI API integration
- Retry handling
- Token usage tracking
- Request/error logging

## Vector Database

ARA-1 uses ChromaDB for persistent long-term vector memory.

The configured collection is:

```text
financial_research_memory
```

Persistent ChromaDB data is stored locally in:

```text
chromadb_data/
```

Generated database files are excluded from Git.

The full embedding, storage, retrieval, and memory pipeline is implemented during the memory-system phase of the project.

## Logging

Application logs are written to:

```text
logs/agent.log
```

The logging system records concise operational information including:

- Agent decisions
- Tool calls
- Tool observations
- LLM requests
- Errors
- Vector database initialization

Sensitive API credentials and private hidden chain-of-thought are not logged.

## Running Tests

Run:

```bash
python -m pytest -v
```

Current Day 2 tool-registry test suite:

```text
13 passed
```

## Tool Registry

The project defines 12 research tools:

1. SEC Filing Search
2. Web Search
3. Earnings Transcript
4. Financial Data API
5. News Sentiment
6. Vector DB Search
7. Vector DB Store
8. Company Profile
9. Peer Comparison
10. Report Generator
11. Fact Checker
12. Calculation Engine

During the initial development stage, realistic mock implementations are used before integration with external APIs.

## Architecture

ARA-1 follows a hybrid:

**Plan-and-Execute + ReAct**

workflow.

High-level flow:

```text
User Query
    ↓
Query Analysis
    ↓
Research Planning
    ↓
Agent Controller
    ↓
Tool Registry
    ↓
Evidence Collection
    ↓
RAG / Context Assembly
    ↓
Multi-Source Synthesis
    ↓
Conflict Resolution
    ↓
Fact Verification
    ↓
Research Report
```

The complete architecture specification is available in:

```text
architecture_specification.md
```

The architecture diagram is available in:

```text
docs/architecture_diagram.png
```

## Security

- API credentials are loaded through environment variables.
- `.env` is excluded from version control.
- `.env.example` contains placeholders only.
- Generated logs and vector database files are excluded from Git.
- Tool inputs are validated before execution.
- Errors are handled without exposing credentials.

## AI Assistance

AI assistance is used during development for implementation guidance, debugging support, documentation assistance, and code review.

All generated code is tested and reviewed against the project requirements before inclusion in the repository.

## Author

**Ayshath Shahaziya**

Project: **Autonomous Financial Research Agent (ARA-1)**

Project Type: **Agentic AI / Financial Research System**