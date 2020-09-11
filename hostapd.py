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

    fsid = str(random.randint(1, 1000))
    try:
        with open('/data/config/FSID.txt', 'r') as ff:
            fsid = ff.read().strip()
    except:
        fsid = str(random.randint(1, 1000))


    if config.hostapd.ssid_randomize:
        ssid = config.hostapd.ssid + '_' + fsid
    else:
        ssid = config.hostapd.ssid

    conf_file = """
interface={}
ssid={}
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
logger_syslog=-1
logger_syslog_level=4
logger_stdout=-1
logger_stdout_level=4
""".format(config.hostapd.iface, ssid)

    with open(CONF_FILE, 'w+') as f:
        f.write(conf_file)

    with open('/tmp/farmware-lcdmsg', 'w+') as ff:
        ff.write('Broadcasting setup:\n{}'.format(ssid))

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
