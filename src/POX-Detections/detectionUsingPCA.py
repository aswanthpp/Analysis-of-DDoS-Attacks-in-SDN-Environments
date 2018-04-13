import numpy as np
from numpy import linalg as LA

import math
from pox.core import core

log = core.getLogger()

def ipToNum(ip):      	  
  ipNum = 0
  j=0
  ipOctet=str(ip).split(".")
  for i in ipOctet :
     ipNum += int(i)*pow(256,3-j)
     j=j+1
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
      dstEnt = []
      value = 1
      meanSrc = 0
      meanDst = 0
      srcDict = {}
      dstDict = {}
     
      def updateMean(self,s,d):
      	  if(self.count!=0):
      	     self.meanSrc=(self.meanSrc*(self.count-1)+s)/self.count
      	     self.meanDst=(self.meanDst*(self.count-1)+s)/self.count    
      
      def collectStats(self, srcIp, dstIp):
          self.count +=1
          srcIpNum=ipToNum(srcIp)
          dstIpNum=ipToNum(dstIp)
        
	  self.srcIpList.append(srcIpNum)
	  self.dstIpList.append(dstIpNum)
	  self.updateMean(srcIpNum,dstIpNum)
	  a1=covariance(self.meanSrc, self.meanSrc, self.srcIpList, self.srcIpList)
          a2=covariance(self.meanSrc, self.meanDst, self.srcIpList, self.dstIpList)
          a3=covariance(self.meanDst, self.meanSrc, self.dstIpList, self.srcIpList)
          a4=covariance(self.meanDst, self.meanDst, self.dstIpList, self.dstIpList)
          
          eigenValues, eigenVector = LA.eig(np.array([[a1, a2], [a3, a4]]))
          print "Eigen vector ",eigenVector
      def __init__(self):
	  pass

      
	
      
