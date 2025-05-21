import requests 
import csv
import time
import pandas as pd


csv.field_size_limit(1_000_000_000)


entry = []

puabannotation_refernce = []
with open('output_04_04.tsv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    puabannotation_refernce = []
    count = 0
    for row in reader:
        pmids = row['PMIDs'].split(',')
        for pmid in pmids:
            if pmid :
                entry.append({"trait":row["trait_name"] , "pmid":pmid})
def save_to_tsv(data, filename='pmids.tsv'):
    if not data:
        print("No data to save")
        return
    
    df = pd.DataFrame(data)
    df.drop_duplicates()
    df.to_csv(filename,sep='\t')
    return df

save_to_tsv(entry)
        
                
                






