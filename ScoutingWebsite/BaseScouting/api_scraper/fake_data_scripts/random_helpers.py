'''
Created on Mar 5, 2017

@author: PJ
'''
import random
import math


def getBoolWithPercentage(percentage):
    rando = random.randint(0, 100)

    return rando < percentage


def getRandomNumber(minval, maxval):

    output_range = maxval - minval

    rando = random.randint(0, 100)
    output = math.floor(minval + rando * .01 * output_range)

    precentage = rando
    return precentage
