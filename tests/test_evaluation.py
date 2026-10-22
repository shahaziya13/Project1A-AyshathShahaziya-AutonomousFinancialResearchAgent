from evaluation.metrics import ResearchEvaluator
from evaluation.evaluator import EvaluationRunner


def sample_run():
    return {
        "required_items": 10,
        "completed_items": 10,
        "total_claims": 20,
        "verified_claims": 19,
        "cited_claims": 20,
        "tools_called": 10,
        "successful_tools": 9,
        "useful_tools": 8,
        "conflicts_detected": 2,
        "conflicts_resolved": 2,
        "errors": 2,
        "errors_recovered": 2,
        "fallbacks_attempted": 2,
        "fallbacks_succeeded": 2,
        "retrieved_documents": 10,
        "relevant_documents": 9,
        "memory_queries": 5,
        "memory_hits": 4,
        "answer_relevance": 0.95,
        "citation_correctness": 0.95,
        "source_quality": 0.90,
        "source_diversity": 0.90,
        "evidence_coverage": 0.95,
        "numerical_accuracy": 1.0,
        "conflict_detection": 1.0,
        "hallucination_control": 0.95,
        "tool_selection_accuracy": 0.90,
        "context_grounding": 0.95,
        "report_completeness": 0.95,
        "limitation_disclosure": 1.0,
        "confidence_calibration": 0.90,
        "research_depth": 0.90,
    }


def test_at_least_twenty_metrics():
    evaluator = ResearchEvaluator()

    result = evaluator.evaluate(sample_run())

    assert result["metric_count"] >= 20


def test_tool_efficiency_above_target():
    evaluator = ResearchEvaluator()

    result = evaluator.evaluate(sample_run())

    assert result["scores"]["tool_efficiency"] == 0.8
    assert result["tool_efficiency_target_met"] is True


def test_factual_accuracy():
    evaluator = ResearchEvaluator()

    result = evaluator.evaluate(sample_run())

    assert result["scores"]["factual_accuracy"] == 0.95


def test_evaluation_runner():
    runner = EvaluationRunner()

    result = runner.run(
        "ARA-1 Test Evaluation",
        sample_run(),
    )

    assert result["evaluation_name"] == "ARA-1 Test Evaluation"
    assert result["metric_count"] >= 20


def test_scores_between_zero_and_one():
    evaluator = ResearchEvaluator()

    result = evaluator.evaluate(sample_run())

    for value in result["scores"].values():
        assert 0 <= value <= 1
