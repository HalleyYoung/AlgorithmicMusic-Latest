# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 11:48:37 2014

@author: halley
"""
import probabilityhelpers as ph
from functionalhelpers import *
import random
import functionalhelpers as fh

#These two functions are used to convert between string and list representations of rhythms (because lists aren't hashable and therefore can't be used in the probability dict)
def strNum(rhys):
    return ' '.join([str(i) for i in rhys])
def strToRhy(r_str):
    return [float(i) for i in r_str.split(' ')]
    
prob_dict = {'0.5 0.25 0.25':0.05, '0.25 0.25 0.5': 0.05, '1.0': 0.5, '0.5 0.5': 0.5, '0.25 0.25 0.25 0.25':0.05}

prob_dict_triplets = {'0.5 0.25 0.25':0.05, '0.25 0.25 0.5': 0.05, '1.0': 0.5, '0.5 0.5': 0.5, '0.25 0.25 0.25 0.25':0.05,
                      '0.33333333 0.33333333 0.33333333':0.05}
two_prob_dict = {}
prob_dict_keys = prob_dict.keys()
for i in range(0, len(prob_dict_keys)):
    two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[i]] = 1.2*prob_dict[prob_dict_keys[i]]
    for j in range(i + 1, len(prob_dict_keys)):
        two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[j]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
        two_prob_dict[prob_dict_keys[j] + ' ' + prob_dict_keys[i]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
two_prob_dict['1.5 0.5'] = 0.35
two_prob_dict['1.5 0.25 0.25'] = 0.12
two_prob_dict['2.0'] = 0.4

two_prob_dict_triplets = {}
prob_dict_keys = prob_dict_triplets.keys()
for i in range(0, len(prob_dict_keys)):
    two_prob_dict_triplets[prob_dict_keys[i] + ' ' + prob_dict_keys[i]] = 1.2*prob_dict_triplets[prob_dict_keys[i]]
    for j in range(i + 1, len(prob_dict_keys)):
        two_prob_dict_triplets[prob_dict_keys[i] + ' ' + prob_dict_keys[j]] = ph.geometricMean([prob_dict_triplets[prob_dict_keys[i]], prob_dict_triplets[prob_dict_keys[j]]])
        two_prob_dict_triplets[prob_dict_keys[j] + ' ' + prob_dict_keys[i]] = ph.geometricMean([prob_dict_triplets[prob_dict_keys[i]], prob_dict_triplets[prob_dict_keys[j]]])
two_prob_dict['2.0'] = 0.4
        
#return a similar rhythm to the previous rhythm
def alterRhythm(durs, p_alter = 0.3):
    new_durs = []
    n = 0 #dur index
    while (n < len(durs)):
        durs_appended = False
        ran_alter = ph.getUniform() #random seed
        if (n < len(durs) - 4):
            if (durs[n] == 0.25 and durs[n+1] == 0.25 and durs[n+2] == 0.25 and durs[n+3] == 0.25):
                if ran_alter < p_alter / 2:
                    new_durs.append(1)
                elif ran_alter < p_alter:
                    new_durs.extend([0.5,0.5])
                else:
                    new_durs.extend([0.25,0.25,0.25,0.25]) #keep it the same
                durs_appended = True
                n += 4
        if (n < len(durs) - 2):
            if (durs[n] == 0.5 and durs[n+1] == 0.5):
                if ran_alter < p_alter / 2:
                    new_durs.append(1)
                elif ran_alter < p_alter:
                    new_durs.extend([0.25,0.25,0.25,0.25])
                else:
                    new_durs.extend([0.5, 0.5]) #keep it the same
                durs_appended = True
                n += 2
        if durs[n] == 1.0:
            if ran_alter < p_alter / 2:
                new_durs.extend([0.5,0.5])
            elif ran_alter < p_alter:
                new_durs.extend([0.25,0.25,0.25,0.25])
            else:
                new_durs.append(1.0)
            durs_appended = True
            n += 1
        if not durs_appended:
            new_durs.append(durs[n])
            n += 1
    return new_durs


def randomHalfRhythm(short = False):
    if short:
        return random.choice([[1.5, 0.5], [1.5, 0.25, 0.25], [1.0, 1.0], [1.0,0.5,0.5], [0.5,0.5,1.0]])
    else:        
        return strToRhy(ph.probDictToChoice(two_prob_dict))
        
def halfRhythmDict():
    return two_prob_dict

def randomHalfQuarterEighths():
    half_prob_dict = {'1.0 0.5 0.5':0.3, '00.5 0.5 1': 0.1, '0.5 0.5 0.5 0.5':0.25, '1.0 1.0': 0.15}
    return strToRhy(ph.probDictToChoice(half_prob_dict))


def randomDuration(length, triplets = False):
    if length == 1:
        return strToRhy(ph.probDictToChoice(prob_dict))
    elif length == 2:
        pdict = two_prob_dict_triplets if triplets else two_prob_dict
        return strToRhy(ph.probDictToChoice(pdict))
    elif length == 3:
        return strToRhy(ph.probDictToChoice(two_prob_dict) + strToRhy(ph.probDictToChoice(prob_dict)))
    elif length == 4:
        return strToRhy(ph.probDictToChoice(two_prob_dict) + strToRhy(ph.probDictToChoice(two_prob_dict)))
    else:
        print('error - duration not supported yet')



#get the defining characteristics of the rhythm
def getDefiningRhythm(cells):
    durs = fh.concat([i.durs for i in cells])
    if 0.75 in durs:
        if random.uniform(0,1) < 0.7:
            return [0.75,0.25,0.75,0.25]
        else:
            return [0.75,0.25,0.5,0.5]
    elif 1.5 in durs:
        return [1.5, 0.25, 0.25]
    elif 0.33333333 in durs:
        return [1.0,0.33333333,0.33333333,0.33333333]
    else:
        return randomDuration(2.0, triplets = False)