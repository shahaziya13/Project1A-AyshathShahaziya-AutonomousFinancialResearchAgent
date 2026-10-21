# Challenge 4 — AWS vs Azure vs Google Cloud

## Autonomous Financial Research Agent (ARA-1)

**Research Topic:** Comparative Cloud Platform Analysis  
**Companies:** Amazon, Microsoft, Alphabet  
**Cloud Platforms:** Amazon Web Services (AWS), Microsoft Azure, Google Cloud  
**Challenge Status:** PASSED  
**Tools Used:** `financial_data_api`, `sec_filing_search`, `earnings_transcript`, `web_search`, `peer_comparison`, `calculation_engine`

---

## 1. Research Objective

The objective of Challenge 4 is to compare three major cloud-computing platforms:

- Amazon Web Services (AWS)
- Microsoft Azure
- Google Cloud

The Autonomous Financial Research Agent uses multiple independent tools to collect company-level and cloud-specific evidence, compare the parent companies, verify growth calculations, and identify limitations in the available data.

This challenge is more complex than a normal company comparison because AWS, Azure, and Google Cloud are not separately listed public companies.

They are business operations within:

| Cloud Platform | Parent Company | Ticker |
|---|---|---|
| AWS | Amazon.com, Inc. | AMZN |
| Azure | Microsoft Corporation | MSFT |
| Google Cloud | Alphabet Inc. | GOOGL |

Therefore, ARA-1 separates **parent-company financial metrics** from **cloud-segment metrics** instead of incorrectly treating the two as equivalent.

---

## 2. Research Methodology

ARA-1 used six tools for this challenge.

### 1. `financial_data_api`

Retrieved parent-company financial information for Amazon, Microsoft, and Alphabet.

### 2. `sec_filing_search`

Retrieved recent 10-K filings from SEC EDGAR.

### 3. `web_search`

Retrieved cloud-specific financial and growth information.

### 4. `earnings_transcript`

Located public earnings-call transcript sources for the three companies.

### 5. `peer_comparison`

Compared parent-company financial metrics using a standardized comparison structure.

### 6. `calculation_engine`

Independently calculated percentage growth for cloud revenue where comparable current and prior-period figures were available.

---

# 3. Parent-Company Financial Comparison

The financial-data tool retrieved current financial information for Amazon, Microsoft, and Alphabet.

## Amazon

**Company:** Amazon.com, Inc.  
**Ticker:** AMZN

Retrieved metrics:

- Market capitalization: approximately $2.85 trillion
- Total revenue: approximately $775.68 billion
- Net income: approximately $135.28 billion
- Profit margin: 17.44%
- Revenue growth: 19.6%
- Trailing EPS: $12.43
- Trailing P/E: approximately 21.26

---

## Microsoft

**Company:** Microsoft Corporation  
**Ticker:** MSFT

Retrieved metrics:

- Market capitalization: approximately $3.94 trillion
- Total revenue: approximately $331.84 billion
- Net income: approximately $133.75 billion
- Profit margin: 40.305%
- Revenue growth: 17.7%
- Trailing EPS: $17.95
- Trailing P/E: approximately 29.59

---

## Alphabet

**Company:** Alphabet Inc.  
**Ticker:** GOOGL

Retrieved metrics:

- Market capitalization: approximately $4.20 trillion
- Total revenue: approximately $445.87 billion
- Net income: approximately $244.12 billion
- Profit margin: 54.771%
- Revenue growth: 24.2%
- Trailing EPS: $19.93
- Trailing P/E: approximately 17.23

---

# 4. Parent-Company Comparison

The `peer_comparison` tool successfully compared all three companies without failures.

| Metric | Amazon | Microsoft | Alphabet |
|---|---:|---:|---:|
| Market Cap | ~$2.85T | ~$3.94T | ~$4.20T |
| Total Revenue | ~$775.68B | ~$331.84B | ~$445.87B |
| Net Income | ~$135.28B | ~$133.75B | ~$244.12B |
| Profit Margin | 17.44% | 40.305% | 54.771% |
| Revenue Growth | 19.6% | 17.7% | 24.2% |
| Trailing EPS | $12.43 | $17.95 | $19.93 |
| Trailing P/E | ~21.26 | ~29.59 | ~17.23 |

According to the comparison tool, Alphabet led the retrieved dataset in:

- Market capitalization.
- Net income.
- Profit margin.
- Revenue growth.
- Trailing EPS.

Amazon led in total company revenue.

Microsoft had the highest trailing P/E among the three in the retrieved snapshot.

These metrics describe the parent companies and should not be interpreted as direct financial metrics for their individual cloud businesses.

---

# 5. SEC Filing Verification

ARA-1 successfully retrieved recent SEC 10-K filings for all three parent companies.

## Amazon

CIK: `0001018724`

Latest retrieved 10-K:

- Filing date: February 6, 2026
- Report date: December 31, 2025

Previous retrieved 10-K:

- Filing date: February 7, 2025
- Report date: December 31, 2024

---

## Microsoft

CIK: `0000789019`

Latest retrieved 10-K:

- Filing date: July 29, 2026
- Report date: June 30, 2026

Previous retrieved 10-K:

- Filing date: July 30, 2025
- Report date: June 30, 2025

---

## Alphabet

CIK: `0001652044`

Latest retrieved 10-K:

- Filing date: February 5, 2026
- Report date: December 31, 2025

Previous retrieved 10-K:

- Filing date: February 5, 2025
- Report date: December 31, 2024

The SEC evidence confirms that the agent successfully located regulatory filings for each parent company.

---

# 6. AWS Analysis

Amazon Web Services is Amazon's cloud-computing business.

The retrieved Q2 2026 evidence reported AWS net sales growth of approximately **37% year over year**, described by Amazon as its fastest growth in 18 quarters.

The retrieved evidence also reported an AWS annualized revenue run rate of approximately **$169 billion**.

Another retrieved result reported approximately **$42.2 billion** in AWS Q2 2026 revenue.

AWS operating income was reported at approximately **$16.6 billion**, with evidence indicating substantial year-over-year operating-income growth.

These results indicate that AWS remained a major growth and profitability engine within Amazon.

---

# 7. AWS Growth Verification

ARA-1 used its deterministic calculation engine to independently verify the AWS growth figure.

Input values:

- Prior-period revenue: approximately $30.9 billion
- Current-period revenue: approximately $42.2 billion

Formula:

`((New Value - Old Value) / Old Value) × 100`

Calculation:

`(($42.2B - $30.9B) / $30.9B) × 100`

ARA-1 result:

**36.57%**

The independently calculated result is consistent with the approximately **37%** growth reported in the retrieved evidence.

### Verification Result

**CONSISTENT**

The difference is explained by rounding of the underlying revenue values.

---

# 8. AWS Strengths

The evidence suggests several AWS strengths.

### Strong Revenue Scale

AWS generated tens of billions of dollars in quarterly revenue and had an annualized revenue run rate reported at approximately $169 billion.

### Strong Growth

The retrieved evidence reported approximately 37% year-over-year growth in Q2 2026.

### Profitability

AWS operating income was reported at approximately $16.6 billion.

### AI Infrastructure Opportunity

Cloud demand associated with artificial intelligence provides a potential growth driver for AWS infrastructure and services.

### Parent-Company Support

Amazon's scale provides AWS with substantial resources for infrastructure investment.

---

# 9. AWS Risks

AWS also faces several risks.

These include:

- Competition from Microsoft Azure.
- Competition from Google Cloud.
- Large infrastructure investment requirements.
- AI-related capital expenditure.
- Pricing competition.
- Customer optimization of cloud spending.
- Rapid technological change.

Maintaining high growth becomes progressively more difficult as the revenue base increases.

---

# 10. Microsoft Azure Analysis

Microsoft's retrieved FY2026 Q4 evidence reported that:

**Azure and other cloud services revenue increased 43% year over year.**

The previous quarter's evidence reported approximately **40%** growth.

This indicates acceleration between the retrieved Q3 and Q4 growth rates.

Microsoft also reported Intelligent Cloud revenue of approximately **$39.3 billion** in FY2026 Q4, representing approximately 32% year-over-year growth.

However, Intelligent Cloud is a broader reporting category and must not be treated as identical to Azure.

---

# 11. Azure Revenue Disclosure Limitation

An important comparability problem exists with Azure.

Microsoft's retrieved first-party evidence reports Azure's **percentage growth**, but the evidence collected by ARA-1 does not provide a standalone quarterly Azure revenue figure comparable to the AWS and Google Cloud figures.

Therefore, ARA-1 does **not** estimate or invent Azure quarterly revenue.

This prevents a misleading comparison.

The most defensible retrieved Azure metric is:

**Azure and other cloud services growth: 43% year over year**

for Microsoft's FY2026 fourth quarter.

---

# 12. Azure Strengths

### High Growth

The retrieved 43% growth rate indicates strong demand.

### Enterprise Ecosystem

Azure benefits from Microsoft's broad enterprise software and cloud ecosystem.

### AI Demand

AI workloads can increase demand for cloud computing infrastructure and related services.

### Parent-Company Profitability

Microsoft's retrieved parent-company profit margin was approximately 40.305%, demonstrating substantial overall profitability.

### Scale

Microsoft's large market capitalization and financial resources provide substantial capacity for cloud and AI infrastructure investment.

---

# 13. Azure Risks

Major risks include:

- Competition from AWS.
- Competition from Google Cloud.
- High infrastructure capital requirements.
- AI capacity constraints.
- Technology execution risk.
- Cloud pricing competition.
- Dependence on continued enterprise technology spending.

Rapid growth may require significant ongoing investment in data centers, processors, networking, energy, and other infrastructure.

---

# 14. Google Cloud Analysis

The retrieved Q2 2026 evidence reported Google Cloud revenue of approximately:

**$24.8 billion**

The retrieved evidence also reported approximately:

**82% year-over-year growth**

and Google Cloud operating income of approximately:

**$8.8 billion**

The evidence attributed strong cloud growth partly to demand for AI infrastructure and enterprise AI solutions.

These figures indicate rapid expansion of Alphabet's cloud business in the retrieved period.

---

# 15. Google Cloud Growth Verification

ARA-1 independently tested the reported Google Cloud growth rate using the deterministic calculation engine.

Inputs:

- Prior-period revenue: approximately $13.6 billion
- Current-period revenue: approximately $24.8 billion

Calculation:

`(($24.8B - $13.6B) / $13.6B) × 100`

ARA-1 result:

**82.35%**

This is consistent with the approximately **82%** growth reported by the retrieved web evidence.

### Verification Result

**CONSISTENT WITH RETRIEVED WEB EVIDENCE**

However, because the specific Q2 values used in this calculation were retrieved primarily through secondary web results during this challenge, ARA-1 assigns lower confidence than it would to a directly retrieved first-party financial table.

---

# 16. Google Cloud Strengths

### Rapid Growth

The retrieved evidence indicates extremely strong year-over-year growth.

### AI Demand

Enterprise AI infrastructure and AI solutions were identified as major demand drivers.

### Improving Profitability

The retrieved evidence reported approximately $8.8 billion in Google Cloud operating income.

### Alphabet Resources

Alphabet has substantial financial resources available for infrastructure and AI investment.

### Integrated AI Capabilities

Google's broader AI and technology ecosystem may support continued cloud development.

---

# 17. Google Cloud Risks

Potential risks include:

- Competition from AWS.
- Competition from Azure.
- High capital expenditure.
- AI infrastructure costs.
- Need to maintain rapid growth.
- Enterprise adoption uncertainty.
- Pricing pressure.
- Technology-cycle risk.

A very high growth rate also creates difficult future comparisons because sustaining similar percentage growth becomes harder as the revenue base expands.

---

# 18. Cloud Growth Comparison

Using the latest evidence retrieved during the challenge:

| Cloud Platform | Retrieved Growth Indicator |
|---|---:|
| AWS | ~37% |
| Azure and other cloud services | 43% |
| Google Cloud | ~82% |

On the retrieved figures, Google Cloud had the highest percentage growth, followed by Azure and AWS.

However, these percentages should not be interpreted as a perfectly standardized comparison.

The companies use different:

- Fiscal calendars.
- Reporting definitions.
- Segment structures.
- Disclosure practices.

Therefore, the comparison is useful for directional analysis but not as a perfectly like-for-like accounting comparison.

---

# 19. Revenue Scale Comparison

The evidence retrieved by ARA-1 reported:

### AWS

Approximately **$42.2 billion** quarterly revenue in Q2 2026.

### Google Cloud

Approximately **$24.8 billion** quarterly revenue in Q2 2026.

### Azure

Standalone quarterly Azure revenue was **not established by the first-party evidence retrieved in this challenge**.

Therefore, ARA-1 does not create an estimated Azure revenue value.

Based only on directly comparable retrieved revenue figures, AWS had a larger quarterly cloud revenue base than Google Cloud.

No exact AWS-versus-Azure-versus-Google-Cloud revenue ranking is produced because Azure standalone revenue was unavailable in the collected evidence.

---

# 20. Earnings Transcript Evidence

The earnings-transcript tool successfully returned public transcript sources for all three companies.

## Amazon

The results included an Amazon Q1 2026 earnings-call transcript as well as older transcript results.

## Microsoft

The results included Microsoft's Q4 FY2026 earnings-call transcript dated July 29, 2026, along with Q3 2026 and older transcript material.

## Alphabet

The strongest result was Alphabet's official Investor Relations page for its **2026 Q2 Earnings Call**.

This provided first-party transcript discovery from Alphabet Investor Relations.

---

# 21. Transcript Tool Limitation

The `earnings_transcript` tool was called using:

`quarter = "latest"`

However, its results sometimes included multiple historical periods.

For example, Amazon's search included Q1 2026 as well as older calls, while Microsoft's results included Q4 FY2026, Q3 2026, and an older Q1 2025 result.

Therefore:

**`latest` currently functions as a search instruction rather than a guaranteed chronological filter.**

This is a known limitation of the current transcript implementation.

Future versions should extract transcript dates, normalize fiscal periods, rank them chronologically, and verify the latest period before returning results.

---

# 22. Parent-Company Financial Strength

The parent-company comparison provides useful context for each cloud platform.

### Amazon

Amazon had the highest total revenue among the three companies in the retrieved dataset.

This demonstrates enormous company-wide scale.

### Microsoft

Microsoft showed strong parent-company profitability and a substantial market valuation.

Its broader enterprise ecosystem may reinforce Azure adoption.

### Alphabet

Alphabet led several metrics in the retrieved peer-comparison snapshot, including market capitalization, net income, profit margin, revenue growth, and trailing EPS.

Its strong financial position provides substantial capacity to invest in Google Cloud and AI infrastructure.

---

# 23. AI as a Common Growth Driver

Artificial intelligence is a major strategic factor across all three cloud providers.

Cloud platforms provide infrastructure required for:

- Model training.
- Model inference.
- Data processing.
- Enterprise AI applications.
- Storage.
- Networking.
- AI development platforms.

Therefore, growth in generative AI and enterprise AI adoption may increase demand across AWS, Azure, and Google Cloud.

At the same time, AI creates substantial infrastructure requirements.

This creates a common strategic trade-off:

**Higher AI demand → higher cloud opportunity → higher infrastructure investment requirements.**

---

# 24. Competitive Position

## AWS

AWS demonstrates substantial revenue scale and strong profitability in the retrieved evidence.

**Position:** Scale leader among the directly disclosed cloud revenue figures retrieved.

## Azure

Azure demonstrates very strong reported growth and benefits from Microsoft's enterprise ecosystem.

**Position:** Strong enterprise cloud competitor with high growth.

## Google Cloud

Google Cloud demonstrates the fastest retrieved percentage growth.

**Position:** Rapidly expanding challenger with strong AI-related momentum in the retrieved evidence.

---

# 25. Comparative Assessment

| Category | AWS | Azure | Google Cloud |
|---|---|---|---|
| Retrieved Growth | ~37% | 43% | ~82% |
| Standalone Revenue Retrieved | Yes | No | Yes |
| Parent Company | Amazon | Microsoft | Alphabet |
| Major Strength | Scale and profitability | Enterprise ecosystem and growth | Rapid growth and AI demand |
| Major Risk | Maintaining growth at scale | High infrastructure requirements | Sustaining exceptional growth |
| Evidence Confidence | High/Medium | High for growth rate | Medium pending stronger first-party numeric verification |

No single provider can be declared universally superior because each has different strengths and the available disclosures are not perfectly comparable.

---

# 26. Data Quality and Conflict Resolution

ARA-1 identified several data-quality considerations.

### Issue 1 — Different Reporting Structures

AWS and Google Cloud provide segment-level revenue figures in the retrieved evidence, while Microsoft's retrieved first-party result primarily provides Azure growth rather than standalone Azure revenue.

**Resolution:** Do not invent an Azure revenue estimate.

### Issue 2 — Secondary Google Cloud Evidence

The Google Cloud Q2 2026 revenue and growth figures were retrieved mainly through secondary web results.

**Resolution:** Retain the figures with a confidence limitation rather than presenting them as independently verified first-party values.

### Issue 3 — Transcript Period Mixing

The transcript search returned multiple fiscal periods when asked for `"latest"`.

**Resolution:** Identify the limitation and avoid assuming every returned transcript represents the latest quarter.

### Issue 4 — Parent vs. Segment Data

Parent-company financial metrics cannot be treated as cloud-segment financial metrics.

**Resolution:** Keep parent-company and segment analysis separate throughout the report.

---

# 27. Tool Performance

| Tool | Status | Main Contribution |
|---|---|---|
| `financial_data_api` | Success | Parent-company financial data |
| `sec_filing_search` | Success | Recent 10-K filings |
| `web_search` | Success | Cloud-specific metrics |
| `earnings_transcript` | Success with limitation | Earnings-call source discovery |
| `peer_comparison` | Success | Parent-company comparison |
| `calculation_engine` | Success | Independent growth calculations |

All six required Challenge 4 tools executed successfully.

---

# 28. Key Findings

The research produced five major findings.

**First**, AWS demonstrated substantial cloud scale, with retrieved Q2 2026 revenue of approximately $42.2 billion and growth of approximately 37%.

**Second**, Azure and other cloud services reported 43% year-over-year growth in Microsoft's FY2026 Q4 results.

**Third**, retrieved web evidence reported Google Cloud Q2 2026 revenue of approximately $24.8 billion and growth of approximately 82%.

**Fourth**, ARA-1's deterministic calculation engine reproduced approximately 36.57% AWS growth and 82.35% Google Cloud growth from the retrieved rounded revenue inputs.

**Fifth**, disclosure differences prevent a completely standardized three-way revenue comparison.

---

# 29. Overall Conclusion

Challenge 4 demonstrates ARA-1's ability to perform a complex multi-company research task requiring evidence from multiple tools.

AWS, Azure, and Google Cloud all showed strong cloud momentum in the retrieved evidence.

AWS demonstrated major scale and profitability.

Azure demonstrated strong growth and benefits from Microsoft's broader enterprise ecosystem.

Google Cloud showed the highest retrieved percentage growth, although its specific Q2 2026 figures require a lower confidence level because the numeric evidence collected in this run relied more heavily on secondary sources.

The analysis also demonstrates an important principle of autonomous financial research:

**Missing or non-comparable data should be disclosed rather than estimated without sufficient evidence.**

ARA-1 therefore avoids inventing standalone Azure revenue and clearly separates parent-company financial performance from cloud-segment performance.

---

# 30. Final Challenge Result

**Challenge 4 Status: PASSED**

### Required Tool Coverage

- `financial_data_api` — PASS
- `sec_filing_search` — PASS
- `earnings_transcript` — PASS with documented retrieval limitation
- `web_search` — PASS
- `peer_comparison` — PASS
- `calculation_engine` — PASS

### Research Quality Notes

- Multi-source evidence: Completed
- Parent/segment distinction: Completed
- Independent calculation: Completed
- Missing-data disclosure: Completed
- Tool limitations documented: Completed
- Unsupported Azure revenue estimation avoided: Completed

**Overall Result: PASS**