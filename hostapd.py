import config
import random
import time
import os
import subprocess as sp

CONF_FILE = '/tmp/hostapd.conf'

process = None

MAX_ATTEMPTS = 5
attempts = 0

def start():
    global process
    global attempts
    if config.hostapd.ssid_randomize:
        addon = os.environ['RESIN_DEVICE_NAME_AT_INIT'] if 'RESIN_DEVICE_NAME_AT_INIT' in os.environ else str(random.randint(1, 1000))
        ssid = config.hostapd.ssid + '_' + addon
    else:
        ssid = config.hostapd.ssid

    conf_file = """
interface={}
ssid={}
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
""".format(config.hostapd.iface, ssid)

    with open(CONF_FILE, 'w+') as f:
        f.write(conf_file)

    process = sp.Popen(['hostapd', CONF_FILE], stdout=sp.PIPE, stderr=sp.PIPE)
    time.sleep(2)
    process.poll()
    if process.returncode:
        if attempts <= MAX_ATTEMPTS:
            restart()
            attempts += 1
        else:
            print("HOSTAPD: max attempts reached")

def stop():
    process.kill()

def restart():
    stop()
    time.sleep(1)
    start()
