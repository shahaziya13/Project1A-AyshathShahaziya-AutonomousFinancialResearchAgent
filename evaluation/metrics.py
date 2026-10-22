"""Evaluation metrics for ARA-1."""

from __future__ import annotations

from typing import Any


class ResearchEvaluator:
    """Evaluate autonomous financial research runs."""

    METRIC_NAMES = [
        "task_completion",
        "answer_relevance",
        "factual_accuracy",
        "citation_coverage",
        "citation_correctness",
        "source_quality",
        "source_diversity",
        "evidence_coverage",
        "numerical_accuracy",
        "conflict_detection",
        "conflict_resolution",
        "hallucination_control",
        "tool_selection_accuracy",
        "tool_success_rate",
        "tool_efficiency",
        "memory_utilization",
        "retrieval_relevance",
        "context_grounding",
        "report_completeness",
        "limitation_disclosure",
        "error_recovery",
        "fallback_success",
        "confidence_calibration",
        "research_depth",
        "overall_quality",
    ]

    def safe_ratio(self, numerator: float, denominator: float) -> float:
        if denominator <= 0:
            return 0.0
        return round(min(max(numerator / denominator, 0.0), 1.0), 4)

    def evaluate(self, run: dict[str, Any]) -> dict[str, Any]:
        required = float(run.get("required_items", 0))
        completed = float(run.get("completed_items", 0))

        claims = float(run.get("total_claims", 0))
        verified = float(run.get("verified_claims", 0))
        cited = float(run.get("cited_claims", 0))

        tools_called = float(run.get("tools_called", 0))
        successful_tools = float(run.get("successful_tools", 0))
        useful_tools = float(run.get("useful_tools", 0))

        conflicts = float(run.get("conflicts_detected", 0))
        resolved = float(run.get("conflicts_resolved", 0))

        errors = float(run.get("errors", 0))
        recovered = float(run.get("errors_recovered", 0))

        fallbacks = float(run.get("fallbacks_attempted", 0))
        fallback_successes = float(run.get("fallbacks_succeeded", 0))

        retrieved = float(run.get("retrieved_documents", 0))
        relevant = float(run.get("relevant_documents", 0))

        memory_queries = float(run.get("memory_queries", 0))
        memory_hits = float(run.get("memory_hits", 0))

        scores = {
            "task_completion": self.safe_ratio(completed, required),
            "answer_relevance": float(run.get("answer_relevance", 0)),
            "factual_accuracy": self.safe_ratio(verified, claims),
            "citation_coverage": self.safe_ratio(cited, claims),
            "citation_correctness": float(run.get("citation_correctness", 0)),
            "source_quality": float(run.get("source_quality", 0)),
            "source_diversity": float(run.get("source_diversity", 0)),
            "evidence_coverage": float(run.get("evidence_coverage", 0)),
            "numerical_accuracy": float(run.get("numerical_accuracy", 0)),
            "conflict_detection": float(run.get("conflict_detection", 0)),
            "conflict_resolution": (
                self.safe_ratio(resolved, conflicts)
                if conflicts
                else 1.0
            ),
            "hallucination_control": float(run.get("hallucination_control", 0)),
            "tool_selection_accuracy": float(run.get("tool_selection_accuracy", 0)),
            "tool_success_rate": self.safe_ratio(successful_tools, tools_called),
            "tool_efficiency": self.safe_ratio(useful_tools, tools_called),
            "memory_utilization": self.safe_ratio(memory_hits, memory_queries),
            "retrieval_relevance": self.safe_ratio(relevant, retrieved),
            "context_grounding": float(run.get("context_grounding", 0)),
            "report_completeness": float(run.get("report_completeness", 0)),
            "limitation_disclosure": float(run.get("limitation_disclosure", 0)),
            "error_recovery": (
                self.safe_ratio(recovered, errors)
                if errors
                else 1.0
            ),
            "fallback_success": (
                self.safe_ratio(fallback_successes, fallbacks)
                if fallbacks
                else 1.0
            ),
            "confidence_calibration": float(run.get("confidence_calibration", 0)),
            "research_depth": float(run.get("research_depth", 0)),
        }

        base_values = list(scores.values())

        scores["overall_quality"] = round(
            sum(base_values) / len(base_values),
            4,
        )

        return {
            "metric_count": len(scores),
            "scores": scores,
            "overall_quality": scores["overall_quality"],
            "tool_efficiency_target_met": scores["tool_efficiency"] >= 0.70,
        }


def evaluate_research(run: dict[str, Any]) -> dict[str, Any]:
    return ResearchEvaluator().evaluate(run)
