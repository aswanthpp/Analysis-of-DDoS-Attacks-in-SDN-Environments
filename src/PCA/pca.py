import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import math
from numpy import linalg as LA

class PCA(object):
      def covariance(x, y, dataX, dataY):
	  sum = 0
	  for i in range(0, len(dataX)):
	      sum = sum + (x - dataX[i]) * (y - dataY[i])
	  sum = sum / len(dataX)
	  return sum
	
      sum = 0
      dataX = []
      dataY = []
      covmat = []
      rowFeatureVector = []
      data = pd.read_csv('test.csv', index_col = 0)

      for i in range(1, len(data.x) + 1):
	  dataX.append(data.x[i])
	  dataY.append(data.y[i])

      lm = smf.ols(formula = 'y ~ x', data = data).fit()
      xmid = (data.x.min() + data.x.max()) / 2
      X_new = pd.DataFrame({'x': [xmid]})
      ymid = lm.predict(X_new)[0]

      graph = pd.DataFrame({'x': [data.x.min(), data.x.max()]})
      preds = lm.predict(graph)
      data.plot(kind = 'scatter', x = 'x', y = 'y')

      # plot principal component axis
      plt.plot(graph, preds, c = 'red', linewidth = 2)
      array = []

      for i in range(1, len(data.x) + 1):
	  temp = math.sqrt(pow(data.x[i] - xmid, 2) + pow(data.y[i] - ymid, 2))
	  array.append(temp)

      covmat.append(covariance(xmid, xmid, dataX, dataX))
      covmat.append(covariance(xmid, ymid, dataX, dataY))
      covmat.append(covariance(ymid, xmid, dataY, dataX))
      covmat.append(covariance(ymid, ymid, dataY, dataY))

      print "\n\n\tCovariance matrix:"
      print "\t-------------------------\n"
      print "\t",covmat[0],"   \t",covmat[1]
      print "\t",covmat[2],"   \t",covmat[3]

      a1 = covmat[0]
      a2 = covmat[1]
      a3 = covmat[2]
      a4 = covmat[3]

      #eigen1 = (a1 + a4 + math.sqrt(pow((a1 + a4), 2) - 4 * (a1 * a4 - a2 * a3))) / 2
      #eigen2 = (a1 + a4 - math.sqrt(pow((a1 + a4), 2) - 4 * (a1 * a4 - a2 * a3))) / 2

      
      eigenValues, eigenVector = LA.eig(np.array([[a1, a2], [a3, a4]]))
      
      print "\n\n\tEigenvalues:"
      print "\t--------------\n"
      print "\t",eigenValues[0]
      print "\t",eigenValues[1]
      
      
      print "\n\n\tEigen vectors:"
      print eigenVector
      
      rowFeatureVector.append(v[1])
      rowFeatureVector.append(v[0])
      
      plt.title('Principal Component Axis')
      plt.show()
