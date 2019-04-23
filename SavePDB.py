import urllib.request
import csv
import pandas as pd
import re
from pathlib import Path


print("Choose CSV")
chosen_csv = input()
print("Which Class")
scop_class = input()
csv_input = pd.read_csv(chosen_csv, sep='\s*,\s*',header=0, encoding='ascii', engine='python')
df = pd.DataFrame(csv_input)
df["PDB Stored"] = 'empty'
df["PDB ID"] = 'empty'



x = 0
def DownloadPDB (x):
    try:
        URL= "http://scop.berkeley.edu/astral/pdbstyle/?ver=2.07&id={}&output=text".format(domain)
        data = urllib.request.urlretrieve(URL, "PDBs/{}/{}.ent".format(scop_class, domain))
        with open('PDBs/{}/{}.ent'.format(scop_class, domain), 'r') as pdb:
            pdb_entry_lines = pdb.readlines()
            pdb_entry = pdb_entry_lines[6]
            print(pdb_entry)
            pdb_id = re.search('Source-PDB: (.*)\n', pdb_entry)
            print(pdb_id.group(1))
            df.iloc[x,5] = 'PDBs/{}.ent'.format(domain)
            df.iloc[x,6] = pdb_id.group(1)
    except Exception as e:
        print(e)

while x < len(df.index):
    #print(df.ix[x,0])
    domain = df.iloc[x,0]
    print(domain)
    existing_pdb = Path("PDBs/{}/{}.ent".format(scop_class, domain))
    if existing_pdb.is_file() == False:
        DownloadPDB( x )
    x += 1



df.to_csv(chosen_csv, index=False, quotechar = '"', quoting = csv.QUOTE_NONE, doublequote = False, escapechar =',')
