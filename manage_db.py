#!/usr/bin/python3

import sqlite3
from collections import namedtuple
from helper_functions import *

class rentalDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('QuarrieTenants.db')
        self.c = self.conn.cursor()

    def printTenants(self):
        tenants = self.conn.execute("SELECT * from tenants")
        print("USER_ID\t\tNAME\t\tEMAIL")
        print("-----\t\t-----\t\t-----")
        for row in tenants:
            print ("{}\t|\t{}\t|\t{}".format(row[0],
                                         str(row[1]),
                                         str(row[2])))
        print("")


    def printTenantsByMonth(self, input_date):
        date = dateToTimeStamp(input_date)
        sql_query = "SELECT tenants.user_id, tenants.name,\
                     rent.room_id, rent.paid, tenants.email\
                     FROM rent\
                     INNER JOIN tenants ON tenants.user_id = rent.user_id\
                     WHERE rent.date='{}'\
                     ORDER BY rent.room_id".format(date)
        tenants = self.conn.execute(sql_query)
        print("ID\t\tNAME\t\tROOM\t\tPAID\t\tEMAIL")
        print("-----\t\t-----\t\t-----\t\t-----\t\t-----")
        for row in tenants:
            print ("{}\t|\t{}\t|\t{}\t|\t{}\t|\t{}"\
                    .format(row[0], str(row[1]), 
                            str(row[2]), str(row[3]), str(row[4])))
        print("")


    def printRent(self):
        rent_records = self.conn.execute("\
                SELECT name, room_id, date, paid\
                FROM rent\
                INNER JOIN tenants\
                ON tenants.user_id = rent.user_id")
        print("NAME\t\tROOM_ID\t\tDATE\t\tPAID")
        print("-----\t\t-----\t\t-----\t\t-----")
        for row in rent_records:
            print ("{}\t|\t{}\t|\t{}\t|\t{}".format(row[0],
                    str(row[1]), str(row[2][:7]),
                    "True" if row[3] else "False"))
        print("")

    def getTenantNameById(self, user_id):
        sql_query = "SELECT name FROM tenants\
                     WHERE user_id={}".format(user_id)
        result = self.conn.execute(sql_query)
        return(next(result)[0])


    def printAvailableRooms(self, term):
        date = termLookup(term)[0]
        sql_query = "SELECT rooms.room_id from rooms\
                     WHERE rooms.room_id not in (\
                     SELECT room_id from rent\
                     WHERE date='{}')".format(date)
        available_room_gen = self.c.execute(sql_query)
        available_rooms = [] 
        for room in available_room_gen:
            available_rooms.append(str(room[0]))
        print ("{}".format(", ".join(available_rooms)))

    '''
    ------- MODIFY DB --------
    '''

    def addTenant(self, name, email):
        '''
        adds a new tenant to the database
        '''
        sql_query = "INSERT into tenants (name, email)\
                     VALUES ('{}', '{}')".format(name, email)
        sql_retrieval = "SELECT user_id from tenants\
                         WHERE email='{}'".format(email)
        self.c.execute(sql_query)
        self.conn.commit()
        user_id = self.c.execute(sql_retrieval)
        return self.c.fetchone()[0]

    def placeTenant(self, user_id, room_id, term):
        '''
        places a tenant in the house for a specific term
        '''
        dates = termLookup(term)
        sql_queries = []
        for i in range(0,4):
            date = dates[i]
            sql_query = "INSERT INTO rent (user_id, room_id, date, paid)\
                         VALUES({}, '{}', '{}', {})".format(user_id, 
                                                            room_id,
                                                            date,
                                                            0)
            sql_queries.append(sql_query)
        for q in sql_queries:
            self.c.execute(q)
        self.conn.commit()


    def markPaid(self, user_id, mo_year):
        '''
        sets a tenant as paid
        '''
        date = dateToTimeStamp(mo_year)
        sql_query = "UPDATE rent\
                     SET paid=1\
                     WHERE user_id={}\
                     AND date='{}'".format(user_id, date)
        self.c.execute(sql_query)
        self.conn.commit()

    def markRecMade(self, user_ids, mo_year):
        '''
        takes in a list of user_id and marks them as paid
        for a specific month
        '''
        date = dateToTimeStamp(mo_year)
        sql_query = "UPDATE rent\
                     SET receipt_issued=1\
                     WHERE user_id IN ({})\
                     AND date='{}'".format(', '.join([str(uid) for uid in user_ids]), date)
        self.c.execute(sql_query)
        self.conn.commit()

    def getRentRecords(self, sql_query):
        tenants = self.conn.execute(sql_query)
        rentRecords = []
        RentRecord = namedtuple('RentRecord',
                                 ['tenant_id',
                                  'tenant_name',
                                  'tenant_email',
                                  'room_id',
                                  'date',
                                  'room_price',
                                  'rent_paid',
                                  'receipt_issued'])
        rentRecords = [RentRecord(*row) for row in tenants]
        return rentRecords


    def getOccupiedStatusByMonth(self, mo_year):
        '''
        return a list of all of the occupied rooms including the
        tenant id, tenant names, tenant email,
        room, room price, rent paid and reciept issued
        '''
        date = dateToTimeStamp(mo_year)
        sql_query = "SELECT tenants.user_id, tenants.name, tenants.email,\
                     rent.room_id, rent.date, rooms.price, rent.paid,\
                     rent.receipt_issued\
                     FROM rent\
                     INNER JOIN tenants\
                     ON tenants.user_id = rent.user_id\
                     INNER JOIN rooms\
                     ON rent.room_id = rooms.room_id\
                     WHERE rent.date='{}'\
                     ORDER BY rent.room_id".format(date)
        return self.getRentRecords(sql_query)

    def getSetReceiptsToSend(self):
        sql_query = "SELECT tenants.user_id, tenants.name, tenants.email,\
                     rent.room_id, rent.date, rooms.price, rent.paid,\
                     rent.receipt_issued\
                     FROM rent\
                     INNER JOIN tenants\
                     ON tenants.user_id = rent.user_id\
                     INNER JOIN rooms\
                     ON rent.room_id = rooms.room_id\
                     WHERE rent.receipt_issued=1 AND rent.paid=1\
                     AND rent.receipt_sent=0"
        recordsToSend = self.getRentRecords(sql_query)

        sql_update_query = "UPDATE rent\
                     SET receipt_sent=1\
                     WHERE paid=1 AND receipt_issued=1"
        self.c.execute(sql_update_query)
        self.conn.commit()
        return (recordsToSend)

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    db = rentalDatabase()
    db.printTenants()
    #db.printRent()
    #tenant_id = db.addTenant('Tracy Meng', 'tcmeng@gmail.com')
    #db.placeTenant(1, 'E', 'Winter 2018')
    #db.printTenantsByMonth('January 2018')
    #db.markPaid(10, 'November 2018')
    #db.printRent()
    #db.getTenantNameById(14)
    #db.getAvailableRooms('Fall 2018')
    #print(db.getOccupiedStatusByMonth('Fall 2018'))
    for record in db.getSetReceiptsToSend():
        print (record)
    #print(db.getSetReceiptsToSend())
    db.__del__()
