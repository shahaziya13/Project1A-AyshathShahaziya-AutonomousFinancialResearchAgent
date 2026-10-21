# Autonomous Financial Research Agent (ARA-1)

## Project Overview

The **Autonomous Financial Research Agent (ARA-1)** is an agentic AI system designed to perform multi-step financial research using planning, tool execution, evidence collection, memory, verification, calculation, comparison, and structured report generation.

The project follows a hybrid **Plan-and-Execute + ReAct** architecture.

Given a financial research query, ARA-1 is designed to:

1. Understand the research objective.
2. Create a research plan.
3. Select appropriate tools.
4. Execute tools through a centralized registry.
5. Collect evidence from multiple sources.
6. Store and retrieve useful research through memory.
7. Compare and verify financial information.
8. Identify conflicts, missing data, and limitations.
9. Perform deterministic financial calculations.
10. Generate a structured research report.

The system emphasizes evidence-grounded financial research rather than unsupported generation.

---

## Core Features

- Hybrid Plan-and-Execute + ReAct agent architecture
- Centralized registry containing 12 financial research tools
- OpenAI-function-style JSON tool schemas
- Tool input validation and standardized responses
- Mock implementations for safe development and testing
- Real financial and research data integrations
- SEC EDGAR filing retrieval
- Yahoo Finance-based financial data retrieval
- Tavily-powered web research
- News sentiment analysis using VADER
- Public earnings-transcript discovery
- Parent-company peer comparison
- Deterministic financial calculations
- Cross-source fact checking
- Structured Markdown report generation
- Persistent ChromaDB vector memory
- Short-term context management
- Episodic memory
- Vector-memory search and storage tools
- Environment-based configuration
- Retry and rate-limit handling
- API caching
- Agent and tool logging
- Automated testing with Pytest
- Progressive financial research challenges

---

## Current Development Status

Completed development phases:

- Day 1 - Agent Architecture Specification
- Day 2 - Tool Registry Design and Implementation
- Day 3 - Environment Setup and LLM Integration
- Day 4 - Core Agent Loop Implementation
- Day 5 - Real API Integration
- Day 6 - Memory System Implementation
- Day 7 - Complete Tool Implementation

### Research Challenges Completed

- Challenge 1 - Microsoft Company Profile
- Challenge 2 - Apple Quarterly Earnings Research
- Challenge 3 - Tesla Risk Assessment
- Challenge 4 - AWS vs Azure vs Google Cloud Comparison

The project currently has all **12 planned research tools registered**, with real implementations available for the core research workflow.

Development continues with advanced synthesis, conflict resolution, verification, evaluation, stress testing, and optimization phases.

---

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
- yfinance
- VADER Sentiment
- Tavily Search API
- SEC EDGAR

---

## Project Structure

```text
Project1A-AyshathShahaziya-AutonomousFinancialResearchAgent/
|
|-- agent/
|   |-- __init__.py
|   |-- core.py
|   |-- llm_client.py
|   |-- parser.py
|   `-- prompts.py
|
|-- config/
|   |-- __init__.py
|   |-- settings.py
|   |-- logging_config.py
|   `-- vector_db.py
|
|-- docs/
|   |-- architecture_diagram.md
|   `-- architecture_diagram.png
|
|-- memory/
|   |-- context_manager.py
|   |-- episodic.py
|   `-- vector_store.py
|
|-- tools/
|   |-- schemas/
|   |   |-- __init__.py
|   |   `-- tool_schemas.py
|   |
|   |-- __init__.py
|   |-- api_utils.py
|   |-- calculation_engine.py
|   |-- earnings_transcript.py
|   |-- fact_checker.py
|   |-- financial_api.py
|   |-- memory_tools.py
|   |-- mock_tools.py
|   |-- news_sentiment.py
|   |-- peer_comparison.py
|   |-- report_generator.py
|   |-- sec_edgar.py
|   |-- tool_registry.py
|   `-- web_search.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_agent.py
|   |-- test_memory.py
|   `-- test_tools.py
|
|-- results/
|   |-- challenge_1.md
|   |-- challenge_2.md
|   |-- challenge_3.md
|   `-- challenge_4.md
|
|-- synthesis/
|-- evaluation/
|
|-- architecture_specification.md
|-- ERROR_LOG.md
|-- .env.example
|-- .gitignore
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Project1A-AyshathShahaziya-AutonomousFinancialResearchAgent
```

### 2. Create a Virtual Environment

Windows PowerShell:

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

---

## Environment Configuration

Create a local `.env` file from the example configuration.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

The project supports mock LLM operation:

```text
LLM_PROVIDER=mock
```

This allows development and testing without requiring paid LLM usage.

To use OpenAI, configure the appropriate environment variables:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_name
```

External research services may require their corresponding API credentials.

Never commit the `.env` file or real API keys to Git.

---

## Agent Architecture

ARA-1 follows a hybrid:

**Plan-and-Execute + ReAct**

architecture.

High-level workflow:

```text
User Query
    |
    v
Query Analysis
    |
    v
Research Planning
    |
    v
Agent Controller
    |
    v
Tool Registry
    |
    v
Evidence Collection
    |
    v
Memory / Context Assembly
    |
    v
Multi-Source Synthesis
    |
    v
Conflict Resolution
    |
    v
Fact Verification
    |
    v
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

---

## Core Agent Loop

The main agent implementation is located in:

```text
agent/core.py
```

Supporting components include:

```text
agent/prompts.py
agent/parser.py
agent/llm_client.py
```

The agent controls iterative research execution while enforcing iteration limits and structured tool usage.

Operational logs record concise decisions, actions, tool observations, and errors without storing private hidden chain-of-thought.

---

## Tool Registry

ARA-1 defines 12 financial research tools.

1. `sec_filing_search`
2. `web_search`
3. `earnings_transcript`
4. `financial_data_api`
5. `news_sentiment`
6. `vector_db_search`
7. `vector_db_store`
8. `company_profile`
9. `peer_comparison`
10. `report_generator`
11. `fact_checker`
12. `calculation_engine`

The registry is implemented in:

```text
tools/tool_registry.py
```

Tool schemas are stored in:

```text
tools/schemas/tool_schemas.py
```

The registry performs tool discovery, input validation, dispatch, and standardized error handling.

---

## SEC Filing Research

SEC filing retrieval is implemented in:

```text
tools/sec_edgar.py
```

The tool uses SEC EDGAR data to locate company filings such as 10-K reports.

The implementation includes:

- Company/CIK resolution
- Filing metadata retrieval
- Filing-date information
- Report-period information
- Filing URLs
- Rate limiting
- Caching

---

## Financial Data

Financial data retrieval is implemented in:

```text
tools/financial_api.py
```

The implementation uses Yahoo Finance data through `yfinance`.

Depending on data availability, retrieved metrics can include:

- Market capitalization
- Revenue
- Net income
- Profit margin
- Revenue growth
- EPS
- P/E ratio
- Company profile information

Financial values are time-sensitive and depend on the upstream data provider.

---

## Web Research

Web research is implemented in:

```text
tools/web_search.py
```

The current implementation uses Tavily for external research discovery.

It is used to supplement regulatory and financial-data sources with relevant public web evidence.

---

## News Sentiment

News sentiment analysis is implemented in:

```text
tools/news_sentiment.py
```

The tool combines retrieved news evidence with VADER sentiment scoring.

Sentiment scores are treated as supporting signals rather than definitive financial conclusions because lexical sentiment models may not fully understand complex financial context.

---

## Earnings Transcript Research

Public earnings-transcript discovery is implemented in:

```text
tools/earnings_transcript.py
```

The tool retrieves relevant public transcript sources and excerpts.

The current implementation does not claim that retrieved excerpts represent a complete transcript.

A known limitation is that a request for the `"latest"` quarter may return results from multiple reporting periods. This limitation is documented in the research results and should be improved through fiscal-period normalization and chronological ranking.

---

## Peer Comparison

Peer comparison is implemented in:

```text
tools/peer_comparison.py
```

It compares multiple companies using standardized financial metrics retrieved through the financial-data layer.

Supported comparison metrics include values such as:

- Market capitalization
- Revenue
- Net income
- Profit margin
- Revenue growth
- EPS
- P/E ratio

The tool also identifies metric leaders when comparable numerical values are available.

---

## Calculation Engine

Deterministic calculations are implemented in:

```text
tools/calculation_engine.py
```

Supported operations include:

- Percentage change
- Profit margin
- Current ratio
- Debt-to-equity ratio
- Basic discounted cash flow calculation

Using deterministic calculations helps reduce arithmetic errors in financial research.

---

## Fact Checker

Cross-source verification is implemented in:

```text
tools/fact_checker.py
```

The fact checker evaluates evidence from multiple sources and can identify:

- Supporting evidence
- Conflicting evidence
- Numerical disagreement
- Insufficient evidence

Numerical disagreement can be evaluated using a configurable tolerance threshold.

---

## Report Generator

Structured Markdown report generation is implemented in:

```text
tools/report_generator.py
```

Reports can contain:

- Research title
- Research query
- Structured sections
- Sources
- Confidence information
- Limitations

The report generator provides a consistent final output structure for research tasks.

---

## Memory Architecture

ARA-1 uses a three-layer memory architecture.

### Short-Term Memory

Implemented through:

```text
memory/context_manager.py
```

It manages relevant working context and selective retention.

### Long-Term Vector Memory

Implemented through:

```text
memory/vector_store.py
```

ChromaDB provides persistent semantic storage and retrieval.

The configured collection is:

```text
financial_research_memory
```

### Episodic Memory

Implemented through:

```text
memory/episodic.py
```

Episodic memory stores useful information about previous research execution, strategies, and errors.

### Memory Tools

The agent accesses long-term memory through:

```text
vector_db_search
vector_db_store
```

This allows previous research evidence to be reused in later research tasks.

---

## Research Challenges

### Challenge 1 - Microsoft Company Profile

ARA-1 retrieved and organized company-profile and financial information for Microsoft.

Result:

```text
results/challenge_1.md
```

### Challenge 2 - Apple Quarterly Earnings Research

ARA-1 performed multi-source quarterly earnings research for Apple.

Result:

```text
results/challenge_2.md
```

### Challenge 3 - Tesla Risk Assessment

ARA-1 used SEC filings, financial data, web evidence, news sentiment, and earnings-transcript discovery to perform a risk assessment of Tesla.

The challenge also documented limitations in lexical sentiment analysis and transcript-period retrieval.

Result:

```text
results/challenge_3.md
```

### Challenge 4 - AWS vs Azure vs Google Cloud

ARA-1 compared AWS, Microsoft Azure, and Google Cloud using:

- Parent-company financial data
- SEC filings
- Cloud-specific web evidence
- Earnings transcripts
- Peer comparison
- Deterministic calculations

The research explicitly distinguishes parent-company metrics from cloud-segment metrics and avoids inventing missing standalone Azure revenue.

Result:

```text
results/challenge_4.md
```

---

## Testing

Run the complete automated test suite with:

```bash
python -m pytest -v
```

Tests cover components including:

- Tool registry behavior
- Tool validation
- Core agent behavior
- Memory functionality
- Deterministic calculations
- Error handling

The test suite should be run before each development-phase commit to confirm that new changes have not broken existing functionality.

---

## Error Handling

ARA-1 is designed to handle research failures transparently.

The architecture supports:

- Retry handling
- Exponential backoff
- Rate limiting
- Caching
- Standardized tool errors
- Source fallback strategies
- Missing-data disclosure
- Graceful degradation

When reliable evidence is unavailable, the system should state the limitation rather than fabricate a result.

---

## Logging

Application logs are written to:

```text
logs/agent.log
```

The logging system records concise operational information such as:

- Agent decisions
- Tool calls
- Tool observations
- LLM requests
- Errors
- Memory operations

Sensitive credentials and private hidden chain-of-thought are not logged.

---

## Security

- API credentials are loaded through environment variables.
- `.env` is excluded from version control.
- `.env.example` contains placeholders only.
- Generated logs are excluded from Git where appropriate.
- Runtime vector-database data is excluded from Git.
- Tool inputs are validated before execution.
- Errors are handled without intentionally exposing credentials.
- Private hidden chain-of-thought is not stored as application logging output.

---

## Known Limitations

Current limitations include:

- External financial data depends on upstream provider availability.
- Web-search quality depends on retrieved sources.
- News sentiment is lexical and may miss financial nuance.
- Earnings-transcript `"latest"` retrieval can include multiple reporting periods.
- Some companies disclose business-segment data differently, reducing direct comparability.
- Cloud-segment comparisons may require different evidence than parent-company comparisons.
- Full advanced synthesis and evaluation phases are still under development.

These limitations are documented rather than hidden from the final research output.

---

## AI Assistance

AI assistance is used during development for implementation guidance, debugging support, documentation assistance, and code review.

Generated code and documentation are reviewed and tested against project requirements before inclusion in the repository.

---

## Author

**Ayshath Shahaziya**

Project: **Autonomous Financial Research Agent (ARA-1)**

Project Type: **Agentic AI / Financial Research System**