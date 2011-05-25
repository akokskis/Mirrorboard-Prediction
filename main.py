#! /usr/bin/env python

## main.py
## Author: Ryan Kingston
## Last Updated: 5/2011
## Description: Contains UI environment for running Mirrorboard
##      text prediction and supporting functions.

import cmd, os, sys, platform
from cPickle import load, dump
import test, build, mirror_functions, viterbi

mainConfig = {"path_separator":"/",
              "rslts":6,
              "learnFile":"catch22.txt",
              "testFile": "test.txt" }

# variable to hold the viterbi object
vit = None

# save our current config. called anytime one of the config vars is modified
def saveConfig():
    global mainConfig
    outfile = open("config.pickle","wb")
    dump(mainConfig,outfile)
    outfile.close()

# load the config vars.  if none exist, we'll create new ones based on the defaults up top.
def loadConfig():
    global mainConfig
    try:
        outfile = open("config.pickle","r")
        mainConfig = load(outfile)
        outfile.close()
    except:
        saveConfig()
    
def wait():
    raw_input("[ Hit enter to continue ]")

def isValidInput(w,flag=True):
    retVal = True
    if flag: chars = mirror_functions.reg_layout
    else: chars = mirror_functions.mir_layout
    for c in w:
        if (c not in chars):
            retVal = False
            break
    return retVal

def drawScreen():
    #os.system('CLS')
    print '\n' * 80
    print "**************************************************************"
    print "* Mirrorboard Prediction v.0.1                               *"
    print "**************************************************************"
    print "* 1. Refresh all bigrams and probabilities and write to disk"
    print "* 2. Read all tables from disk"
    print "* 3. Set new learning file (Current: " + mainConfig['learnFile'] + ")"
    print "* 4. Show statistics for current learning set"
    print "* ----------------"
    print "* 5. Manually test prediction"
    print "* 6. Test prediction against test file"
    print "* 7. Set new testing file (Current: " + mainConfig['testFile'] + ")"
    print "* 8. Change number of predictions per input (Current:" + str(mainConfig["rslts"]) + ')'
    print "**************************************************************"

def drawTest():
    #os.system('CLS')
    print '\n' * 80
    print "**************************************************************"
    print "* Mirrorboard Prediction v.0.1 [Testing]                     *"
    print "**************************************************************"
    print "* 1. Next word "
    print "* 2. Words from prefix "
    print "* 3. Dumb Mirrorboard "
    print "* 4. Viterbi Mirrorboard "
    print "**************************************************************"
    
def testLoop():
    global mainConfig,vit
    while True:
        drawTest()
        ans = raw_input("* Select an option: ")
        if (ans == ""): break
        elif (ans == '1'):
            w = raw_input("Enter a whole word to predict next word: ")
            if isValidInput(w): mirror_functions.getTopNext(w,'word',mainConfig['rslts'])
            else: print "ERROR: Please use only [a-z] or apostrophe"
            wait()
        elif (ans == '2'):
            w = raw_input("Enter a prefix to predict word: ")
            if isValidInput(w): mirror_functions.getTopPrefix(w,mainConfig['rslts'])
            else: print "ERROR: Please use only [a-z] or apostrophe"
            wait()
        elif (ans == '3'):
            w = raw_input("Enter a mirrored prefix or word to predict word: ")
            if isValidInput(w,False): mirror_functions.getTopNext(w,'tran',mainConfig['rslts'],"")
            else: print "ERROR: Please use only [qwertasdfgzxcvb], apostrophe, or pipe"
            wait()
        elif (ans == '4'):
            w = raw_input("Enter a mirrored word to predict word: ")
            if isValidInput(w,False): print vit.runViterbi(w)
            else: print "ERROR: Only use [qwertasdfgzxcvb] or apostrophe"
            wait()


def main():
    global mainConfig,vit
    loadConfig()
    if (platform.system() == "Windows"):
       # in case we're using... winblows
       mainConfig['path_separator'] = "\\"
       saveConfig()
    while True:
        drawScreen()
        ans = raw_input("* Select an option: ")
        if ans == "": break

        elif (ans == '1'):
            print "Refreshing all tables from file..."
            build.refreshAll(mainConfig['learnFile'])
            vit = viterbi.viterbi(build.startProbs, build.transProbs, build.obsProbs)
            print "Refreshing complete"
            wait()
        elif (ans == '2'):
            print "Unpickling tables..."
            build.unpickleTables()
            vit = viterbi.viterbi(build.startProbs, build.transProbs, build.obsProbs)
            print "Unpickling complete."
            wait()
        elif (ans == '3'):
            print "Training text file must be in "+mainConfig['path_separator']+"train directory!"
            f = raw_input("Select a new training file: ")
            newPath = "train"+mainConfig['path_separator']+f
            if (not os.path.isfile(newPath)):
                print "ERROR: Not a valid file"
            else:
                mainConfig['learnFile'] = f
                saveConfig()
                print "Updated successfully"
            wait()
        elif (ans == '4'):
            build.printStats()
            wait()
        elif (ans == '5'):
            testLoop()
        elif (ans == '6'):
            test.runTest(mainConfig["testFile"],mainConfig["rslts"])
            wait()
        elif (ans == '7'):
            print "Testing text file must be in "+mainConfig['path_separator']+"test directory!"
            f = raw_input("Select a new training file: ")
            newPath = "test"+mainConfig['path_separator']+f
            if (not os.path.isfile(newPath)):
                print "ERROR: Not a valid file"
            else:
                mainConfig['testFile'] = f
                saveConfig()
                print "Updated successfully"
            wait()
        elif (ans == '8'):
                r = raw_input("Select desired number of results (1-14): ")
                if (r.isdigit() and (int(r) in range(1,15))):
                    mainConfig['rslts'] = int(r)
                    saveConfig()
                    print "Updated successfully"
                else:
                    print "ERROR: Not a valid option. Enter 1-14 only."
                wait()


main()
    
