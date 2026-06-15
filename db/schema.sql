CREATE DATABASE IF NOT EXISTS telecom_db;
USE telecom_db;

CREATE TABLE IF NOT EXISTS raw_telecom_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    quarter INT,
    fiber_optic INT,
    adsl INT,
    fixed_4g INT,
    fixed_5g INT,
    satellite INT,
    other_service INT,
    total_fixed_broadband INT
);

CREATE TABLE IF NOT EXISTS telecom_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    quarter INT,
    total_fixed_broadband INT,
    growth_rate FLOAT,
    usage_per_service FLOAT,
    quarterly_change FLOAT,
    normalized_traffic_index FLOAT
);