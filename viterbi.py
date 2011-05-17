#!/usr/bin/python

import build
from math import log,exp
import pprint

# run some setup stuff
build.unpickleTables()

pp = pprint.PrettyPrinter(indent=4)
tinyVal = 0.000000000000001#log(0.000000000000001)

states_all = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
          'r','s','t','u','v','w','x','y','z','\'')
states_leftH = ('a','b','c','d','e','f','g','g','e','f','d','s','v','v','w','q','q','r','s','t','r','v','w','x','t','z','a','z','x','\'')


def initProbs():
    probs = {}
    for st in states_all:
        probs[st] = {}
    return probs
    
def formatStartProbs(p):
    probs = initProbs()
    it = p.iteritems()
    for cur in it:
        probs[cur[0][2]] = cur[1]#log(cur[1]) #take just the letter and the prob.  least neg is biggest
    probs = fixStartProbs(probs)
    return probs

def formatTransProbs(p):
    probs = initProbs()
    it = p.iteritems()
    for cur in it:
        tmp = probs[cur[0][0]]
        tmp[cur[0][2]] = cur[1]#log(cur[1])
#    probs = fixOtherProbs(probs)
    return probs

def formatObsProbs(p):
    probs = initProbs()
    it = p.iteritems()
    for cur in it:
        tmp = probs[cur[0][2]]
        tmp[cur[0][0]] = cur[1]#log(cur[1])
#    probs = fixOtherProbs(probs)
    return probs

def fixStartProbs(p):
    for s in states_all:
        if p[s] == {}:
            p[s] = tinyVal
    return p

def fixOtherProbs(p):
    for sOuter in states_all:
        tmp = p[sOuter]
        for sInner in states_all:
            try: 
                if tmp[sInner] == {}:
                    tmp[sInner] = tinyVal
            except:
                tmp[sInner] = tinyVal
    return p

#def fixObsProbs(p):
#    probs = initProbs()
#    it = p.iteritems()
#    for cur in it:
#        tmp = probs[cur[0][0]]
#        tmp[cur[0][2]] = log(cur[1])
#    return probs

 
# input up to now 
observations = ('walk', 'shop', 'clean')

#initial prob
start_probability = formatStartProbs(build.startProbs)
 
transition_probability = formatTransProbs(build.transProbs)
#{
#   'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
#   'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
#   }
 
emission_probability = formatObsProbs(build.obsProbs)
#{
#   'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
#   'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
#   }



# Helps visualize the steps of Viterbi.
def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7s" % ("%d" % i),
    print
 
    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print
 
def viterbi(obs, states, start_p, trans_p, emit_p):
    global states_all #just the states at top of this file
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
#    print "************************************************"
#    pp.pprint(start_p)
#    print "************************************************"
#    pp.pprint(emit_p)
#    print "************************************************"
    for y in states_all:
        #V[0][y] = start_p[y] * emit_p[y][obs[0]]
        if (start_p[y] == {}):
            tmp1 = log(0.000000000000001)
        else:
            tmp1 = start_p[y]

        try:
            tmp2 = emit_p[y][obs[0]]
        except KeyError:
            tmp2 = log(0.000000000000001) #derp?!

        V[0][y] = tmp1 * tmp2
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
 
        for y in states_all:
            (prob, state) = max( [ (V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states_all] )
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
 
#    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states_all])
    return (prob, path[state])
    
    
def example():
    observations = ()
    x = raw_input("observations: ")
    for i in range(len(x)):
        observations += (x[i],)
    #print observations
    (prob,path) = viterbi(observations,
                   states_all,
                   start_probability,
                   transition_probability,
                   emission_probability)
    out = ""
    for s in path:
        out += s
    return "most likely sequence: " + out

