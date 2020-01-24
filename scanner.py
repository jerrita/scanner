import argparse
import queue
import time
import os
from lib.PortScanner import PortScanner, get_port_lists
from lib.DomainBoomer import Boomer
from lib.AliveDetector import AliveDetector


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
    parser.add_argument('-a', action='store_true', dest='alive', help='Alive detection')
    parser.add_argument('-d', dest='domain', help='Select the domain or ip')
    parser.add_argument('-m', dest='mode', default='1000', help='Select the port_scan mode (0, 50, 100, 1000)')
    parser.add_argument('-n', dest='thread_num', default='100', help='Select the thread num')
    parser.add_argument('-c', dest='dic', help='Select the dictionary')
    parser.add_argument('-w', dest='url', help='Test for waf (linux only)')
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
        os.system('wafw00f ' + res.url)

    end = time.time()
    print(f'[Use time] {end - start}')
