# -*- coding: UTF-8 -*-
import io
import json
import os
from threading import Timer
import time as tt
import websocket
import subprocess


def on_open(ws):
	def HandleData():
		content = ''
		ps = subprocess.Popen("rm -rf output.json &&scrapy crawl quotes -o output.json",shell=True,stderr=subprocess.PIPE)
		ps.wait()
		if ps.returncode ==0:
			try:
				with open("output.json","r") as b:
					f = b.read()
					if len(f) > 0:
						for time in json.loads(f):
							if time['title']:
								content += time['title']+'|'+time['bt'] +','
						ws.send(content)
						b.close()
			except Exception as e:
				print e
		t=Timer(10,HandleData)
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
	ws = websocket.WebSocketApp("ws://" + '111.231.82.173' + ":5000/",
								on_error = on_error,
								on_close = on_close)
	
	ws.on_open = on_open
	
	try:
		ws.run_forever()
	except:
		ws.run_forever()

