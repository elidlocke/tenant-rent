#!/usr/bin/python3
import app.utils as utils
import app.rentalDatabase as rentalDatabase

from collections import OrderedDict
from writeReceipts import writeReceipts
from app.tenantEmail import sendEmails

'''
class programOption:
    def __init__(self, description, function=None):
        self.description = description.upper()
        self.function = function
'''


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
        except BaseException:
            self.putErr("Couldn't add that tenant.")

    def placeTenant(self):
        try:
            print("Select the ID of an available tenant: ")
            self.db.printQuery(
                    """ SELECT user_id, name email
                    FROM tenants """)
            user_id = input("user_id to place [eg. 1]: ")
            term = input("Term [eg. Fall 2018]: ")
            timestamp = utils.dateToTimeStamp(term)
            name = db.getTenantNameById(user_id)
            print("Which room are you placing {} in? ".format(name))
            rooms = self.db.getQuery(
                    """ SELECT rooms.room_id
                    FROM rooms
                    WHERE rooms.rentable = 1
                    AND rooms.room_id not in (
                        SELECT room_id from rent
                        WHERE date='{}'""").format(timestamp)
            print(', '.join(rooms))
            room_id = input("Room letter [eg. A]: ")
            self.db.placeTenant(user_id, room_id, term)
            self.putSuccess("Placed {} in {} for the {} term."
                            .format(name, room_id, term))
        except BaseException:
            self.putErr("Wasn't able to place that tenant there.")

    def listTenants(self):
        try:
            term = input("Term [eg. Fall 2018]: ")
            timestamp = utils.dateToTimeStamp(term)
            print("Here are all the tenants for that term: \n")
            self.db.printQuery(
                """ SELECT tenants.user_id, tenants.name,
                rent.room_id, rent.paid, tenants.email
                FROM rent
                INNER JOIN tenants
                ON tenants.user_id = rent.user_id
                WHERE rent.date='{}'
                ORDER BY rent.room_id
                """).format(timestamp)
        except BaseException:
            self.putErr("Wasn't able to find any tenants to list")

    def recordRent(self):
        try:
            month = input("Month [eg. January 2018]: ")
            print("Here are all the tenants for that month: \n")
            timestamp = utils.dateToTimeStamp(month)
            self.db.printQuery(
                """ SELECT tenants.user_id, tenants.name,
                rent.room_id, rent.paid
                FROM rent
                INNER JOIN tenants
                ON tenants.user_id = rent.user_id
                WHERE rent.date='{}'
                ORDER BY rent.room_id
                """).format(timestamp)
            user_id = input("user_id to mark as paid [eg. 1]: ")
            name = db.getTenantNameById(user_id)
            update_sql = """UPDATE rent
                              SET paid = 1
                              WHERE user_id={}
                              AND date='{}'"""\
                           .format(user_id, timestamp)
            self.db.updateQuery(update_sql)
            self.putSuccess("Recorded {} as paid for {}"
                            .format(name, month))
        except BaseException:
            self.putErr("Didn't properly record that payment.")

    def generateReciepts(self):
        try:
            tenantNames = writeReceipts(self.db)
            if len(tenantNames) == 0:
                print("\nAll receipts have already been made\n")
            else:
                printFriendlyNames = utils.concatStrings(tenantNames)
                self.putSuccess("Generated receipts for {}"
                                .format(printFriendlyNames))
        except BaseException:
            self.putErr("Issue generating receipt.")

    def sendRent(self):
        try:
            peopleEmailed = sendEmails(self.db)
            if len(peopleEmailed) == 0:
                print("All receipts have aleady been sent")
            else:
                printFriendlyNames = utils.concatStrings(peopleEmailed)
                self.putSuccess(
                    "Sent new receipts to {}".format(printFriendlyNames))
        except BaseException:
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
                break
            else:
                programOptions[selection].function()


if __name__ == "__main__":
    db = rentalDatabase()
    p = Program(db)
    p.runProgram()
