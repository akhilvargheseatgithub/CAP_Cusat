# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:44:31 2022

@author: Akhil Varghese
"""

"Program for Idea Data Analysis"

from pywinauto.application import Application 
import pyautogui
import numpy as np
import pandas as pd

import time

start=time.time()


pos=[]				#plasma cross sections to be analysed
ipixel=250
fpixel=750
interval=10
for n in range(ipixel,fpixel+1,interval):
    pos.append(n)
    
print('positions=',pos)
maxorder=15			#Order up to which Abel inversion approximation has to be analysed

df=pd.DataFrame()

for i in range(0,len(pos)):
    xpos=pos[i]


    app=Application(backend='uia').start('D:\Akhil\idea\idea_v1731.exe')
    
    
    app.InstallDialog.YesButton.wait('ready', timeout=30).click_input()
    app.connect(title='Idea',timeout=30)
    
    
    app.Idea.menu_select("File -> Open...")
    #time.sleep(1)
    
    file_dlg=app.Idea.window(title_re="Specify a File to Open", found_index=0)
    file_dlg.FileNameEdit.set_edit_text("12_5.pha").click_input()
    
    app.Idea.child_window(title="Open", auto_id="1", control_type="SplitButton").click_input()
    
    app.Idea.menu_select("Abel-Inversion -> Get Intgral Data")
    
    "Coordinates of Points"
    
    cordinatx1=app.Idea.window(title_re='Point Coordinates', found_index=0)
    cordinatx1.x1Edit.set_edit_text(xpos).click_input()
    
    cordinatx2=app.Idea.window(title_re='Point Coordinates', found_index=0)
    cordinatx2.x2Edit.set_edit_text(xpos).click_input()
    
    cordinaty1=app.Idea.window(title_re='Point Coordinates', found_index=0)
    cordinaty1.y1Edit.set_edit_text("90").click_input()
    
    cordinaty2=app.Idea.window(title_re='Point Coordinates', found_index=0)
    cordinaty2.y2Edit.set_edit_text("190").click_input()
    
    app.Idea.PointCoordinatesDialog.OKButton.click_input()
    
    app.Idea.menu_select("Edit -> 1D Data")
    app.Idea.child_window(title="Remove Linear Tilt", auto_id="2360", control_type="MenuItem", found_index=0).click_input()
    
    app.Idea.menu_select("Edit -> 1D Data")
    app.Idea.child_window(title="Average Left and Right", auto_id="2381", control_type="MenuItem", found_index=0).click_input()
    
    app.Idea.menu_select("Abel-Inversion -> Abel Inversion-Probelem Analysis")
    
    fcsplines=app.Idea.window(title_re='Abel Analysis', found_index=0)
    fcsplines.NumberofCubicSplinesEdit.set_edit_text(maxorder).click_input()
    
    fmorder=app.Idea.window(title_re='Abel Analysis', found_index=0)
    fmorder.MaximumOrderofFucntionEdit.set_edit_text(maxorder).click_input()
    
    app.Idea.AbelAnalysisDialog.OKButton.click_input()
    
    app.Idea.menu_select("Window -> 7 2D-Data: Noname1-fint-four-Deviations00.bin")
    app.Idea.menu_select("Information -> Line Data")
    
    valuex1=app.Idea.window(title_re='Point Coordinates', found_index=0)
    valuex1.x1Edit.set_edit_text("0").click_input()
    
    valuey1=app.Idea.window(title_re='Point Coordinates', found_index=0)
    valuey1.y1Edit.set_edit_text("0").click_input()
    
    valuex2=app.Idea.window(title_re='Point Coordinates', found_index=0)
    valuex2.x2Edit.set_edit_text(maxorder).click_input()
    
    valuey2=app.Idea.window(title_re='Point Coordinates', found_index=0)
    valuey2.y2Edit.set_edit_text(maxorder).click_input()
    
    app.Idea.PointCoordinatesDialog.OKButton.click_input()
    
    app.Idea.menu_select("Window -> 9 Noname1-fint-four-Deviations00.bin")
    app.Idea.menu_select("File -> Save As...")
    
    file_dlg2=app.Idea.window(title_re="Please Specify a Filename to Save", found_index=0)
    file_dlg2.SaveButton.click_input()
    time.sleep(1)
    pyautogui.click(1041,607)
    pyautogui.click(1041,607)  #ok
    
    devfile='D:\\Akhil\\idea\\Noname1-fint-four-Deviations00.asc'
    with open(devfile,'r') as fl:
        eachfile2=[x.strip().split('\t') for x in fl]
        
    matrix2=np.array(eachfile2)
    floatArray2 = matrix2.astype(float)
    
    value2=[]
    for v in range(2,maxorder):
        value2.append(floatArray2[v][0])
    g=value2.index(min(value2))
        
    #print("deviation List=",value2)
    
    pol=g+2
    print("min order=",pol)

    
    app.Idea.menu_select("Window -> 5 Integral Abel Noname1.abl")

    app.Idea.menu_select("Abel-Inversion -> Abel Inversion -f-Interpolation ")
    order=app.Idea.window(title_re='Abel Inversion: f-Interpolation', found_index=0)
    order.NumberofCubicPolynomsEdit.set_edit_text(pol).click_input()
    time.sleep(1)
    
    pyautogui.click(881,637) #Click ok
    time.sleep(1)
    
    app.Idea.menu_select("File -> Save As...")
    time.sleep(1)

    pyautogui.click(102,153)
    pyautogui.click(357,556) #Save as type
    pyautogui.click(357,635) #1D raw asci
    pyautogui.click(738,609) #Save
    time.sleep(1)
    pyautogui.click(1044,607)
    time.sleep(2)
    pyautogui.click(1044,607)
   
   
    "For Exiting the Program"
    
    pyautogui.click(1005,608)
    app.Idea.menu_select("File -> Exit")
    time.sleep(2)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    pyautogui.click(1005,608)
    time.sleep(3)

    print('Finished for position',xpos)


    file="D:\\Akhil\\idea\\Noname1-fint-Abel-Reconstruction01.asc"
    with open(file,'r') as f:
        eachfile=[x.strip().split('\t') for x in f]
        
        
    
    matrix=np.array(eachfile)
    floatArray = matrix.astype(float)
    

    value=[]
    for v in range(0,101):
        value.append(floatArray[v][0])
        
    lamda=0.8 #micrometer
    scale=6 #micrometer
    nc=1.56*10**21
    
    densityelements=[]
    for c in range(0,101):
        ne=lamda*nc/(np.pi*scale)
        new=ne*abs(value[c])
        densityelements.append(new)
        
    df[xpos,i]=densityelements
    #print(df)
print("Total Data\n",df)
df.to_csv('D:\Akhil\idea\Density12_5.csv')
print("Task Completed")

end=time.time()
print("Elapsed Time=",end-start, "s")