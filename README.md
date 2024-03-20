# Serial Number Backsheet Printer Controller

This project tells a Keyence MK-G1000 Inkjet printer what the next serial number to write next is, then associates the newly created serial numbers to the carriers the module was transported on during production and saves that information to a tracking database.

## Install

#### Install dependencies 

    > pip install -r requirements.txt


#### Create .env file

    LINE = 4  # MWT
    LOCATION = "B"
    PRODUCT_TYPE = 'M_OR_C'
    MACHINE_NAME = 'MACHINE_NAME'

    RELAY_PORT = "YOUR_COMPORT"

    DB_SERVER = 'YOUR_SERVER_ADDRESS'
    DB_NAME = 'YOUR_DATABASE_NAME'
    DB_USERNAME = 'YOUR_USERNAME'
    DB_PASSWD = 'YOUR_PASSWORD'

    MKG1000_PRINTER_IP = 'IP_ADDRESS'
    MKG1000_PRINTER_PORT = 9004

    SR1000_SCANNER_IP = "IP_ADDRESS"
    SR1000_SCANNER_PORT = 9004


## Create Windows Service

    > python service.py --startup=auto install
    
    > python "C:\Program Files\Python311\Scripts\pywin32_postinstall.py" -install

    > python service.py remove


---

nssm.exe install [SERVICE NAME] [C:\PATH\TO\PYTHON\INTERPRETER.exe] [C:\PATH\TO\SCRIPT.py]

nssm.exe install SerialPrinterController "C:\Program Files\Python311\python.exe" C:\bin\serial_controller\main.py

Set dependency:

sc config [service name] depend= <Dependencies(separated by / (forward slash))>

sc config SerialPrinterController depend="MSSQL$SQLEXPRESS"