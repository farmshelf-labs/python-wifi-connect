import config
import time
import subprocess as sp

CONF_FILE = '/tmp/dnsmasq.conf'

process = None

def start():
    global process
    config_file = """
bogus-priv
server=/localnet/{0}
local=/localnet/
address=/#/{0}
domain=localnet
interface={2}
dhcp-range={1}
dhcp-option=3,{0}
dhcp-option=6,{0}
dhcp-authoritative
bind-interfaces""".format(config.dnsmasq.gateway, config.dnsmasq.dhcp_range, config.hostapd.gateway)

    with open(CONF_FILE, 'w+') as f:
        f.write(config_file)

    process = sp.Popen(['dnsmasq', '-k', '-C', CONF_FILE], stdout=sp.PIPE)

def stop():
    process.kill()

def restart():
    stop()
    time.sleep(1)
    start()
