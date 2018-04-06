import math
from pox.core import core

log = core.getLogger()

class Entropy(object):
      count = 0
      destFrequency = {}
      destIP = []
      destEntropy = []
      value = 1

      def collectStats(self, element):
          l = 0
          self.count +=1
          self.destIP.append(element)
          if self.count == 50:
             for i in self.destIP:
                 l +=1
                 if i not in self.destFrequency:
                    self.destFrequency[i] = 0
                 self.destFrequency[i] += 1
             self.findEntropy(self.destFrequency)
             log.info(self.destFrequency)
             self.destFrequency = {}
             self.destIP = []
             l = 0
             self.count = 0

      def findEntropy (self, lists):
	  l = 50
	  entropyList = []
	  for k,p in lists.items():
	      c = p/float(l)
	      c = abs(c)
	      entropyList.append(-c * math.log(c, 10))

	      log.info('Entropy = ') 
	      log.info(sum(entropyList))

	      self.destEntropy.append(sum(entropyList))

	  if(len(self.destEntropy)) == 80:
	      print self.destEntropy
	      self.destEntropy = []
	  self.value = sum(entropyList)

      def __init__(self):
	  pass
