import sqlite3
import requests
import csv


conn = sqlite3.connect('./ricetrait.db.sqlite3')
cursor = conn.cursor()
conn2 = sqlite3.connect('./RiceAlterome.db.sqlite3')
cursor2 = conn2.cursor()

query = """
    SELECT distinct ename from rto_data;
    """

result = cursor.execute(query).fetchall()
flat_results = [row[0] for row in result]
rice_alterome_evidence = []
PMID  = []
count = 0
for res  in flat_results:
    entry = {"trait_name": res}
    strv = ""
    query1 = " SELECT Gene,PMID,Title,Sentence,GOTerm,TOTerm,RichSentence FROM RiceAlteromeModel where GOTerm like '%"+res+"%' or TOTerm like '%"+res+"%' or Sentence like '%"+res+"%' or Sentence like '%"+res.lower()+"%';"
    rice_alterome = conn2.execute(query1).fetchall()
    rice_flat_results = [row for row in rice_alterome]
    sub_entry = []
    for res1 in rice_flat_results:
        sub_entry.append({'Gene' : res1[0],'PMID' : res1[1],'Title' : res1[2],'Sentence' : res1[3],'GOTerm' : res1[4],'TOTerm' : res1[5],'RichSentence' : res1[6]})
        strv += ","+res1[1]
        if count == 0:
            print(res,sub_entry)
            count += 1
    entry["trait_evidence"] = sub_entry
    entry["trait_evidence_length"] = len(sub_entry)
    entry["PMIDs"] = strv
    rice_alterome_evidence.append(entry)

def save_to_tsv(data, filename='output_04_04.tsv'):
    if not data:
        print("No data to save")
        return

    # Get all possible field names
    fieldnames = set()
    for entry in data:
        fieldnames.update(entry.keys())

    fieldnames = sorted(fieldnames)

    # Write to TSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

save_to_tsv(rice_alterome_evidence)

conn.close()
conn2.close()

