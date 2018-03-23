import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import math

def covariance(x,y,datax,datay):
	sum=0
	for i in range(0,len(datax)):
		sum=sum+(x-datax[i])*(y-datay[i])
	sum=sum/len(datax)
	return sum
	

sum=0
datax=[]
datay=[]
covmat=[]
data=pd.read_csv('test.csv',index_col=0)
for i in range(1,len(data.x)+1):
	datax.append(data.x[i])
	datay.append(data.y[i])

lm = smf.ols(formula='y ~ x', data=data).fit()
xmid=(data.x.min()+data.x.max())/2
X_new = pd.DataFrame({'x': [xmid]})
ymid=lm.predict(X_new)[0]

graph = pd.DataFrame({'x': [data.x.min(), data.x.max()]})
preds = lm.predict(graph)
data.plot(kind='scatter', x='x', y='y')

# plot principal component axis
plt.plot(graph, preds, c='red', linewidth=2)
array=[]
for i in range(1,len(data.x)+1):
    temp=math.sqrt(pow(data.x[i]-xmid,2)+pow(data.y[i]-ymid,2))
    array.append(temp)

covmat.append(covariance(xmid,xmid,datax,datax))
covmat.append(covariance(xmid,ymid,datax,datay))
covmat.append(covariance(ymid,xmid,datay,datax))
covmat.append(covariance(ymid,ymid,datay,datay))
print "\n\n\tCovariance matrix:"
print "\t-------------------------\n"
print "\t",covmat[0],"   \t",covmat[1]
print "\t",covmat[2],"   \t",covmat[3]

a1=covmat[0]
a2=covmat[1]
a3=covmat[2]
a4=covmat[3]

eigen1=(a1+a4+math.sqrt(pow((a1+a4),2)-4*(a1*a4-a2*a3)))/2
eigen2=(a1+a4-math.sqrt(pow((a1+a4),2)-4*(a1*a4-a2*a3)))/2

print "\n\n\tEigenvalues:"
print "\t--------------\n"
print "\t",eigen1
print "\t",eigen2

print "\n\tPlotting the Principal Component Axis:"
print "\t----------------------------------------\n"

