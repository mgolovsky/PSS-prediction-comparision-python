import pandas as pd
import csv
import sklearn.metrics
from pathlib import Path
import ReadPDB
import re 
import sys
import os
import numpy as np
from io import StringIO
sys.path.append(os.path.abspath("Users⁩/macbook⁩/Documents⁩/PSS⁩/Scripts"))

print("Select Class") 
scop_class = input().upper()

print("Which Predictor")
predictor = input().upper()

csv_predictedStructures = '{}/{}Out{}.csv'.format(predictor,predictor,scop_class)
csv_trueStructures = 'CSVs/Scop{}Class.csv'.format(scop_class)

predicted_file_ending = '.csv'

if predictor == 'SPIDER3':
    predicted_file_ending = '.spd33'
    phi = 'Phi'
    psi = 'Psi'
    sep = '\s+'
if predictor == 'SPOT1D':
    predicted_file_ending = '.spot1d8'
    phi = 'phi'
    psi = 'psi'
    sep = '\s+'
if predictor == 'MUFOLD':
    predicted_file_ending = '.angles'
    phi = 'Phi'
    psi = 'Psi'
    sep = ','




predictedStructures = pd.read_csv(csv_predictedStructures, sep='\s*,\s*',header=0, encoding='ascii', engine='python')
predictedStructures = pd.DataFrame(predictedStructures)
predictedStructures['MAE PHI'] = 'empty'
predictedStructures['MAE PSI'] = 'empty'

trueStructures = pd.read_csv(csv_trueStructures, sep='\s*,\s*', encoding='ascii', engine='python')
trueStructures = pd.DataFrame(trueStructures)


def phiPrediction(predictedData, trueData, ids):
    #trueData = pd.read_csv(trueData, sep='\s*,\s*',header= 'none', encoding='ascii', engine='python')
    
    trueData = pd.DataFrame(trueData)
    predictedData = pd.DataFrame(predictedData)
    
    trueData[["ID", "Phi", "Psi"]] = trueData[["ID", "Phi", "Psi"]].apply(pd.to_numeric, errors = 'coerce')
    print(type(trueData.iloc[1,1]))
    
    truePhiValues = trueData['Phi'].tolist()
    
    #print("Overlap start {} end {}".format(start_delete, end_delete))
    #create dataframe to
    #df.iloc[0] = [0,0]
    first_id = int(ids[0])
    last_id = int(ids[len(ids) - 1])
    print('First ID {}, last ID {}'.format(first_id, last_id))
    #the second missing flag isnt getting deleted
    
    new_index = range(first_id, last_id)
    trueData = trueData[~trueData.ID.duplicated()]
    trueData = (trueData.set_index('ID')
        .reindex(new_index)
        .interpolate()
        .reset_index())
    trueData[['Domain', 'Residue', 'Ramachandran_Type']] = trueData[['Domain', 'Residue', 'Ramachandran_Type']].ffill()
                

                #del truePhiValues [0]
    
    x = len(trueData.index) - 1
    while x >= 0 :
        if(trueData.iloc[x, 5] == 'Missing'):
            try:
                print('Deleting Missing Data from row {}'.format(x))
                trueData.drop(x)
                predictedData.drop(x)
            except:
                break
        x -= 1
    
    trueData[~trueData.Ramachandran_Type.str.contains("Missing")]
#predictedData[~trueData.Ramachandran_Type.str.contains("Missing")]
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        trueData.dropna()
        predictedData.dropna()
        print(trueData)
        
    predictedPhiValues = predictedData[phi].tolist()
    truePhiValues = trueData['Phi'].tolist()
    while True:
        if len(predictedPhiValues) > len(trueData.index) :
            print('Deleting Last phi value')
            print(predictedPhiValues [len(predictedPhiValues) - 1])
            del predictedPhiValues [len(predictedPhiValues) - 1]
        else:
            break
    del truePhiValues[0]
    del predictedPhiValues[0]

    print(len(truePhiValues))
    print(len(predictedPhiValues))
    
    try:
        mae_phi = sklearn.metrics.mean_absolute_error(predictedPhiValues, truePhiValues)
        print(mae_phi)
        return mae_phi
    except Exception as e:
        print(e)
        return "Mismatched Length"

def psiPrediction(predictedData, trueData, ids):

    #trueData = pd.read_csv(trueData, sep='\s*,\s*',header= 'none', encoding='ascii', engine='python')
    
    trueData = pd.DataFrame(trueData)
    predictedData = pd.DataFrame(predictedData)
    
    trueData[["ID", "Psi", "Psi"]] = trueData[["ID", "Psi", "Psi"]].apply(pd.to_numeric, errors = 'coerce')
    print(type(trueData.iloc[1,1]))
    
    truePsiValues = trueData['Psi'].tolist()
    
    #print("Overlap start {} end {}".format(start_delete, end_delete))
    #create dataframe to
    #df.iloc[0] = [0,0]
    first_id = int(ids[0])
    last_id = int(ids[len(ids) - 1])
    print('First ID {}, last ID {}'.format(first_id, last_id))
    #the second missing flag isnt getting deleted
    
    new_index = range(first_id, last_id)
    trueData = trueData[~trueData.ID.duplicated()]
    trueData = (trueData.set_index('ID')
        .reindex(new_index)
        .interpolate()
        .reset_index())
    trueData[['Domain', 'Residue', 'Ramachandran_Type']] = trueData[['Domain', 'Residue', 'Ramachandran_Type']].ffill()
        
        
        #del truePsiValues [0]
    
    x = len(trueData.index) - 1
    while x >= 0 :
        if(trueData.iloc[x, 5] == 'Missing'):
            try:
                print('Deleting Missing Data from row {}'.format(x))
                trueData.drop(x)
                predictedData.drop(x)
            except:
                break
        x -= 1
    
    trueData[~trueData.Ramachandran_Type.str.contains("Missing")]
#predictedData[~trueData.Ramachandran_Type.str.contains("Missing")]
#trueData[~trueData.Ramachandran_Type.str.contains("Missing")]

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        trueData.dropna()
        predictedData.dropna()
        print(trueData)
        
    predictedPsiValues = predictedData[psi].tolist()
    truePsiValues = trueData['Psi'].tolist()
    while True:
        if len(predictedPsiValues)  > len(trueData.index) :
            print('Deleting Last psi value')
            print(predictedPsiValues [len(predictedPsiValues) - 1])
            del predictedPsiValues [len(predictedPsiValues) - 1]
        else:
            break
    del truePsiValues[0]
    del predictedPsiValues[0]

    print(len(truePsiValues))
    print(len(predictedPsiValues))
        
    try:
        mae_psi = sklearn.metrics.mean_absolute_error(predictedPsiValues, truePsiValues)
        print(mae_psi)
        return mae_psi
    except Exception as e:
        print(e)
        return "Mismatched Length"

x = 0
while x < len(predictedStructures.index):
   

    predicted_domain = predictedStructures.iloc[x,0]
    
    angleData = Path( '{}/{}/{}{}'.format(predictor,scop_class,predicted_domain,predicted_file_ending))
    if angleData.is_file() == False:
        x += 1 
        continue
   
    dihedral_angle = Path('DihedralAnglesMissing/{}/{}_biopython.csv'.format(scop_class, predicted_domain))
    if dihedral_angle.is_file() == False:
        print("Generating CSV of True Values")
        ReadPDB.Main(scop_class,predicted_domain)

    #temp_trueData_holder = open('DihedralAngles/{}/{}_biopython.csv'.format(scop_class, predicted_domain), "r")
    #temp_trueData_holder = temp_trueData_holder.read()


    predictedDataCSV = pd.read_csv('{}/{}/{}{}'.format(predictor,scop_class,predicted_domain,predicted_file_ending),sep= sep)

    trueDataCSV = pd.read_csv('DihedralAnglesMissing/{}/{}_biopython.csv'.format(scop_class, predicted_domain), sep='\s*,\s*', encoding='ascii', engine='python')
    print(predicted_domain)
 

    lenDifference = (len(trueDataCSV.index) - len(predictedDataCSV.index))
    print(lenDifference)
    ids = trueDataCSV['ID'].values.tolist()

# predictedData = predictedData.head(len(trueData.index))


    mae_phi = phiPrediction(predictedDataCSV, trueDataCSV, ids)
    mae_psi = psiPrediction(predictedDataCSV, trueDataCSV, ids)

    predictedStructures.iloc[x,7] = mae_phi
    predictedStructures.iloc[x,8] = mae_psi


    x += 1



predictedStructures.to_csv(csv_predictedStructures, index=False, quotechar = '"', doublequote = False, escapechar =',')
print(predictedStructures)

