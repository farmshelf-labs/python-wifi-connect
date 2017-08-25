try:
    import ConfigParser as parser
except ModuleNotFoundError:
    import configparser as parser

import os
from collections import namedtuple

CONF_FILE = os.environ('PYTHON_WIFI_CONNECT_CONF') if 'PYTHON_WIFI_CONNECT_CONF' in os.environ else './pwc.conf'

HOSTAPD_PROPS = ['iface', 'ssid', 'psk']
DNSMASQ_PROPS = ['gateway', 'dhcp_range']

config = parser.ConfigParser()
config.read(CONF_FILE)

configs = dict(config.items('CONFIGS'))

hostapd = namedtuple('hostapd', HOSTAPD_PROPS)
for prop in HOSTAPD_PROPS:
    env_var = 'HOSTAPD_{}'.format(prop.upper())
    try:
        prop_val = os.environ[env_var] if env_var in os.environ else configs[prop]
        setattr(hostapd, prop, prop_val)
    except KeyError:
        raise KeyError('No value for {} in config file or environment'.format(prop))

dnsmasq = namedtuple('dnsmasq', DNSMASQ_PROPS)
for prop in DNSMASQ_PROPS:
    env_var = 'DNSMASQ_{}'.format(prop.upper())
    try:
        prop_val = os.environ[env_var] if env_var in os.environ else configs[prop]
        setattr(dnsmasq, prop, prop_val)
    except KeyError:
        raise KeyError('No value for {} in config file or environment'.format(prop))
