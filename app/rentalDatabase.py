#!/usr/bin/python3

import sqlite3
import app.utils as utils
import pandas as pd

from collections import namedtuple


class rentalDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('app/database/QuarrieRental.db')
        self.c = self.conn.cursor()

    def printQuery(self, sql_query):
        print("")
        df = pd.read_sql_query(sql_query,
                               self.conn,
                               index_col=None)
        print(df.to_string(index=False))

    def getQuery(self, sql_query):
        result = self.conn.execute(sql_query)
        return (list(result))

    def updateQuery(self, sql_query):
        self.c.execute(sql_query)
        self.conn.commit()

    def getTenantNameById(self, user_id):
        sql_query = """SELECT name FROM tenants
                     WHERE user_id={}""".format(user_id)
        result = self.conn.execute(sql_query)
        return(next(result)[0])

    def addTenant(self, name, email):
        sql_query = """INSERT INTO tenants (name, email)
                     VALUES ('{}', '{}')""".format(name, email)
        self.c.execute(sql_query)
        self.conn.commit()

    def placeTenant(self, user_id, room_id, term):
        dates = utils.termLookup(term)
        for i in range(0, 4):
            date = dates[i]
            sql_query = """"INSERT INTO
                        rent (user_id, room_id, date, paid)
                        VALUES({}, '{}', '{}', {})"""\
                        .format(user_id, room_id, date, 0)
            self.c.execute(sql_query)
        self.conn.commit()

    def markRecMade(self, user_ids, mo_year):
        '''
        takes in a list of user_id and marks them as paid
        for a specific month
        '''
        date = utils.dateToTimeStamp(mo_year)
        sql_query = """UPDATE rent
                     SET receipt_issued=1
                     WHERE user_id IN ({})
                     AND date='{}'"""\
                     .format(', '.join(
                                    [str(uid) for uid in user_ids]
                                 ), date)
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

    def getSetEmails(self):
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
