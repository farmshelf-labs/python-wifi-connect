from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import time

import scan_wifi
import hostapd
import dnsmasq
import networkconf

app = Flask(__name__)

ssids = []

@app.route('/ssid_select', methods=['GET', 'POST'])
def ssid_select():
    if request.method == 'GET':
        return render_template('ssid_select.html', ssids=ssids)
    else:
        ssid = request.form['ssid']
        psk = request.form['psk']
        networkconf.save_config(ssid, psk)
        if networkconf.conn_active():
            shutdown_server()
            return 'OK'
        else:
            networkconf.stop_nm()
            networkconf.set_iface()
            hostapd.restart()
            dnsmasq.restart()

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
    if networkconf.conn_active():
        print('Network is configured, continuing start up')
    else:
        main()
        app.run(host="0.0.0.0", port=80)
