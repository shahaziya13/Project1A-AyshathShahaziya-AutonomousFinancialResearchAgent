from evaluation.failure_simulator import FailureSimulator
from evaluation.fallback_manager import FallbackManager


def successful_tool(**kwargs):
    return {
        "success": True,
        "data": kwargs,
    }


def test_zero_failure_rate():
    simulator = FailureSimulator(
        failure_rate=0.0,
        seed=42,
    )

    result = simulator.execute(
        "financial_data_api",
        successful_tool,
        company="NVIDIA",
    )

    assert result["success"] is True
    assert result["simulated_failure"] is False


def test_full_failure_rate():
    simulator = FailureSimulator(
        failure_rate=1.0,
        seed=42,
    )

    result = simulator.execute(
        "sec_filing_search",
        successful_tool,
        company="NVIDIA",
    )

    assert result["success"] is False
    assert result["simulated_failure"] is True


def test_configured_fifty_percent_rate():
    simulator = FailureSimulator(
        failure_rate=0.5,
        seed=42,
    )

    assert simulator.failure_rate == 0.5


def test_failure_statistics():
    simulator = FailureSimulator(
        failure_rate=1.0,
        seed=42,
    )

    for _ in range(4):
        simulator.execute(
            "financial_data_api",
            successful_tool,
        )

    stats = simulator.statistics()

    assert stats["attempts"] == 4
    assert stats["failures"] == 4
    assert stats["observed_failure_rate"] == 1.0


def test_primary_source_success():
    manager = FallbackManager()

    result = manager.execute_chain(
        "primary",
        lambda: {"success": True, "data": "primary"},
        [
            (
                "fallback",
                lambda: {"success": True, "data": "fallback"},
            )
        ],
    )

    assert result["success"] is True
    assert result["fallback_used"] is False
    assert result["used_source"] == "primary"


def test_fallback_used_after_failure():
    manager = FallbackManager()

    result = manager.execute_chain(
        "financial_data_api",
        lambda: {"success": False, "error": "API unavailable"},
        [
            (
                "web_search",
                lambda: {
                    "success": True,
                    "data": "secondary evidence",
                },
            )
        ],
    )

    assert result["success"] is True
    assert result["fallback_used"] is True
    assert result["used_source"] == "web_search"
    assert result["data_gap"] is not None


def test_all_sources_fail_gracefully():
    manager = FallbackManager()

    result = manager.execute_chain(
        "sec_filing_search",
        lambda: {"success": False},
        [
            (
                "web_search",
                lambda: {"success": False},
            )
        ],
    )

    assert result["success"] is False
    assert result["data_gap"] is not None
