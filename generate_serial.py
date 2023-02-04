from datetime import datetime

daily_count = 0


def new_serial():
    global daily_count
    daily_count = daily_count + 1
    serial_number = datetime.now().strftime('%y%m%d') + str(daily_count).zfill(4) + 'W'
    return serial_number.encode()


if __name__ == '__main__':
    print("Running new_serial() test.")

    for s in range(25):
        print(new_serial())
