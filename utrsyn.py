#!/usr/bin/env python3

# Yizhu Lin
# 4/5/2021

import pandas as pd
from copy import deepcopy
class seqwithDB(object):

    startCodon = 'ATG'
    stopCodon = 'TAA' # UAA has less readthrough?  PMID: 29325104
    stopCodons = ['TGA', 'TAG', 'TAA']
    NCCstartCodons = ['CTG', 'GTG'] # TODO: add extra if needed 
    nonStartCodons = ['AAG'] 

    def __init__(self, utrseq, strucDB=''):
        self.utrseq = utrseq
        self.strucDB = strucDB
        self.utrLen = len(self.utrseq)
        if len(strucDB) == 0:
            # DB = dot-bracket format with only (.)
            # if no structrue input, use dot . 
            self.strucDB = '.'*self.utrLen
        else:
            # else seq and structure need have same length:
            assert(len(utrseq)==len(strucDB))
        self.uORFstarts = []
        self.uORFlengths = [] # len=-1 indicate no stop codon in UTR, run into main ORF. min length is 0, i.e. sth like ATGTGA
        return 
    
    def insertSeqDB(self, other, startloc, replaceLen=0):
        # replace (startloc, startloc+replaceLen) to insertSeq
        # if replaceLen == 0, i.e. insert
        # check original utr (startloc, end) is longer than length of insertSeq
        if startloc+replaceLen >= self.utrLen:
            print('cannot replace %d nt starting from %d, original seq too short' % (startloc, replaceLen))
            return
        self.utrseq = self.utrseq[0:startloc] + other.utrseq + self.utrseq[startloc+replaceLen:]
        self.strucDB = self.strucDB[0:startloc] + other.strucDB + self.strucDB[startloc+replaceLen:]
        self.utrLen = len(self.utrseq)
        return self.utrseq

    def mutateToStopCodon(self, loc):
        self.utrseq = self.utrseq[0:loc] + seqwithDB.stopCodon + self.utrseq[loc+3:]
        return

    def getPrintLine(self, sep=','):
        line = sep.join([self.utrseq, self.strucDB, 
                        ' '.join([str(x) for x in self.uORFstarts]), 
                        ' '.join([str(x) for x in self.uORFlengths])]
        )
        return line

class fivePrimeUTR(seqwithDB):
    upstreamFlankSeq = 'promoter'  # Fixed seq with promoter. TODO:replace with actuall seq
    downstreamFlankSeq = 'ATGgfpCDS' # fixed seq in main ORF. TODO:replace with actuall seq
    def __init__(self, utrseq, strucDB=''):
        super().__init__(utrseq, strucDB=strucDB)

def test():
    testSeq = 'A'*10
    utr = fivePrimeUTR(testSeq)
    elem = seqwithDB('G'*13, '...((...))...')
    print(utr.utrseq)
    utr.insertSeqDB(elem, 3, 0)
    print(len(utr.utrseq))
    print(len(utr.strucDB))
    print(utr.utrseq)
    utr.mutateToStopCodon(5)
    print(utr.utrseq)
    print(utr.strucDB)
    print(len(utr.utrseq))
    print(len(utr.strucDB))

def readUTRbackbones(filename):
    # csv
    UTRs = []
    df = pd.read_csv(filename)
    print(df)
    for index,row in df.iterrows():
        UTRs.append(fivePrimeUTR(row['seq']))
    return UTRs

def readStructElems(filename):
    # csv
    elems = []
    df = pd.read_csv(filename)
    print(df)
    for index,row in df.iterrows():
        elem = fivePrimeUTR(row['seq'], row['db'])
        elem.uORFstarts.append(row['AUGloc'])
        elems.append(elem)
    return elems

def combine(UTRs,elems, insertLocs=[10, 50] , uORFLengths=[0, 15]):
    ###
    outputUTRs = []
    for utr in UTRs:
        for insertLoc in insertLocs:
            for elem in elems:
                for l in uORFLengths:
                    newUTR = deepcopy(utr)
                    newUTR.insertSeqDB(elem, insertLoc, 0)
                    if elem.uORFstarts[0] >=0 :
                        stopCodonLoc = insertLoc+elem.uORFstarts[0]+l+3
                        newUTR.uORFstarts.append(insertLoc+elem.uORFstarts[0])
                        newUTR.uORFlengths.append(l)
                        newUTR.mutateToStopCodon(stopCodonLoc)
                    else:
                        # do not introduce uORF
                        pass
                    outputUTRs.append(newUTR)
    return outputUTRs

if __name__ == '__main__':
    UTRs = readUTRbackbones('utrbb.csv')
    elems = readStructElems('structElems.csv')
    outputUTRs = combine(UTRs, elems)
    outputFile='output.csv'
    with open(outputFile, 'a') as fh:
        for utr in outputUTRs:
            fh.write(utr.getPrintLine()+'\n')
    

