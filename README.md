# Banking ETL Pipeline — Analytics Dashboard

## Project Background

Retail banks generate millions of transactions daily across multiple channels, customer segments, and product categories. Without structured data pipelines and analytics, identifying performance trends, flagging risk, and optimizing operations becomes impossible at scale.

This project builds a **production-style ETL pipeline** using Python and MySQL that ingests raw banking transaction data, applies rigorous data quality checks, and loads clean data into an analytical layer. The output powers an executive-level Power BI dashboard for operational and risk leadership.

This project uses analytics to:
- Evaluate transaction volume, channel performance, and revenue trends
- Diagnose data quality issues (nulls, duplicates, invalid values)
- Identify high-risk customers based on failure rate patterns
- Segment customers by spend behavior (Platinum / Gold / Silver / Standard)
- Build an executive-level Power BI dashboard for banking operations leadership
- Recommend interventions to improve data reliability and vendor/customer strategy

---

## Data Structure

The pipeline processes raw transaction data through a **staged architecture**:

```
raw_transactions.csv (25,500 records)
        ↓
stg_transactions       ← Raw staging table (no constraints)
        ↓
fact_transactions      ← Clean production table (typed, validated, enriched)
        ↓
etl_audit_log          ← Pipeline run history and health metrics
```

**Analytical views built on top of fact_transactions:**

| View | Purpose |
|---|---|
| `vw_monthly_trend` | Transaction volume and value by month |
| `vw_customer_segments` | Platinum / Gold / Silver / Standard segmentation |
| `vw_channel_performance` | Volume, value, and failure rate by channel |
| `vw_risk_customers` | Customers flagged by high transaction failure rates |
| `vw_category_breakdown` | Spend distribution across categories |

---

## Executive Summary

### Overview of Findings

Analysis reveals that transaction performance is highly unequal across channels, customer segments, and time periods. A small group of customers and channels disproportionately drives financial outcomes, while data quality issues and risk signals are concentrated in identifiable patterns.

- **Online and Mobile channels contribute over 80% of transaction volume**, while Branch banking accounts for less than 25%. This highlights a digital-first shift with implications for channel investment strategy.
- **Platinum and Gold customers represent ~47% of the customer base but drive the majority of high-value transactions**, indicating that customer tier is a reliable proxy for revenue contribution.
- **Bulk transaction patterns reveal that large-value transactions (>₹50,000) follow predictable customer and channel profiles**, enabling proactive risk management and targeted servicing.

![Power BI Dashboard](https://github.com/user-attachments/assets/1b68ca8d-d46c-409a-b5ae-d609aaa2d677)

---

### Data Quality & Pipeline Performance

The ETL pipeline applies 6 transformation checks before loading data into production:

| Check | Records Affected |
|---|---|
| Null critical fields (customer_id, amount) | ~397 rows dropped |
| Invalid amount values | Coerced and flagged |
| Invalid date formats | Coerced and flagged |
| Invalid status values | Standardized to SUCCESS / FAILED / PENDING |
| Duplicate transaction IDs | Deduplicated on primary key |
| Whitespace & casing issues | Stripped and uppercased |

**98.4% of records passed all validation checks and were loaded into production.**

---

### Customer Segmentation by Spend

Customers are segmented into four tiers based on cumulative successful transaction value:

- **Platinum** — Total spend > ₹5,00,000
- **Gold** — Total spend > ₹1,00,000
- **Silver** — Total spend > ₹50,000
- **Standard** — All remaining customers

This segmentation enables targeted retention, upsell, and risk strategies per tier.

---

### High-Risk Customer Identification

Customers with transaction failure rates exceeding defined thresholds are flagged automatically by the pipeline:

- **HIGH RISK** — Failure rate > 40%
- **MEDIUM RISK** — Failure rate > 20%
- **LOW RISK** — Failure rate ≤ 20%

These flags surface directly in the Power BI Risk Dashboard for immediate operational review.

---

### Channel Performance Analysis

Ranking channels by transaction volume and failure rate identifies where operational investment is most needed. Online and Mobile channels lead in volume but carry different failure rate profiles compared to ATM and Branch channels, highlighting distinct risk exposures per channel type.

---

## Recommendations

1. **Prioritize Digital Channel Reliability**
   - Online and Mobile channels drive the majority of volume; even small failure rate improvements yield outsized impact on customer experience and revenue.

2. **Build Retention Programs for Platinum and Gold Customers**
   - Top-tier customers justify preferential servicing, proactive outreach, and dedicated relationship management.

3. **Automate Risk Escalation for HIGH RISK Customers**
   - Customers flagged by the pipeline should trigger automated review workflows rather than relying on manual identification.

4. **Formalize Data Quality SLAs**
   - The pipeline's audit log provides a foundation for tracking rejection rates over time; target < 2% rejection rate per run as a data quality KPI.

5. **Expand Pipeline to Support Incremental Loading**
   - The current pipeline performs full loads; implementing incremental loading (via `loaded_at` timestamps) will reduce runtime and enable near-real-time analytics.

---

## Included Files

| File | Description |
|---|---|
| `scripts/generate_data.py` | Generates 25,500 synthetic banking transaction records |
| `scripts/extract.py` | Reads raw CSV and loads into MySQL staging table |
| `scripts/transform.py` | Applies 6-step data cleaning and enrichment |
| `scripts/load.py` | Loads clean data into production table with audit logging |
| `main.py` | Orchestrates the full ETL pipeline end-to-end |
| `sql/create_tables.sql` | Creates staging, production, and audit log tables |
| `sql/analysis_queries.sql` | 5 analytical SQL views for Power BI |
| `Banking_ETL_Dashboard.pbix` | Power BI dashboard (Executive Overview, Risk, Pipeline Health) |
| `config.py` | Database connection configuration |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Generation | Python (pandas, numpy, uuid) |
| ETL Pipeline | Python (pandas, mysql-connector) |
| Database | MySQL 8.0 |
| SQL Analytics | MySQL Views (5 analytical views) |
| Dashboard | Power BI Desktop (2024/2025) |
| IDE | VS Code + MySQL Workbench |
