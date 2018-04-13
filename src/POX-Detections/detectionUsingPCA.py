from numpy import linalg as LA

import math
from pox.core import core

log = core.getLogger()

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

      def covariance(x, y, dataX, dataY):
	  sum = 0
	  for i in range(0, len(dataX)):
	      sum = sum + (x - dataX[i]) * (y - dataY[i])
	  sum = sum / len(dataX)
	  return sum
      def updateMean(s,d)
      		if(count!=0):
      			meanSrc=(meanSrc*(count-1)+s)/count
      			meanDst=(meanDst*(count-1)+s)/count

      def statcolect(self, srcIp, dstIp):
        self.count +=1
        tempSrc=srcIp.split(".")
        tempDst=dstIp.split(".")
        
	self.srcIpList.append(int(tempSrc[-1]))
	self.dstIpList.append(int(tempDst[-1])))
	updateMean(srcIp,dstIp)
	a1=covariance(meanSrc, meanSrc, srcIpList, srcIpList)
        a2=covariance(meanSrc, meanDst, srcIpList, dstIpList)
        a3=covariance(meanDst, meanSrc, dstIpList, srcIpList)
        a4=covariance(meanDst, meanDst, dstIpList, dstIpList)
        eigenValues, eigenVector = LA.eig(np.array([[a1, a2], [a3, a4]]))
	

      
	
      
