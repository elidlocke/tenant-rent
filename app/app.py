#!/usr/bin/python3
from collections import OrderedDict
import manage_db
from receipt_factory import batchGenerateReceipts
from helper_functions import concatStrings
from send_email import tenantEmail

class programOption:
    def __init__(self, description, function=None):
        self.description = description.upper()
        self.function = function

class Program():
    def __init__(self, database):
        self.db = database

    def putErr(self, message):
        print("\n ERROR: {} Please try again!\n".format(message))
    
    def putSuccess(self, message):
        print("\n SUCCESS: {}\n".format(message))

    def addTenant(self):
        try:
            name = input('Name [eg. Mary Smith]: ')
            email = input('Email [eg. mary@gmail.com]: ')
            self.db.addTenant(name, email)
            self.putSuccess("Added {} to tenants".format(name))
        except:
            self.putErr("Couldn't add that tenant.")

    def placeTenant(self):
        try:
            print ("Select the ID of an available tenant: ")
            self.db.printTenants()
            user_id = input("user_id to place [eg. 1]: ")
            term  = input("Term [eg. Fall 2018]: ")
            name = db.getTenantNameById(user_id)
            print ("Which room are you placing {} in? ".format(name))
            self.db.printAvailableRooms(term)
            room_id = input("Room letter [eg. A]: ")
            self.db.placeTenant(user_id, room_id, term)
            self.putSuccess("Placed {} in {} for the {} term."\
                    .format(name, room_id, term))
        except:
            self.putErr("Wasn't able to place that tenant there.")

    def listTenants(self):
        try:
            term = input("Term [eg. Fall 2018]: ")
            print ("Here are all the tenants for that term: \n")
            self.db.printTenantsByMonth(term)
        except:
            self.putErr("Wasn't able to find any tenants to list")

    def recordRent(self):
        try:
            month = input("Month [eg. January 2018]: ")
            print ("Here are all the tenants for that month: \n")
            self.db.printTenantsByMonth(month)
            user_id = input("user_id to mark as paid [eg. 1]: ")
            name = db.getTenantNameById(user_id)
            self.db.markPaid(user_id, month)
            self.putSuccess("Recorded {} as paid for {}".format(name, month))
        except:
            self.putErr("Didn't properly record that payment.")

    def generateReciepts(self):
        try:
            mo_year = input("Month [eg. January 2018]: ")
            tenantList = batchGenerateReceipts(self.db, mo_year)
            if len(tenantList) == 0:
                print("\nAll receipts for {} have already been made\n"\
                        .format(mo_year.lower()))
                return
            tenantIDs = [n[0] for n in tenantList]
            tenantNames = [n[1] for n in tenantList]
            self.db.markRecMade(tenantIDs, mo_year)
            printFriendlyNames = concatStrings(tenantNames)
            self.putSuccess("Generated {} receipts for {}"\
                    .format(mo_year.capitalize(), printFriendlyNames))
        except:
            self.putErr("Issue generating receipt.")

    def sendRent(self):
        try:
            records = self.db.getSetReceiptsToSend()
            people_emailed = []
            if len(records) == 0:
                print("All receipts have aleady been sent")
                return
            for record in records:
                e = tenantEmail(record)
                e.send()
                people_emailed.append(record.tenant_name)
            printFriendlyNames = concatStrings(people_emailed)
            self.putSuccess("Sent new receipts to {}".format(printFriendlyNames))
        except:
            self.putErr("Wasn't able to send those emails")


    '''
    Move this to one function outside of class that is 'run program'
    '''

    def createProgramOptions(self):
        options = OrderedDict({
            '1': programOption("add a new tenant", self.addTenant),
            '2': programOption("place a tenant", self.placeTenant),
            '3': programOption("list tenants", self.listTenants),
            '4': programOption("record rent payments", self.recordRent),
            '5': programOption("generate rent receipts", self.generateReciepts),
            '6': programOption("send rent receipts", self.sendRent),
            '7': programOption("quit")
        })
        return options

    def runProgram(self):
        programOptions = self.createProgramOptions()
        while (1):
            print("*********************************\n" +
                  "*    QUARRIE HOUSE RENT TIME    *\n" + 
                  "*********************************\n")
            for key in programOptions:
                print("{} - {}".format(key, programOptions[key].description))
            selection = input('choose an option: ')
            if programOptions[selection].description == "QUIT":
                print("You chose to quit the program. Goodbye.")
                break ;
            else:
                programOptions[selection].function()

'''
this is the only main i am allowed to keep !!
'''

if __name__ == "__main__":
    db = manage_db.rentalDatabase()
    p = Program(db)
    p.runProgram()
