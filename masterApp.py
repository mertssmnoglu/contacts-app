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
        self.contactNameLabel = Label(self.leftbar, text="Enter Name:")
        self.contactNameLabel.pack(anchor="w")
        self.contactNameEntry = Entry(self.leftbar)
        self.contactNameEntry.pack(anchor="w")
        self.contactSurnameLabel = Label(self.leftbar, text="Enter Surname:")
        self.contactSurnameLabel.pack(anchor="w")
        self.contactSurnameEntry = Entry(self.leftbar)
        self.contactSurnameEntry.pack(anchor="w")
        self.contactPhoneLabel = Label(self.leftbar, text="Enter Phone Number:")
        self.contactPhoneLabel.pack(anchor="w")
        self.contactPhoneEntry = Entry(self.leftbar)
        self.contactPhoneEntry.pack(anchor="w")
        self.contactGroupsLabel = Label(self.leftbar, text="Enter Groups:")
        self.contactGroupsLabel.pack(anchor="w")
        self.contactGroupsEntry = Entry(self.leftbar)
        self.contactGroupsEntry.pack(anchor="w")
        self.setCountryCodeEntry = Entry(self.leftbar)
        self.setCountryCodeEntry.pack(anchor="w",side=BOTTOM)
        self.setCountryLabel = Label(self.leftbar, text="Set Default Country Code:")
        self.setCountryLabel.pack(anchor="w",side=BOTTOM)
        self.addContactButton = Button(self.footer,text="Add Contact",command=self.addNewContact)
        self.addContactButton.pack(side=LEFT)
        self.setCountryCodeButton = Button(self.footer,text="Set default country code",command=self.setDefaultCountryCode)
        self.setCountryCodeButton.pack(side=LEFT)
        self.helpButton = Button(self.footer, text="Help", command=self.help)
        self.helpButton.pack(side=RIGHT,pady="20")
    def addContactGroup(self,groupName,groupDescription):
        with open(self.contactsFile, "r") as jsonFile:
            data = json.load(jsonFile)
            data["contactGroups"].append({"name":groupName,"description":groupDescription})
        with open(self.contactsFile, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
    def setDefaultCountryCode(self):
        defaultCountryCode = self.setCountryCodeEntry.get()
        if defaultCountryCode == '':
            messagebox.showerror("Oops!", "Country code can not be empty.")
        elif "+" not in defaultCountryCode or len(defaultCountryCode) <= 1:
            messagebox.showerror("Oops!", "Country code is invalid.")
        else:
            with open(self.contactsFile, "r",) as jsonFile:
                data = json.load(jsonFile)
                data["defaultCountryCode"] = str(defaultCountryCode)
            with open(self.contactsFile, "w") as jsonFile:
                json.dump(data, jsonFile, indent=2)
            print(f"Default Country Code setted {defaultCountryCode}.")
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
            "name":self.contactNameEntry.get(),
            "surname":self.contactSurnameEntry.get(),
            "phoneNumber": self.getCountryCode() + self.contactPhoneEntry.get(),
            "groups":self.contactGroupsEntry.get().split(sep=",")
        }
        if(contactData["groups"] == [""]):
            contactData["groups"] = []
        if(contactData["name"] == ''):
            messagebox.showerror("Oops!", "Name can not be empty.")
        elif(contactData["surname"] == ''):
            messagebox.showerror("Oops!", "Surname can not be empty.")
        elif(self.contactPhoneEntry.get() == ''):
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
        for widgets in self.rightbar.winfo_children():
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