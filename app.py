from flask import Flask, redirect, url_for, render_template, request

#import scan_wifi
#import hostapd

app = Flask(__name__)

ssids = []

@app.route('/')
def root():
    return redirect(url_for('ssid_select'))

@app.route('/ssid_select', methods=['GET', 'POST'])
def ssid_select():
    if request.method == 'GET':
        return render_template('ssid_select.html', ssids=ssids)
    else:
        pass

def main():
    ssids = scan_wifi.scan()
    hostapd.start()
    dnsmasq.start()

if __name__ == '__main__':
    app.run()
    # main()
