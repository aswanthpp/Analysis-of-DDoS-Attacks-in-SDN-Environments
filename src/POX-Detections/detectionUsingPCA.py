import time 
import math
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

from numpy import linalg as LA
from pox.core import core

log = core.getLogger()

def ipToNum(ip):      	  
  ipNum = 0
  ipOctet=str(ip).split(".")
  ipNum=int(ipOctet[-1])
  return ipNum

def covariance(x, y, dataX, dataY):
	  sum = 0
	  for i in range(0, len(dataX)):
	      sum = sum + (x - dataX[i]) * (y - dataY[i])
	  sum = sum / len(dataX)
	  return sum

class PCA(object):

      count = 0
      srcIpList = []
      dstIpList = []
      
      meanSrc = 0
      meanDst = 0
      srcDict = {} 
     
      intercept = 0    
      slope = 0    
       
      sqDistSum = 0   
      sdDeviation = 0
      meanYDist = 0
      yDist =0
      
      rmsSqSum = 0   
      rms = 0
      
      def calcMean(self,s,d):
      	  if(self.count!=0):
      	     self.meanSrc=(self.meanSrc*(self.count-1)+s)/self.count
      	     self.meanDst=(self.meanDst*(self.count-1)+d)/self.count    
      
      def calcSqDeviation(self) :
       
      	  if(self.count !=0 ) :
	  	self.meanYDist=(self.meanYDist*(self.count-1)+self.yDist)/self.count
	 
	  self.sqDistSum += pow((self.yDist-self.meanYDist),2)                     
	  if(self.count-1 != 0):
	  	self.sdDeviation=math.sqrt(self.sqDistSum/(self.count-1))
      
      def calcRms(self):
      	  self.rmsSqSum += pow(self.yDist,2)
      	  self.rms =math.sqrt(self.rmsSqSum/self.count)
      
      def calcYDistance(self,srcIpNum,dstIpNum) :
      	  temp = self.slope*srcIpNum + self.intercept
      	  self.yDist = (dstIpNum-temp)  
      
      
      def getsdDeviation(self) :
      	  self.calcSqDeviation()
      	  return self.sdDeviation
      	  
      def getYDist(self):
      	  return self.yDist
      	  
      def getRms(self):
      	  self.calcRms()
      	  return self.rms
      	  
      def collectStats(self, srcIp, dstIp):
          self.count +=1
          if(self.srcDict.has_key(str(srcIp))==1):
          	srcIpNum=self.srcDict[str(srcIp)]	
          else :
          	self.srcDict[str(srcIp)]=len(self.srcDict) + 1
          	srcIpNum=self.srcDict[str(srcIp)]
          dstIpNum=ipToNum(dstIp)
        
	  self.srcIpList.append(srcIpNum)
	  self.dstIpList.append(dstIpNum)
	  d={'x' : self.srcIpList,'y' : self.dstIpList}
	  data=pd.DataFrame(data=d)
          
          lm = smf.ols(formula = 'y ~ x', data = data).fit()
	  
	  self.intercept= lm.params.Intercept
	  self.slope= lm.params.x
	  
	  self.calcYDistance(srcIpNum,dstIpNum) 
	  
	  
	  '''
	  graph = pd.DataFrame({'x': [data.x.min(), data.x.max()]})
          preds = lm.predict(graph)
          data.plot(kind = 'scatter', x = 'x', y = 'y')
	  plt.plot(graph, preds, c = 'red', linewidth = 2)
	  plt.title('Principal Component Axis')
          plt.show()
	  '''
	  
	  '''
	  a1=covariance(self.meanSrc, self.meanSrc, self.srcIpList, self.srcIpList)
          a2=covariance(self.meanSrc, self.meanDst, self.srcIpList, self.dstIpList)
          a3=covariance(self.meanDst, self.meanSrc, self.dstIpList, self.srcIpList)
          a4=covariance(self.meanDst, self.meanDst, self.dstIpList, self.dstIpList)
          
          eigenValues, eigenVector = LA.eig(np.array([[a1, a2], [a3, a4]]))
          print "Eigen vector ",eigenVector
          '''
      def __init__(self):
	  pass
	  
	  
