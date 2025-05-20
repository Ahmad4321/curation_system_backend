

import sqlite3




conn = sqlite3.connect('../curation_system/ricetrait.db.sqlite3')
cursor = conn.cursor()
def parse_obo(file_path):
    unique_terms = set()
    with open(file_path, 'r',encoding="utf-8") as file:
        term = {}
        for line in file:
            line = line.strip()
            if line == "[Term]":
                if term:
                    yield term
                    term = {}
            elif line and ":" in line:
                key, val = line.split(":", 1)
                term.setdefault(key.strip(), []).append(val.strip())
                unique_terms.add(key.strip())
        if term:
            yield term
            print(f"Unique keys found: {unique_terms}")

data = parse_obo("./RTO-1.0.obo")
for term in parse_obo("./RTO-1.0.obo"):
    id,name,is_a,sentence,xref,comment,synonym,is_obsolete = None,None,None,None,None,None,None,None
    if term.get('id'):
        id = ",".join(term.get('id'))
    if term.get('name'):
        name = ",".join(term.get('name'))
    if term.get('def'):
        sentence = ",".join(term.get('def'))
    if term.get('is_a'):
        is_a = ",".join(term.get('is_a'))
    if term.get('xref'):
        xref = ",".join(term.get('xref'))
    if term.get('comment'):
        comment = ",".join(term.get('comment'))
    if term.get('synonym'):
        synonym = ",".join(term.get('synonym'))
    if term.get('is_obsolete'):
        is_obsolete = ",".join(term.get('is_obsolete'))

    #  Insert the data into the database
    query = """
    INSERT INTO trait_explaination (sentence, is_obsolete, is_a, xref, synonym, comment, name, trait_ontology_id)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?);
    """ 
    cursor.execute(query, (sentence, is_obsolete, is_a, xref, synonym, comment, name.lower(), id))

conn.commit()
conn.close()

