import requests 
import csv
import time
import pandas as pd


csv.field_size_limit(1_000_000_000)

count = 1
def puabannoationAPI(id):

    try:

        url = "https://pubannotation.org/docs/sourcedb/PubMed/sourceid/"+str(id)+"/annotations.json?projects=OryzaGP_2021_FLAIR,OryzaGP_2021,OryzaGP_2021_v2,OryzaGP"

        payload = ""
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response
    except:
        return "Too many request"
puabannotation_refernce = []


pmid_error = ""
initial = 200
final = 210
df = pd.read_csv("pubannotation_pmids.tsv",sep='\t')
for i in range(0,int(len(df['0'])/10+1)):
    function_perform = df['0'][initial:final]
    print(initial,final)

    for re in function_perform:
        entry = {}
        if count == 10:
            try:
                print ("System has posted more than 10 ,No system is going to pause for 10 minutes!")
                time.sleep(180)
                count = 0 
                old_data = pd.read_csv("pubannotation_done.tsv",sep='\t')
                print(len(puabannotation_refernce),len(old_data))
                if len(old_data) != 0:
                    dd =pd.DataFrame(puabannotation_refernce)
                    new_data = pd.concat([old_data, dd], ignore_index=True)
                    new_data.to_csv("pubannotation_done.tsv",sep='\t')
                    puabannotation_refernce = []
                else:
                    # dd =pd.DataFrame(puabannotation_refernce).to_csv("pubannotation_done.tsv",sep='\t')
                    print("exception")
            except:
                pd.DataFrame(puabannotation_refernce).to_csv("pubannotation_done.tsv",sep='\t')
        response = puabannoationAPI(re)
        if response == "Too many request":
            pmid_error += str(re)+","
            time.sleep(180)
            continue
        else:
            if response.status_code == 200:
                response = response.json()
                if response :
                    entry["target"] = response['target']
                    entry["sourcedb"] = response["sourcedb"]
                    entry["sourceid"]= response["sourceid"]
                    entry["text"]= response["text"]
                    entry["tracks"]= response["tracks"]
                    entry["project_name"] = "OryzaGP_2021_FLAIR,OryzaGP_2021,OryzaGP_2021_v2,OryzaGP"
                
                if entry:
                    puabannotation_refernce.append(entry)
        count += 1
        print(count)
    initial = int(final)
    final = int(initial+10)



        
                
                






