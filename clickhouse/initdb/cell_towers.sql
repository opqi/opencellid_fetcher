-- cell_towers.sql

CREATE DATABASE IF NOT EXISTS opencellid;

USE opencellid;

-- Create the cell_tower table with MergeTree engine
CREATE TABLE IF NOT EXISTS cell_tower
(
    id UUID DEFAULT generateUUIDv4(),
    radio String,
    mcc UInt16,
    net UInt16,
    area UInt32,
    cell String,
    unit Int16,
    lon Float32,
    lat Float32,
    range UInt32,
    samples UInt32,
    changeable UInt8,
    created DateTime,
    updated DateTime,
    averageSignal UInt8

)
ENGINE = MergeTree()
ORDER BY id;