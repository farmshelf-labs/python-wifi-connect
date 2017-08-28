import config
import time
import subprocess as sp

CONF_FILE = '/tmp/hostapd.conf'

process = None

def start():
    global process
    conf_file = """
interface={}
ssid={}
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
""".format(config.hostapd.iface, config.hostapd.ssid)

    with open(CONF_FILE, 'w+') as f:
        f.write(conf_file)

    process = sp.Popen(['hostapd', CONF_FILE], stdout=sp.PIPE, stderr=sp.PIPE)

def stop():
    process.kill()

def restart():
    stop()
    time.sleep(1)
    start()
