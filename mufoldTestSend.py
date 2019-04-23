import csv 
import pandas as pd 
import requests 
import re


URL = "http://dslsrv2.eecs.missouri.edu/~zlht3/ss/submit"
email = 'pssresearchproject@gmail.com'
# its not letting me pass multiple strings in this
stateStructure = "1"
torsionAngles = "2"

#csv_input = pd.read_csv('CSVOutTest.csv', sep='\s*,\s*',header=0, encoding='ascii', engine='python')
#csv_input[MufoldID] = 'empty'

#df = pd.DataFrame(csv_input)


#requests.post(url, data={'interests': ['football', 'basketball']})

substring = ']}'
insertText = '\n'
#targetName = 'Test_2'

'''
r = requests.post(url = URL, data = {'email':email, 'target_name' : targetName, 'tasks[]': torsion, 'sequence' : sequence})
    print(r.text)
    
    result = re.search('results/(.*)">ss', r.text)
    print (result.group(1))
    
    df.iloc[x,5] = result.group(1)

'''

print("Enter your CSV")
csv = input()
print("Which SCOP Class?")
scopClass = input()


csv_input = pd.read_csv(csv + '.csv', sep='\s*,\s*',header=0, encoding='ascii', engine='python')
df = pd.DataFrame(csv_input)

if 'MufoldID' in df.columns:
    print("Already Has ID Column")
else:
    df['MufoldID'] = 'Empty'




def sendFasta( x ):
    try:
        
        fileName = df.iloc[x,4]
        file = open("SavedFastas/" +  fileName, "r")
        
        sequence = file.read().replace('\n', '').upper()
        idx = sequence.index(substring) + len(substring)
        sequence = sequence[:idx] + insertText + sequence[idx:]
        print(sequence)
        

        r = requests.post(url = URL, data = {'email':email, 'target_name' : targetName, 'tasks[]': torsionAngles, 'sequence' : sequence})
        #print(r.text)
    
        result = re.search('results/(.*)">ss', r.text)
        print (result.group(1))
    
        df.iloc[x,5] = result.group(1)

        return True
    except ValueError:
        print('error downloading fasta')
        return False
    except Exception as e:
        print('Unexpected Error')
        return False

x = 0
while x < len(df.index):
    
    targetName = df.iloc[x,0]
    
    print(targetName)
    print(df.iloc[x,5])
    
    if(df.iloc[x,5] == 'Empty'):
        if sendFasta(x):
            print('Sucess!')

    x += 1



df.to_csv('MUFOLD/MUFOLDOut' + scopClass + '.csv', index=False, quotechar = '"', doublequote = False, escapechar =',')
print(df)



