import requests
import math
import re
import json


def getFollws(uid, pn):
    url = 'https://api.bilibili.com/x/relation/followings?vmid=%d&pn=%d&jsonp=json' % (uid, pn)
    return get(url)


def postFollws(uid):
    url = 'https://api.bilibili.com/x/relation/modify'

    data = {
        'fid': uid,
        'act': 1,
        're_src': 14,
        'cross_domain': 'true',
        'csrf': getCsrf(cookies)
    }

    return post(url, data)


def getSubs(uid, pn):
    url = 'https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=0&vmid=%d&pn=%d' % (uid, pn)
    return get(url)


def postSubs(sid):
    url = 'https://api.bilibili.com/pgc/web/follow/add'
    data = {
        'season_id': sid,
        'csrf': getCsrf(cookies)
    }

    return post(url, data)


def getCsrf(cookie):
    searchObj = re.search(r'bili_jct=(.*?);', cookie, re.M | re.I)
    return searchObj.group(1)


def get(url):
    i = 0
    while i < 3:
        try:
            r = requests.get(url=url, headers=headers, timeout=10)
            return json.loads(r.content.decode())
        except requests.exceptions.RequestException:
            i = i + 1


def post(url, data):
    i = 0
    while i < 3:
        try:
            r = requests.post(url=url, headers=headers, data=data, timeout=10)
            return json.loads(r.content.decode())
        except requests.exceptions.RequestException:
            i = i + 1


copyUid = 1  # 被复制账户的uid
cookies = ""  # 破站的cookies

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 BiliDroid/4.34.0 (bbcallen@gmail.com)",
    "Referer": "http://www.bilibili.com/",
    "Cookie": cookies
}

# 关注
pn = 1
while True:
    data = getFollws(copyUid, pn)
    for v in data['data']['list']:
        print(postFollws(v['mid']))

    if math.ceil(data['data']['total'] / 50) == pn:
        print('复制关注完成 %d个' % data['data']['total'])
        break
    pn = pn + 1

# 追番
pn = 1
while True:
    data = getSubs(copyUid, pn)
    for v in data['data']['list']:
        print(postSubs(v['season_id']))

    if math.ceil(data['data']['total'] / 50) == pn:
        print('复制追番完成 %d个' % data['data']['total'])
        break
    pn = pn + 1
