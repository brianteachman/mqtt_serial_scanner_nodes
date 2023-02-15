# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
import pyodbc
import contextlib
from dotenv import dotenv_values


class Database:

    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.last_serial_number = 0
        self.error = False

    @contextlib.contextmanager
    def _connect(self):
        # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'+
                            f'SERVER={self.server};DATABASE={self.database};'+
                            'ENCRYPT=no;trusted_connection=yes;'+
                            f'UID={self.username};'+
                            f'PWD={self.password}')
        try:
            yield conn
        finally:
            conn.close()

    def _query(self, statement):
        with self._connect() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(statement)
                return list(cursor.fetchall())
            finally:
                cursor.close()
    
    def _execute(self, statement):
        with self._connect() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(statement)
                result_set = list(cursor.fetchall())
                cursor.commit()
                return result_set
            finally:
                cursor.close()

    def add_panel(self, serial_number, carrier_number):
        serial_number = serial_number.strip()
        stmt = f"EXEC spNewSerial '{serial_number}', {carrier_number}"
        result_set = self._execute(stmt)
        self.last_serial_number = serial_number
        print(result_set)

    def get_panel(self, serial_number):
        statement = "SELECT SerialNumber,SerialNumber_tstamp,Engraved,Rework FROM serialtracker.dbo.serials WHERE SerialNumber LIKE '%s'" % serial_number
        result_set = self._query(statement)
        print(result_set)

    # def get_serials(self, start, end):
    #     statement = "SELECT SerialNumber,SerialNumber_tstamp,Laminator,LamPosition FROM [serialtracker].[dbo].serials WHERE [SerialNumber_tstamp] BETWEEN %s AND %s", (start, end)
    #     result_set = self.query(statement)
    #     print(result_set)


if __name__ == '__main__':
    print("Running Database test.")

    c = dotenv_values()

    db = Database(c["DB_SERVER"], c["DB_NAME"], c["DB_USERNAME"], c["DB_PASSWD"])
    # conn = db._connect()
    # cursor = conn.cursor()

    # cursor.execute("exec spNewSerial @SerialNumber = '2302130001W', @Carrier = 5;")
    # cursor.execute("exec spNewSerial @SerialNumber = '2302030104W', @Carrier = 2;")
    # cursor.execute("exec spLaminated '2302030104W', 'LAM1';")
    # cursor.commit()

    # cursor.execute("select * from serials;")
    # row = cursor.fetchone()  
    # while row:  
    #     print(str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + " " + str(row[5]))     
    #     row = cursor.fetchone()  
    
    # cursor.close()
    # conn.close()

    # for panel in db._query("select * from serials;"):
        # print(str(panel))

    db.add_panel("2302135001W", 1)
    db.get_panel("2302135001W")

