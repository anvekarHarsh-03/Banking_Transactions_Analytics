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

<img width="1281" height="790" alt="Screenshot 2026-04-21 125847" src="https://github.com/user-attachments/assets/20c9b59d-9e1f-4f09-9f03-0af3c609df18" />

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

- **Platinum** — Total spend > ₹25,00,000
- **Gold** — Total spend > ₹20,00,000
- **Silver** — Total spend > ₹15,00,000
- **Standard** — All remaining customers

<img width="279" height="439" alt="Screenshot 2026-04-21 125735" src="https://github.com/user-attachments/assets/aaa647e3-7ca4-400f-ad1e-9433bcc1b88b" />

This segmentation enables targeted retention, upsell, and risk strategies per tier.

---

### High-Risk Customer Identification

Customers with transaction failure rates exceeding defined thresholds are flagged automatically by the pipeline:

- **HIGH RISK** — Failure rate > 28%
- **MEDIUM RISK** — Failure rate > 18%
- **LOW RISK** — Failure rate ≤ 18%

These flags surface directly in the Power BI Risk Dashboard for immediate operational review.

<img width="1276" height="789" alt="Screenshot 2026-04-21 130403" src="https://github.com/user-attachments/assets/65e15906-0176-40ed-a2a4-1e585219e318" />

---

### Channel Performance Analysis

Ranking channels by transaction volume and failure rate identifies where operational investment is most needed. Online and Mobile channels lead in volume but carry different failure rate profiles compared to ATM and Branch channels, highlighting distinct risk exposures per channel type.

<img width="686" height="326" alt="Screenshot 2026-04-21 130916" src="https://github.com/user-attachments/assets/bd0515d6-5424-46ec-836c-71a119cfb2dc" />
<br>
<img width="686" height="326" alt="Screenshot 2026-04-21 131745" src="https://github.com/user-attachments/assets/3e4251b5-89b2-4bb9-8c99-84d12a113df2" />

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
| [extract.py](Python/scripts/extract.py) | Reads raw CSV and loads into MySQL staging table |
| [transform.py](Python/scripts/transform.py) | Applies 6-step data cleaning and enrichment |
| [load.py](Python/scripts/load.py) | Loads clean data into production table with audit logging |
| [main.py](Python/main.py) | Orchestrates the full ETL pipeline end-to-end |
| [create_tables.sql](sql/create_tables.sql) | Creates staging, production, and audit log tables |
| [analysis_queries](sql/analysis_queries.sql) | 5 analytical SQL views for Power BI |
| [PowerBI Dashboard](dashboard/dashboard.pbix) | Power BI dashboard (Executive Overview, Risk, Pipeline Health) |
| [Executive PPT Deck](PPT%20Deck/Executive%20Deck.pdf) | Executive Summary of the Whole Project |
| [config.py](Python/config.py) | Database connection configuration |

---

## Tech Stack

| Layer | Technology |
|---|---|
| ETL Pipeline | Python (pandas, mysql-connector) |
| Database | MySQL 8.0 |
| SQL Analytics | MySQL Views (5 analytical views) |
| Dashboard | Power BI Desktop (2024/2025) |
| IDE | VS Code + MySQL Workbench |
