import os
import fcntl

LCD_FILE = '/tmp/farmware-lcdmsg'
LCD_LOCK = open('/tmp/farmware-lcdmsg.lock', 'w+')

def write_lcd(msg):
    try:
        fcntl.flock(LCD_LOCK, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return False

    with open(LCD_FILE, 'w+') as ff:
        ff.write(msg)
        return True

def release_lcd():
    if os.path.exists(LCD_FILE): os.remove(LCD_FILE)
    fcntl.flock(LCD_LOCK, fcntl.LOCK_UN)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
