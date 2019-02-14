###Descripe
Python3.5
just notice any cartorn were ready let me know  and  let my home PC download  .

###ALERT
the go lib websocket maxSize is 512,so when you send outsize data that websocket will close and not recv msg,
you need to  change /Users/wupeijin/go/src/gopkg.in/olahol/melody.v1/config.go 		MaxMessageSize:    4096,
		MessageBufferSize: 4096, and rebuild your go program


###Step: Mac
pip install scrapy

cd ${project}
scrapy crawl quotes -o  output.json

####Step: Mac
pip install virtualenv
virtualenv venv/bin/activate
pip3.5 install  pyqt5

start websocket server
./chat &

###schema link
(https://github.com/jinjin123/GetReady/blob/master/cartoon.pdf)

####demo
![demo](https://github.com/jinjin123/GetReady/blob/master/mcdemo2.png)
![demo](https://github.com/jinjin123/GetReady/blob/master/macclient.png)
![demo](https://github.com/jinjin123/GetReady/blob/master/recivedmsg.png)

#client
source venv/bin/activate
python ScmGUI.py

###[ home windows7 python2.7 pywin32  and code ]
(https://github.com/jinjin123/VirtualOpeation)

########

```
spider ioop get the  website  cartoon start time
            |
            |
            |
            |

go handle  spider data  push to socket channel to Mac

            |
            |
            |
            |
mac Pyqt5 socket daemon get the socket message then open window Notice me
```
