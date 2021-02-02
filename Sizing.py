#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:00:15 2021

@author: Mathew
"""

from skimage.io import imread
import matplotlib.pyplot as plt
from skimage import filters,measure
from skimage.filters import threshold_local
from PIL import Image
import pandas as pd






# Paths to analyse below


pathList=[]


pathList.append(r"/Users/Mathew/Dropbox (Cambridge University)/Ed Code/DL_agg_sizing/8h_u")
pathList.append(r"/Users/Mathew/Dropbox (Cambridge University)/Ed Code/DL_agg_sizing/24h_n")
pathList.append(r"/Users/Mathew/Dropbox (Cambridge University)/Ed Code/DL_agg_sizing/120h_u")

filename="DL.tif"

pixel_size=103 # Pixel size in nm


# Function to load images:

def load_image(toload):
    
    image=imread(toload)
    
    return image



# Threshold image using otsu method and output the filtered image along with the threshold value applied:
    
def threshold_image_otsu(input_image):
    threshold_value=filters.threshold_otsu(input_image)    
    binary_image=input_image>threshold_value

    return threshold_value,binary_image

def subtract_bg(input_image):
    block_size = 51
    local_thresh = threshold_local(input_image, block_size,method='gaussian')
    filtered = image - local_thresh
   
    return filtered
# Threshold image using otsu method and output the filtered image along with the threshold value applied:
    
def threshold_image_fixed(input_image,threshold_number):
    threshold_value=threshold_number   
    binary_image=input_image>threshold_value

    return threshold_value,binary_image

# Label and count the features in the thresholded image:
def label_image(input_image):
    labelled_image=measure.label(input_image)
    number_of_features=labelled_image.max()
 
    return number_of_features,labelled_image
    
# Function to show the particular image:
def show(input_image,color=''):
    if(color=='Red'):
        plt.imshow(input_image,cmap="Reds")
        plt.show()
    elif(color=='Blue'):
        plt.imshow(input_image,cmap="Blues")
        plt.show()
    elif(color=='Green'):
        plt.imshow(input_image,cmap="Greens")
        plt.show()
    else:
        plt.imshow(input_image)
        plt.show() 
    
        
# Take a labelled image and the original image and measure intensities, sizes etc.
def analyse_labelled_image(labelled_image,original_image):
    measure_image=measure.regionprops_table(labelled_image,intensity_image=original_image,properties=('area','perimeter','centroid','orientation','major_axis_length','minor_axis_length','mean_intensity','max_intensity'))
    measure_dataframe=pd.DataFrame.from_dict(measure_image)
    return measure_dataframe



for i in range(len(pathList)):
    
    directory=pathList[i]+"/"
    
    toload=directory+filename
    
    image=load_image(toload)
    
    
   
    filt=subtract_bg(image)
    im_threshold,im_binary=threshold_image_otsu(filt)
    im = Image.fromarray(im_binary)
    im.save(directory+'Binary.tif')
    im_number,im_labelled=label_image(im_binary)
    print("%d feautres were detected in the aptamer image."%im_number)
    im_measurements=analyse_labelled_image(im_labelled,image)
    im_measurements.to_csv(directory + '/' + 'all_metrics.csv', sep = '\t')
    
    
    
 
 
    # Plot histograms
    
    areas= im_measurements['area']*((pixel_size/1000)**2)
    plt.hist(areas, bins = 20,range=[0,1], rwidth=0.9,color='#607c8e')
    plt.xlabel('Area (\u03bcm$^{2}$)')
    plt.ylabel('Number of Aggregates')
    plt.savefig(directory+'/'+'Areas.pdf')
    plt.show()
    
    intensities= im_measurements['mean_intensity']
    plt.hist(intensities, bins = 20,range=[0,100000], rwidth=0.9,color='#607c8e')
    plt.xlabel('Mean intensity (AU)')
    plt.ylabel('Number of Aggregates')
    plt.savefig(directory+'/'+'Intensities.pdf')
    plt.show()
    
    lengths= im_measurements['major_axis_length']*pixel_size/1000
    plt.hist(lengths, bins = 20,range=[0,10], rwidth=0.9,color='#607c8e')
    plt.xlabel('Length (\u03bcm)')
    plt.ylabel('Number of Aggregates')
    plt.savefig(directory+'/'+'lengths.pdf')
    plt.show()