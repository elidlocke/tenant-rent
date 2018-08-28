#!/usr/bin/python3
import sys

from email.utils import parseaddr
from .utility import concatStrings
from collections import OrderedDict
from .rentalDatabase import rentalDatabase
from .writeReceipts import writeReceipts
from .tenantEmail import sendEmails


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
            if parseaddr(email) == ('', ''):
                raise BaseException()
            self.db.addTenant(name, email)
            self.putSuccess("Added {} to tenants".format(name))
        except BaseException:
            self.putErr("Couldn't add that tenant.")

    def placeTenant(self):
        try:
            print("Select the ID of an available tenant: ")
            self.db.printTenantList()
            user_id = input("user_id to place [eg. 1]: ")
            term = input("Term [eg. Fall 2018]: ")
            name = db.getTenantNameById(user_id)
            print("Which room are you placing {} in? ".format(name))
            self.db.printAvailableRooms(term)
            room_id = input("Room letter [eg. A]: ")
            self.db.placeTenant(user_id, room_id, term)
            self.putSuccess("Placed {} in {} for the {} term."
                            .format(name, room_id, term))
        except BaseException:
            self.putErr("Wasn't able to place that tenant there.")

    def listTenants(self):
        try:
            term = input("Term [eg. Fall 2018]: ")
            print("Here are all the tenants for that term: \n")
            self.db.printTenantsByTerm(term)
        except BaseException:
            self.putErr("Wasn't able to find any tenants to list")

    def recordRent(self):
        try:
            month = input("Month [eg. January 2018]: ")
            print("Here are all the tenants for that month: \n")
            options = self.db.printTenantsRentStatus(month)
            if options.empty:
                raise BaseException()
            user_id = input("user_id to mark as paid [eg. 1]: ")
            self.db.recordRentPayment(user_id, month)
            name = db.getTenantNameById(user_id)
            self.putSuccess("Recorded {} as paid for {}"
                            .format(name, month))
        except BaseException:
            self.putErr("Wasn't able to record that rent payment.")

    def generateReciepts(self):
        try:
            tenantNames = writeReceipts(self.db)
            if len(tenantNames) == 0:
                print("\nAll receipts have already been made\n")
            else:
                printFriendlyNames = concatStrings(tenantNames)
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
                printFriendlyNames = concatStrings(peopleEmailed)
                self.putSuccess(
                    "Sent new receipts to {}".format(printFriendlyNames))
        except BaseException:
            self.putErr("Wasn't able to send those emails."
                        " Did you set the env variables?")

    def exit(self):
        print("You chose to quit the program. Goodbye.")
        sys.exit()


def runProgram(program):
    programOptions = OrderedDict({
        '1': ("add a new tenant", program.addTenant),
        '2': ("place a tenant", program.placeTenant),
        '3': ("list tenants", program.listTenants),
        '4': ("record rent payments", program.recordRent),
        '5': ("generate rent receipts", program.generateReciepts),
        '6': ("send rent receipts", program.sendRent),
        '7': ("quit", program.exit)
    })
    while (1):
        print("*********************************\n" +
              "*    QUARRIE HOUSE RENT TIME    *\n" +
              "*********************************\n")
        for key in programOptions:
            print("{} - {}".format(key, programOptions[key][0]))
        selection = input('choose an option: ')
        try:
            programOptions[selection][1]()
        except BaseException:
            print("\nEnter a valid number\n")


if __name__ == "__main__":
    db = rentalDatabase()
    p = Program(db)
    runProgram(p)
