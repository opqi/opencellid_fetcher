-- init.sql

CREATE DATABASE IF NOT EXISTS opencellid;

USE opencellid;

-- Create the cell_tower table with MergeTree engine
CREATE TABLE IF NOT EXISTS cell_tower
(
    column1 UUID DEFAULT generateUUIDv4(),
    column2 String,
    column3 String
)
ENGINE = MergeTree()
ORDER BY column1;