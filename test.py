## test.py
## Author: Ryan Kingston
## Last Updated: 5/2011
## Description: Contains testing functionality for mirrorboard

import build
import mirror_functions
import os, re, time, string

path_separator = "\\"


##################################
## ----- FUNCTION HELPERS ----- ##
##################################

def incrementDict(key,dict):
    if (dict.has_key(key)):
        dict[key] += 1
    else:
        dict[key] = 1

                        
######################################                        
## ----- TESTING SCRIPT ----- ##
######################################
                     
def runTest(s,n):
        startTime = time.time()
        infile = open("test"+ path_separator + s,"r")
        outfile = open("test" + path_separator + "results.csv", "w")
        outfile.write("word,mirror,length,numMirrors,predIndx,correct\n\n")

        ## Initialize testing counts
        wordCount = 0
        correctWords = 0
        allRslts = {}

        for line in infile:
                words = line.split()
                firstword = ' '
                secondword = ' '
                endOfSentence = False

                for w in words:
                        wordCount += 1
                        word = build.sanitizeWord(w)
                        mirror = mirror_functions.mirror(word)

                        #specify how to get these results
                        results = mirror_functions.getTopNext(mirror+'|','tran',n,"",True)

                        outfile.write(word + ',' + mirror + ',' + str(len(word)) + ',' + \
                                  str(mirror_functions.mirrorCount(word)) + ',')

                        # Correct prediction
                        if (word in results):
                                correctWords += 1
                                indx = results.index(word)
                                incrementDict(word + '|' + str(indx),allRslts)
                                outfile.write(str(indx) + ",1,\n")
                        else:
                                outfile.write(" ,0,\n")

        infile.close()
        outfile.close()

        ## Print results
        print "Seconds: ", time.time() - startTime
        print "Total words tested:", wordCount
        print "Total correctly predicted:", correctWords
        # print allRslts #debug
