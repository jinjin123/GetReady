# -*- coding: UTF-8 -*-
import io
import json
import os
import subprocess
from threading import Timer
import websocket


def on_open(ws):
	def HandleData():
		content = ''
		ps = subprocess.Popen("rm -rf dm.json;scrapy crawl dm -o  dm.json",shell=True,stderr=subprocess.PIPE)
		ps.wait()
		if ps.returncode ==0:
			try:
				with open("dm.json","r")as b:
					f = json.loads(b.read())
					for time in f:
						if time['title']:
							content += time['title']+'|'+time['bt'] +','
				ws.send(content)
				b.close()
			except Exception as e:
				print e
		t=Timer(3600,HandleData)
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
	ws = websocket.WebSocketApp("ws://" + '0.0.0.0' + ":5000/",
								on_error = on_error,
								on_close = on_close)
	
	ws.on_open = on_open
	
	try:
		ws.run_forever()
	except:
		ws.run_forever()

