from dotenv import dotenv_values
from sr1000 import Scanner
from generate_serial import new_serial

carrier_data = []
carrier_ids = []
serials = []

last_count = 0

def track(serial_number=None, carrier_number=None):
    global last_count, carrier_data, carrier_ids, serials

    if serial_number:
        serials.append(serial_number)

    if carrier_number:
        carrier_ids.append(carrier_number)

    if len(carrier_ids) is len(serials):
        carrier_data.append((serials.pop(), carrier_ids.pop()))
        last_count = last_count + 1
        return carrier_data.pop()


if __name__ == '__main__':
    print("Testing Carrier Scanning")

    # c = dotenv_values()
    # s = Scanner(c["SR1000_SCANNER_IP"], c["SR1000_SCANNER_PORT"])
    # s.read_code()
    
    for i in range(5):
        # track(serial_number=new_serial(), carrier_number=i+1)
        data = track(serial_number=new_serial())
        if data:
            print(data)
        data = track(carrier_number=i+1)
        if data:
            print(data)

    # print(carrier_ids)
    # print(serials)
    print(carrier_data)
