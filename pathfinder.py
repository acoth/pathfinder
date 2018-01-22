# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import re, random
import mpld3
 
def die(sides):
    return(np.concatenate((np.zeros((1)),np.ones((sides))))/sides)

def multiDie(number,sides=1):
    md = np.ones((1))
    d = die(sides)
    for n in range(number):
        md = np.convolve(md,d)
    return(md)

def stringToDie(dieString):
#    dss = re.split(r'[^0-9+d]+',dieString)
    splitString = re.findall(r'([0-9]*)([d+])([0-9]+)(?!d)',dieString)
    dieList = map(lambda x:[int(x[0]) if x[0] else 1,int(x[2])] if x[1]=='d' else [int(x[2]),1],
                            splitString)
    #    dieList = list()
#    for ds in dss:
#        m=re.match(r'^[+]?([0-9]*)d([0-9]+)$',ds)
#        if m:
#            number = int(m.group(1)) if m.group(1) else 1
#            sides = int(m.group(2))
#        else:
#            m = re.match(r'^[+]([0-9]+)',ds)
#            if m:
#                number = int(m.group(1))
#                sides = 1
#            else:
#                print('Error: invalid specifier "'+ds)
#                return
#        dieList.append([number,sides])
    return(dieList)

def dieListToPMF(dieList):
    pmf = np.ones((1))    
    for die in dieList:
        pmf = np.convolve(pmf,multiDie(*die))
    return(pmf)
    
def stringToPMF(dieString):
    return(dieListToPMF(stringToDie(dieString)))

def PMFToSuccess(pmf):
    return(np.cumsum(pmf[::-1])[::-1])

def checkVsBlessings(check,dieString,maxBlessings=6):
    chances = np.zeros(maxBlessings+1)
    dieList = stringToDie(dieString)
    for blessings in range(maxBlessings+1):
        pmf = dieListToPMF(dieList)
        chances[blessings] = np.sum(pmf[check:])
        dieList[0][0] = dieList[0][0]+1
    return(chances.reshape((len(chances),1)))
    
def damageVsBlessings(check,dieString,maxBlessings=6):
    damage = np.zeros(maxBlessings+1)
    dieList = stringToDie(dieString)
    for blessings in range(maxBlessings+1):
        pmf = dieListToPMF(dieList)
        damage[blessings] = sum(pmf[:check]*np.arange(check,0,-1))
        dieList[0][0] = dieList[0][0]+1
    return(damage.reshape(len(damage),1))    

def PlotSuccessDist(dieString,axes):
    cmf = PMFToSuccess(stringToPMF(dieString))
    axes.bar(np.arange(len(cmf)),cmf)
    return

def Analyze(dieStrings, check):
    fig,ax = plt.subplots()
    dieStringList = dieStrings.split(';')
    maxBlessings = 5
    success = np.zeros((maxBlessings+1,0))
    cMat = np.mat(check)
    cms = np.shape(cMat)
    dsl = len(dieStringList)
    if cms[1]==1:
        cMat = np.tile(cMat,(1,dsl))
        cms = np.shape(cMat)
    else:
        if dsl==1:
            dieStringList = cms[1]*dieStringList
            dsl = len(dieStringList)
        else:
            if dsl!=cms[1]:
                print "Error! Size of check(%s) and die (%d) are incompatible."%(cms,dsl)
    
    checkLegend = list()
    for m in range(dsl):
        dieString = dieStringList[m]
        for k in range(cms[0]):
            success = np.concatenate((success,checkVsBlessings(cMat[k,m],dieString,maxBlessings)),axis=1)
            checkLegend = checkLegend+[dieString+" vs %d"%cMat[k,m]]

    blessAr = np.arange(maxBlessings+1)
    points = ax.plot(blessAr,success*100,'o-')
    ax.set_ybound(lower=0,upper=100)
    ax.set_xlabel('Number of Blessings')
    ax.set_ylabel('Chance of Success (%)')
    ax.grid(True)
    ax.set_title('Odds with blessings against given check')
    ax.legend(checkLegend)
    return (mpld3.fig_to_html(fig, figid="graph"))

def roll(dieString):
    dieList = stringToDie(dieString)
    total = 0
    for die in dieList:
        if die[1]>1:
            for n in range(die[0]):
                r = random.randint(1,die[1])
                print ' %2d (d%d)'%(r,die[1])
                total = total+r
        else:
            total = total+die[0]
            print '+%2d'%die[0]
    print '-------'
    print total