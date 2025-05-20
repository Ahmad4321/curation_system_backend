import requests 
import csv

def puabannoationAPI(id):

    url = "https://pubannotation.org/docs/sourcedb/PubMed/sourceid/"+str(id)+"/annotations.json?projects=OryzaGP_2021_FLAIR,OryzaGP_2021,OryzaGP_2021_v2,OryzaGP"
    print(url)

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response
puabannotation_refernce = []
with open('pubannotation_data.tsv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    puabannotation_refernce = []
    for row in reader:
        pmids = row['PMIDs'].split(',')
        pmidValue = ""
        for pmid in pmids:
            if pmid:
                entry = []
                response1 = puabannoationAPI(pmid)
                
                response = response1.json()
                if response and response1.status_code == 200:
                    entry["target"] = row['target']
                    entry["sourcedb"] = row["sourcedb"]
                    entry["sourceid"]= row["sourceid"]
                    entry["text"]= row["text"]
                    entry["tracks"]= row["tracks"]
                    entry["trait_name"] = row['trait_name']
                    entry["project_name"] = "OryzaGP_2021_FLAIR,OryzaGP_2021,OryzaGP_2021_v2,OryzaGP"
                
                if entry:
                    puabannotation_refernce.append(entry)

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

save_to_tsv(puabannotation_refernce)
        
                
                






