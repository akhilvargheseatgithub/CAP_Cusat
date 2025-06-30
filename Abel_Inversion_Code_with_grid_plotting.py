# -*- coding: utf-8 -*-
"""
Created on Sat May 24 18:45:31 2025

@author: Akhil Varghese
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import abel
from PIL import Image

# Step 1: Load the ASCII file
name=["14_5","14","13_75","13_5","13_25","13","12_5","12"]

images=[]
for k in range(0,len(name)):
    filename = "C:/Users/VICTUS/Downloads/Phase Data/"+name[k]+str(".asc")
    data = np.loadtxt(filename)
    
    
    # Step 2: Identify rows and columns that are NOT all NaN
    valid_rows = ~np.all(np.isnan(data), axis=1)
    valid_cols = ~np.all(np.isnan(data), axis=0)
    
    # Step 3: Crop the array
    cropped_data1 = data[valid_rows][:, valid_cols]
    cropped_data = cropped_data1[45:109,238:586]
    
    # Step 4: Print the new size
    new_height, new_width = cropped_data.shape
    print(f"New size after cropping: {new_height} x {new_width}")
    
    # Optional: set NaNs in cropped_data to zero or mask them
    #cropped_data = np.nan_to_num(cropped_data,nan=0.0)
    
    # Fit a linear model (y = mx + b) to each vertical slice (each column in the 2D data) and remove linear tilt
    def remove_tilt(data):
        corrected_data = data.copy()
        for col in range(data.shape[1]):
            # Fit linear model to each column
            x = np.arange(data.shape[0])
            y = data[:, col]
            slope, intercept, _, _, _ = stats.linregress(x, y)
            
            # Subtract the linear tilt
            corrected_data[:, col] = y - (slope * x + intercept)
        
        return corrected_data
    
    # Apply tilt removal
    corrected_data = remove_tilt(cropped_data)
    
    # Average data assuming symmetry
    def symmetrize_rows(data):
        
        #Symmetrize each column (i.e., vertical slice) using top-bottom averaging.
        nrows, ncols = data.shape
        center = nrows // 2
    
        top = data[:center, :]
        if nrows % 2 == 0:
            bottom = data[center:, :]
            middle = None
        else:
            bottom = data[center+1:, :]
            middle = data[center:center+1, :]
    
        # Flip bottom half vertically
        bottom_flipped = bottom[::-1, :]
    
        # Average top and flipped bottom
        sym_half = 0.5 * (top + bottom_flipped)
    
        # Reconstruct full symmetrized data
        if middle is not None:
            sym_data = np.vstack((sym_half, middle, sym_half[::-1, :]))
        else:
            sym_data = np.vstack((sym_half, sym_half[::-1, :]))
    
        return sym_data
    
    # Apply to tilt-corrected data
    symmetrized_data = symmetrize_rows(corrected_data)
    
    # Abel Transform on the data
    rotated_data = np.rot90(symmetrized_data, k=1)
    inverse_abel = abel.Transform(rotated_data, direction='inverse',
                                  method='direct').transform
    inverted_data = np.rot90(inverse_abel, k=-1)
    
    # Convert into electron density data
    lamda=0.8
    nc=1.2e21
    sf=6.5
    electron_density=np.abs(inverted_data)*lamda*nc/(np.pi*sf)
    images.append(electron_density)
    np.savetxt("output"+str(name[k])+".asc", electron_density, fmt='%.6f', delimiter=' ')
    
# Create Image grid
fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(12,12 ), constrained_layout=True)
axs = axs.flatten()
titles=["0 ps","3.2 ps","4.86 ps","6.52 ps","8.18 ps","9.84 ps","13.16 ps","14.68 ps"]

# Settings for each Plot
x_range=cropped_data.shape[1]*6.5
y_range=cropped_data.shape[0]*6.5
vmin=1e18
vmax=2e19

# Plot each processed image
for i, (ax, img) in enumerate(zip(axs, images)):
    im = ax.imshow(img, cmap='viridis', extent=[0, x_range,-y_range/2,y_range/2],origin='lower',vmin=vmin, vmax=vmax,aspect='auto')
    ax.set_title("Delay "+titles[i], fontsize=10)
    #ax.axis('off')  # Hide ticks and labels

# Add shared colorbar
cbar = fig.colorbar(im, ax=axs, orientation='vertical', fraction=0.03, pad=0.02)
cbar.set_label('Electron Density ($cm^-3$)', fontsize=12)

# Save the final grid image
x=plt.savefig('D:/Academic/Pythonfiles/Abel Inversion/OutputFiles/Phase DataTime Evolution of Plasma2.png', dpi=300)
plt.close()