import sqlite3
import pandas as pd




conn = sqlite3.connect('../curation_system/ricetrait.db.sqlite3')
cursor = conn.cursor()


df = pd.read_csv('./data_from_database.tsv', sep='\t')



for _, row in df.iterrows():
    query = """
    INSERT INTO rto_data (tag, level, cname, ename, toid, parent_id, created_by_id, updated_by_id)
    VALUES(?, ?, ?, ?, ?, ?, 1,1);
    """

    conn.execute(query, (row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6]))
# Commit changes and close
conn.commit()
conn.close()

print("Records updated successfully!")