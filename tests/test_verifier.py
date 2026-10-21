from synthesis.verifier import ResearchVerifier


def test_verified_claim():
    verifier = ResearchVerifier()

    result = verifier.verify_claim(
        "Revenue increased.",
        [
            {
                "source": "SEC EDGAR",
                "confidence": 1.0,
                "supports_claim": True,
            }
        ],
    )

    assert result["status"] == "verified"


def test_unsupported_claim():
    verifier = ResearchVerifier()

    result = verifier.verify_claim(
        "Revenue doubled.",
        [],
    )

    assert result["status"] == "unsupported"


def test_conflicting_claim():
    verifier = ResearchVerifier()

    result = verifier.verify_claim(
        "Revenue increased.",
        [
            {
                "source": "SEC EDGAR",
                "confidence": 1.0,
                "supports_claim": True,
            },
            {
                "source": "News Source",
                "confidence": 0.8,
                "supports_claim": False,
            },
        ],
    )

    assert result["status"] == "conflicting"


def test_report_verification_rate():
    verifier = ResearchVerifier()

    claims = [
        {
            "claim": "Claim A",
            "evidence": [
                {
                    "source": "SEC EDGAR",
                    "confidence": 1.0,
                    "supports_claim": True,
                }
            ],
        },
        {
            "claim": "Claim B",
            "evidence": [
                {
                    "source": "SEC EDGAR",
                    "confidence": 1.0,
                    "supports_claim": True,
                }
            ],
        },
    ]

    result = verifier.verify_report(claims)

    assert result["verification_rate"] == 1.0
    assert result["passed"] is True


def test_report_fails_with_unsupported_claim():
    verifier = ResearchVerifier()

    claims = [
        {
            "claim": "Verified claim",
            "evidence": [
                {
                    "source": "SEC EDGAR",
                    "confidence": 1.0,
                    "supports_claim": True,
                }
            ],
        },
        {
            "claim": "Unsupported claim",
            "evidence": [],
        },
    ]

    result = verifier.verify_report(claims)

    assert result["verification_rate"] == 0.5
    assert result["passed"] is False
