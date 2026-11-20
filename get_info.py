import re
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor

# 固定的 CDN 前缀（从浏览器抓包确认的，注意域名是 96f 不是 96f1）
CDN_PREFIX = 'https://96f.1ting.com/local_to_cube_202004121813/96kmp3'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'Referer': 'https://so.1ting.com/',
    'Cookie': 'Hm_lvt_8c210ed87276c6e2fd297c0a71dba826=1789477437; Hm_lpvt_8c210ed87276c6e2fd297c0a71dba826=1789477437; HMACCOUNT=D03C60D966B4F540; acw_tc=275bb91517894776748684024e8462f539299513c55d7ae2105f713def; cdn_sec_tc=275bb91517894776748684024e8462f539299513c55d7ae2105f713def; Hm_lvt_9824b0780871fa69383f690b38a23445=1789477680; Hm_lpvt_9824b0780871fa69383f690b38a23445=1789477773'
}


def get_mp3_url(player_url):
    """根据播放页 URL，提取 wma 路径并转成 mp3 直链"""
    try:
        r = requests.get(player_url, headers=HEADERS, timeout=20)
        r.encoding = 'utf-8'
        # 从页面里找 xxx.wma 路径（在 $YP.create([[...]]) 数组里）
        match = re.search(r'"([^"]+\.wma)"', r.text)
        if match:
            wma_path = match.group(1).replace('\\/', '/')  # 还原 JSON 转义的斜杠
            # 把 .wma 换成 .mp3，前面拼 CDN 前缀
            mp3_path = wma_path.replace('.wma', '.mp3')
            return CDN_PREFIX + mp3_path
    except Exception:
        pass  # 请求失败就返回空串，不打印（GUI 打包后没有控制台，print 会导致程序崩溃）
    return ''


def get_music(song_name, page):
    url = f'https://so.1ting.com/song?q={song_name}&page={page}'
    r = requests.get(url, headers=HEADERS)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

    song_list = soup.find_all('td', class_='song')
    singer_list = soup.find_all('td', class_='singer')
    album_list = soup.find_all('td', class_='album')

    # 第1步：先把所有歌曲的基本信息提取出来
    songs = []
    for i in range(len(song_list)):
        song_a = song_list[i].find('a')
        title = song_a.get_text(strip=True) if song_a else ''
        if not title:  # 跳过空行
            continue
        href = song_a.get('href', '') if song_a else ''
        player_url = 'https:' + href if href.startswith('//') else href

        singer_a = singer_list[i].find('a') if i < len(singer_list) else None
        singer = singer_a.get_text(strip=True) if singer_a else ''

        album_a = album_list[i].find('a') if i < len(album_list) else None
        album = album_a.get_text(strip=True) if album_a else ''

        songs.append({'title': title, 'singer': singer, 'album': album, 'player_url': player_url})

    # 第2步：多线程并发获取每首歌的 mp3 直链
    with ThreadPoolExecutor(max_workers=10) as executor:
        urls = list(executor.map(lambda s: get_mp3_url(s['player_url']) if s['player_url'] else '', songs))

    # 第3步：组装结果
    track_info = []
    for i, s in enumerate(songs):
        track_info.append([s['title'], s['singer'], s['album'], urls[i]])

    return track_info


if __name__ == '__main__':
    song_name = '爱情'
    page = 1
    track_info = get_music(song_name, page)
    print('\n=== 结果 ===')
    for t in track_info:
        print(t)
