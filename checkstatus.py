import subprocess
from NUTClient import NUTClient
from config import *

if __name__ == '__main__':
    client = NUTClient(server, 3493, debug=False)
    try:
        client.connect()
        client.login('nutuser', 'nutpwd!')
        battery_charge = client.get_var(upsname, 'battery.charge')
        ups_status = client.get_var(upsname, 'ups.status')
        if battery_charge and ups_status != "OL":
            try:
                battery_charge_int = int(battery_charge)
                if client.debug:
                    print('Battery charge:', battery_charge_int)
                if battery_charge_int < battery_threshold:
                    print(f"Battery charge is below {battery_threshold}, initiating shutdown...")
                    subprocess.run(['sudo', 'halt', '-p'], check=True)
            except ValueError:
                if client.debug == True:
                    print(f'Error converting {battery_charge} to integer.')
    finally:
        client.close()