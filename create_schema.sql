DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_region CASCADE;

CREATE TABLE dim_date (
    date_id     SERIAL PRIMARY KEY,
    full_date   DATE UNIQUE NOT NULL,
    day         INT NOT NULL,
    month       INT NOT NULL,
    month_name  VARCHAR(20) NOT NULL,
    quarter     INT NOT NULL,
    year        INT NOT NULL
);

CREATE TABLE dim_product (
    product_id      SERIAL PRIMARY KEY,
    product_name    VARCHAR(255) NOT NULL,
    category        VARCHAR(100),
    sub_category    VARCHAR(100)
);

CREATE TABLE dim_customer (
    customer_id     SERIAL PRIMARY KEY,
    customer_name   VARCHAR(255) NOT NULL,
    segment         VARCHAR(50)
);

CREATE TABLE dim_region (
    region_id       SERIAL PRIMARY KEY,
    region          VARCHAR(100),
    state           VARCHAR(100),
    city            VARCHAR(100)
);

CREATE TABLE fact_sales (
    sale_id         SERIAL PRIMARY KEY,
    date_id         INT REFERENCES dim_date(date_id),
    product_id      INT REFERENCES dim_product(product_id),
    customer_id     INT REFERENCES dim_customer(customer_id),
    region_id       INT REFERENCES dim_region(region_id),
    quantity        INT,
    sales_amount    NUMERIC(12, 2),
    profit          NUMERIC(12, 2)
);
