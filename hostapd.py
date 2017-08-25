import config
import subprocess as sp

CONF_FILE = '/tmp/hostapd.conf'

process = None

def start():
    conf_file = """
interface={}
ssid={}
psk={}
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
""".format(config.hostapd['iface'], config.hostapd['ssid'], config.hostapd['psk'])

    with open(CONF_FILE, 'w+') as f:
        f.write(conf_file)

    process = sp.Popen(['hostapd', CONF_FILE], stdout=sp.PIPE)
