import sqlite3
import pandas as pd




conn = sqlite3.connect('../curation_system/RTO_data.db')
cursor = conn.cursor()

all_rows = []
cursor = conn.cursor()
cursor.execute("SELECT *from RTOdata ")
rows = cursor.fetchall()
all_rows.extend(rows)
final_df = pd.DataFrame(all_rows)

final_df.to_csv('data_from_database.tsv', sep='\t', index=False)
print("Data saved to output.tsv")

conn.close()