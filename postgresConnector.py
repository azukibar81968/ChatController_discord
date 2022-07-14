import psycopg2
import os
import random

class postgres_connecter:
    def __init__(self, database, user, password, host):
        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = 5432

    def _getConnection(self):

        connection = psycopg2.connect(
            database = self._database,
            user = self._user,
            password = self._password,
            host = self._host,
            port = self._port
        )
        return connection

    def select(self, target, table, where): #安全ではない！SQLインジェクションでボコられます
        if len(target) == 0 or table == "":
            return
        sql = ["SELECT"]
        sql.append(" ,".join(target))
        sql.append("FROM")
        sql.append(", ".join(table))
        sql.append(self._getWherePhrase(where))
        # if where != None and len(where) == 2:
        #     sql.append("WHERE ")
        #     sql.append("=".join(where))
        # elif where != None and len(where) == 3:
        #     sql.append("WHERE ")
        #     sql.append(where[2].join(where[0:2]))

        sql.append(";")
        query = " ".join(sql)

        rows = []
        #print("query = " + query)
        with self._getConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        return rows

    def insert(self, data, table):#安全ではない！SQLインジェクションでボコられます
        if len(table) == 0 or table == "":
            return
        
        key = []
        value = []
        for t in data:
            key.append(t[0])
            value.append(t[1])
        key_joined = ", ".join(key)
        value_joined = ", ".join(value)
        
        sql = ["INSERT", "INTO"]
        sql.append(table)
        sql.append("(")
        sql.append(key_joined)
        sql.append(") VALUES (")
        sql.append(value_joined)
        sql.append(");")
        query = " ".join(sql)

        print("query = " + query)   
        with self._getConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
            conn.commit()


    def set(self, target, table, value, where):
        if len(table) == 0 or table == "":
            return
        
        sql = ["UPDATE"]
        sql.append(table)
        sql.append("SET")
        sql.append(target)
        sql.append("=")
        sql.append(value)
        sql.append(self._getWherePhrase(where))

        query = " ".join(sql)

        print("query = " + query)   
        with self._getConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
            conn.commit()


    def _getWherePhrase(self, where):
        sql = []

        if where != None and len(where) == 2:
            sql.append("WHERE ")
            sql.append("=".join(where))
        elif where != None and len(where) == 3:
            sql.append("WHERE ")
            sql.append(where[2].join(where[0:2]))

        return " ".join(sql)


if __name__ == "__main__":


    con = postgres_connecter(
        'postgres',
        'postgres',
        'passw0rd',
        '0.0.0.0',
    )

    # rows = con.select("city", "temp_lo", "prcp", "date", table = ["weather"], where = ("city", "'Nagoya'", "="))    
    # for row in rows:
    #     print(row)

    # con.insert(
    #     ("city" , "'Nagoya'"),
    #     ("temp_lo" , str(40)),
    #     ("temp_hi", str(40 + 30*random.random())),
    #     ("prcp", str(random.random())),
    #     ("date", "'1999-11-30'"),
    #     table = "weather"
    # )

