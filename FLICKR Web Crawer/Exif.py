#!/usr/bin/env python
# coding: utf-8

# In[134]:


import flickrapi
import urllib.request
import os
import sys
import csv
import xml.etree.cElementTree as ET


# In[156]:


#API Account
API_KEY = #Your Own API KEY
API_SECRET = #Your Own API SECRET
flickr=flickrapi.FlickrAPI(API_KEY, API_SECRET, cache=True)

#File to write
filename = "EXIF.csv"
Column_Name = ['id', 'camera', 'exposure', 'aperture', 'ISO', 'Date', 'Brightness', 'EV', 'F', 'exposure_mode', 'White_Balance', 'F_equal', 'latitude', 'longitude', 'GPS_Alt', 'nsid', 'views', 'locality', 'county', 'region', 'country']


# In[ ]:


#Open file to write
file = open(filename, 'w', newline='', encoding='utf-8')
w = csv.writer(file)
w.writerow(Column_Name)

#Searching Center
try:
    photos=flickr.walk(lat=23.6689173,lon=120.4860729, radius=5,  extras='geo')
except Exception as e:
    print('Error')

#parameters and file writing

count = 0
i=0

for photo in photos:
    
    #Get ID for photo infos and EXIF    
    id=photo.get("id")
    try:
        infos = flickr.photos.getInfo(api_key=API_KEY, photo_id=id)
        EXIF = flickr.photos.getExif(api_key=API_KEY, photo_id=id)
    except Exception as e:
        print('Error')
        
    #Use the labels for parameter searching
    
    child_layer = 0
    
    for child in EXIF[0]:
        
        try:
            if EXIF[0][child_layer].get('label')=='Exposure':
                exposure = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Aperture':
                aperture = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='ISO Speed':
                ISO = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Date and Time (Original)':
                Date = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Brightness Value':
                Brightness = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Exposure Bias':
                EV = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Focal Length':
                F = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Exposure Mode':
                exposure_mode = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='White Balance':
                White_Balance = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='Focal Length (35mm format)':
                F_equal = EXIF[0][child_layer].find('raw').text
            elif EXIF[0][child_layer].get('label')=='GPS Altitude':
                GPS_Alt = EXIF[0][child_layer].find('raw').text
        
            camera = EXIF[0].get("camera")
            views = infos[0].get("views")
            latitude = photo.get("latitude")
            longitude = photo.get("longitude")
            nsid = infos[0][0].get("nsid")
            locality = infos[0][12].find('locality').text
            county = infos[0][12].find('county').text
            region = infos[0][12].find('region').text
            country = infos[0][12].find('country').text
            
        except AttributeError:
            print('Error')
        child_layer += 1
    
    #Write the row into the file
    row = [id, camera, exposure, aperture, ISO, Date, Brightness, EV, F, exposure_mode, White_Balance, F_equal, latitude, longitude, GPS_Alt, nsid, views,locality, county, region, country]
        
    if count == 0:
        print("Begin Writing")
        
    if count == i:
        print(i)
        i += 50
    if i == 500:
        break
    try:    
        w.writerow(row)            
        count += 1     
    except UnicodeEncodeError:
        continue 
        
file.close()            
print("finish")

