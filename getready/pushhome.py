# -*- coding: UTF-8 -*-
import websocket
import os,io
import json
from  XunLeiDownloader import XunLeiDownloader


def on_open(ws):
	ws.send('hello')

def on_error(error):
	print error
	
def on_message(msg):
	##bt resource
	xld = XunLeiDownloader()
	xld.startDownload(msg)
def on_close(ws):
	ws.close()
		
if __name__ == '__main__':
	##debug
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://" + '0.0.0.0' + ":4000/",
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    try:
   	ws.run_forever()
    except:
   	ws.run_forever()
