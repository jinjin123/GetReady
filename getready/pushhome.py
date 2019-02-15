# -*- coding: UTF-8 -*-
import websocket
import os,io,sys,time
import win32gui
import win32api
import win32con
import win32clipboard
from ctypes import *
reload(sys)
sys.setdefaultencoding( "utf-8" )


def on_open(ws):
    xunleiExePath = r"D:\Thunder Network\Program\Thunder.exe"
    os.startfile(xunleiExePath)
def on_error(ws,error):
    print error
                
def on_message(ws,message):
    ##bt resource
    print message
    startDownload(message)
    
def on_close(ws):
    ws.close()


def ctrlV(a=None):
    win32api.keybd_event(win32con.VK_CONTROL, 0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(ord('V'), 0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(ord('V'), 0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.1)
    win32api.keybd_event(win32con.VK_CONTROL, 0,win32con.KEYEVENTF_KEYUP,0)

def leftMouseClick(posX, posY):
    win32api.SetCursorPos([posX, posY])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    time.sleep(0.1)

def startDownload(downloadUrls):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, "")
    win32clipboard.CloseClipboard()

    #os.startfile(xunleiExePath)
    wndMain = None
    while not wndMain:
        time.sleep(1)
        wndMain = win32gui.FindWindow(None, u"迅雷")
        #print wndMain
        #main window point
    wndMainRect = win32gui.GetWindowRect(wndMain)

    leftMouseClick(wndMainRect[0]+35, wndMainRect[1]+100)
    time.sleep(0.1)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    #win32clipboard.SetClipboardData(win32con.CF_TEXT, downloadUrls.decode('utf-8').encode('gbk'))
    win32clipboard.SetClipboardData(win32con.CF_TEXT, downloadUrls)
    win32clipboard.CloseClipboard()

    wndCreateDownload = win32gui.FindWindow(None, u"迅雷")
    #print wndCreateDownload
    ### open the download window and cv resource in it
    #if wndCreateDownload:
    wndCreateDownloadRect = win32gui.GetWindowRect(wndCreateDownload)
    leftMouseClick(wndCreateDownloadRect[0]+60, wndCreateDownloadRect[1]+70)
    ctrlV(None)
    #leftMouseClick(wndCreateDownloadRect[2]+100, wndCreateDownloadRect[3]-100)
    ##after window show then cv resource
    time.sleep(0.5)
    c = gdi32.GetPixel(hdc,wndCreateDownloadRect[0] + 150,wndCreateDownloadRect[1]+ 215)
    chex = hex(c)
    print chex
    #win32api.SetCursorPos([wndCreateDownloadRect[0] + 150,wndCreateDownloadRect[1]+ 215])
    leftMouseClick(wndCreateDownloadRect[1]+850, wndCreateDownloadRect[3]-280)
    if ((chex == "0xfefefe") or (chex == "0xffffff") or(chex == "0xfff4e3")):
        #开始下载
        time.sleep(3)
        print 'downlaod ...'
        leftMouseClick(wndCreateDownloadRect[1]+850, wndCreateDownloadRect[3]-150)
    else:
        print 'url faild'
        leftMouseClick(wndCreateDownloadRect[2]-30, wndCreateDownloadRect[1]+15)


    print "close download button"
    #alreadyExistDlg = win32gui.FindWindowEx(None,None,'XLUEModalHostWnd',"MessageBox")
    #if alreadyExistDlg:
                #        alreadyExistDlgRect = win32gui.GetWindowRect(alreadyExistDlg)
                #        leftMouseClick(alreadyExistDlgRect[0]+390, alreadyExistDlgRect[1]+35)
        # win32gui.SendMessage(wndCreateDownload, win32con.WM_CLOSE) 这么关闭迅雷自己撸的非标准GUI框架窗体会有BUG
    #else:
    # print "button not exists"            
if __name__ == '__main__':
    ##debug
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://" + '111.231.82.173' + ":4000/",
                              on_message =on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    try:
        ws.run_forever()
    except:
        ws.run_forever()
