# Serial Number Backsheet Printer Controller

This project tells a Keyence MK-G1000 Inkjet printer what the next serial number to write next is, then associates the newly created serial numbers to the carriers the module was transported on during production and saves that information to a tracking database.

## Install

#### Install dependencies 

    > pip install -r requirements.txt


#### Create .env file

    LINE = 5  # Line Number
    LOCATION = 2  # Plant Location

    RELAY_PORT = "YOUR_COMPORT"

    DB_SERVER = 'YOUR_SERVER_ADDRESS'
    DB_NAME = 'YOUR_DATABASE_NAME'
    DB_USERNAME = 'YOUR_USERNAME'
    DB_PASSWD = 'YOUR_PASSWORD'

    MKG1000_PRINTER_IP = 'IP_ADDRESS'
    MKG1000_PRINTER_PORT = 9004

    SR1000_SCANNER_IP = "IP_ADDRESS"
    SR1000_SCANNER_PORT = 9004