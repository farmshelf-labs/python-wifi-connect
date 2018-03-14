import config
import random
import time
import subprocess as sp

CONF_FILE = '/tmp/hostapd.conf'

process = None

def start():
    global process
    if config.hostapd.ssid_randomize:
        ssid = config.hostapd.ssid + '_' + str(random.randint(1, 1000))
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

def stop():
    process.kill()

def restart():
    stop()
    time.sleep(1)
    start()
