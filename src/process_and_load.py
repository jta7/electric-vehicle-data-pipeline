import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
import numpy as np

CHUNKSIZE = 10_000
CSV_PATH = "data/data_file_raw.csv"

def prepare_records(chunk):
    """
    Prepara los datos del DataFrame para inserción en PostgreSQL.
    - Convierte tipos NumPy a tipos nativos de Python
    - Convierte NaN a None
    - Asegura el formato correcto de los datos
    """
    
    str_cols = ['County', 'City', 'State', 'Make', 'Model']
    for col in str_cols:
        if col in chunk.columns:
            chunk[col] = chunk[col].str.strip().str.title()
    
    records = []
    for row in chunk.itertuples(index=False):
        processed_row = []
        for value in row:
            if pd.isna(value):
                processed_row.append(None)
            elif isinstance(value, (np.int64, np.int32)):
                processed_row.append(int(value))
            elif isinstance(value, (np.float64, np.float32)):
                processed_row.append(float(value))
            else:
                processed_row.append(value)
        records.append(tuple(processed_row))
    
    return records

try:
    conn = psycopg2.connect(
        host="localhost",
        database="data_challenge",
        user="challenge",
        password="challenge"
    )

    with conn.cursor() as cur:
        
        for chunk in tqdm(pd.read_csv(CSV_PATH, chunksize=CHUNKSIZE), desc="Loading data"):
            records = prepare_records(chunk)
            
            execute_values(
                cur,
                """
                INSERT INTO electric_vehicles VALUES %s
                """,
                records,
                page_size=CHUNKSIZE
            )
            conn.commit()
            
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
    raise  
finally:
    if 'conn' in locals():
        conn.close()
