# ERROR LOG

## Autonomous Financial Research Agent – ARA-1

**Student Name:** Ayshath Shahaziya  
**Project:** Project 1A – Autonomous Financial Research Agent

---

## Purpose

The project specification states that exactly seven deliberate factual or logical errors are embedded throughout Parts A–E of the project document.

This file records each identified error, explains why it is incorrect, and provides the corrected interpretation.

The log will be updated as additional errors are identified during development.

---

# Error 1 – Incorrect Memory Utilization Formula

**Location:** Part A – Section A5.2, Metric AB-4: Memory Utilization

### Statement in the project document

The document defines memory utilization as the ratio of memory hits to total external API calls, but then states that the metric is calculated as:

```text
memory_hits multiplied by total_api_calls
```

### Why This Is Incorrect

A ratio requires division, not multiplication.

Multiplication would cause the value to increase rapidly with the number of API calls and would not represent the proportion of calls avoided or supported through memory.

### Correct Formula

```text
Memory Utilization = memory_hits / total_external_api_calls
```

For example:

```text
memory_hits = 6
total_external_api_calls = 20

Memory Utilization = 6 / 20
                   = 0.30
```

Therefore, the memory utilization is 30%.

### Status

**Confirmed logical/formula error**

---

# Error 2 – Incorrect Source Reliability Ordering

**Location:** Part A – Section A6.2: Source Reliability Hierarchy

### Statement in the project document

The document ranks:

```text
Tier 4 – Social media posts and anonymous forum discussions
Tier 5 – Major news outlets such as Reuters, Bloomberg News,
         and the Financial Times
```

Since Tier 1 is defined as the highest reliability, this hierarchy places anonymous social-media and forum content above established professional news organizations.

### Why This Is Incorrect

Anonymous forum discussions and social-media posts generally lack the editorial review, verification procedures, accountability, and sourcing standards associated with established financial journalism.

Therefore, they should not normally receive a higher default reliability ranking than major professional news organizations.

### Corrected Interpretation

A more reasonable default hierarchy would be:

```text
Tier 1 – Primary regulatory filings / authoritative disclosures
Tier 2 – High-quality structured financial data
Tier 3 – Earnings calls and official company communications
Tier 4 – Established professional financial/news sources
Tier 5 – Social media, anonymous forums, and unverified sources
```

The exact reliability of an individual source should still be evaluated using factors such as provenance, recency, directness, and independent confirmation.

### Status

**Confirmed logical error**

---

# Error 3 – Incorrect SCAP / Dodd-Frank Timeline

**Location:** Part A – Section A7.3: Handling Ambiguous Queries

### Statement in the project document

The document states:

```text
The first US bank stress tests under SCAP were conducted
in 2007 following the Dodd-Frank Act.
```

### Why This Is Incorrect

The statement contains an impossible chronology.

The Supervisory Capital Assessment Program (SCAP) was associated with the U.S. bank stress-testing exercise conducted during the 2009 financial crisis.

The Dodd-Frank Wall Street Reform and Consumer Protection Act was enacted later, in 2010.

Therefore, a SCAP exercise could not have occurred in 2007 "following" legislation that did not yet exist.

### Corrected Interpretation

```text
SCAP was conducted in 2009 during the financial crisis.

The Dodd-Frank Act was enacted in 2010 and subsequently
established additional stress-testing requirements.
```

### Status

**Confirmed factual/timeline error**

---

# Errors Remaining

The project specification states that there are exactly:

```text
7 deliberate errors
```

Currently identified:

```text
Confirmed errors: 3
Remaining errors: 4
```

The remaining errors will be investigated and documented during subsequent development stages.

---

# Tracking Table

| Error | Section | Type | Status |
|---|---|---|---|
| 1 | A5.2 – AB-4 Memory Utilization | Formula / Logic | Confirmed |
| 2 | A6.2 – Source Reliability Hierarchy | Logic | Confirmed |
| 3 | A7.3 – SCAP / Dodd-Frank Timeline | Factual / Timeline | Confirmed |
| 4 | To be identified | TBD | Pending |
| 5 | To be identified | TBD | Pending |
| 6 | To be identified | TBD | Pending |
| 7 | To be identified | TBD | Pending |

---

## Development Note

Errors will only be marked as confirmed when sufficient evidence exists that the statement is deliberately incorrect. Potential errors will not be added as confirmed merely to reach the required count of seven.