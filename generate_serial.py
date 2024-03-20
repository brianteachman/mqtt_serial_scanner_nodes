from datetime import datetime
import json

LOCATION = 'B'
TYPE = 'M'
LINE = '04'

daily_count = 0

new_day = False


def new_serial():
    """
    Format: YYMMDDLTLNXXXX

    Where:
        YY = Year
        MM = Month
        DD = Day
        L = Location (ex, B = Burlington)
        T = Type (M = Module, C = Cell)
        LN = Line Number (ex, 04)
        XXXX = Daily Product Count

    Example: 240318BM040072
    """
    _check_last_serial_data()
    now = datetime.now()
    global daily_count
    daily_count = daily_count + 1
    serial_number = now.strftime('%y%m%d') + LOCATION + TYPE + LINE + str(daily_count).zfill(4)
    _persist(daily_count, now.strftime('%y%m%d'), now.strftime('%H:%M'))
    return serial_number

def _check_last_serial_data():
    global daily_count
    data = _fetch_last()
    if data["lastid_date"] < datetime.now().strftime('%y%m%d'):
        daily_count = 0000
    elif data["lastid"] > 0 and daily_count == 0:
        daily_count = data["lastid"]
    # print(data)

def _fetch_last():
    with open("./data/last_serial_data.json", "r") as read_file:
        data = json.load(read_file)
    return data

def _persist(id, last_date, last_time):
    data = {
        "lastid": id,
        "lastid_date": last_date,
        "lastid_time": last_time
    }
    with open("./data/last_serial_data.json", "w") as write_file:
        json.dump(data, write_file)


if __name__ == '__main__':
    print("Running new_serial() test.")

    for s in range(25):
        print(new_serial())
