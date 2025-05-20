import requests 
import csv

def puabannoationAPI(id):

    url = "https://pubannotation.org/docs/sourcedb/PubMed/sourceid/"+str(id)+"/annotations.json?projects=OryzaGP_2021_FLAIR,OryzaGP_2021,OryzaGP_2021_v2,OryzaGP"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response

with open('output_04_04.tsv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    puabannotation_refernce = []
    for row in reader:
        pmids = row['pmids'].split(',')
        for pmid in pmids:
            entry = []
            response = puabannoationAPI(pmid)
            response = response.json()
            if response:
                entry["target"] = row['target']
                entry["sourcedb"] = row["sourcedb"]
                entry["sourceid"]= row["sourceid"]
                entry["text"]= row["text"]
                entry["tracks"]= row["tracks"]
                entry["project_name"] = "OryzaGP_2021_FLAIR,OryzaGP_2021,OryzaGP_2021_v2,OryzaGP"
            
            if entry:
                puabannotation_refernce.append(entry)
                row["pubannotation"]
        
                
                






