import pandas as pd
import csv
import requests
import re
import urllib.request




print("Which Server?")
prediction_server = input().upper()
print("Which Class")
scop_class = input().upper()

csv_input = '{}/{}Out{}.csv'.format(prediction_server,prediction_server, scop_class)


csv_input = pd.read_csv(csv_input, sep='\s*,\s*',header=0, encoding='ascii', engine='python')
csv_input['Prediction Location'] = 'empty'

def DownloadPredictionSpider(access_code, domain_name):
    url = 'http://sparks-lab.org/info/SPIDER3/{}/s0.spd33'
    try:
        data = urllib.request.urlretrieve(url.format(access_code),'SPIDER3/{}/{}.spd33'.format(scop_class.upper(), domain_name))
        print ('Success!')
        return 'SPIDER3/{}/{}.spd33'.format(scop_class.upper(), domain_name)
    except:
        print("Failed to Download Spider")
        return 'Failed to Download'

def DownloadPredictionSpot(access_code, domain_name):
    url = 'http://sparks-lab.org/info/SPOT-1D/{}/s0.spot1d8'
    try:
        data = urllib.request.urlretrieve(url.format(access_code),'SPOT1D/{}/{}.spot1d8'.format(scop_class.upper(), domain_name))
        print ('Success!')
        return 'SPOT1D/{}/{}.spot1d8'.format(scop_class.upper(), domain_name)
    except:
        print("Failed to Download Spot")
        return 'Failed to Download'

def DownloadPredictionMuFold(access_code, domain_name):
    url = 'http://dslsrv2.eecs.missouri.edu/~zlht3/ss/download_angle_results_only/'
    try:
        data = urllib.request.urlretrieve(url + access_code, 'MUFOLD/Lists/{}/{}.angles'.format(scop_class.upper(),  domain_name))
        print('Success!')
        return 'MUFOLD/Lists/{}/{}.angles'.format(scop_class.upper(),  domain_name)
    except:
        print("Failed to Download Mufold")
        return 'Failed to Download'


x=0
while x< len(csv_input.index):
    access_code = csv_input.iloc[x,5]
    domain_name = csv_input.iloc[x,0]
    print(access_code)
    print(domain_name)
    if(csv_input.iloc[x,6] == 'empty' or csv_input.iloc[x,6] == 'Failed to Download') and access_code.upper() != 'EMPTY':
        if(prediction_server.upper() == "SPIDER3"):
            success = DownloadPredictionSpider(access_code, domain_name)
        elif(prediction_server.upper() == "SPOT1D"):
            success = DownloadPredictionSpot(access_code, domain_name)
        elif (prediction_server.upper() == "MUFOLD"):
            success = DownloadPredictionMuFold(access_code, domain_name)
    csv_input.iloc[x,6] = success
    
    x +=1

csv_input.to_csv('{}/{}Out{}.csv'.format(prediction_server, prediction_server, scop_class), index=False, quotechar = '"', doublequote = False, escapechar =',')
print(csv_input)

