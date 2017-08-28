import config
import time
import dbus
import uuid
import subprocess as sp

device = None
conn = None

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

DBUS_NETWORK_MANAGER = 'NetworkManager.service'
CONNECTION_ID        = 'fshelf-wifi'
CONNECTION_UUID      = '3a5538c8-4bab-465e-837d-80ccf8bf1e48'

def save_config(ssid, psk):
    manager.StartUnit(DBUS_NETWORK_MANAGER, 'fail')
    time.sleep(2)

    import NetworkManager as nm
    reload(nm)

    for dev in nm.NetworkManager.GetDevices():
        if dev.DeviceType == nm.NM_DEVICE_TYPE_WIFI:
            device = dev
            break

    conn = {
        '802-11-wireless': {
             'mode': 'infrastructure',
             'security': '802-11-wireless-security',
             'ssid': str(ssid)
             },
        '802-11-wireless-security': {
            'auth-alg': 'open',
            'key-mgmt': 'wpa-psk',
            'psk': str(psk)
            },
        'connection': {
            'id': CONNECTION_ID,
            'type': '802-11-wireless',
            'uuid': str(uuid.uuid4())
            },
        'ipv4': {'method': 'auto'},
        'ipv6': {'method': 'auto'}
    }

    conn = nm.Settings.AddConnection(conn)
    nm.NetworkManager.ActivateConnection(conn, device, "/")

def stop_nm():
    manager.StopUnit(DBUS_NETWORK_MANAGER, 'fail')

def set_iface():
    process = sp.Popen(['ifconfig', config.hostapd.iface, '{}/24'.format(config.dnsmasq.gateway), 'up'])
    process.wait()

def conn_active():
    # check active connection
    import NetworkManager as nm

    conns = list(filter(lambda c: c.Id == CONNECTION_ID, nm.NetworkManager.ActiveConnections))

    try:
        if len(conns) > 0:
            conn = conns[0]
            while conn.State == nm.NM_ACTIVE_CONNECTION_STATE_ACTIVATING: pass

            return conn.State == nm.NM_ACTIVE_CONNECTION_STATE_ACTIVATED
        else:
            return False
    except nm.ObjectVanished:
        return False

    return len(conns) > 0
