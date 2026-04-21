CREATE DATABASE IF NOT EXISTS banking_etl;
USE banking_etl;

-- STAGING table: raw data lands here first (no constraints)
CREATE TABLE IF NOT EXISTS stg_transactions (
    transaction_id    VARCHAR(20),
    customer_id       VARCHAR(20),
    transaction_date  VARCHAR(30),      -- kept as string intentionally
    amount            VARCHAR(20),      -- kept as string intentionally
    transaction_type  VARCHAR(20),
    channel           VARCHAR(20),
    category          VARCHAR(30),
    status            VARCHAR(20),
    merchant_name     VARCHAR(100),
    balance_after     VARCHAR(20),
    loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PRODUCTION table: clean, validated, typed data
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id    VARCHAR(20) PRIMARY KEY,
    customer_id       VARCHAR(20) NOT NULL,
    transaction_date  DATETIME NOT NULL,
    amount            DECIMAL(15, 2) NOT NULL,
    transaction_type  VARCHAR(20),
    channel           VARCHAR(20),
    category          VARCHAR(30),
    status            VARCHAR(20),
    merchant_name     VARCHAR(100),
    balance_after     DECIMAL(15, 2),
    is_large_txn      BOOLEAN,          -- enriched flag
    txn_month         VARCHAR(10),      -- enriched column
    loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AUDIT log table: track every pipeline run
CREATE TABLE IF NOT EXISTS etl_audit_log (
    log_id            INT AUTO_INCREMENT PRIMARY KEY,
    run_timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    records_extracted INT,
    records_rejected  INT,
    records_loaded    INT,
    status            VARCHAR(20),
    notes             TEXT
);


