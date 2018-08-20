#!/user/bin/python3
import manage_db
from receipt_factory import batchGenerateReceipts

class programOption:
    def __init__(self, description, function=None):
        self.description = description.upper()
        self.function = function

class Program():
    def __init__(self, database):
        self.db = database

    def addTenant(self):
        try:
            name = input('Name [eg. Mary Smith]: ')
            email = input('Email [eg. mary@gmail.com]: ')
            self.db.addTenant(name, email)
            print ("\n... success! Added {} to tenants\n".format(name))
        except:
            print ("Oops, error Adding Tenant to DB")

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
            print ("\nSUCCESS! Placed {} in {} for the {} term.\n".format(name, room_id, term))
        except:
            print("Oops, error placing tenant.")

    def listTenants(self):
        try:
            term = input("Term [eg. Fall 2018]: ")
            print ("Here are all the tenants for that term: \n")
            self.db.printTenantsByMonth(term)
        except:
            print("oops")

    def recordRent(self):
        try:
            month = input("Month [eg. January 2018]: ")
            print ("Here are all the tenants for that month: \n")
            self.db.printTenantsByMonth(month)
            user_id = input("user_id to mark as paid [eg. 1]: ")
            name = db.getTenantNameById(user_id)
            self.db.markPaid(user_id, month)
            print ("Success! Recorded {} as paid for {}".format(name, month))
        except:
            print("Oops, error recording rent payment!")

    def generateReciepts(self):
        try:
            mo_year = input("Month [eg. January 2018]: ")
            tenantList = batchGenerateReceipts(self.db, mo_year)
            if len(tenantList) == 0:
                print("\nAll receipts for {} have already been made\n".format(mo_year.lower()))
                return
            tenantIDs = [n[0] for n in tenantList]
            tenantNames = [n[1] for n in tenantList]
            printFriendlyNames = ""
            if len(tenantNames) > 2:
                printFriendlyNames = ', '.join(tenantNames[:-1]) + ' and ' + str(tenantNames[-1])
            elif len(tenantNames)==2:
                printFriendlyNames = ' and '.join(tenantNames)
            elif len(tenantNames)==1:
                printFriendlyNames =  tenantNames[0]
            self.db.markRecMade(tenantIDs, mo_year)
            print("SUCCESS. Generated {} receipts for {}"\
                    .format(mo_year.lower(), printFriendlyNames))
       except:
           print("Oops had an issue making those receipts")

    def sendRent(self):
        print("Choose M - month or U - user_id")

    def createProgramOptions(self):
        options = {
            '1': programOption("add a new tenant", self.addTenant),
            '2': programOption("place a tenant", self.placeTenant),
            '3': programOption("list tenants", self.listTenants),
            '4': programOption("record rent payments", self.recordRent),
            '5': programOption("generate rent receipts", self.generateReciepts),
            '6': programOption("send rent receipts", self.sendRent),
            '7': programOption("quit")
        }
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

if __name__ == "__main__":
    db = manage_db.rentalDatabase()
    p = Program(db)
    p.runProgram()
