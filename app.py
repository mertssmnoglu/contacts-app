import json
from tkinter import *
import datetime
now = datetime.datetime.now()
class Application():
    def __init__(self):
        self.title ="Contacts"
        self.contactsFile = "contacts.json"
        self.countriesFile = "lib/countries.json"
        self.masterApp = Tk()
        self.topbar = Frame(self.masterApp,bg="#0d1117")
        self.topbar.place(relx=0,rely=0,relwidth=1,relheight=0.1)
        self.dateTime = Label(self.topbar, fg="#ffffff",bg="#0d1117",text=f"{now.day} / {now.month} / {now.year}", font="Verdana 18 bold")
        self.dateTime.pack(side="right")
        self.leftbar = Frame(self.masterApp,bg="#0d1117")
        self.leftbar.place(relx=0,rely=0.15,relwidth=0.35,relheight=0.5)
        self.rightbar = Frame(self.masterApp,bg="#0d1117")
        self.rightbar.place(relx=0.4,rely=0.15,relwidth=0.60,relheight=0.5)
        self.title = Label(self.topbar, fg="#ffffff",bg="#0d1117",text=self.title, font="Verdana 18 bold")
        self.title.pack(side="left")
        self.masterApp.mainloop()
    def addContactGroup(self,groupName,groupDescription):
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)
            data["contactGroups"].append({"name":groupName,"description":groupDescription})
        with open(self.contactsFile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
    def setDefaultCountryCode(self,countryCode="+1"):
        with open(self.contactsFile, "r",) as jsonFile:
            data = json.load(jsonFile)
            data["defaultCountryCode"] = str(countryCode)
        with open(self.contactsFile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
        print(f"Default Country Code setted {countryCode}.")
    def getCountryCode(self):
        with open(self.contactsFile, "r") as jsonFile:
            countryCode = json.load(jsonFile)
            return countryCode["defaultCountryCode"]
    def increaseId(self):
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)
            data["newContactId"] = data["newContactId"] +1
        with open(self.contactsFile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
    def getId(self):
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)
            return data["newContactId"]
    def addNewContact(self,name,surname,phoneNumber,groups):
        contactData = {
            "_id": self.getId(),
            "name":name,
            "surname":surname,
            "phoneNumber": self.getCountryCode() + phoneNumber,
            "groups":groups
        }
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)
            data["contactList"].append(contactData)
        with open(self.contactsFile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
        contactBasicInfo=f"{name + ' ' + surname.upper()}"
        self.increaseId()
        print(f"New contact {contactBasicInfo} added.")
    def getContactList(self):
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)["contactList"]
            for i in range (0,len(data)):
                if data[i]['_id'] != 0:
                    contactlist = Label(self.rightbar, fg="#ffffff",bg="#0d1117",text=f"{data[i]['name']} {data[i]['surname']}", font="Verdana 12 bold")
                    contactlist.pack(side="top")
app = Application()
app.getContactList()