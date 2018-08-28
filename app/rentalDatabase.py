#!/usr/bin/python3

import sqlite3

from .utility import termLookup
import pandas as pd
from .utility import dateToTimeStamp


class rentalDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('./app/database/QuarrieRental.db')
        self.c = self.conn.cursor()

    def printQuery(self, sql_query):
        print("")
        df = pd.read_sql_query(sql_query,
                               self.conn,
                               index_col=None)
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("No items found")
            return(None)
        print("")
        return (df)

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
        dates = termLookup(term)
        for i in range(0, 4):
            date = dates[i]
            sql_query = """INSERT INTO
                        rent (user_id, room_id, date, paid)
                        VALUES({}, '{}', '{}', {})"""\
                        .format(user_id, room_id, date, 0)
            self.c.execute(sql_query)
        self.conn.commit()

    def printTenantList(self):
        self.printQuery(
            """ SELECT user_id, name, email
            FROM tenants """
        )

    def printAvailableRooms(self, term):
        timestamp = dateToTimeStamp(term)
        rooms = self.getQuery(
              """ SELECT rooms.room_id
              FROM rooms
              WHERE rooms.rentable = 1
              AND rooms.room_id not in (
              SELECT room_id from rent
              WHERE date='{}')""".format(timestamp))
        print(', '.join([item[0] for item in rooms]))

    def printTenantsByTerm(self, term):
        timestamp = dateToTimeStamp(term)
        self.printQuery(
            """ SELECT tenants.user_id, tenants.name,
            rent.room_id, tenants.email
            FROM rent
            INNER JOIN tenants
            ON tenants.user_id = rent.user_id
            WHERE rent.date='{}'
            ORDER BY rent.room_id
            """.format(timestamp))

    def printTenantsRentStatus(self, month):
        timestamp = dateToTimeStamp(month)
        options = self.printQuery(
          """ SELECT tenants.user_id, tenants.name,
          rent.room_id, rent.paid
          FROM rent
          INNER JOIN tenants
          ON tenants.user_id = rent.user_id
          WHERE rent.date='{}'
          ORDER BY rent.room_id
          """.format(timestamp))
        return options

    def recordRentPayment(self, user_id, month):
        timestamp = dateToTimeStamp(month)
        update_sql = """UPDATE rent
                SET paid = 1
                WHERE user_id={}
                AND date='{}'""".format(user_id, timestamp)
        self.updateQuery(update_sql)

    def __del__(self):
        self.conn.close()
