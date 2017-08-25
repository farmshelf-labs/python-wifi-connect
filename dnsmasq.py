import config
import subprocess as sp

CONF_FILE = '/tmp/dnsmasq.conf'

process = None

def start():
    config_file = """
bogus-priv
server=/localnet/{0}
local=/localnet/
address=/#/{0}
interface=wlan0
domain=localnet
dhcp-range={1}
dhcp-option=3,{0}
dhcp-option=6,{0}
dhcp-authoritative
bind-nterfaces""".format(config.dnsmasq.gateway, config.dnsmasq.dhcp_range)

    with open(CONF_FILE, 'w+') as f:
        f.write(config_file)

    process = sp.Popen(['dnsmasq', CONF_FILE], stdout=sp.PIPE)
