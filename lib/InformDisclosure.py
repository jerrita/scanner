import requests

dict = ['.git', '.svn', '.workspace']
# 常见信息泄露地址，可自行补充

def InformDisclosure(domain):
    print('[Info] Detecting...')
    for i in dict:
        try:
            res = requests.get(domain + '/' + i, timeout=3)
            if res.status_code != 404:
                print(f'[Find] {res.status_code} => {domain + "/" + i}')
        except Exception as e:
            print('[Debug]', e)
