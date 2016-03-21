#Author: Ian Fennen

import requests
from bs4 import BeautifulSoup as bs
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime as dt

def toF(tempC):
    tempF = float(tempC) * 9 / 5 + 32
    return tempF
   

#appid = input("Please enter appid: ")
try:
    url="http://api.openweathermap.org/data/2.5/weather?zip=77493,us&appid=67b33a9422a924f5e2697376795b15ef"#for just current weather
    r=requests.get(url)

    soup = r.content


    reg=re.split("[:,}]",str(soup))
    tempK=""

    for i in range(0,len(reg)):
        if "temp" in reg[i]:
            if i< len(reg)-1:
                tempK = float(reg[i+1])
                

    tempC=tempK - 273.15

    CurrentTempF = tempC * 9 / 5 + 32

    """f = open('data.dat', 'a')

    f.write(str(tempF)+'\n')

    f.close()"""
    t=str(dt.now().time())
    test= re.search("(\d+)\:(\d+)\:(\d+\.\d+)",str(t))

    start=int(test.group(1))*60*60+int(test.group(2))*60+float(test.group(3))
    print('temp F= '+str(CurrentTempF))
    url2="http://api.openweathermap.org/data/2.5/forecast?q=77493,us&mode=xml&appid=67b33a9422a924f5e2697376795b15ef" #for forecast
    r2=requests.get(url2)

    t=str(dt.now().time())
    test= re.search("(\d+)\:(\d+)\:(\d+\.\d+)",str(t))
    end=int(test.group(1))*60*60+int(test.group(2))*60+float(test.group(3))
    difference =end-start
    out=re.search("(\d+\.\d\d\d)",str(difference))
    print("time taken " +str(out.group(1))+" seconds")
    print()

    xml=r2.content

    root=ET.fromstring(xml)

    data=[]
    for forecast in root.findall('forecast'):
        for temp in forecast.findall("time"):
            for t in temp.findall("temperature"):
               data.append(t.attrib)

    #\'value\': \'(\d+\.\d+)\'


    m=[]
    for d in data:
        m.append(re.search("\'value\': \'(-?\d+\.\d+)\'",str(d)))


    time=str(dt.now().time())
    currentHr=re.search("(\d+)\:",str(time))


    time=int(int(currentHr.group(1))/3)#current 3 hour range 

    i=time
    allTemps=[]
    for d in m: #gets all temps for next 12 hours ***can change later to use args from command 
        if d:
            allTemps.append(toF(d.group(1)))
            #if i%8!=0:
            #    print(toF(d.group(1)))
            #elif i%8==0:
                #print(toF(d.group(1)))
                #print()
        i+=1
        if i >3+time:
            break
    #print(i)

    maxT=max(allTemps)
    minT=min(allTemps)
    
    print("<maxTemp = \""+str(maxT)+"\">")
    print("<minTemp = \""+str(minT)+"\">")
        
    #break
    

except requests.exceptions.ConnectionError:
    print("failure to connect to website.")





