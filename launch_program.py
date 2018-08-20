#!/user/bin/python3
import manage_db

class programOption:
    def __init__(self, description, function=None):
        self.description = description.upper()
        self.function = function

class Program():
    def __init__(self, database):
        self.db = database

    def addTenant(self):
        name = input('Name [eg. Mary Smith]: ')
        email = input('Email [eg. mary@gmail.com]: ')
        try:
            self.db.addTenant(name, email)
        except:
            print ("Oops, error Adding Tenant to DB")
        print ("\n... success! Added {} to tenants\n".format(name))

    def placeTenant(self):
        print ("Select the ID of an available tenant: ")
        self.db.printTenants()
        user_id = input("user_id to place [eg. 1]: ")
        term  = input("Term [eg. Fall 2018]: ")
        name = db.getTenantNameById(user_id)
        print ("Which room are you placing {} in? ".format(name))
        self.db.printAvailableRooms(term)
        room_id = input("Room letter [eg. A]: ")
        try:
            self.db.placeTenant(user_id, room_id, term)
        except:
            print("Oops, error placing tenant.")
        print ("\nSUCCESS! Placed {} in {} for the {} term.\n".format(name, room_id, term))

    def listTenants(self):
        term = input("Term [eg. Fall 2018]: ")
        print ("Here are all the tenants for that term: \n")
        self.db.printTenantsByMonth(term)

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
        print("... generating reciepts for all months paid ... ")
        

    def sendRent(self):
        print("Choose M - month or U - user_id")

    def createProgramOptions(self):
        options = {
            '1': programOption("add a new tenant", self.addTenant),
            '2': programOption("place a tenant", self.placeTenant),
            '3': programOption("list tenants", self.listTenants),
            '4': programOption("record rent payments", self.recordRent),
            '5': programOption("generate rent reciepts", self.generateReciepts),
            '6': programOption("send rent reciepts", self.sendRent),
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
