from synthesis.synthesizer import EvidenceSynthesizer
from synthesis.conflict_resolver import ConflictResolver


def test_sec_evidence_ranked_above_web():
    engine = EvidenceSynthesizer()

    evidence = [
        {
            "claim": "revenue",
            "value": 100,
            "source": "Tavily Search API",
            "confidence": 0.9,
        },
        {
            "claim": "revenue",
            "value": 100,
            "source": "SEC EDGAR",
            "confidence": 1.0,
        },
    ]

    result = engine.rank_evidence(evidence)

    assert result[0]["source"] == "SEC EDGAR"


def test_synthesis_counts_sources():
    engine = EvidenceSynthesizer()

    result = engine.synthesize(
        [
            {
                "claim": "revenue",
                "value": 100,
                "source": "SEC EDGAR",
                "confidence": 1.0,
            },
            {
                "claim": "growth",
                "value": 20,
                "source": "Yahoo Finance via yfinance",
                "confidence": 0.9,
            },
        ]
    )

    assert result["evidence_count"] == 2
    assert result["source_count"] == 2


def test_conflict_above_five_percent():
    resolver = ConflictResolver(tolerance_percent=5)

    result = resolver.detect_numerical_conflict(
        [
            {"source": "Source A", "value": 100},
            {"source": "Source B", "value": 110},
        ]
    )

    assert result["has_conflict"] is True


def test_no_conflict_inside_tolerance():
    resolver = ConflictResolver(tolerance_percent=5)

    result = resolver.detect_numerical_conflict(
        [
            {"source": "Source A", "value": 100},
            {"source": "Source B", "value": 103},
        ]
    )

    assert result["has_conflict"] is False


def test_resolution_selects_highest_reliability():
    resolver = ConflictResolver()

    evidence = [
        {
            "source": "Web",
            "value": 110,
            "confidence": 0.8,
            "reliability_score": 0.6,
        },
        {
            "source": "SEC EDGAR",
            "value": 100,
            "confidence": 1.0,
            "reliability_score": 1.0,
        },
    ]

    result = resolver.resolve(evidence)

    assert result["selected"]["source"] == "SEC EDGAR"


def test_empty_evidence():
    resolver = ConflictResolver()

    result = resolver.resolve([])

    assert result["status"] == "insufficient_evidence"

from synthesis.pipeline import SynthesisPipeline


def test_pipeline_detects_conflicting_claim():
    pipeline = SynthesisPipeline(tolerance_percent=5)

    evidence = [
        {
            "claim": "revenue",
            "value": 100,
            "source": "SEC EDGAR",
            "confidence": 1.0,
        },
        {
            "claim": "revenue",
            "value": 120,
            "source": "Tavily Search API",
            "confidence": 0.8,
        },
    ]

    result = pipeline.run(evidence)

    assert result["status"] == "success"
    assert result["conflict_count"] == 1
    assert "revenue" in result["conflicting_claims"]


def test_pipeline_single_source_limitation():
    pipeline = SynthesisPipeline()

    result = pipeline.run(
        [
            {
                "claim": "growth",
                "value": 20,
                "source": "SEC EDGAR",
                "confidence": 1.0,
            }
        ]
    )

    assert len(result["limitations"]) == 1


def test_pipeline_multiple_consistent_sources():
    pipeline = SynthesisPipeline(tolerance_percent=5)

    result = pipeline.run(
        [
            {
                "claim": "revenue",
                "value": 100,
                "source": "SEC EDGAR",
                "confidence": 1.0,
            },
            {
                "claim": "revenue",
                "value": 102,
                "source": "Yahoo Finance via yfinance",
                "confidence": 0.9,
            },
        ]
    )

    assert result["conflict_count"] == 0
    assert result["source_count"] == 2
