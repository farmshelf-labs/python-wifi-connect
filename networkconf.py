import config
import time
import dbus
import uuid
from importlib import reload
import subprocess as sp

device = None
conn = None

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

DBUS_NETWORK_MANAGER = 'NetworkManager.service'
CONNECTION_ID        = 'fshelf-wifi'

def save_config(ssid, psk, hidden=False):
    manager.StartUnit(DBUS_NETWORK_MANAGER, 'fail')
    time.sleep(2)

    import NetworkManager as nm
    reload(nm)

    for dev in nm.NetworkManager.GetDevices():
        if dev.DeviceType == nm.NM_DEVICE_TYPE_WIFI and dev.Interface == config.hostapd.iface:
            device = dev
            break

    keymgmt = ('none' if len(psk) == 0 else 'wpa-psk')

    _uuid = str(uuid.uuid4())
    conn = {
        '802-11-wireless': {
             'mode': 'infrastructure',
             'security': '802-11-wireless-security',
             'ssid': str(ssid),
             'hidden': hidden
             },
        '802-11-wireless-security': {
            'auth-alg': 'open'
            },
        'connection': {
            'id': CONNECTION_ID + '-{}'.format(ssid),
            'type': '802-11-wireless',
            'uuid': _uuid
            },
        'ipv4': {'method': 'auto'},
        'ipv6': {'method': 'auto'}
    }

    if len(psk) > 0:
        conn['802-11-wireless-security']['key-mgmt'] = 'wpa-psk'
        conn['802-11-wireless-security']['psk'] = psk
    else:
        conn.pop('802-11-wireless-security')


    try:
        conn = nm.Settings.AddConnection(conn)
        conatmps = 5
        while conatmps > 0:
            try:
                nm.NetworkManager.ActivateConnection(conn, device, "/")
                return True
            except:
                conatmps -= 1
                time.sleep(0.5)
        return False
    except dbus.exceptions.DBusException:
        return False

def stop_nm():
    manager.StopUnit(DBUS_NETWORK_MANAGER, 'fail')
     #TODO wait for it to actually stop

def start_nm():
    manager.StartUnit(DBUS_NETWORK_MANAGER, 'fail')

def set_iface():
    process = sp.Popen(['ifconfig', config.hostapd.iface, '{}/24'.format(config.dnsmasq.gateway), 'up'])
    process.wait()

def conn_active():
    # check active connection
    import NetworkManager as nm

    conns = nm.NetworkManager.ActiveConnections

    try:
        if len(conns) > 0:
            for conn in conns:
                while conn.State == nm.NM_ACTIVE_CONNECTION_STATE_ACTIVATING: pass

                return conn.State == nm.NM_ACTIVE_CONNECTION_STATE_ACTIVATED
        else:
            return False
    except nm.ObjectVanished:
        return False

    return len(conns) > 0
