## mirror_functions.py
## Author: Ryan Kingston
## Last Updated: 5/16/2011
## Description: Contains misc. funcions for translating
##      and returning words.

from string import maketrans
import build
import re

## Functions for keyboard/word mirroring
## -------------------------------------------

reg_layout = "abcdefghijklmnopqrstuvwxyz\'.,"
mir_layout = "abcdefggefdscvwqqrstrvwxtzazx"
unique_right = "yuiophjklnm\'"
trantable = maketrans(reg_layout,mir_layout)
revtrantable = maketrans(mir_layout,reg_layout)

## Convert string to its mirrored keyboard equivalent
def mirror(n):
    return n.translate(trantable)

def unmirror(n):
    return n.translate(revtrantable)

def mirrorCount(n):
    return len(filter(lambda x: x in unique_right, n))

## Accessing words from distribution
## -------------------------------------------

def getTopNext(pref, c, n, delin='|', silent=False):
    if n<1: return []

    if c == 'word': corp = build.wordbigrams
    elif c == 'char': corp = build.charbigrams
    elif c == 'tran': corp = build.tranbigrams
    else:
        if (not silent): print "Error: Please pass a correct bigram type"
        if (not silent): print "options - \'word\', \'char\', or \'tran\'"
        return []
    
    l = corp.items(prefix=(pref + delin))
    l = sorted(l, key=lambda pair: pair[1])

    if len(l) == 0:
            if (not silent): print "Error: prefix", pref, "not found in corpus"
            return []

    else:
        ## loop on top n words
        retVal = list()
        it = min(len(l),n)
        for i in range(1,it+1):
            pair = l[-i][0]
            nxt = pair.split('|')[1]
            if (not silent): print nxt, "(" + str(l[-i][1]) + ")"
            retVal.append(nxt)
        return retVal

def getTopPrefix(pref, n, silent=False):
    if n<1: return ""
    l = build.corpus.items(prefix=pref)
    l = sorted(l, key=lambda pair: pair[1])

    if len(l) == 0:
            if (not silent): print "Error: prefix", pref, "not found in corpus"
            return []
    else:
        retVal = list()
        it = min(len(l),n)
        for i in range(1,it+1):
            w = l[-i][0]
            if (not silent): print w, "(" + str(l[-i][1]) + ")"
            retVal.append(w)
        return retVal
