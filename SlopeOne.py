import re
import math
import random

# 计算用户的平均rating
def calAvg(user_vector):
    user_sum = 0.0
    for i in user_vector:
        user_sum += user_vector[i]
    avg = user_sum / len(user_vector)
    return avg


def SlopeOne(matrix, testUser, testItem, typeSum = 'weights'):
	# the implement of sloop one
    supposeList = []
    itemUser = matrix[testUser]
    
    for item in itemUser:
        diffSum = 0.0
        userNum = 0
        for user in matrix:
            userItem = matrix[user]
            
            if testItem in userItem and item in userItem:
                diffSum += userItem[testItem] - userItem[item]
                userNum += 1
        if userNum:
            diffAvg = diffSum / userNum
            supposeRate = itemUser[item] + diffAvg
            supposeList.append((supposeRate, userNum))

    if not supposeList:
       
        avg = calAvg(itemUser)
        return avg

   
    molecusar = 0.0
    denominator = 0.0
    for suppose in supposeList:
    	# sloop with weights
        if typeSum == "weights":
            molecusar += suppose[0] * suppose[1]
            denominator += suppose[1]

        # sloop one without weight
        else:
            molecusar += suppose[0] 
            denominator += 1
    
    return molecusar / denominator

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


def main(typeSum):
    mae_sum = 0
    rmae_sum = 0
    rmse_sum = 0
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
            rating = SlopeOne(matrix, i[0], i[1],typeSum)

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
        #print number

    print "MAE: " + str(mae_sum * 1.0 / number)
    print "RMSE: " + str(math.sqrt(rmae_sum * 1.0 /number))


if __name__ == '__main__':
	main('weights')#('No')
