import pandas as pd
import sqlite3

df = pd.read_csv('./pubannoptation_processed.tsv',sep='\t')
conn = sqlite3.connect('./ricetrait.db.sqlite3')
cursor = conn.cursor()



for _, row in df.iterrows():
    query = """
    UPDATE RiceAlteromePubannotation SET pubannotation_target=?,pubannotation_text=?,pubannotation_source_db=?,pubannotation_project_name=?,pubannotation_tracks=? where alterome_PMID = ? ;
    """ 

    cursor.execute(query, (row["target"], row["text"],row["sourcedb"], row["project_name"], row["tracks"], row["sourceid"]))

conn.commit()
conn.close()
