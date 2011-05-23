#!/usr/bin/python

#import build
from math import log,exp
import pprint

# run some setup stuff
#build.unpickleTables()

#pp = pprint.PrettyPrinter(indent=4)
#tinyVal = 0.000000000000001#log(0.000000000000001)
class viterbi(object):
    states_all = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
              'r','s','t','u','v','w','x','y','z','\'')
    
    start_probability = {}
    transition_probability = {}
    emission_probability = {}
    
    def __init__(self, startP, transP, obsP):
        self.start_probability = self.__formatStartProbs__(startP)
        self.transition_probability = self.__formatTransProbs(transP)
        self.emission_probability = self.__formatObsProbs(obsP)
    
    def __initProbs__(self):
        probs = {}
        for st in self.states_all:
            probs[st] = {}
        return probs
        
    def __formatStartProbs__(self,p):
        probs = self.__initProbs__()
        it = p.iteritems()
        for cur in it:
            probs[cur[0][2]] = cur[1]#log(cur[1]) #take just the letter and the prob.  least neg is biggest
        probs = self.__fixStartProbs__(probs)
        return probs
    
    def __formatTransProbs(self,p):
        probs = self.__initProbs__()
        it = p.iteritems()
        for cur in it:
            tmp = probs[cur[0][0]]
            tmp[cur[0][2]] = cur[1]#log(cur[1])
    #    probs = fixOtherProbs(probs)
        return probs
    
    def __formatObsProbs(self,p):
        probs = self.__initProbs__()
        it = p.iteritems()
        for cur in it:
            tmp = probs[cur[0][2]]
            tmp[cur[0][0]] = cur[1]#log(cur[1])
    #    probs = fixOtherProbs(probs)
        return probs
    
    def __fixStartProbs__(self,p):
        for s in self.states_all:
            if p[s] == {}:
                print "shoot"
                p[s] = tinyVal
        return p
    #
    #def fixOtherProbs(p):
    #    for sOuter in states_all:
    #        tmp = p[sOuter]
    #        for sInner in states_all:
    #            try: 
    #                if tmp[sInner] == {}:
    #                    print "shit"
    #                    tmp[sInner] = tinyVal
    #            except:
    #                print "damn"
    #                tmp[sInner] = tinyVal
    #    return p
    
    #def fixObsProbs(p):
    #    probs = __initProbs__()
    #    it = p.iteritems()
    #    for cur in it:
    #        tmp = probs[cur[0][0]]
    #        tmp[cur[0][2]] = log(cur[1])
    #    return probs
    
     
    # input up to now 
    #observations = ('walk', 'shop', 'clean')
    
    #initial prob
    #start_probability = __formatStartProbs(build.startProbs)
     
    #transition_probability = __formatTransProbs(build.transProbs)
    #{
    #   'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
    #   'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
    #   }
     
    #emission_probability = __formatObsProbs(build.obsProbs)
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
    
    # actually runs viterbi algo.  name changes to not collide with this class name
    def viterbize(self, obs, states, start_p, trans_p, emit_p):
        V = [{}]
        path = {}
     
        # Initialize base cases (t == 0)
        for y in states:
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
#            if (start_p[y] == {}):
#                tmp1 = log(0.000000000000001)
#                print "viterbi shit"
#            else:
#            tmp1 = start_p[y]
    
#            try:
#            tmp2 = emit_p[y][obs[0]]
#            except KeyError:
#                tmp2 = log(0.000000000000001) #derp?!
#                print "viterbi damn"
    
#            V[0][y] = tmp1 * tmp2
            path[y] = [y]
     
        # Run Viterbi for t > 0
        for t in range(1,len(obs)):
            V.append({})
            newpath = {}
     
            for y in states:
                (prob, state) = max( [ (V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states] )
                V[t][y] = prob
                newpath[y] = path[state] + [y]
     
            # Don't need to remember the old paths
            path = newpath
     
    #    print_dptable(V)
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
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
    
    # to be called from main. all probs come from build
    def runViterbi(self, obsStr):#, startP, transP, obsP):
        # obs is a string. need to convert
        obs = ()
        for i in range(len(obsStr)):
            obs += (obsStr[i],)
        
        #start_probability = __formatStartProbs(startP)
        #transition_probability = __formatTransProbs(transP)
        #emission_probability = __formatObsProbs(obsP)
        global states_all
        
        (prob,path) = self.viterbize(obs,
                           self.states_all,
                           self.start_probability,
                           self.transition_probability,
                           self.emission_probability)
        out = ""
        for s in path:
            out += s
        return "Most likely sequence: " + out
        
    