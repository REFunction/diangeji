# -*- coding: utf-8 -*-
import requests
import json
import urllib
import sys, os
import subprocess


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
        try:
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
                    mp3_path = self.change_volume(path)

                    os.system('.\\ffplay -nodisp -autoexit ' + '\"' + mp3_path + '\"')
                    break
                except Exception:
                    print('下载' + data['title'] + '失败')
                    print(Exception)
        except Exception:
            pass


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

    def get_song_volume(self, path):
        cmd = 'ffmpeg -i ' + '\"' + path + '\"' + ' -af \"volumedetect\" -f null NUL'
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        result = str(result)
        result = result[result.find('mean_volume'):]
        result = result[: result.find('\\r\\n')]
        result = result[len('mean_volume: '):]
        result = float(result[: result.find(' ')])
        result = -15 - result
        result = str(round(result, 3)) + ' dB'
        return result

    def change_volume(self, path):
        volume = self.get_song_volume(path)
        output_path = path.replace('.m4a', '.mp3')
        print('.\\ffmpeg -i ' + '\"' + path + '\"' + ' -af \"volume=' + volume + '\" ' +
                  '\"' + output_path + '\"')
        os.system('.\\ffmpeg -i ' + '\"' + path + '\"' + ' -af \"volume=' + volume + '\" ' +
                  '\"' + output_path + '\"')
        return output_path


if __name__ == '__main__':
    qq_music = Music_tx()
    # qq_music.qq_music('she is my sin')
    qq_music.qq_music('告白气球 周杰伦')
    # print(qq_music.get_song_volume('mp3\\She Is My Sin-Nightwish.m4a'))
