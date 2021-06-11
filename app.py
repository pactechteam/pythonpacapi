from json.encoder import JSONEncoder
from flask import Flask
from flask import request
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()
import os
SECRET_KEY = os.getenv("pythonapi")


app = Flask(__name__)

import sys

## stuff from caldav example
sys.path.insert(0, '..')
sys.path.insert(0, '.')

import caldav





global tempTest
tempTest = 'Hello fellow PACers!'

@app.route('/')
def index():
    global tempTest
    return tempTest



@app.route('/create',methods=["POST"])
def create():
    params = request.json
    if SECRET_KEY == params["key"]:
        now = datetime.now()
        global tempTest
        tempTest  = params["name"]
        caldav_url = 'https://cal.bonner.hopto.org/'
        username = os.getenv("caluser")
        password = os.getenv("calpass")

        client = caldav.DAVClient(url=caldav_url, username=username, password=password)

        my_principal = client.principal()


        pacCalendar = client.calendar(url="https://cal.bonner.hopto.org/user1/eccc554d-2a25-6b9e-ee95-59d96066cea4/")

        my_event = pacCalendar.save_event("""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PYVOBJECT//NONSGML Version 1//EN
BEGIN:VEVENT
UID:thisisUnique
DTSTAMP:20210526T060000Z
DTSTART:20210527T060000Z
DTEND:20210527T230000Z
RRULE:FREQ=YEARLY
SUMMARY:{0}
DESCRIPTION:This is a lo
 ng description
 that exists on a long line.
END:VEVENT
END:VCALENDAR
""".format(tempTest,now)                     
                                        )
    return 'complete'




@app.route('/update',methods=["POST"])
def update():
    params = request.json
    if SECRET_KEY == params["key"]:
        now = datetime.now()
        global tempTest
       # tempTest  = params["name"]
        name = params["name"]
        uid = params["uid"]
        caldav_url = 'https://cal.bonner.hopto.org/'
        username = os.getenv("caluser")
        password = os.getenv("calpass")

        client = caldav.DAVClient(url=caldav_url, username=username, password=password)

        my_principal = client.principal()


        pacCalendar = client.calendar(url="https://cal.bonner.hopto.org/user1/eccc554d-2a25-6b9e-ee95-59d96066cea4/")

        event = pacCalendar.event_by_uid(uid)
  

        oldDescription = event.vobject_instance.vevent.description.value
        newDescription = """{0} 
{1}
""".format(name,oldDescription)

       # this will update description
        event.vobject_instance.vevent.description.value = newDescription
        event.save()    
                                        
    return newDescription



@app.route('/upgrade',methods=["POST"])
def upgrade():
    params = request.json
    if SECRET_KEY == params["key"]:

        caldav_url = 'https://cal.bonner.hopto.org/'
        username = os.getenv("caluser")
        password = os.getenv("calpass")

        client = caldav.DAVClient(url=caldav_url, username=username, password=password)

        my_principal = client.principal()


        pacCalendar = client.calendar(url="https://cal.bonner.hopto.org/user1/eccc554d-2a25-6b9e-ee95-59d96066cea4/")
# datetime(year,month,day)
        events_fetched = pacCalendar.date_search(
            start=datetime(2021, 5, 20), end=datetime(2021, 6, 1), expand=True)
        for event in events_fetched:
            uid = event.vobject_instance.vevent.uid.value
            oldDescription = event.vobject_instance.vevent.description.value
            newDescription = oldDescription
            if "https://www.paccenter.org/calupdate?uid=" in oldDescription:
                newDescription = oldDescription
            else:
                newDescription = """{1}
https://www.paccenter.org/calupdate?uid={0}
 """.format(uid,oldDescription)
            event.vobject_instance.vevent.description.value = newDescription
            event.save()

    
                                        
    return 'complete'


    
@app.route('/getFacts',methods=["POST"])
def getFacts():
    params = request.json
    if SECRET_KEY == params["key"]:
        uid = params["uid"]
        caldav_url = 'https://cal.bonner.hopto.org/'
        username = os.getenv("caluser")
        password = os.getenv("calpass")

        client = caldav.DAVClient(url=caldav_url, username=username, password=password)


        pacCalendar = client.calendar(url="https://cal.bonner.hopto.org/user1/eccc554d-2a25-6b9e-ee95-59d96066cea4/")

        event = pacCalendar.event_by_uid(uid)


        payload = {"data":event.data,"description":event.vobject_instance.vevent.description.value}

    
                                        
    return payload


    
    
@app.route('/getAll',methods=["POST"])
def getAll():
    params = request.json
    if SECRET_KEY == params["key"]:
        caldav_url = 'https://cal.bonner.hopto.org/'
        username = os.getenv("caluser")
        password = os.getenv("calpass")

        client = caldav.DAVClient(url=caldav_url, username=username, password=password)


        pacCalendar = client.calendar(url="https://cal.bonner.hopto.org/user1/eccc554d-2a25-6b9e-ee95-59d96066cea4/")
        events = pacCalendar.events()

        payload = []
        for event in events:
            title = event.vobject_instance.vevent.summary.value
            start =  event.vobject_instance.vevent.dtstart.value
            end =  event.vobject_instance.vevent.dtend.value
            description =  event.vobject_instance.vevent.description.value
            uid =  event.vobject_instance.vevent.uid.value

            startStr = start.timestamp()
            endStr= end.timestamp()

            payload.append(({"title":title,"start":startStr,"end":endStr,"description":description,"uid":uid}))
        
        

      

    jsonStr = json.dumps(payload)
                                        
    return {"events":jsonStr}