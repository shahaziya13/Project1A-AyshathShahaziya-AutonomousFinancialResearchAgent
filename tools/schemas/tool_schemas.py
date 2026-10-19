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
            "description": "Retrieve or search a company's earnings-call transcript.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "Company name or ticker symbol."
                    },
                    "quarter": {
                        "type": "string",
                        "description": "Quarter such as Q1, Q2, Q3, or Q4."
                    },
                    "year": {
                        "type": "integer",
                        "description": "Fiscal year."
                    }
                },
                "required": ["company"]
            }
        }
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
            "description": "Store verified research evidence in long-term vector memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Evidence or research content to store."
                    },
                    "source": {
                        "type": "string",
                        "description": "Source of the evidence."
                    },
                    "company": {
                        "type": "string",
                        "description": "Related company, if applicable."
                    }
                },
                "required": ["content", "source"]
            }
        }
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
            "description": "Generate a structured financial research report from verified findings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Report title."
                    },
                    "findings": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Verified research findings."
                    },
                    "include_sources": {
                        "type": "boolean",
                        "description": "Whether sources should be included."
                    }
                },
                "required": ["title", "findings"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "fact_checker",
            "description": "Cross-check a financial claim against available evidence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim": {
                        "type": "string",
                        "description": "Claim that needs verification."
                    },
                    "evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Evidence used to verify the claim."
                    }
                },
                "required": ["claim", "evidence"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculation_engine",
            "description": "Perform supported financial and mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide",
                            "percentage_change"
                        ],
                        "description": "Calculation to perform."
                    },
                    "values": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Numeric values used in the calculation.",
                        "minItems": 2
                    }
                },
                "required": ["operation", "values"]
            }
        }
    }
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