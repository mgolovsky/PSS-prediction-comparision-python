import csv 
import pandas as pd 
import requests 
import re

URL = "http://sparks-lab.org/server/SPIDER3/index.php"
email = 'pssresearchproject@gmail.com'
sequence = ''
targetName = ""
method = 'SPIDER3'


substring = ']}'
insertText = '\n'

print("Enter your CSV")
csv = input()
print("Which SCOP Class?")
scopClass = input()


csv_input = pd.read_csv(csv + '.csv', sep='\s*,\s*',header=0, encoding='ascii', engine='python')
df = pd.DataFrame(csv_input)

def sendFasta( x ):
	try:

		fileName = df.iloc[x,4]
		file = open("SavedFastas/" +  fileName, "r")

		sequence = file.read().replace('\n', '').upper()
		idx = sequence.index(substring) + len(substring)
		sequence = sequence[:idx] + insertText + sequence[idx:]
		print(sequence)
	
		params = {'REPLY-E-MAIL': email, 'SEQUENCE' : sequence, 'TARGET' : targetName, 'METHOD' : method}
		r = requests.post(url = URL, data = params)
	
		result = re.search('info/(.*)/result', r.text)
		print (result.group(1))
	
		df.iloc[x,5] = result.group(1)
		return True
	except ValueError: 
		print('error downloading fasta')
		return False
	except Exception as e: 
		print('Unexpected Error')

x = 0 
while x < len(df.index):
	targetName = df.iloc[x,0]
	print(targetName)
	print(df.iloc[x,5])
	if(df.iloc[x,5] == 'empty'):
		if sendFasta(x):
			print('Sucess!')

	x += 1



df.to_csv('SPIDER3/SPIDER3Out' + scopClass + '.csv', index=False, quotechar = '"', doublequote = False, escapechar =',')
print(df)

