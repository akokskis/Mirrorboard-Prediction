#! /usr/bin/env python

## main.py
## Author: Ryan Kingston
## Last Updated: 5/16/2011
## Description: Contains UI environment for running Mirrorboard
##      text prediction and supporting functions.

import build, cmd, os, sys, mirror_functions, viterbi, platform
from cPickle import load, dump

#path_separator = "/"
#
#learnFile = "oz.txt"
#learnPath = "train"+ path_separator + learnFile
#
#testFile = "none"
#testPath = "train"+ path_separator + testFile
#
#rslts = 6

mainConfig = {"path_separator":"/",
              "rslts":6,
              "learnFile":"oz.txt",
              "testFile": "none",
              }

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
        infile = open("config.pickle","r")
        mainConfig = load(infile)
        outfile.close()
    except:
        saveConfig()
        
    
    
def wait():
    raw_input("[ Hit enter to continue ]")

def drawScreen():
    #os.system('CLS')
    print '\n' * 80
    print "**************************************************************"
    print "* Mirrorboard Prediction v.0.1                               *"
    print "**************************************************************"
    print "* 1. Refresh all bigrams and probabilities and write to disk"
    print "* 2. Read all tables from disk"
    print "* 3. Set new learning file (Current: " + mainConfig['learnFile'] + ")"
    print "* ----------------"
    print "* 4. Manually test prediction"
    print "* 5. Test prediction against test file"
    print "* 6. Set new testing file (Current: " + mainConfig['testFile'] + ")"
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
    print "* 5. Change number of results (Current:"+ str(mainConfig['rslts']) +")"
    print "**************************************************************"
    
def testLoop():
    global mainConfig,vit
    while True:
        drawTest()
        ans = raw_input("* Select an option: ")
        if (ans == ""): break
        elif (ans == '1'):
            w = raw_input("Enter a whole word to predict next word: ")
            mirror_functions.getTopNext(w,'word',mainConfig['rslts'])
            wait()
        elif (ans == '2'):
            w = raw_input("Enter a prefix to predict word: ")
            mirror_functions.getTopPrefix(w,mainConfig['rslts'])
            wait()
        elif (ans == '3'):
            w = raw_input("Enter a mirrored prefix or word to predict word: ")
            mirror_functions.getTopNext(w,'tran',mainConfig['rslts'],"")
            wait()
        elif (ans == '4'):
            #viterbi mirrorboard
            #if vit == None:
            #    print "ERROR: Viterbi object not initialize properly.\nMakre sure tables are refreshed/loaded."
            #else:
            w = raw_input("Enter a mirrored word to predict word: ")
            print vit.runViterbi(w)
            wait()
            
        elif (ans == '5'):
            r = raw_input("Select desired number of results (1-14): ")
            if (r.isdigit() and (int(r) in range(1,15))):
                mainConfig['rslts'] = int(r)
                saveConfig()
                print "Updated successfully"
            else:
                print "ERROR: Not a valid option. Enter 1-14 only."
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
        elif (ans in "123456"):
            if (ans == '1'):
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
                    wait()
                else:
                    mainConfig['learnFile'] = f
                    saveConfig()
            elif (ans == '4'):
                testLoop()
            elif (ans == '5'):
                print "You selected 5"
            elif (ans == '6'):
                print "You selected 6"
                # herp derp
                saveConfig()


main()
    
