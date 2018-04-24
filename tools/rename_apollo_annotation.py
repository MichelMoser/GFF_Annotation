#!/usr/bin/python
#coding: utf-8

from itertools import groupby
import sys
import re

######################################
##
## USAGE: python rename_apollo_annotation.py apollo.gff output.gff
## Author: Michel Moser
#####################################


gff_file = sys.argv[1]
output_file = sys.argv[2]



gene = 0
counter = 0

#gff is 1-based


#get cds for each gene
with open(output_file, "w") as out: 
   with open(gff_file, "r") as gff:

       gene_name = ""
       gene_id = ""
       mRNA_name = ""
       mRNA_id = ""
       mRNA_parent = ""
       exon_name = ""
       exon_id = ""
       seq_name = ""
       cds_positions = []
       exon_positions = []
       strand = ""
       
       for line in gff: 
        if line.startswith("#"): 
            #write cds of previous gene to file when gene ends
            if not gene_name: 
                continue
            else:
                gene += 1
                seq_name = gene_name[:-6]
               
                gene_name = ""
                gene_id = ""
                cds_position = []
                exon_positions = []
                strand = ""

                continue
                        
        line = line.strip()
        line = line.split("\t")
        if line[2] == "gene": 
            #print line[8]
            #get geneid and parent

            gene_name = re.sub(r'Name=([^;]*);.*', r'\1', line[8])
            gene_id = re.sub(r'.*ID=([^;]*);.*', r'\1', line[8])
            description = re.sub(r'.*description=([^;]*);.*', r'\1', line[8])

            print "###"
            
            print "\t".join(line[0:8])+"\tID="+gene_name+";Name="+gene_name+";functional_annotation="+description+";"
            #_name = line[8]
        elif line[2] == "mRNA": 

            mRNA_name = gene_name+".1"

            print "\t".join(line[0:8])+"\tID="+mRNA_name+";Parent="+gene_name+";functional_annotation="+description+";"

        elif line[2] != "mRNA" and line[2] != "gene":
            feature_name = re.sub(r'Parent=[^;]*;', "Parent="+mRNA_name+";", line[8])
            feature_name = re.sub(r'Name', r'ID', feature_name)

            print "\t".join(line[0:8])+"\t"+feature_name

        elif line[2] == "exon" and gene_id not in line[8]: 
            print "FAILED", line

