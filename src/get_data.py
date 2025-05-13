import pandas as pd
import os

url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"

os.makedirs("data", exist_ok=True)

df = pd.read_csv(url)
df.to_csv("data/data_file_raw.csv", index=False)

print("CSV saved: data/data_file_raw.csv")
