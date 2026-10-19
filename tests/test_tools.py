"""Tests for the ARA-1 tool registry and mock tools."""

import pytest

from tools.mock_tools import calculation_engine
from tools.tool_registry import ToolRegistry


@pytest.fixture
def registry():
    """Create a fresh tool registry for each test."""
    return ToolRegistry()


def test_registry_contains_12_tools(registry):
    """Registry should contain all 12 required research tools."""
    tools = registry.list_tools()

    assert len(tools) == 12
    assert "sec_filing_search" in tools
    assert "financial_data_api" in tools
    assert "fact_checker" in tools
    assert "calculation_engine" in tools


def test_company_profile(registry):
    """Company profile tool should execute successfully."""

    result = registry.execute(
        "company_profile",
        {"company": "Microsoft"},
    )

    assert result["success"] is True
    assert result["tool"] == "company_profile"

    data = result["data"]

    assert data["ticker"] == "MSFT"
    assert data["company_name"]
    assert data["sector"]
    assert result["source"] == "Yahoo Finance via yfinance"


def test_web_search(registry):
    """Web search mock should respect max_results."""
    result = registry.execute(
        "web_search",
        {
            "query": "Microsoft artificial intelligence",
            "max_results": 3,
        },
    )

    assert result["success"] is True
    assert result["tool"] == "web_search"
    assert len(result["data"]["results"]) == 3


def test_financial_data_api(registry):
    """Financial data tool should return requested real metrics."""

    result = registry.execute(
        "financial_data_api",
        {
            "company": "Apple",
            "metrics": [
                "total_revenue",
                "net_income",
            ],
            "period": "latest",
        },
    )

    assert result["success"] is True
    assert result["tool"] == "financial_data_api"

    data = result["data"]

    assert data["ticker"] == "AAPL"
    assert data["company_name"]
    assert "total_revenue" in data
    assert "net_income" in data
    assert result["source"] == "Yahoo Finance via yfinance"


def test_calculation_engine_percentage_change(registry):
    """Percentage change calculation should be correct."""
    result = registry.execute(
        "calculation_engine",
        {
            "operation": "percentage_change",
            "values": [100, 125],
        },
    )

    assert result["success"] is True
    assert result["data"]["result"] == pytest.approx(25.0)


def test_calculation_engine_division(registry):
    """Division should return the expected value."""
    result = registry.execute(
        "calculation_engine",
        {
            "operation": "divide",
            "values": [100, 4],
        },
    )

    assert result["success"] is True
    assert result["data"]["result"] == pytest.approx(25.0)


def test_division_by_zero_is_handled(registry):
    """Division by zero should produce a controlled error."""
    result = registry.execute(
        "calculation_engine",
        {
            "operation": "divide",
            "values": [100, 0],
        },
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert "Division by zero" in result["error"]


def test_missing_required_argument(registry):
    """Missing required input should fail validation."""
    result = registry.execute(
        "company_profile",
        {},
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert "company" in result["error"]


def test_unknown_tool(registry):
    """Unknown tools should return a controlled error."""
    result = registry.execute(
        "unknown_tool",
        {},
    )

    assert result["success"] is False
    assert result["error_type"] == "KeyError"


def test_invalid_max_results(registry):
    """max_results above the schema limit should be rejected."""
    result = registry.execute(
        "web_search",
        {
            "query": "NVIDIA financial news",
            "max_results": 100,
        },
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"


def test_peer_comparison_requires_two_companies(registry):
    """Peer comparison should require at least two companies."""
    result = registry.execute(
        "peer_comparison",
        {
            "companies": ["Microsoft"],
        },
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"


def test_invalid_calculation_operation(registry):
    """Unsupported calculation operations should be rejected."""
    result = registry.execute(
        "calculation_engine",
        {
            "operation": "power",
            "values": [2, 3],
        },
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"


def test_direct_calculation_function():
    """Direct calculation implementation should also work."""
    result = calculation_engine(
        "add",
        [10, 20, 30],
    )

    assert result["success"] is True
    assert result["data"]["result"] == pytest.approx(60.0)