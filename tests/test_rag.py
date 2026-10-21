from synthesis.rag_pipeline import RAGPipeline


def test_query_transformation():
    rag = RAGPipeline()

    result = rag.transform_query(
        "revenue growth",
        "Microsoft",
    )

    assert "revenue growth" in result
    assert "Microsoft revenue growth" in result
    assert len(result) >= 3


def test_reranking():
    rag = RAGPipeline()

    documents = [
        {
            "text": "Low relevance",
            "similarity": 0.4,
            "confidence": 0.5,
        },
        {
            "text": "High relevance",
            "similarity": 0.9,
            "confidence": 0.9,
        },
    ]

    ranked = rag.rerank(documents)

    assert ranked[0]["text"] == "High relevance"


def test_context_assembly():
    rag = RAGPipeline()

    context = rag.assemble_context(
        [
            {
                "text": "Revenue increased.",
                "source": "SEC EDGAR",
                "company": "Microsoft",
                "similarity": 0.9,
                "confidence": 1.0,
            }
        ]
    )

    assert "Revenue increased." in context
    assert "SEC EDGAR" in context


def test_empty_context():
    rag = RAGPipeline()

    result = rag.build_grounded_package(
        "financial performance",
        [],
        "Microsoft",
    )

    assert result["grounding_status"] == "insufficient_evidence"


def test_document_limit():
    rag = RAGPipeline()

    documents = [
        {
            "text": f"Evidence {i}",
            "similarity": 0.9,
            "confidence": 0.8,
        }
        for i in range(10)
    ]

    result = rag.build_grounded_package(
        "research",
        documents,
        max_documents=3,
    )

    assert result["selected_count"] == 3
