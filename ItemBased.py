# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 15:35:57 2017

@author: huang
"""

import re
import math
import random
from math import sqrt

import numpy as np

def ItemBased(matrix, testUser, testItem,mes = 'cosine'):
	# the implement of item-based CF
    itemUser = matrix[testUser]
    simList = []
    ratingList = []
    userScore = []
    itemScore = 0
    itemNum = 0
    for i in itemUser:
        itemScore += itemUser[i]
        itemNum += 1
    itemScore = itemScore / itemNum
    for item in itemUser:
        testSum = []
        userSum = []
        userNum = 0
        for user in matrix:
            userItem = matrix[user]
            score = 0
            num = 0
            for i in userItem:
                score += userItem[i]
                num += 1
            score = score / num
            
            if testItem in userItem and item in userItem:
                testSum.append(userItem[testItem])
                userSum.append(userItem[item])
                userScore.append(score)
                userNum += 1
               
                
        Numerator = 0
        DenominatorTest = 1
        DenominatorUser = 1
        if userNum:
            
            if mes == 'cosine':
                for i in range(userNum):
                    Numerator += testSum[i] * userSum[i]
                    DenominatorTest += testSum[i] * testSum[i]
                    DenominatorUser += userSum[i] * userSum[i]
                    
                s = Numerator / (sqrt(DenominatorTest) * sqrt(DenominatorUser))
    
                simList.append(s)
                
                ratingList.append(itemUser[item])
            elif mes == 'cosRelation':
                for i in range(userNum):
                    Numerator += (testSum[i] - userScore[i]) * (userSum[i] - userScore[i])
                    DenominatorTest += (testSum[i] - userScore[i]) * (testSum[i] - userScore[i])
                    DenominatorUser += (userSum[i] - userScore[i]) * (userSum[i] - userScore[i])
                    
                s = Numerator / (sqrt(DenominatorTest) * sqrt(DenominatorUser))
                if s != 0.0:
                    simList.append(s)
                    ratingList.append(itemUser[item])
            else:
                for i in range(userNum):
                    Numerator += (testSum[i] - itemScore) * (userSum[i] - itemScore)
                    DenominatorTest += (testSum[i] - itemScore) * (testSum[i] - itemScore)
                    DenominatorUser += (userSum[i] - itemScore) * (userSum[i] - itemScore)
                    
                s = Numerator / (sqrt(DenominatorTest) * sqrt(DenominatorUser))
                if s != 0.0:
                    simList.append(s)
                    ratingList.append(itemUser[item])
    return simList,ratingList

def predict(simList,ratingList):
    ratingSum = 0.0
    simSum = 0.0
    
    for i in range(len(simList)):
        ratingSum += simList[i] * ratingList[i]
        simSum += simList[i]
    if simSum != 0:
        return ratingSum / simSum
    else:
        return 0

def itemAvg(matrix, testItem):
    ratingSum = 0
    userNum = 0
    for user in matrix:
        userItem = matrix[user]
            
        if testItem in userItem:
	        ratingSum += userItem[testItem]
	        userNum += 1
    if userNum != 0:
        return ratingSum / userNum
    else:
        return 0

def main(mes):
    mae_sum = 0
    rmae_sum = 0
    number = 0

    matrix = {}
    test = []
    f = open("data/train_small.txt", "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(' ')
        if random.randint(0,4) != 0:
            
	        if int(line[0]) in matrix:
	            matrix[int(line[0])][int(line[1])] = int(line[2])
	        else:
	            matrix[int(line[0])] = {int(line[1]):int(line[2])}
        else:
            test.append([int(line[0]),int(line[1]),int(line[2])])
    f.close()
    

    for i in test:
        if i[0] in matrix:
            simList,ratingList = ItemBased(matrix, i[0], i[1],mes)
            rating = predict(simList,ratingList)
            if rating != 0:
                t = rating - i[2]
                mae_sum += abs(t)
                rmae_sum += t * t
                number += 1
        else:
            rating = itemAvg(matrix, i[1])
            if rating != 0:
                t = rating - i[2]
                mae_sum += abs(t)
                rmae_sum += t * t
                number += 1
        print i[0],i[1],i[2],rating

    print "MAE: " + str(mae_sum * 1.0 / number)
    print "RMSE: " + str(math.sqrt(rmae_sum * 1.0 /number))


if __name__ == '__main__':
	main('cosine')#('cosRelation')#('pearson')
