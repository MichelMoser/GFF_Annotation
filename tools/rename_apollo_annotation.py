#!/usr/bin/python
#coding: utf-8

from itertools import groupby
import sys
import re

######################################
##
## USAGE: python extract_mRNA.py file.gff file.fasta outputfile.fasta
##
#####################################


gff_file = sys.argv[1]
output_file = "t" #sys.argv[2]


def rev_comp(seq): 
    revcompl = lambda x: ''.join([{'N':'N','A':'T','C':'G','G':'C','T':'A'}[B] for B in x][::-1])
    return revcompl(seq)

def get_mRNA(position_list, seq): 
    """
    given sequence, list of tuples of start and end positions of exons and gene name, create fasta output
    """
    mRNA = ""
    for start, end in position_list: 
        mRNA += seq[int(start):int(end)]

    return mRNA


def fasta_iter(fasta_name):
        """
        given a fasta file. yield tuples of header, sequence
        """
                    
        fh = open(fasta_name)
        # ditch the boolean (x[0]) and just keep the header or sequence since
        # we know they alternate.
        fa_list = []
        faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
        for header in faiter:
            # drop the ">"
            header = header.next()[1:].strip()
            # join all sequence lines to one.
            seq = "".join(s.strip() for s in faiter.next())
            fa_list.append((header, seq))
        #yield header, seq
        return fa_list



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

