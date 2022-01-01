import flickrapi
import urllib.request
import os
import sys
import csv

API_KEY = #Your Own API KEY
API_SECRET = #Your Own API SECRET
filename = "PINGTUNG.txt"
Column_Name = ['ID', 'Owner','latitude','longitude','accuracy','place_id','woeid', 'nsid', 'location', 'taken', 'tags']
flickr=flickrapi.FlickrAPI(API_KEY, API_SECRET, cache=True)

#Open file to write
file = open(filename, 'w', newline='')
w = csv.writer(file)
w.writerow(Column_Name)

try:
    photos=flickr.walk(lat=23.9673,lon=120.8021, radius=5,  extras='geo')
except Exception as e:
    print('Error')

count = 0

for photo in photos:
    
    id=photo.get("id")
    owner=photo.get("owner")
    latitude=photo.get("latitude")
    longitude=photo.get("longitude")
    accuracy=photo.get("accuracy")
    place_id=photo.get("place_id")
    woeid=photo.get("woeid") 
    
    try:
     infos=flickr.photos.getInfo(api_key=API_KEY, photo_id=id)

    except Exception as e:
        print('Error')
    
    nsid = infos[0][0].get("nsid")
    #username = infos[0][0].get("username")
    #realname = infos[0][0].get("realname")
    location = infos[0][0].get("location")
    taken = infos[0][4].get("taken")
    #
    for tag in infos[0][11]:
     tags=tag.text
    if(str(id) == "None"):
       print("It's None!")
    else:
        if count==0:
            print("Begin Writing")
            count = 1
        try:    
            w.writerow([id, owner, latitude, longitude, accuracy, place_id, woeid, nsid, location, taken, tags])
        except UnicodeEncodeError:
            continue
file.close()
print("finish")