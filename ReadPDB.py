# Please see accompanying webpage:
# 
# http://www.warwick.ac.uk/go/peter_cock/python/ramachandran/calculate/
#
# This code relies on Thomas Hamelryck's Bio.PDB module in BioPython:
#
# http://www.biopython.org
#
# It assumes the input file 1HMP.pdb is in the current directory,
# and generates an output file 1HMP_biopython.tsv in the current directory.

import math
import requests
import pandas as pd
import csv
import Bio
import Bio.SeqUtils
from Bio.SeqUtils import seq1

def degrees(rad_angle) :
    """Converts any angle in radians to degrees.

    If the input is None, the it returns None.
    For numerical input, the output is mapped to [-180,180]
    """
    if rad_angle is None :
        return None
    angle = rad_angle * 180 / math.pi
    while angle > 180 :
        angle = angle - 360
    while angle < -180 :
        angle = angle + 360
    return angle

def ramachandran_type(residue, next_residue) :
    """Expects Bio.PDB residues, returns ramachandran 'type'

    If this is the last residue in a polypeptide, use None
    for next_residue.

    Return value is a string: "General", "Glycine", "Proline"
    or "Pre-Pro".
    """
    if residue.resname.upper()=="GLY" :
        return "Glycine"
    elif residue.resname.upper()=="PRO" :
        return "Proline"
    elif next_residue is not None \
    and next_residue.resname.upper()=="PRO" :
        #exlcudes those that are Pro or Gly
        return "Pre-Pro"
    else :
        return "General"


#URL = 'https://files.rcsb.org/download/%s.pdb' % pdb_code
#urllib.request.urlretrieve(URL, pdb_code+ '.ent')


def Main(scop_class, pdb_code):
    print ("About to load Bio.PDB and the PDB file...")
    
    import Bio.PDB
    
    structure = Bio.PDB.PDBParser().get_structure(pdb_code, "PDBS/{}/{}.ent".format(scop_class, pdb_code))
    print ("Done")

    print ("About to save angles to file...")
    output_file = open("DihedralAnglesMissing/{}/{}_biopython.csv".format(scop_class, pdb_code),"w")
    output_file.write("Domain, ID, Residue, Phi, Psi, Ramachandran_Type\n")
    for chain in structure[0] :
        print ("Chain %s" % str(chain.id))
        polypeptides = Bio.PDB.CaPPBuilder().build_peptides(chain)
        for poly_index, poly in enumerate(polypeptides) :
            phi_psi = poly.get_phi_psi_list()
            for res_index, residue in enumerate(poly):
                phi, psi = phi_psi[res_index]
                if phi and psi:
                    output_file.write("%s:Chain%s,%s,%s,%f,%f,%s\n" \
                                        % (pdb_code, str(chain.id),
                                        residue.id[1],seq1(residue.get_resname()), degrees(phi), degrees(psi),
                                        ramachandran_type(residue, poly[res_index+1])))
                    #Don't write output when missing an angle
                    #residue.id[1] is the number, thats what I need to compare to the domain length
                    #residue.get_resname()       returns the residue name, e.g. "ASN"
                else:
                    output_file.write("{}:Chain{},{},{},{},{},{}\n".format(pdb_code, str(chain.id),residue.id[1],seq1(residue.get_resname()),"Missing", "Missing", "Missing"))
                    print("Missing Phi and Psi")
                            #create a list of residue names(put them into fasta format), compare against a list from the predicted values
    output_file.close()
    print ("Done")

'''
print("Input PDB Code")
pdb_code = input()

print("Scop Class")
scop_class = input()

Main(scop_class, pdb_code)

'''
