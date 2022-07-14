import postgresConnector
import random

class SQLInterface:
    def __init__(self):
        self._con = postgresConnector.postgres_connecter(
            'postgres',
            'talkapi',
            'talkapiPass',
            '127.0.0.1',
        )


    def select(self, target, table, where): 
        return self._con.select(target, table = table, where = where)

    def insert(self, data, table):
        self._con.insert(data,table = table)
        return

    def set(self, target, table, value, where):
        self._con.set(target, table = table, value = value, where = where)



if __name__ == "__main__":


    con = SQLInterface()

    # rows = con.select(["city", "temp_lo", "prcp", "date"] , table = ["weather"], where = ("city", "'Nagoya'", "="))    
    # for row in rows:
    #     print(row)

    # con.insert(
    #     [
    #         ("city" , "'Nagoya'"),
    #         ("temp_lo" , str(40)),
    #         ("temp_hi", str(40 + 30*random.random())),
    #         ("prcp", str(random.random())),
    #         ("date", "'1999-11-30'")
    #     ],
    #     table = "weather"
    # )

    con.set(
        "checked",
        "weather",
        "false",
        ["id", "223"]
    )
