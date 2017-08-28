import config
import re
import subprocess as sp

def scan():
    ssids = set()
    ssid_re = '.*SSID: (.*)'
    signal_re = 'signal: ([-+]?\d*\.\d+|\d+)'

    process = sp.Popen(['iw', config.hostapd.iface, 'scan', 'ap-force'], stdout=sp.PIPE)
    stdout, _ = process.communicate()
    for line in stdout.split('\n'):
        ssid_mt = re.search(ssid_re, line)
        signal_mt = re.search(signal_re, line)
        if ssid_mt:
            ssid = ssid_mt.groups()[0]
            if ssid:
                ssids.add(ssid)



    return sorted(list(ssids))
