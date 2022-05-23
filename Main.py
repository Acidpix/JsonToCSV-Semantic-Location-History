import json
import csv
import locale
from datetime import datetime
from datetime import timedelta
from dateutil.parser import isoparse
from os import listdir
from os.path import isfile , join

locale.setlocale(locale.LC_ALL, 'fr_FR')


addtime =  timedelta(hours=0)
path = "C:/Users/Pixi/Mon Drive/Avocat/JsonToCsv/2022/"


def getfiles(path):
    list = []
    for f in listdir(path):
        if isfile(join(path,f))  : 
            if ".json" in f:
                list.append (f)
                print (f)
                
    return list

def getar(data) :
    
    data = data['duration']['startTimestamp']
    data = str(int(isoparse(data).timestamp() * 1000))
    data = (datetime.fromtimestamp(int(data) / 1000)).strftime("%H:%M:%S")
    return data


def getdep(data) :
        
    data = data['duration']['endTimestamp']
    data = str(int(isoparse(data).timestamp() * 1000))
    data = (datetime.fromtimestamp(int(data) / 1000)).strftime("%H:%M:%S")
    return data

def getdate(data) : 

    data = data['duration']['startTimestamp']
    data = str(int(isoparse(data).timestamp() * 1000))
    data = (datetime.fromtimestamp(int(data) / 1000)).strftime("%Y-%m-%d")
    return data

def getday(data) :
        
    data = data['duration']['endTimestamp']
    data = str(int(isoparse(data).timestamp() * 1000))
    data = (datetime.fromtimestamp(int(data) / 1000)).strftime("%A")
    return data

def getworkingtime(data):

    dataAr = data['duration']['startTimestamp']
    dataAr = str(int(isoparse(dataAr).timestamp() * 1000))
    dataAr = (datetime.fromtimestamp(int(dataAr) / 1000))


    dataDep = data['duration']['endTimestamp']
    dataDep = str(int(isoparse(dataDep).timestamp() * 1000))
    dataDep= (datetime.fromtimestamp(int(dataDep) / 1000))

    workingtime = dataDep - dataAr
    workingtime = str(workingtime)
    workingtime = workingtime.split(".")[0]
    return workingtime
       


files = getfiles(path)

for file in files :
    filepath = path + file
    print (filepath)
    outputFile = path + file.replace(".json", ".csv")
    print (outputFile)
    with open(outputFile, 'wt') as csvfile:
        csvWriter = csv.writer(csvfile,quoting=csv.QUOTE_ALL,lineterminator='\n')
        csvWriter.writerow(['Date','Joure','Arrive', 'Depart','Temps Total', 'Name', 'Address'])
            
        with open (filepath, encoding="utf-8") as jsonFile:
            data = json.load(jsonFile)
            items = data["timelineObjects"]
            
            for item in items:
                for t , v in item.items() : 
                    if t == "placeVisit":   
                        try :
                            title = v['location']['name']
                        except KeyError:
                            title = "inconue"
                        try :    
                            address = v['location']['address']
                        except KeyError :
                            address = "inconue"
                        har = getar(v) 
                        hdep = getdep(v)
                        date = getdate(v)
                        workingtime = getworkingtime(v)
                        day = getday(v) 

                        csvWriter.writerow ([date,day,har,hdep,workingtime,title,address])
                        if day == "vendredi" :
                            addtime = addtime.total_seconds() / 3600
                            csvWriter.writerow (["Fin de semaine","Fin de semaine","Fin de semaine","Fin de semaine","Fin de semaine","Fin de semaine"])
                            addtime = timedelta(hours=0)


