import json
import csv
import locale
from datetime import datetime
from datetime import timedelta
from dateutil.parser import isoparse

locale.setlocale(locale.LC_ALL, 'fr_FR')

files = ["2019_JANUARY.json","2019_FEBRUARY.json","2019_MARCH.json","2019_APRIL.json","2019_MAY.json","2019_JUNE.json","2019_JULY.json","2019_AUGUST.json","2019_SEPTEMBER.json","2019_OCTOBER.json","2019_NOVEMBER.json", "2019_DECEMBER.json"]
addtime =  timedelta(hours=0)


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
       



for file in files :
    outputFile = file.replace(".json", ".csv")
    print (outputFile)
    with open(outputFile, 'wt') as csvfile:
        csvWriter = csv.writer(csvfile,quoting=csv.QUOTE_ALL,lineterminator='\n')
        csvWriter.writerow(['Date','Joure','Arrive', 'Depart','Temps Total', 'Name', 'Address'])
            
        with open (file, encoding="utf-8") as jsonFile:
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


