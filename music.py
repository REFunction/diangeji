# -*- coding: utf-8 -*-
import requests
import json
import urllib
import sys, os


class Music_tx():
    def __init__(self):
        self.header = {
            'Connection': "keep-alive",
            'Pragma': "no-cache",
            'Cache-Control': "no-cache",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/72.0.3626.119 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Referer': "https://y.qq.com",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'cache-control': "no-cache",
        }

    # 通过json接口搜索音乐
    def qq_music(self, keyword, num=2, page=1, file_path=None):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=62240638881390953&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=' + str(
            page) + '&n=' + str(num) + '&w=' + str(
            keyword) + '&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'
        response = requests.get(url, headers=self.header)
        music_data = response.text
        json_music_data = json.loads(music_data)
        music_list = json_music_data['data']['song']['list']
        song_MediaMids = []
        song_mids = []
        song_titles = []
        song_singers = []
        song_albumns = []
        song_id = []
        music_url = []
        num = 0
        if not file_path:
            file_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
            if not os.path.isdir(file_path + 'mp3'):
                os.mkdir(file_path + 'mp3')
            file_path = os.path.dirname(os.path.abspath(__file__)) + '\\mp3\\'
        path = ''
        for data in music_list:
            song_MediaMids.append(data['file']['strMediaMid'])
            song_mids.append(data['mid'])
            song_titles.append(data['title'])
            song_singers.append(data['singer'][0]['name'])
            song_albumns.append(data['album']['name'])
            song_id.append(data['id'])
            music_url.append(self.get_play_url(data['mid'], data['file']['strMediaMid']))
            print('正在下载:', data['title'], '......')
            url = self.get_play_url(data['mid'], data['file']['strMediaMid'])
            if os.path.isfile(file_path + data['title'] + '-' + data['singer'][0]['name'] + '.m4a'):
                num += 1
                path = file_path + data['title'] + '-' + data['singer'][0]['name'] + str(num) + '.m4a'
            else:
                path = file_path + data['title'] + '-' + data['singer'][0]['name'] + '.m4a'
            print(url)
            try:
                urllib.request.urlretrieve(url, path, reporthook=self._progress)
                print('下载' + data['title'] + '成功')
                os.system('.\\ffplay -nodisp -autoexit ' + '\"' + path + '\"')
            except Exception:
                print('下载' + data['title'] + '失败')
                print(Exception)


    # 获取播放地址
    def get_play_url(self, songid, strMediaMid):
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=' + \
              songid + '&filename=C400' + strMediaMid + '.m4a&guid=6612300644'
        # 获取返回文件并解析得到vkey
        response = requests.get(url)
        json_data = json.loads(response.text)
        print(json_data)
        vkey = json_data['data']['items'][0]['vkey']
        real_url = 'http://isure.stream.qqmusic.qq.com/C400' + strMediaMid + '.m4a?vkey=' + vkey + '&guid=6612300644&uin=0&fromtag=66'
        # print(real_url)
        return real_url

    # 显示下载进度
    def _progress(self, block_num, block_size, total_size):
        '''回调函数
           @block_num: 已经下载的数据块
           @block_size: 数据块的大小
           @total_size: 远程文件的大小
        '''
        sys.stdout.write('\r>> 已下载: %.1f%%' % (float(block_num * block_size) / float(total_size) * 100.0))
        sys.stdout.flush()


if __name__ == '__main__':
    qq_music = Music_tx()
    qq_music.qq_music('极乐净土')








