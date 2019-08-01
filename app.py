from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import time

import scan_wifi
import hostapd
import dnsmasq
import networkconf
from util import write_lcd, release_lcd

app = Flask(__name__)

ssids = []

@app.route('/ssid_select', methods=['GET', 'POST'])
def ssid_select():
    if request.method == 'GET':
        return render_template('ssid_select.html', ssids=ssids)
    else:
        if 'ssid' in request.form:
            ssid = request.form['ssid'].strip()
        elif 'ssid-hidden' in request.form:
            ssid = request.form['ssid-hidden'].strip()
        else: ssid = 'NONE'

        psk = request.form['psk'].strip()
        hidden = 'hidden' in request.form

        write_lcd('Trying to connect:\n{}'.format(ssid))
        ret = networkconf.save_config(ssid, psk, hidden)
        if ret and networkconf.conn_active():
            write_lcd('Success! Connected:\n{}'.format(ssid))

            shutdown_server()
            time.sleep(4)
            return 'OK'
        else:
            networkconf.stop_nm()
            networkconf.set_iface()
            hostapd.restart()
            dnsmasq.restart()
            write_lcd('Connection failed:\nTrying again'.format(ssid))

            return redirect(url_for('ssid_select'))

@app.route('/public/<path:filepath>')
def static_file(filepath):
    return send_from_directory('public', filepath)

@app.route('/<path:dummy>')
def root(dummy):
    return redirect('http://farmshelf-setup.com' + url_for('ssid_select'))

def shutdown_server():
    print('Shutting down')
    hostapd.stop()
    dnsmasq.stop()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def main():
    global ssids
    networkconf.stop_nm()
    time.sleep(2)
    networkconf.set_iface()
    ssids = scan_wifi.scan()
    hostapd.start()
    dnsmasq.start()

if __name__ == '__main__':
    try:
        main()
        app.run(host="0.0.0.0", port=80)
    finally:
        release_lcd()
        networkconf.start_nm()
