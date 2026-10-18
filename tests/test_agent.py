"""Tests for the core Autonomous Financial Research Agent."""

import pytest

from agent.core import FinancialResearchAgent
from agent.parser import AgentResponseParser
from agent.prompts import build_system_prompt
from tools.schemas.tool_schemas import TOOL_SCHEMAS


def test_system_prompt_contains_tools():
    """System prompt should contain registered tools."""

    prompt = build_system_prompt(TOOL_SCHEMAS)

    assert "company_profile" in prompt
    assert "financial_data_api" in prompt
    assert "sec_filing_search" in prompt


def test_parser_tool_call():
    """Parser should correctly parse a tool request."""

    parser = AgentResponseParser()

    response = parser.parse(
        """
        {
            "type": "tool_call",
            "tool": "company_profile",
            "arguments": {
                "company": "Microsoft"
            },
            "decision_summary": "Need company information."
        }
        """
    )

    assert response.response_type == "tool_call"
    assert response.tool == "company_profile"
    assert response.arguments["company"] == "Microsoft"


def test_parser_final_response():
    """Parser should correctly parse a final response."""

    parser = AgentResponseParser()

    response = parser.parse(
        """
        {
            "type": "final",
            "answer": "Research complete.",
            "decision_summary": "Enough evidence collected."
        }
        """
    )

    assert response.response_type == "final"
    assert response.answer == "Research complete."


def test_parser_rejects_invalid_response():
    """Parser should reject unsupported response types."""

    parser = AgentResponseParser()

    with pytest.raises(ValueError):
        parser.parse(
            """
            {
                "type": "unknown"
            }
            """
        )


def test_agent_rejects_empty_query():
    """Agent should reject an empty research query."""

    agent = FinancialResearchAgent()

    with pytest.raises(ValueError):
        agent.run("")


def test_agent_rejects_invalid_iteration_limit():
    """Agent should require at least one iteration."""

    with pytest.raises(ValueError):
        FinancialResearchAgent(max_iterations=0)


def test_microsoft_challenge_mock():
    """Challenge 1 should complete using the mock company tool."""

    agent = FinancialResearchAgent()

    result = agent.run(
        "Research Microsoft and provide a basic company profile."
    )

    assert result.status == "completed"
    assert result.iterations == 2
    assert len(result.steps) == 1
    assert result.steps[0].tool == "company_profile"
    assert result.steps[0].arguments["company"] == "Microsoft"
    assert result.steps[0].observation["success"] is True


def test_mock_agent_respects_company_name():
    """Mock agent should identify supported company names."""

    agent = FinancialResearchAgent()

    result = agent.run(
        "Research Apple and provide a company profile."
    )

    assert result.status == "completed"
    assert result.steps[0].arguments["company"] == "Apple"