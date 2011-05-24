#!/usr/bin/python

#import build
from heapq import nlargest
import pprint
import pdb
# run some setup stuff
#build.unpickleTables()

pp = pprint.PrettyPrinter(indent=4)
#tinyVal = 0.000000000000001#log(0.000000000000001)
class viterbi(object):
    states_all = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
              'r','s','t','u','v','w','x','y','z','\'')
    
    start_probability = {}
    transition_probability = {}
    emission_probability = {}
    
    def __init__(self, startP, transP, obsP):
        self.start_probability = self.__formatStartProbs__(startP)
        self.transition_probability = self.__formatTransProbs__(transP)
        self.emission_probability = self.__formatObsProbs__(obsP)
    
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
    
    def __formatTransProbs__(self,p):
        probs = self.__initProbs__()
        it = p.iteritems()
        for cur in it:
            tmp = probs[cur[0][0]]
            tmp[cur[0][2]] = cur[1]#log(cur[1])
    #    probs = fixOtherProbs(probs)
        return probs
    
    def __formatObsProbs__(self,p):
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
     
    #transition_probability = __formatTransProbs__(build.transProbs)
    #{
    #   'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
    #   'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
    #   }
     
    #emission_probability = __formatObsProbs__(build.obsProbs)
    #{
    #   'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    #   'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
    #   }
    
    
    
    # Helps visualize the steps of Viterbi.
    def print_dptable(self, V):
        print "    ",
        for i in range(len(V)): print "%7s" % ("%d" % i),
        print
     
        for y in V[0].keys():
            print "%.5s: " % y,
            for t in range(len(V)):
                print "%.9s" % ("%f" % V[t][y]),
            print
    
    # actually runs viterbi algo.  name changes to not collide with this class name
    def viterbize(self, obs, states, start_p, trans_p, emit_p, num=1):
        #V = [{}]
        #path = {}
        #pdb.set_trace()
        W = [] #wrapper for V
        P = [] #wrapper for path
        for i in range(num):
            W.append([{}]) # wow.
            P.append({})
        
        V = W[0]#[{}]
        path = P[0]#{}
        
        
        # Initialize base cases (t == 0)
        for i in range(num):
            for y in states:
                W[i][0][y] = start_p[y] * emit_p[y][obs[0]]
                #V[0][y] = start_p[y] * emit_p[y][obs[0]]
                P[i][y] = [y]
                #path[y] = [y]

        # Run Viterbi for t > 0
        for t in range(1,len(obs)):
            NP = []
            for i in range(num):
                #V.append({})
                W[i].append({})
                #newpath = {}
                NP.append({})

            for y in states:
                #(prob, state) = max( [ (V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states] )
                tmp = []
                for y0 in states:
                    tmp.append((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0))
                maxN = nlargest(num,tmp)
                
                for i in range(num):
                    #V[t][y] = prob
                    W[i][t][y] = maxN[i][0]
                    #newpath[y] = path[state] + [y]
                    NP[i][y] = P[i][maxN[i][1]] + [y]

            # Don't need to remember the old paths
            for i in range(num):
                #path = newpath
                P[i] = NP[i]
            #end for t in range...
        pp.pprint("======={P}========")
        pp.pprint(P)
        pp.pprint("======={P}========")
    #    print_dptable(V)
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
        tmp = []
        for y in states:
            tmp.append((V[len(obs) - 1][y], y))
        maxN = nlargest(num,tmp)
        pp.pprint("++++++++++++++")
        pp.pprint(maxN)
        pp.pprint("++++++++++++++")
        for i in range(num):
            pp.pprint(P[i][maxN[0][1]]) ############ WINNER WINNER CHICKEN DINNER
        #pp.pprint(P[0][maxN[0][1]])
        pp.pprint("++++++++++++++")
        return (prob, path[state])


    
    # to be called from main. all probs come from build
    def runViterbi(self, obsStr, singleUse=False,):
        mir_layout = "abcdefggefdsvvwqqrstrvwxtzazx"
        # obs is a string. need to convert
        obs = ()
        for i in range(len(obsStr)):
            if (obsStr[i] not in mir_layout):
                print "Warning: Non-Mirrored input detected."
                raw = raw_input("Please re-enter your string as mirrored input: ")
                return viterbi.runViterbi(self, raw)
            obs += (obsStr[i],)
        
        #start_probability = __formatStartProbs(startP)
        #transition_probability = __formatTransProbs__(transP)
        #emission_probability = __formatObsProbs__(obsP)
        global states_all
        
        (prob,path) = self.viterbize(obs,
                           self.states_all,
                           self.start_probability,
                           self.transition_probability,
                           self.emission_probability,
                           4)
        pp.pprint("===================================")
        pp.pprint(prob)
        pp.pprint(path)
        pp.pprint("===================================")

        out = ""
        #for word in path:
        for s in path:
            out += s
         #   out += "\n\t\t"

        if singleUse:
            return out
        else:
            return "Most likely sequence: " + out
    
    # wrapper for runViterbi used for multiple words
    def runViterbiMultiWord(self, obsStr):
        seq = ""
        for word in obsStr.split(" "):
            seq += self.runViterbi(word, True) + " "
        
        return "Most likely sequence: " + seq[:-1] # that's all but the last char, which is a space anyways
    

