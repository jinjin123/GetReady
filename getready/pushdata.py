# -*- coding: UTF-8 -*-
import websocket
import os,io
import json
from threading import Timer


def on_open(ws):
	def HandleData():
		os.system("rm -rf output.json;scrapy crawl quotes -o  output.json")
		content = ''
		f = json.load(io.open("output.json", encoding='utf-8'))
		for time in f:
			#if time['time'].encode('utf-8').find("今日") > -1:
			if time['title']:
					# for p in time['product']:
				content += time['title'].encode('utf-8') + ','
			ws.send(content)
		t=Timer(1800,HandleData)
		t.start()
	HandleData()

def on_error(error):
	print error

def on_close(ws):
	ws.close()
		
if __name__ == '__main__':
	##debug
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://" + '0.0.0.0' + ":5000/",
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    try:
   	ws.run_forever()
    except:
   	ws.run_forever()
