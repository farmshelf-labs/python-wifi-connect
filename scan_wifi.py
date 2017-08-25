import config

import NetworkManger as nm

def scan():
    ssids = []
    for dev in nm.NetworkManger.GetDevices():
        if dev.DeviceType != nm.NM_DEVICE_TYPE_WIFI:
            continue
        for ap in dev.GetAccessPoints():
            ssids.append(ap.Ssid, ap.Frequency, ap.Strength)

    return sorted(ssids, key=lambda s: s[2])
