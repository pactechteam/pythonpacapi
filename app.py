from flask import Flask
from flask import request
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
import os
SECRET_KEY = os.getenv("pythonapi")


app = Flask(__name__)

from datetime import datetime
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
        print(event.vobject_instance.vevent.description.value)      
        print(event.vobject_instance.vevent.uid.value)   

        oldDescription = event.vobject_instance.vevent.description.value
        newDescription = """{0} 

https://www.paccenter.org/api/calupdate?uid={1}

{2}
""".format(name,uid,oldDescription)

       # this will update description
        event.vobject_instance.vevent.description.value = newDescription
        event.save()
        print("complete")        
                                        
    return 'complete'
