# -*- coding: UTF-8 -*-
import websocket
import os,io
import json
from threading import Timer


class Saber:
    def __init__(self):
	pass

    def on_open(self,ws):
		def HandleData():
			os.system("rm -rf output.json;scrapy crawl quotes -o  output.json")
			content = ''
			f = json.load(io.open("output.json", encoding='utf-8'))
			for time in f:
				if time['time'].encode('utf-8').find("今日") > -1:
					if len(time['product']) > 0:
						for p in time['product']:
							content += p.encode('utf-8') + '\n'
						ws.send(content)
			t=Timer(3,HandleData)
			t.start()
		HandleData()

    def on_error(self,error):
	print error

    def on_close(self,ws):
	ws.close()
		
if __name__ == '__main__':
    saber = Saber()
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://" + 'localhost' + ":5000/",
                              on_error = saber.on_error,
                              on_close = saber.on_close)

    ws.on_open = saber.on_open
    try:
   	ws.run_forever()
    except:
   	ws.run_forever()
