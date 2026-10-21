"""
Tool schemas for the Autonomous Financial Research Agent (ARA-1).

These schemas describe the tools available to the agent in a
function-calling compatible format.
"""

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "sec_filing_search",
            "description": (
                "Search recent SEC EDGAR filings for a public company."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": (
                            "Company name or stock ticker, "
                            "for example Microsoft or MSFT."
                        ),
                    },
                    "filing_type": {
                        "type": "string",
                        "description": (
                            "SEC filing form type such as "
                            "10-K, 10-Q, or 8-K."
                        ),
                        "default": "10-K",
                    },
                    "limit": {
                        "type": "integer",
                        "description": (
                            "Maximum number of filings to return."
                        ),
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5,
                    },
                },
                "required": ["company"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for recent and relevant financial information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return.",
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "earnings_transcript",
            "description": (
                "Discover public earnings-call transcript sources "
                "and relevant transcript excerpts for a company."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": (
                            "Company name or ticker symbol."
                        ),
                    },
                    "quarter": {
                        "type": "string",
                        "description": (
                            "Quarter to research, for example "
                            "Q3 FY2026 or latest."
                        ),
                        "default": "latest",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": (
                            "Maximum number of transcript sources "
                            "to retrieve."
                        ),
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5,
                    },
                },
                "required": ["company"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "financial_data_api",
            "description": "Retrieve structured company financial data and market metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "Company name or ticker symbol."
                    },
                    "metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Financial metrics to retrieve."
                    },
                    "period": {
                        "type": "string",
                        "description": "Requested reporting period."
                    }
                },
                "required": ["company"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "news_sentiment",
            "description": (
                "Retrieve recent company news and analyze "
                "its sentiment using VADER."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": (
                            "Company name or stock ticker, "
                            "for example Apple or AAPL."
                        ),
                    },
                    "max_results": {
                        "type": "integer",
                        "description": (
                            "Maximum number of recent news "
                            "articles to analyze."
                        ),
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5,
                    },
                },
                "required": ["company"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "vector_db_search",
            "description": "Search long-term research memory for previously stored evidence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Semantic search query."
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of memory results to return.",
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "vector_db_store",
            "description": (
                "Store financial research evidence in the "
                "ARA-1 long-term vector memory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": (
                            "Research evidence or findings to store."
                        ),
                    },
                    "company": {
                        "type": "string",
                        "description": (
                            "Company associated with the research."
                        ),
                    },
                    "source": {
                        "type": "string",
                        "description": (
                            "Source or research result from which "
                            "the evidence was obtained."
                        ),
                    },
                    "source_type": {
                        "type": "string",
                        "description": (
                            "Category of the stored source."
                        ),
                        "default": "research",
                    },
                    "research_query": {
                        "type": "string",
                        "description": (
                            "Original research query associated "
                            "with the evidence."
                        ),
                        "default": "",
                    },
                    "confidence": {
                        "type": "number",
                        "description": (
                            "Confidence score for the stored evidence."
                        ),
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 0.8,
                    },
                },
                "required": [
                    "text",
                    "company",
                    "source",
                ],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "company_profile",
            "description": "Retrieve a structured overview of a company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "Company name or ticker symbol."
                    }
                },
                "required": ["company"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "peer_comparison",
            "description": "Compare financial or business metrics across multiple companies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "companies": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Companies to compare.",
                        "minItems": 2
                    },
                    "metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Metrics used for comparison."
                    }
                },
                "required": ["companies"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "report_generator",
            "description": (
                "Generate a structured Markdown financial "
                "research report from collected findings, "
                "sources, confidence, and limitations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the report.",
                    },
                    "research_query": {
                        "type": "string",
                        "description": (
                            "Original financial research query."
                        ),
                    },
                    "sections": {
                        "type": "array",
                        "description": (
                            "Structured sections of the report."
                        ),
                        "items": {
                            "type": "object",
                            "properties": {
                                "heading": {
                                    "type": "string"
                                },
                                "content": {
                                    "type": "string"
                                },
                            },
                            "required": [
                                "heading",
                                "content",
                            ],
                            "additionalProperties": False,
                        },
                        "minItems": 1,
                    },
                    "sources": {
                        "type": "array",
                        "description": (
                            "Sources used to support the report."
                        ),
                        "items": {
                            "type": "string"
                        },
                    },
                    "confidence": {
                        "type": "number",
                        "description": (
                            "Overall report confidence from 0 to 1."
                        ),
                        "minimum": 0,
                        "maximum": 1,
                        "default": 0.8,
                    },
                    "limitations": {
                        "type": "array",
                        "description": (
                            "Known limitations or evidence gaps."
                        ),
                        "items": {
                            "type": "string"
                        },
                    },
                },
                "required": [
                    "title",
                    "research_query",
                    "sections",
                ],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "fact_checker",
            "description": (
                "Verify a financial claim using evidence from "
                "multiple sources and flag numerical disagreements "
                "greater than the allowed tolerance."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "claim": {
                        "type": "string",
                        "description": (
                            "Financial claim to verify."
                        ),
                    },
                    "evidence": {
                        "type": "array",
                        "description": (
                            "Evidence collected from one or more "
                            "independent sources."
                        ),
                        "items": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string"
                                },
                                "value": {
                                    "type": "number"
                                },
                                "supports_claim": {
                                    "type": "boolean"
                                },
                            },
                            "required": ["source"],
                            "additionalProperties": False,
                        },
                        "minItems": 1,
                    },
                    "tolerance_percent": {
                        "type": "number",
                        "description": (
                            "Maximum numerical disagreement allowed "
                            "before evidence is flagged as conflicting."
                        ),
                        "minimum": 0,
                        "default": 5.0,
                    },
                },
                "required": [
                    "claim",
                    "evidence",
                ],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "calculation_engine",
            "description": (
                "Perform deterministic financial calculations "
                "including growth, financial ratios, and basic DCF."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": (
                            "Financial calculation to perform."
                        ),
                        "enum": [
                            "percentage_change",
                            "profit_margin",
                            "current_ratio",
                            "debt_to_equity",
                            "basic_dcf",
                        ],
                    },
                    "values": {
                        "type": "object",
                        "description": (
                            "Named numerical inputs required "
                            "for the selected calculation."
                        ),
                        "additionalProperties": {
                            "type": "number"
                        },
                    },
                },
                "required": [
                    "operation",
                    "values",
                ],
                "additionalProperties": False,
            },
        },
    },
]


def get_tool_schemas():
    """Return all registered tool schemas."""
    return TOOL_SCHEMAS


def get_tool_schema(tool_name):
    """Return the schema for one tool by name."""
    for schema in TOOL_SCHEMAS:
        if schema["function"]["name"] == tool_name:
            return schema

    return None