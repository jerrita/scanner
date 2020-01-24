import argparse
import queue
import time
import os
import platform
from lib.PortScanner import PortScanner, get_port_lists
from lib.DomainBoomer import Boomer
from lib.AliveDetector import AliveDetector
from lib.InformDisclosure import InformDisclosure


# redrock task for jerrita
# 目前实现：
# 子域名爆破，存活检测，端口扫描，waf检测，信息泄露检测
# sql注入检测暂时使用 sqlmap 代替

def domain_boom(url, dic, thread_num):
    count = 0
    find = 0
    timeout = 0
    fp = open(dic, 'r')
    print(f'Searching for subdomains in {url}...\nGenerating list...')
    s_list = queue.Queue()
    for t in fp.readlines():
        s_list.put(t.strip() + '.' + url)
    threads = []
    print('Booming...')
    for t in range(thread_num):
        threads.append(Boomer(s_list, url))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    for thread in threads:
        count += thread.count
        timeout += thread.timeout
        find += thread.find
    fp.close()
    print(f'[Info] {count} subdomains searched, {find} found, {timeout} timeout')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store_true', dest='boom', help='Booming subdomains')
    parser.add_argument('-p', action='store_true', dest='port', help='Port scan mode')
    parser.add_argument('-i', action='store_true', dest='inf', help='Detect information disclosure')
    parser.add_argument('-a', action='store_true', dest='alive', help='Alive detection')
    parser.add_argument('-d', dest='domain', help='Select the domain or ip')
    parser.add_argument('-m', dest='mode', default='1000', help='Select the port_scan mode (0, 50, 100, 1000)')
    parser.add_argument('-n', dest='thread_num', default='100', help='Select the thread num')
    parser.add_argument('-c', dest='dic', help='Select the dictionary')
    parser.add_argument('-w', dest='url', help='Test for waf (linux only)')
    parser.add_argument('-s', dest='sql_url', help='Test for sql inject (you need sqlmap)')
    res = parser.parse_args()
    start = time.time()

    if res.boom:
        if not res.domain:
            exit('Missing subdomains')
        if not res.dic:
            exit('Missing dictionary')
        domain_boom(res.domain, res.dic, int(res.thread_num))

    if res.port:
        if not res.domain:
            exit('Missing ip')
        print('Scanning...')
        port_scanner = PortScanner()
        port_list = get_port_lists(int(res.mode))
        port_queue = queue.Queue()
        thread_list = []
        for port in port_list:
            port_queue.put(port)
        for i in range(int(res.thread_num)):
            thread_list.append(port_scanner.PortScan(port_queue, res.domain))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        print(f'{len(port_list)} ports scanned.')

    if res.alive and not res.boom:
        if not res.domain:
            exit('Missing domain or ip')
        AliveDetector(res.domain)

    if res.url:
        if platform.system() == 'Windows':
            print('This script is linux only.')
        os.system('wafw00f ' + res.url)

    if res.inf:
        if not res.domain:
            exit('Missing domain or ip')
        InformDisclosure(res.domain)
        # 具体地址可在 lib/InformDisclosure.py 中添加

    if res.sql_url:
        os.system('sqlmap -u ' + res.sql_url)

    end = time.time()
    print(f'[Use time] {end - start}')
