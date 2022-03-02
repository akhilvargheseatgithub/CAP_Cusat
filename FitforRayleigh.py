# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 11:06:38 2021

@author: USER
"""
import time
t0= time.process_time()

import numpy as np
rawwidth= [113.0929646312799, 99.63329455133892, 86.24933739749872, 74.57049059099859, 60.619324198849135, 46.7273606061327, 31.936252375070094, 19.86469871, 16.79429333949661, 14.550294024840365, 13.739096816624892, 12.229615639721944, 12.205026627040697, 12.157059833529976, 11.614220033924163, 12.154690386585939, 13.453171815128261, 15.052699439160127, 21.481484056996003, 27.658887923434218, 33.6547509833088, 42.557845219012364, 45.74717999845166, 58.307154698513386, 74.73576792985685, 89.3505329694733, 92.96554521069186, 98.92159609548257]
position=[19.506,19.508,19.51,19.512,19.514,19.516,19.518,19.52,19.521,19.522,19.523,19.524,19.525,19.526,19.527,19.528,19.529,19.53,19.532,19.534,19.536,19.538,19.54,19.542,19.544,19.546,19.548,19.55]
width=np.asarray(rawwidth)/4.0    #Magnification Factor
print("w0=",min(width),"Micrometer")


lamda=532*10**-9
theoreticalRayleigh=(np.pi*(2*min(width)*10**-6)**2)/(lamda)
print('Theoretical Rayleigh Length=',theoreticalRayleigh,'m',theoreticalRayleigh*1000,'mm')

k=np.round(width)
print(k)
yforrayleigh=(np.sqrt(2))*min(width)
print(yforrayleigh)
#print('Width at Maximum Rayleigh Length=',yforrayleigh)

i=rawwidth.index(min(rawwidth))
#print(i)

#width=np.asarray(width)
#position=np.asarray(position)

x1=position[i:len(position)]
y1=width[i:len(position)]

print(x1,y1)

width2=-1*(width)
#fwidth=width.append(width2)
#print(fwidth)
from matplotlib import pyplot as plt
plt.scatter(position,width,label="FWHM Values")
plt.scatter(position,width2,label="Symmetric FWHM Values")
plt.title("Rayleigh Length Calculation")
plt.xlabel("Position (mm)")
plt.ylabel("FWHM (micro meter)")
plt.legend(fontsize = 'small')
#plt.plot(y=0, c="grey",marker ="-",label="x=0")
plt.show()

##Interpolation

from scipy import interpolate

def f(x):
    x_points = np.asarray(x1)
    y_points = np.asarray(y1)
    
    tck = interpolate.splrep(y_points, x_points)
    return interpolate.splev(x, tck)


l=f(yforrayleigh)
print('l=',l)
print('minpos=',position[i])
rayleighlength=l-position[i]
print('Experimental Rayleigh Length=',rayleighlength,'meter=',rayleighlength*1000,'mm')


from scipy.optimize import curve_fit
from scipy.stats import norm
xdata = np.asarray(x1)
ydata = np.asarray(y1)
p=np.asarray(position)
wid=np.asarray(width)        
def Ray(x,w1,lam):
    w=w1*np.sqrt((1+(lam*x/3.141*w1**2)**2)**1/2)
    return w
            
parameters, covariance = curve_fit(Ray, p, wid)
fit_w1=parameters[0]
fit_lam=parameters[1]
fit_w = Ray(p,fit_w1,fit_lam)
#Plotting Gaussian Fitted Curve
plt.plot(p, wid, 'o', label='data')
plt.plot(p, fit_w, '-', label='fit')
plt.title("Fitted Data")
plt.xlabel("Position (mm)")
plt.ylabel("FWHM(micrometer)")
plt.legend()

t1 = time.process_time() - t0
print("Time elapsed: ", t1,"seconds")