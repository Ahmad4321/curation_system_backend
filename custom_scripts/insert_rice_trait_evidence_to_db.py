import pandas as pd
import sqlite3

df = pd.read_csv('./rice_alterome_evidence.tsv',sep='\t')
conn = sqlite3.connect('../curation_system/ricetrait.db.sqlite3')
cursor = conn.cursor()


for _, row in df.iterrows():
    query = """
    INSERT INTO rice_alterome_pubannotation (alterome_GoTerm, alterome_Gene, alterome_PMID, alterome_RichSentence, alterome_sentence, alterome_title, alterome_trait_name, alterome_TOTerm)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);
    """ 
    cursor.execute(query, (row["GOTerm"], row["Gene"], row["PMID"], row["RichSentence"], row["Sentence"], row["Title"], row["trait_name"], row["TOTerm"]))

conn.commit()
conn.close()
