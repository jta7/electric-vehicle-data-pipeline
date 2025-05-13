#!/bin/bash

set -e 

echo "=== Running ETL process ==="
echo ""

mkdir -p data

echo "--> Downloading CSV from source ..."
python3 src/get_data.py
echo ""

echo "--> Initializing database ..."
python3 src/init_db.py
echo ""

echo "--> Processing and inserting into PostgreSQL..."
python3 src/process_and_load.py
echo ""

echo "--> Exporting table to CSV..."
PGPASSWORD=challenge psql -h localhost -U challenge -d data_challenge -c "\copy public.electric_vehicles TO 'data/data_file.csv' WITH CSV HEADER"
echo ""

echo "ETL completed successfully. File exported to: data/data_file.csv"
