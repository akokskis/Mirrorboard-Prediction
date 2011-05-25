## build.py
## Author: Ryan Kingston
## Last Updated: 5/2011
## Description: Contains functions to convert a text input-stream
##      into bigram and probability tables for various prediction
##      algorithms such as Viterbi.

from __future__ import division #floating-point division
import os, re, time, string, operator
from cPickle import load, dump
import mirror_functions
from pytrie import StringTrie as trie

path_separator = "\\"

## Initialize corpus of words
corpus = trie()

## Initialize bigram tries
wordbigrams = trie()
charbigrams = trie()
tranbigrams = trie()
obsbigrams = trie()

## Initialize probability tries
startProbs = trie()
transProbs = trie()
obsProbs = trie()

## All structures that are to be swapped to disk
structs = ("wordbigrams","charbigrams","tranbigrams", "obsbigrams", \
                   "transProbs", "startProbs", "obsProbs", "corpus")

##################################
## ----- FUNCTION HELPERS ----- ##
##################################
reg = re.compile('[^a-z\']+')
def sanitizeWord(n):
        global reg
        word = n.lower()
        word = word.strip('\'\.\,\?\!')
        word = re.sub(reg,'',word)
        return word

def isEndofSentence(n):
        for c in string.punctuation:
                if c == n[-1]: return True
        return False

def addObservation(c):
        m = mirror_functions.mirror(c)
        incrementInTable(m,c,obsbigrams)

def incrementInTable(x,y,t):
        curKey = x + '|' + y
        if t.has_key(curKey):
                curCount = t.__getitem__(curKey)
                t.__setitem__(curKey,curCount+1)
        else:
                t.__setitem__(curKey,1)

def incrementInTrie(key,trie):
        if trie.has_key(key):
                curCount = corpus.__getitem__(key)
                trie.__setitem__(key,curCount+1)
        else:
                trie.__setitem__(key,1)
                
def incrementInDict(key,dic):
        if dic.has_key(key):
                dic[key] += 1
        else:
                dic[key] = 1

def printStats():
        length = {}
        mirrors = {}
        
        for cur in corpus:
                incrementInDict(len(cur),length)
                incrementInDict(mirror_functions.mirrorCount(cur),mirrors)

        length = sorted(length.iteritems(), key=operator.itemgetter(0))
        mirrors = sorted(mirrors.iteritems(), key=operator.itemgetter(0))
        
        print " [Total Unique Words:", str(len(corpus)), "]"
        #print " ======================================"
        print " Length of Word\t Unique Occurrences"
        print " --------------\t ------------------"
        for cur in length:
                print "\t",cur[0], "\t\t", cur[1]

        print "\n # of Mirrors\t Unique Occurrences"
        print " --------------\t -------------------"
        for cur in mirrors:
                print "\t", cur[0], "\t\t", cur[1]
                

# Add-One Smoothing
# Note: Call after build but BEFORE build*Probs
#       This alters counts, not probabilities
def addOneCharSmooth():
        for i in (string.ascii_lowercase + '\' '):
                for j in (string.ascii_lowercase + '\' '):
                        incrementInTable(i,j,charbigrams)

def addOneObsSmooth():
        for i in "qwertasdfgzxcvb":
                for j in (string.ascii_lowercase + '\''):
                        incrementInTable(i,j,obsbigrams)

############################################
## ----- BUILD PROBABILITIES TABLES ----- ##
############################################

def buildObsProbs():
        global obsProbs,obsbigrams
        if len(obsbigrams)==0:
                print "ERROR: Empty observation bigrams. Please build or unpickle tables."
                return
        # \' is the only non-letter char that can precede other chars
        for i in (string.ascii_lowercase + "'.,?!"):
                prefixCount = 0
                prefixList = obsbigrams.items(prefix=(i+"|"))
                for occ in prefixList:
                        prefixCount += occ[1]
                for occ in prefixList:
                        obsProbs.__setitem__(occ[0],(occ[1]/prefixCount))

def buildStartProbs():
        global charbigrams,startProbs
        if len(charbigrams)==0:
                print "ERROR: Empty character bigrams. Please build or unpickle tables."
                return
        prefixCount = 0
        curList = charbigrams.items(prefix=" |")
        for occ in curList:
                prefixCount += occ[1]
        for occ in curList:
                startProbs.__setitem__(occ[0],(occ[1]/prefixCount))
        
def buildTransitionProbs():
        global transProbs,charbigrams,transProbs
        if len(charbigrams)==0:
                print "ERROR: Empty character bigrams. Please build or unpickle tables."
                return
        # \' is the only non-letter char that can precede other chars
        for i in (string.ascii_lowercase + '\''):
                prefixCount = 0
                prefixList = charbigrams.items(prefix=(i+"|"))
                for occ in prefixList:
                        prefixCount += occ[1]
                for occ in prefixList:
                        transProbs.__setitem__(occ[0],(occ[1]/prefixCount))
                        
######################################                        
## ----- BUILD BIGRAMS TABLES ----- ##
######################################
                        
def buildTables(s):
        startTime = time.time()
        infile = open("train"+ path_separator + s,"r")
        lineCount = 0
        wordCount = 0

        ## careful of string overflows!
        for line in infile:
                lineCount += 1
                line = line.replace('\x97',' ') # remove long dashes
                words = line.split()
                firstword = ' '
                secondword = ' '
                endOfSentence = False

                for w in words:
                        wordCount += 1
                        word = sanitizeWord(w)
                        firstword = secondword
                        secondword = word
                        if endOfSentence:
                                firstword = ' '
                                endOfSentence = False
                        if isEndofSentence(w): endOfSentence = True

                        ## - charbigrams -
                        firstletter = ' '
                        secondletter = ' '
                        for character in word:
                                ## - obsbigrams -
                                addObservation(character)
                                firstletter = secondletter
                                secondletter = character
                                incrementInTable(firstletter,secondletter,charbigrams)
                        ## - corpus -
                        incrementInTrie(word,corpus)
                        
                        ## - wordbigrams -
                        incrementInTable(firstword,secondword,wordbigrams)

                        ## - tranbigrams -
                        incrementInTable(mirror_functions.mirror(secondword),secondword,tranbigrams)
                      

        print "Lines Processed: ", str(lineCount)
        print "Words Processed: ", str(wordCount)
        print "Seconds: ", time.time() - startTime

        infile.close()

##########################
## ----- FILE I/O ----- ##
##########################

def refreshAll(s):
        print "Building counts..."
        buildTables(s)
        print "Smoothing transition counts..."
        addOneCharSmooth()
        print "Smoothing observation counts..."
        addOneObsSmooth()
        print "\nBuilding start probabilities..."
        buildStartProbs()
        print "Building transition probabilities..."
        buildTransitionProbs()
        print "Building observation probabilities..."
        buildObsProbs()
        print "Pickling tables..."
        pickleTables()

    
def pickleTables():
        global structs
        for s in structs:
                path = "train"+ path_separator + s + ".pickle"
                outfile = open(path,"wb")
                dump(eval(s),outfile)
                outfile.close()

def unpickleTables():
        global structs
        for s in structs:
                path = "train"+ path_separator + s + ".pickle"
                infile = open(path,"r")
                globals()[s] = load(infile)
                infile.close()
