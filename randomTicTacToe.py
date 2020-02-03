from random import *
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def eval(game):
    x = set([game[0], game[2], game[4], game[6], game[8]])
    o = set([game[1], game[3], game[5], game[7]])
    if (set([1, 2, 3]).issubset(x) 
        or set([4, 5, 6]).issubset(x) 
        or set([7, 8, 9]).issubset(x) 
        or set([1, 4, 7]).issubset(x) 
        or set([2, 5, 8]).issubset(x) 
        or set([3, 6, 9]).issubset(x) 
        or set([1, 5, 9]).issubset(x) 
        or set([3, 5, 7]).issubset(x)):
        return 1
    elif (set([1, 2, 3]).issubset(o) 
        or set([4, 5, 6]).issubset(o) 
        or set([7, 8, 9]).issubset(o) 
        or set([1, 4, 7]).issubset(o) 
        or set([2, 5, 8]).issubset(o) 
        or set([3, 6, 9]).issubset(o) 
        or set([1, 5, 9]).issubset(o) 
        or set([3, 5, 7]).issubset(o)):
        return -1
    else: 
        return 0

def randGame():
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    game = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        x = choice(l)
        game[i] = x
        l.remove(x)
        if (eval(game) == 1 or eval(game) == -1):
            break
    #print(game)    
    return game

def createRandomSteps(n):
    df = pd.DataFrame(columns = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8', 'step9', 'value'], index = range(9 * n), dtype = float)
    
    df.reset_index()
    
    row = 0
    
    for i in range(n):
        x = randGame()
        print(str(i))
        print(x)
        ev =  eval(x)
        max = len(np.trim_zeros(x))
        for k in range(max):
            for j in range(9):
                df['step' + str(j + 1)][row] = x[j]
                if ev == 0:
                    df['value'][row] = 0.25
                elif ((ev == -1) & (k % 2) == 0):
                    df['value'][row] = 1
                elif ((ev == 1) & (k % 2) == 1):
                    df['value'][row] = 1
                else: 
                    df['value'][row] = 0
            x[max - 1 - k] = 0
            row += 1
            
    df = df.dropna()
    
    df = df.reset_index()
            
    df = df.groupby(['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8', 'step9'])['value'].mean().reset_index()
    
    return df

def createTrainingsData(n):
    df = createRandomSteps(n)
    
    maxByStep1 = df['value'].transform(lambda x: max(df['value']))
    maxByStep2 = df.groupby(['step1'])['value'].transform(max)
    maxByStep3 = df.groupby(['step1', 'step2'])['value'].transform(max)
    maxByStep4 = df.groupby(['step1', 'step2', 'step3'])['value'].transform(max)
    maxByStep5 = df.groupby(['step1', 'step2', 'step3', 'step4'])['value'].transform(max)
    maxByStep6 = df.groupby(['step1', 'step2', 'step3', 'step4', 'step5'])['value'].transform(max)
    maxByStep7 = df.groupby(['step1', 'step2', 'step3', 'step4', 'step5', 'step6'])['value'].transform(max)
    maxByStep8 = df.groupby(['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7'])['value'].transform(max)
    maxByStep9 = df.groupby(['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8'])['value'].transform(max)

    isMaxByStep1 = maxByStep1 == df['value']
    isMaxByStep2 = maxByStep2 == df['value']
    isMaxByStep3 = maxByStep3 == df['value']
    isMaxByStep4 = maxByStep4 == df['value']
    isMaxByStep5 = maxByStep5 == df['value']
    isMaxByStep6 = maxByStep6 == df['value']
    isMaxByStep7 = maxByStep7 == df['value']
    isMaxByStep8 = maxByStep8 == df['value']
    isMaxByStep9 = maxByStep9 == df['value']

    df1 = df[(df['step2'] == 0) & isMaxByStep1]
    df2 = df[(df['step2'] != 0) & (df['step3'] == 0) & isMaxByStep2]
    df3 = df[(df['step3'] != 0) & (df['step4'] == 0) & isMaxByStep3]
    df4 = df[(df['step4'] != 0) & (df['step5'] == 0) & isMaxByStep4]
    df5 = df[(df['step5'] != 0) & (df['step6'] == 0) & isMaxByStep5]
    df6 = df[(df['step6'] != 0) & (df['step7'] == 0) & isMaxByStep6]
    df7 = df[(df['step7'] != 0) & (df['step8'] == 0) & isMaxByStep7]
    df8 = df[(df['step8'] != 0) & (df['step9'] == 0) & isMaxByStep8]
    df9 = df[(df['step9'] != 0) & isMaxByStep9]

    dfOut = df1.append(df2).append(df3).append(df4).append(df5).append(df6).append(df7).append(df8).append(df9).reset_index().drop(['index'], axis = 1)

    dfOut['nextStep'] = ""

    foo = 0

    for i in range(len(dfOut['step1'])):
        if dfOut['step9'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step9'][i]
            dfOut['step9'][i] = 0
        elif dfOut['step8'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step8'][i]
            dfOut['step8'][i] = 0
        elif dfOut['step7'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step7'][i]
            dfOut['step7'][i] = 0
        elif dfOut['step6'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step6'][i]
            dfOut['step6'][i] = 0
        elif dfOut['step5'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step5'][i]
            dfOut['step5'][i] = 0
        elif dfOut['step4'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step4'][i]
            dfOut['step4'][i] = 0
        elif dfOut['step3'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step3'][i]
            dfOut['step3'][i] = 0
        elif dfOut['step2'][i] != 0:
            dfOut['nextStep'][i] = dfOut['step2'][i]
            dfOut['step2'][i] = 0
        else:
            dfOut['nextStep'][i] = dfOut['step1'][i]
            dfOut['step1'][i] = 0

    dfOut = dfOut.drop(['value', 'step9'], axis = 1).drop_duplicates(subset = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7', 'step8'])

    return dfOut

dfOut = createTrainingsData(200)

dfOut.to_csv('foo4.csv')