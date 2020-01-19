import platform
import subprocess
import requests

def AliveDetector(domain):
    if platform.system() == 'Windows':
        ans = subprocess.getstatusoutput(f'ping -n 1 -w 1 {domain}')
    else:
        ans = subprocess.getstatusoutput(f'ping -c1 -w1 {domain}')
    if ans[0] == 0:
        print(f'[Ping] {domain} is alive.')
    else:
        # try to request html data
        try:
            response = requests.get('http://' + domain, timeout=1)
            print(f'[Request] {domain} is alive.')
        except Exception:
            print(f'[Info] {domain} is not alive.')