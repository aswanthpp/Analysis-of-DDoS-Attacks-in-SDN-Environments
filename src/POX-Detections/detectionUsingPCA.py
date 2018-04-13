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
	  
      def ipToNum(ip):
      	  
      	  ipOctet=ip.split(".")
      	  ipNum=(int(ipOctet[0])*pow(256,3))+ (int(ipOctet[1])*pow(256,2)) + (int(ipOctet[2])*pow(256,1)) + (int(ipOctet[3])*pow(256,0))
          return ipNum
          
      def updateMean(s,d):
      	  if(count!=0):
      	     meanSrc=(meanSrc*(count-1)+s)/count
      	     meanDst=(meanDst*(count-1)+s)/count

      def collectStats(self, srcIp, dstIp):
          self.count +=1
          srcIpNum=ipToNum(srcIp)
          dstIpNum=ipToNum(dstIp)
        
	  self.srcIpList.append(srcIpNum)
	  self.dstIpList.append(dstIpNum)
	  updateMean(srcIp,dstIp)
	  a1=covariance(meanSrc, meanSrc, srcIpList, srcIpList)
          a2=covariance(meanSrc, meanDst, srcIpList, dstIpList)
          a3=covariance(meanDst, meanSrc, dstIpList, srcIpList)
          a4=covariance(meanDst, meanDst, dstIpList, dstIpList)
          eigenValues, eigenVector = LA.eig(np.array([[a1, a2], [a3, a4]]))
          print "Eigen vector ",eigenVector
	

      
	
      
