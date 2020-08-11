import requests
import json


def codemao(identity,password):
    url = 'https://api.codemao.cn/tiger/v3/web/accounts/login'
    reqdata = json.dumps({'identity': identity, 'password': password, 'pid': '65edCTyg'})
    header = {'Host': 'api.codemao.cn', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0', 'Accept': '/', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2 ', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json;charset=utf-8', 'Product-Code': 'community', 'Platform': 'web', 'SDK-Account-Version': '0.2.1', 'Content-Length': '65', 'Origin': 'https://shequ.codemao.cn', 'Connection': 'keep-alive', 'Referer': 'https://shequ.codemao.cn'}
    response = requests.post(url,
    data=reqdata,
    headers=header)
    html = response.text
    data = json.loads(html)
    if ('error_category' in data):
        return({"code":"ERROR","message":"用户名或密码错误"})
    else:
        data = data['user_info']
        del data['fullname']
        del data['birthday']
        return data


