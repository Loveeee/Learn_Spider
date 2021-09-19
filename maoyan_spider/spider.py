import json

import requests
from requests.exceptions import RequestException
import re


# 爬取页面
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68',
            # 'cookie': '__mta=245808699.1617453162045.1617456408501.1617456489607.9; uuid_n_v=v1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1617453161; _lxsdk_cuid=17897b89b48c8-0e33b6396fe4f7-7166786d-144000-17897b89b49c8; _lxsdk=AD6A3FE0947811EBBE637B8382B2095A39660437B57745E395E3885A57DAA891; __mta=245808699.1617453162045.1617453162045.1617453167521.2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1617456489; _lxsdk_s=17897b89b4a-34d-f3d-da8%7C%7C22; uuid=363272E0948111EBAB1D1FE68B47685D217009CA23EE409180D3A439994BF5FD; _csrf=4de39c3dba88b6d0fb4737970aa53044a43d8f441d5d41994d8533f0fcfd376f; lt=91EGK6lFntWC79uyilKIazlsoqYAAAAAJg0AAPymiYQQf4Xe4D8znTg47vVVNgjX4HAZ_Zg88vQ8s6Nrn-_3iPjm9jefSHxjiU7olA; lt.sig=g0kDBB6zO4lOMihF3-2kxkIVl_8'
        }
        # 这里的cookies需要单独拿出来，放在headers里不好使
        cookies = {
            # "__mta": "245808699.1617453162045.1617456408501.1617456489607.9",
            # "uuid_n_v": "v1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1617453161",
            # "_lxsdk_cuid": "17897b89b48c8-0e33b6396fe4f7-7166786d-144000-17897b89b49c8",
            # "_lxsdk": "AD6A3FE0947811EBBE637B8382B2095A39660437B57745E395E3885A57DAA891",
            # "__mta": "245808699.1617453162045.1617453162045.1617453167521.2",
            # "Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2": "1617456489",
            # "_lxsdk_s": "17897b89b4a-34d-f3d-da8%7C%7C22",
            # "uuid": "363272E0948111EBAB1D1FE68B47685D217009CA23EE409180D3A439994BF5FD",
            # "_csrf": "4de39c3dba88b6d0fb4737970aa53044a43d8f441d5d41994d8533f0fcfd376f",
            # " lt": "91EGK6lFntWC79uyilKIazlsoqYAAAAAJg0AAPymiYQQf4Xe4D8znTg47vVVNgjX4HAZ_Zg88vQ8s6Nrn-_3iPjm9jefSHxjiU7olA",
            # " lt.sig": "g0kDBB6zO4lOMihF3-2kxkIVl_8"
            "__mta": "245808699.1617453162045.1617456489607.1617456827070.10",
            "uuid_n_v": "v1",
            "_lxsdk_cuid": "17897b89b48c8-0e33b6396fe4f7-7166786d-144000-17897b89b49c8",
            "__mta": "245808699.1617453162045.1617453162045.1617453167521.2",
            "uuid": "363272E0948111EBAB1D1FE68B47685D217009CA23EE409180D3A439994BF5FD",
            "_csrf": "4de39c3dba88b6d0fb4737970aa53044a43d8f441d5d41994d8533f0fcfd376f",
            "lt": "91EGK6lFntWC79uyilKIazlsoqYAAAAAJg0AAPymiYQQf4Xe4D8znTg47vVVNgjX4HAZ_Zg88vQ8s6Nrn-_3iPjm9jefSHxjiU7olA",
            "lt.sig": "g0kDBB6zO4lOMihF3-2kxkIVl_8",
            "uid": "106637866",
            "uid.sig": "3usYN8wSzN739pLKFfPGgIbprBg",
            "Hm_lvt_703e94591e87be68cc8da0da7cbd0be2": "1617453161,1617456826",
            "Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2": "1617456826",
            "_lxsdk": "363272E0948111EBAB1D1FE68B47685D217009CA23EE409180D3A439994BF5FD",
            "_lxsdk_s": "17897b89b4a-34d-f3d-da8%7C%7C24"
        }
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            # 更改编码格式,默认的是ISO什么开头的
            response.encoding = 'utf8'
            return response.text

    except RequestException:
        return None


# 解析页面
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">'
        + '(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            # 把“主演:”过滤掉
            'actors': item[3].strip()[3:],
            # 把“上映时间：”过滤掉
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


# 数据写入到本地文件
def write_result(content):
    with open('res.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = f'https://maoyan.com/board/4?offset={offset}'
    html = get_one_page(url)
    print(html)
    for item in parse_one_page(html):
        print(item)
        write_result(item)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
