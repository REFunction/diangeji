import requests
import win32com.client
import time
from music import Music_tx
from queue import Queue
from threading import Thread
import os
from tkinter import *
import tkinter.font as tf
from tkinter import scrolledtext
from tkinter.simpledialog import *
import re
import subprocess
from index_queue import IndexQueue
from PyQt5.QtCore import QObject, pyqtSignal


old_list = []
#创建一个old_list列表用于辅助后面的text_danmu方法提取新消息
class Danmu():
#定义一个Danmu类
    tip_label = {'text':''}
    def __init__(self):
        self.url = "https://api.live.bilibili.com/ajax/msg"
        self.headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Referer": "https://live.bilibili.com/21197548?visit_id=45e09yabx2k0",
            # "Referer": "https://live.bilibili.com/1111?visit_id=847swo7d59s0"
            }
        self.data = {
            "roomid":'21197548', #  彪哥直播间 21197548
            "csrf_token":"",
            "csrf":"",	
            "visit_id":""
            }
        self.blacklist = []
        self.song_queue = IndexQueue()
        self.qq_music = Music_tx()
        play_thread = Thread(target=self.play)
        play_thread.setDaemon(True)
        play_thread.start()

        gui_thread = Thread(target=self.listen_danmu)
        gui_thread.setDaemon(True)
        gui_thread.start()

        # self.app = Tk()
        # self.app.title('点歌姬-普通的函数')
        # self.app.geometry('300x130')
        #
        # self.font = tf.Font(size=16, weight='normal')
        # self.create_components()
        # self.place_components()
        #
        # self.app.mainloop()


        #在 __init__方法中先定义好要使用的请求url,请求头，和请求参数
    def speak_text(self,text):
    #定义一个speak_text方法，并创建形参text，用于作为接下来读取的文字
        speak = win32com.client.Dispatch("SAPI.SpVoice")
        #创建发声对象
        speak.Speak(text)
        #使用发生对象读取文字


    def get_blacklist(self, path):
        if not os.path.isfile(path):
            print(path, '不存在')
            file = open(path, 'w', encoding='utf-8')
            file.close()
        file = open(path, 'r', encoding='utf-8')
        self.blacklist = file.read().split('\n')
        file.close()


    def is_in_blacklist(self, song_name):
        for ban_name in self.blacklist:
            if len(re.findall(song_name, ban_name, flags=re.IGNORECASE)) > 0:
                return True
        return False
        
    def text_danmu(self,html):
    #创建一个text_danmu方法，用于提取弹幕信息
        global old_list
        #设置变量作用域，使得该方法可以修改全局变量old_list的值
        temp_list = []
        #创建一个temp_list列表用于作为临时列表辅助提取弹幕消息
        for text in html["data"]["room"]:
        #for循环提取html字典中嵌套的子字典data中嵌套的子字典room的内容赋值给text变量
        #这个html字典来自于get_danmu方法传递
            temp_list.append(text["text"])
            #将变量text字典中text键的值添加到temp_list中
        if temp_list == old_list:
            pass
        #检测temp_list临时列表的内容和old_list是否相同，如果相同则跳过
        else:
            for text_number in range (1,11):
            #创建for循环一次将1到10的数字赋给text_number
                if "".join(temp_list[:text_number]) in "".join(old_list):
                    pass
                #使用join方法以""为分割符提取temp_list切割后的列表的内容
                #使用join方法以""为分割符提取old_list列表的内容
                #比较内容是否相同，如果相同则跳过
                else:
                    try:
                        pass
                        # print (temp_list[text_number-1])
                    except:
                        pass
                    else:
                        if temp_list[text_number-1][0:3] == '点歌 ':
                            song_name = temp_list[text_number-1][3:]
                            self.get_blacklist('blacklist.txt')
                            if not self.is_in_blacklist(song_name):
                                self.song_queue.put(song_name)
                        # self.speak_text(temp_list[text_number-1])
                    #尝试打印temp_list指定索引的内容，如果报错则跳过
                    #否则调用speak_text方法，进行文字转语言
            old_list = temp_list[:]
            #将temp_list的值赋给old_list，进行更新旧信息列表
            
    def get_danmu(self):
        html = requests.post(url=self.url,headers=self.headers,data=self.data)
        html.json()
        self.text_danmu(eval(html.text))

    def play(self):
        while 1:
            if self.song_queue.isEmpty():
                time.sleep(1)
                continue
            song_name = self.song_queue.get()
            print('正在播放:', song_name)
            self.tip_label['text'] = '正在播放:' + song_name
            self.qq_music.qq_music(song_name)
            self.tip_label['text'] = '没有歌曲播放'
            self.clear_mp3_dir()

    def clear_mp3_dir(self):
        filenames = os.listdir('mp3')
        for filename in filenames:
            path = 'mp3/' + filename
            os.remove(path)

    def pause(self):
        os.system('.\pssuspend64.exe ffplay.exe')

    def recover(self):
        os.system('.\pssuspend64.exe -r ffplay.exe')

    def on_click_pause_button(self):
        if self.tip_label['text'] == '没有歌曲播放':
            return
        if self.pause_button['text'] == '暂停':
            self.pause_button['text'] = '播放'
            self.pause()
        else:
            self.pause_button['text'] = '暂停'
            self.recover()

    def create_components(self):
        self.pause_button = Button(self.app,
                            text='暂停',
                            command=self.on_click_pause_button,
                            width=10)
        self.tip_label = Label(self.app, text='没有歌曲播放', width=30)

    def place_components(self):
        self.pause_button.place(x=30, y=10)
        self.tip_label.place(x=10, y=50)

    def listen_danmu(self):
        while True:
            self.get_danmu()
            time.sleep(3)
            #每三秒钟调用一个bzhan实例的get_danmu方法



if __name__ == '__main__':
    danmu = Danmu()


