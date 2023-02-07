# import pymssql
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import dotenv_values


class Database:

    def __init__(self, connection_string):
        self.db_address = connection_string
        self.last_serial_number = 0
        self.error = False

    def query(self, statement):
        db = create_engine(self.db_address)
        connection = db.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(statement)
            result_set = list(cursor.fetchall())
            cursor.close()
            connection.commit()
            return result_set
        except SQLAlchemyError as er:
            print(str(er.__dict__['orig']))
            return []
        finally:
            connection.close()

    def update_panel(self, serial_number, station):
        serial_number = serial_number.strip()
        # stmt = f"EXEC spCheckpoint @SerialNumber = '{serial_number}', @MachineName = '{station}'"
        stmt = f"EXEC spCheckpoint '{serial_number}', '{station}'"
        print(stmt)
        result_set = self.query(stmt)
        self.last_serial_number = serial_number
        print(result_set)

    # def get_panel(self, serial_number):
    #     statement = "SELECT [SerialNumber],[StartDate],[StartTime],[Engraved],[Rework] FROM [serialtracker].[dbo].serials WHERE [SerialNumber] like '%s'" % serial_number
    #     result_set = self.query(statement)
    #     print(result_set)

    # def get_serials(self, start, end):
    #     statement = "SELECT SerialNumber,StartDate,StartTime,Laminator,LamPosition,Trimmer FROM [serialtracker].[dbo].serials WHERE [StartDate] BETWEEN %s AND %s", (start, end)
    #     result_set = self.query(statement)
    #     print(result_set)


if __name__ == '__main__':
    print("Running Database test.")

    c = dotenv_values()

    db = Database(c["DB_ADDRESS"])
    db.update_panel("2302030001W", "Serial Printer")
