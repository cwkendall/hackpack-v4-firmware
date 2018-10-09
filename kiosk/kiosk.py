import os
import sys
import subprocess
import threading
import time

import webview
import paho.mqtt.client as mqtt


_firmware_path = '/home/pi/firmware'

sys.path.append(_firmware_path + '/drivers/leds/lib_python')

from led_client import LEDClient


class Api:
    def __init__(self):
        self.default_variable = False

    def show_lights(self, params):
        msg = ''

	try:
            lightbar = LEDClient()
            lightbar.pattern('led_scanner')

            msg = 'Successfully displayed lights'

        except Error as e:
            msg = 'Could not activate lights: ' % e.message

        r = {
            'status': 200,
            'message': str(msg)
        }

        return r

_threads = []
_fileMonitorActive = True
_current_url = 'http://hackpack-hoppo.herokuapp.com'


def file_monitor():
    while _fileMonitorActive:
        time.sleep(5)
        print 'Checking file..'

        file_path = '/home/pi/config.txt'

        file_exists = os.path.isfile(file_path)

        print('Current url: ' + _current_url)

        if file_exists:
            f = open('/home/pi/config.txt', 'r')

            if f.mode == 'r':
                requested_url = f.read()

                if requested_url != _current_url:
                    _current_url = requested_url
                    webview.load_url(contents)

if __name__ == '__main__':
    t = threading.Thread(target=file_monitor)
    _threads.append(t)
    t.start()

    api = Api()

    webview.create_window(
        "",
        #url="file:///home/pi/firmware/system_api/snake.htm",
        #url="../../hoppo/index.htm",
        url=_current_url,
	#url="http://frankpoth.info/content/pop-vlog/javascript/2017/009-control/control.html",
        width=640,
        height=480,
        fullscreen=True,
        text_select=False,

        js_api=api
    )