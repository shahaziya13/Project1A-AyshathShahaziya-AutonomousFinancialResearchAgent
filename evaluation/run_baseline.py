from evaluation.evaluator import EvaluationRunner

data = {
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

runner = EvaluationRunner()
result = runner.run("ARA-1 Baseline Evaluation", data)
runner.save(result, "evaluation/baseline_results.json")

print("Metric count:", result["metric_count"])
print("Overall quality:", result["overall_quality"])
print("Tool efficiency:", result["scores"]["tool_efficiency"])
print("70% efficiency target met:", result["tool_efficiency_target_met"])
