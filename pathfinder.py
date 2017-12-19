# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import re, random
 
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

def Analyze(dieStringList, check, figNum=1):
    dieStringList = dieStringList.split(';')
    if not isinstance(figNum,int):
        plt.ioff()
        fig = plt.figure(1)
    else:
        fig = plt.figure(figNum)
    fig.clear()
    fig.subplots_adjust(right=1.5)
    axAr = 2*[0]
    for k in range(2):
        axAr[k]=fig.add_subplot(121+k)
    if not isinstance(dieStringList,(list,tuple)):
        dieStringList = [dieStringList]
    cmfs = np.zeros((0,0))
    maxBlessings = 5
    success = np.zeros((maxBlessings+1,0))
    damage = np.zeros((maxBlessings+1,0))
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
        cmf = PMFToSuccess(stringToPMF(dieString))
        oldShape = np.shape(cmfs)
        thisShape = np.shape(cmf)
        sizeDiff = thisShape[0]-oldShape[0]
        if sizeDiff>0:
            cmfs = np.concatenate((cmfs,np.zeros((sizeDiff,oldShape[1]))),axis=0)
        if sizeDiff<0:
            cmf = np.concatenate((cmf,np.zeros((-sizeDiff,1))),axis=0)
        cmfs = np.concatenate((cmfs,cmf.reshape(len(cmf),1)),axis=1)
        for k in range(cms[0]):
            success = np.concatenate((success,checkVsBlessings(cMat[k,m],dieString,maxBlessings)),axis=1)
            damage = np.concatenate((damage,damageVsBlessings(cMat[k,m],dieString,maxBlessings)),axis=1)
            checkLegend = checkLegend+[dieString+" vs %d"%cMat[k,m]]
    axAr[0].plot(np.arange(1,np.shape(cmfs)[0]),cmfs[1:,:]*100,'o-')
    axAr[0].grid(True)
    axAr[0].legend(dieStringList,loc=1)
    axAr[0].set_xlabel('Check')
    axAr[0].set_ylabel('Chance of Success (%)')
    axAr[0].set_ybound(lower=0,upper=100)
    axAr[0].yaxis.set_major_locator(ticker.LinearLocator(11))
    axAr[0].set_title('Odds for given roll(s)')
    
    blessAr = np.arange(maxBlessings+1)
    axAr[1].plot(blessAr,success*100,'<-')
    axAr[1].set_ybound(lower=0,upper=100)
    axAr[1].yaxis.set_major_locator(ticker.LinearLocator(11))
    axAr[1].set_xlabel('Number of Blessings')
    axAr[1].set_ylabel('Chance of Success (%)')
    axAr[1].grid(True)
    axAr[1].set_title('Odds with blessings against given check')
 #   axAr[1].legend(dieStringList,loc=(0,))
    #axAr[1].set_axis_off()
    a2 = axAr[1].twinx()
    a2.plot(blessAr,damage,'>-')
    a2.set_ybound(lower=0,upper=5)
    a2.yaxis.set_major_locator(ticker.LinearLocator(11))
    a2.set_ylabel('Expected Damage (for a combat check)')
    a2.legend(checkLegend,loc='center right')
    if not isinstance(figNum,int):
        fig.savefig(figNum, format='svg',bbox_inches='tight')
        plt.close(fig)
    return

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