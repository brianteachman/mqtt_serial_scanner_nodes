import sqlalchemy as db
from sqlalchemy import create_engine


class SQL:

    def __init__(self, connection_string):
        self.db_address = connection_string
        self.serial_number = None
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
        except:
            return []
        finally:
            connection.close()

    def update_panel(self, serialno, station):
        result_set = self.query("EXEC spCheckpoint "+serialno.strip()+", "+station)
        print(result_set)

    # def get_panel(self, serialno):
    #     statement = "SELECT [SerialNo],[StartDate],[StartTime],[Engraved],[Rework] FROM [silfaberp].[dbo].serials WHERE [SerialNo] like '%s'" % serialno
    #     result_set = self.query(statement)
    #     print(result_set)

    # def get_serials(self, start, end):
    #     statement = "SELECT SerialNo,StartDate,StartTime,Laminator,LamPosition,Trimmer FROM [silfaberp].[dbo].serials WHERE [StartDate] BETWEEN %s AND %s", (start, end)
    #     result_set = self.query(statement)
    #     print(result_set)


if __name__ == '__main__':
    print("Running SQL test.")

    sql = SQL()
    sql.update_panel('2302030001W', 'Serial Printer')
