import requests
import json

# print(res.Session())
session = requests.Session()
header = {
	"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
}
res = session.get('http://www.zhihu.com',headers=header)
print(res.cookies.get_dict())
print(res.text)