from evaluation.performance import (
    PerformanceMonitor,
    ToolCallOptimizer,
)


def test_performance_monitor():
    monitor = PerformanceMonitor()

    result = monitor.track(
        "test_tool",
        lambda: {"success": True},
    )

    assert result["success"] is True

    summary = monitor.summary()

    assert summary["total_calls"] == 1
    assert summary["successful_calls"] == 1


def test_tool_efficiency_target():
    monitor = PerformanceMonitor()

    for _ in range(8):
        monitor.track(
            "useful_tool",
            lambda: {"success": True},
            useful=True,
        )

    for _ in range(2):
        monitor.track(
            "less_useful_tool",
            lambda: {"success": True},
            useful=False,
        )

    summary = monitor.summary()

    assert summary["tool_efficiency"] == 0.8
    assert summary["target_met"] is True


def test_optimizer_avoids_duplicate_call():
    optimizer = ToolCallOptimizer()
    calls = {"count": 0}

    def tool(arguments):
        calls["count"] += 1
        return {
            "success": True,
            "company": arguments["company"],
        }

    arguments = {"company": "NVIDIA"}

    first = optimizer.execute(
        "company_profile",
        arguments,
        tool,
    )

    second = optimizer.execute(
        "company_profile",
        arguments,
        tool,
    )

    assert first == second
    assert calls["count"] == 1

    stats = optimizer.statistics()

    assert stats["cache_hits"] == 1
    assert stats["duplicate_calls_avoided"] == 1


def test_different_arguments_not_cached_together():
    optimizer = ToolCallOptimizer()
    calls = {"count": 0}

    def tool(arguments):
        calls["count"] += 1
        return {"success": True}

    optimizer.execute(
        "company_profile",
        {"company": "NVIDIA"},
        tool,
    )

    optimizer.execute(
        "company_profile",
        {"company": "Microsoft"},
        tool,
    )

    assert calls["count"] == 2
    assert optimizer.statistics()["cache_misses"] == 2


def test_empty_performance_summary():
    monitor = PerformanceMonitor()

    summary = monitor.summary()

    assert summary["total_calls"] == 0
    assert summary["tool_efficiency"] == 0.0
