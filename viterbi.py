from math import log,exp
import pprint
import build

pp = pprint.PrettyPrinter(indent=4)

class viterbi(object):
    states_all = ("abcdefghijklmnopqrstuvwxyz\'")
    
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
            probs[cur[0][2]] = cur[1]#log(cur[1]) #take just the letter and the prob. least neg is biggest
        return probs
    
    def __formatTransProbs__(self,p):
        probs = self.__initProbs__()
        it = p.iteritems()
        for cur in it:
            tmp = probs[cur[0][0]]
            tmp[cur[0][2]] = cur[1]#log(cur[1])
        return probs
    
    def __formatObsProbs__(self,p):
        probs = self.__initProbs__()
        it = p.iteritems()
        for cur in it:
            tmp = probs[cur[0][2]]
            tmp[cur[0][0]] = cur[1]#log(cur[1])
        return probs

    
    # Helps visualize the steps of Viterbi.
    def print_dptable(self,V):
        print " ",
        for i in range(len(V)): print "%7s" % ("%d" % i),
        print
     
        for y in V[0].keys():
            print "%.5s: " % y,
            for t in range(len(V)):
                print "%.7s" % ("%f" % V[t][y]),
            print

######## HERE ##############
############################
    
    # actually runs viterbi algo. name changes to not collide with this class name
    def viterbize(self, obs, states, start_p, trans_p, emit_p):
        V = [{}]
        path = {}
     
        # Initialize base cases (t == 0)
        for y in states:
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
            path[y] = [y]
        
        
        # Run Viterbi for t > 0
        for t in range(1,len(obs)):
            V.append({})
            newpath = {}
        
            #for y in states:
            #    (prob, state) = max( [ (V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states] )
            #    V[t][y] = prob
            #    newpath[y] = path[state] + [y]
            #path = newpath
            noMorePfx = False
            for y in states:
                #(prob, state) = max( [ (V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states] )
                tmp = []
                for y0 in states:
                    tmp.append((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0))
                
                tmp.sort(reverse=True)
                if noMorePfx:
                    # ie: this is all fucked
                    (prob, state) = tmp[0]

                else:
                    i = 0
                    pfx = "".join(path[tmp[i][1]]+[y])
                    while ( len(build.corpus.keys(prefix=pfx )) < 1):
                        i += 1
                        if i >= len(tmp):
                            # there are no new prefixes of current path in the corpus.
                            # dump out of the loop and just use the most likely
                            break
                        pfx = "".join(path[tmp[i][1]]+[y])
                    

                    if (i == len(tmp)):
                        noMorePfx = True
                        i = 0
                    # what we want is the most likely state that is a prefix in the corpus
                    (prob, state) = tmp[i]
                
                ######
                # can make sure we've got the word w1 by checking corpus agains: w1|
                                
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            
            # Don't need to remember the old paths
            path = newpath

        #print_dptable(V)
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
        return (prob, path[state])
        
############### END ###############
    
    # to be called from main. all probs come from build
    def runViterbi(self, obs):#, startP, transP, obsP):
        global states_all
        (prob,path) = self.viterbize(obs,
                           self.states_all,
                           self.start_probability,
                           self.transition_probability,
                           self.emission_probability)

        return ["".join(path)]
