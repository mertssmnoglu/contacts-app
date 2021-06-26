import json
import os
from tkinter import *
from tkinter import messagebox
import datetime
import time
now = datetime.datetime.now()
class Application():
    def __init__(self):
        self.primaryColor = "#0d1117"
        self.secondaryColor = ""
        self.title ="Contacts"
        self.contactsFile = "contacts.json"
        self.countriesFile = "lib/countries.json"
        self.masterApp = Tk()
        self.masterApp.attributes('-zoomed', True)
        self.topbar = Frame(self.masterApp,bg=self.primaryColor)
        self.topbar.place(relx=0,rely=0,relwidth=1,relheight=0.1)
        self.dateTime = Label(self.topbar, fg="#ffffff",bg=self.primaryColor,text=f"{now.day} / {now.month} / {now.year}", font="Verdana 18 bold")
        self.dateTime.pack(side="right")
        self.leftbar = Frame(self.masterApp,bg=self.primaryColor)
        self.leftbar.place(relx=0,rely=0.15,relwidth=0.35,relheight=0.5)
        self.rightbar = Frame(self.masterApp,bg=self.primaryColor)
        self.rightbar.place(relx=0.4,rely=0.15,relwidth=0.60,relheight=0.5)
        self.footer = Frame(self.masterApp,bg=self.primaryColor)
        self.footer.place(relx=0,rely=0.83,relwidth=1,relheight=0.17)
        self.title = Label(self.topbar, fg="#ffffff",bg=self.primaryColor,text=self.title, font="Verdana 18 bold")
        self.title.pack(side="left")
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
    def addNewContact(self):
        contactData = {
            "_id": self.getId(),
            "name":contactNameEntry.get(),
            "surname":contactSurnameEntry.get(),
            "phoneNumber": self.getCountryCode() + contactPhoneEntry.get(),
            "groups":contactGroupsEntry.get().split(sep=",")
        }
        if(contactData["groups"] == [""]):
            contactData["groups"] = []
        if(contactData["name"] == ''):
            messagebox.showerror("Oops!", "Name can not be empty.")
        elif(contactData["surname"] == ''):
            messagebox.showerror("Oops!", "Surname can not be empty.")
        elif(contactPhoneEntry.get() == ''):
            messagebox.showerror("Oops!", "Phone Number can not be empty.")
        else:
            with open(self.contactsFile, "r") as jsonFile:
                data = json.load(jsonFile)
                data["contactList"].append(contactData)
            with open(self.contactsFile, "w") as jsonFile:
                json.dump(data, jsonFile, indent=2)
            contactBasicInfo=f"{contactData['name'] + ' ' + contactData['surname'].upper()}"
            self.increaseId()
            print(f"New contact {contactBasicInfo} added.")
            self.clear_rightbar()
            self.getContactList()
    def clear_rightbar(self):
        for widgets in app.rightbar.winfo_children():
            widgets.destroy()
    def getContactList(self):
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)["contactList"]
            scrollbar = Scrollbar(self.rightbar)
            scrollbar.pack( side = RIGHT, fill = Y )
            mylist = Listbox(self.rightbar,width=100,yscrollcommand = scrollbar.set)
            for i in range (1,len(data)):
                mylist.insert(END, f"{data[i]['name']} {data[i]['surname']}")
            mylist.pack()
    def help(self):
        import webbrowser
        webbrowser.open("https://github.com/mertssmnoglu/contacts-app/issues/new")
app = Application()
app.getContactList()
contactNameLabel = Label(app.leftbar, text="Enter Name:")
contactNameLabel.pack(anchor="w")
contactNameEntry = Entry(app.leftbar)
contactNameEntry.pack(anchor="w")
contactSurnameLabel = Label(app.leftbar, text="Enter Surname:")
contactSurnameLabel.pack(anchor="w")
contactSurnameEntry = Entry(app.leftbar)
contactSurnameEntry.pack(anchor="w")
contactPhoneLabel = Label(app.leftbar, text="Enter Phone Number:")
contactPhoneLabel.pack(anchor="w")
contactPhoneEntry = Entry(app.leftbar)
contactPhoneEntry.pack(anchor="w")
contactGroupsLabel = Label(app.leftbar, text="Enter Groups:")
contactGroupsLabel.pack(anchor="w")
contactGroupsEntry = Entry(app.leftbar)
contactGroupsEntry.pack(anchor="w")
addContactButton = Button(app.leftbar,text="Add Contact",command=app.addNewContact)
addContactButton.pack(side=LEFT)
helpButton = Button(app.footer, text="Help", command=app.help)
helpButton.pack(side=TOP,pady="20")
app.masterApp.mainloop()