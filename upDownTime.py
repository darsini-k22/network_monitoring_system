import socket
import time
import datetime
import os
import sys
import subprocess
import datetime as dt
from pythonping import ping
import datetime as dt

LOG_FNAME = "network.log"
FILE = os.path.join(os.getcwd(), LOG_FNAME)


def get_computer_info():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    with open(FILE, "a") as file:
        file.write("\n")
        file.write(hostname + "\n" + IPAddr + "\n")


def get_router_name():
    results = subprocess.check_output(["netsh", "wlan", "show", "network"])
    results = results.decode("ascii")
    results = results.replace("\r", "")
    ls = results.split("\n")
    ls = ls[4:]
    ssids = []
    x = 0
    while x < len(ls):
        if x % 5 == 0:
            ssids.append(ls[x])
        x += 1
        return (ssids)


def available_networks():
    nw = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    decode_nw = nw.decode('ascii')
    return(decode_nw)


def send_ping_request(host="1.1.1.1", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

    except OSError as error:
        return False
    else:
        s.close()
        return True


def write_permission_check():
    try:
        with open(FILE, "a") as file:
            pass
    except OSError as error:
        print("Log file creation failed")
        sys.exit()
    finally:
        pass


def calculate_time(start, stop):
    time_difference = stop - start
    seconds = float(str(time_difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def mon_net_connection(ping_freq=2):
    monitor_start_time = datetime.datetime.now()
    get_computer_info()
    print('Visible networks ', available_networks())
    print("You have connected to the device:", get_router_name())

    with open(FILE, "a") as file:
        file.write("\n")
        file.write('Your device: ' + str(get_computer_info()) + "\n" +
                   'Visible networks: ' + str(available_networks()) + "\n" +
                   'Currently connected to: ' + str(get_router_name()))

    motd = "Network connection monitoring started at : " + str(
        monitor_start_time).split(".")[0] + " Sending ping request in " + str(
            ping_freq) + " seconds"
    print(motd)

    with open(FILE, "a") as file:
        file.write("\n")
        file.write(motd + "\n")
    while True:
        if send_ping_request():
            time.sleep(ping_freq)
        else:
            down_time = datetime.datetime.now()
            fail_msg = "Network connection unavailable at:" + str(
                down_time).split(".")[0]
            print(fail_msg)
            with open(FILE, "a") as file:
                file.write(fail_msg + "\n")
                i = 0
            while not send_ping_request():
                time.sleep(1)
                i += 1
                if i >= 3600:
                    i = 0
                    now = datetime.datetime.now()
                    continous_message = "Network Unavailability Persistant at: " + str(
                        now).split(".")[0]
                    print(continous_message)
                    with open(FILE, "a") as file:
                        file.write(continous_message + "\n")
            up_time = datetime.datetime.now()
            uptime_message = "Network Connectivity Restored at: " + str(
                up_time).split(".")[0]

            down_time = calculate_time(down_time, up_time)
            _m = "Network Connection was Unavailable for " + down_time
            print(uptime_message)
            print(_m)

            with open(FILE, "a") as file:
                file.write(uptime_message + "\n")
                file.write(_m + "\n")
            
        #return '\n'.join(map(lambda y: f"{y[0]}",uptime_message))


