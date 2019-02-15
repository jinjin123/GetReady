# -*- coding: UTF-8 -*-
import io
import json
import os
from threading import Timer
import time as tt
import websocket


def on_open(ws):
	def HandleData():
		os.system("rm -rf output.json;scrapy crawl quotes -o  output.json")
		content = ''
		tt.sleep(1)
		f = json.load(io.open("output.json", encoding='utf-8'))
		for time in f:
			if time['title']:
				content += time['title']+'|'+time['bt'] +','
		ws.send(content)
		t=Timer(1800,HandleData)
		t.start()
	HandleData()

def on_error(ws,error):
	print error

def on_close(ws):
	try:
		# ws.run_forever()
		pass
	except websocket.WebSocketConnectionClosedException as e:
		print e
		ws.run_forever()
	

if __name__ == '__main__':
	#debug
	websocket.enableTrace(False)
	ws = websocket.WebSocketApp("ws://" + '0.0.0.0 + ":5000/",
								on_error = on_error,
								on_close = on_close)
	
	ws.on_open = on_open
	
	try:
		ws.run_forever()
	except:
		ws.run_forever()

