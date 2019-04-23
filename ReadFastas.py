import csv
import pandas as pd
import requests
import re 

URL = "http://sparks-lab.org/jack/server/SPOT-1D/index.php"
email = 'pssresearchproject@gmail.com'
tasks = [1]
sequence = ""
targetName = ""
method = 'SPOT-1D'

substring = ']}'
insertText = '\n'

print("Enter your CSV")
csv = input()

csv_input = pd.read_csv(csv, sep='\s*,\s*',header=0, encoding='ascii', engine='python')
df = pd.DataFrame(csv_input)


x = 1
while x < 2:
	targetName = df.iloc[x,1]
	print(targetName)

	fileName = df.iloc[x,4]
	file = open("SavedFastas/" + fileName, "r")
	
	sequence = file.read().replace('\n', '').upper()
	idx = sequence.index(substring) + len(substring)
	sequence = sequence[:idx] + insertText + sequence[idx:]
	print(sequence)



	#params = {'REPLY-E-MAIL': email, 'SEQUENCE' : sequence, 'TARGET' : targetName, 'METHOD' : method}
	#r = requests.post(url = URL, data = params)
#
	#result = re.search('info/(.*)/result', r.text)
	#print (result.group(1))



	x += 1

