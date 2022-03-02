import time
t0= time.process_time()

print("----Gausian Fitting of CCD Data----")

#Opening and Reading Signal Data Folder
list=[]
name=[]
import os
directory="C:\\Users\\USER\\Desktop\\Sample"
count=0
for filename in os.listdir(directory):
    file=os.path.join(directory,filename)
    if os.path.isfile(file):
        count=count+1
        
        #Opening each text file
        with open(file,'r') as f:
            eachfile=[x.strip().split('\t') for x in f]
        fileName=os.path.basename(file)
        name.append(fileName)
        import numpy as np
        
        
        #Processing Image data as matrix
        from matplotlib import pyplot as plt
        matrix=np.array(eachfile)
        floatArray = matrix.astype(int)
        
        #plotting as Image
        #plt.imshow(floatArray, interpolation='nearest')
        #plt.title("Cropped Image")
        #plt.xlabel("Pixels")
        #plt.ylabel("Pixels")
        #plt.show()

        #finding Local maxima cordinates
        max=(np.max(floatArray))
        xmax = np.where(floatArray==max)[0][0]
        ymax = np.where(floatArray==max)[1][0]
        
        #processing cross section
        x1=[]
        y1=[]
        for i in range(-50,50):
            y1.append(floatArray[xmax][ymax-i])
            x1.append(i)
            i=i-1
        #Plotting Cross Section
        #plt.plot(x1,y1)
        #plt.show()    
        
        #Gaussian Fitting
        from scipy.optimize import curve_fit
        from scipy.stats import norm
        xdata = np.asarray(x1)
        ydata = np.asarray(y1)
        
        def Gauss(x,y0,amp,mu,sigma):
            y=y0+amp*np.exp(-0.5*((x-mu)/sigma)**2)
            return y
            
        parameters, covariance = curve_fit(Gauss, xdata, ydata)
        
        fit_y0 = parameters[0]
        fit_amp = parameters[1]
        fit_mu = parameters[2]
        fit_sigma = parameters[3]
        fit_y = Gauss(xdata, fit_y0, fit_amp, fit_mu, fit_sigma)
        
        #Finding Important Parameters
        FWHM = abs(np.sqrt(np.log(4))*2*fit_sigma)
        Area=fit_amp*2*fit_sigma*np.sqrt(np.pi/2)
        list.append(FWHM)
        
        #Plotting Gaussian Fitted Curve
        #plt.plot(xdata, ydata, 'o', label='data')
        #plt.plot(xdata, fit_y, '-', label='fit')
        #plt.title("Gaussian Fitted Data")
        #plt.xlabel("X Cross Section(Pixels)")
        #plt.ylabel("Intensity(Counts)")
        #plt.legend()
        
#Taking Average of Fixed Number of Frames
width=[]
frames=100
for k in range(0,count,frames):
    parts=list[k:k+frames]
    meanparts=np.mean(parts)*4.65   #Multiply by pixel dimension and divide by magnification factor
    width.append(meanparts) 
    print('Mean Width=',meanparts,)        
    
print("Mean Width=",width)    
position=[19.5,19.502,19.504,19.506,19.508,19.51,19.512,19.514,19.516,19.518,19.52,19.521,19.522,19.523,19.524,19.525,19.526,19.527,19.528,19.529,19.53,19.532,19.534,19.536,19.538,19.54,19.542,19.544,19.546,19.548,19.55]

#Importing as csv File
import pandas as pd
dict = {'Position(mm)':position,'FWHM(micro meter)': width} 
df = pd.DataFrame(dict) 
df.to_csv('C:\\Users\\USER\\Desktop\\test.csv',index=False)

t1 = time.process_time() - t0
print("Time elapsed: ", t1,"Seconds")