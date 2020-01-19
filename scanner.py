import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import argparse
import queue
import time
from lib.PortScanner import PortScanner, get_port_lists


def getrecord(url):
    try:
        a = dns.resolver.query(url, 'A')
        ips = []
        for i in a.response.answer:
            for j in i.items:
                if j.rdtype == 1:
                    ips.append(j.address)
        print(f'Find: {url} -> {" , ".join(ips)}')
    except dns.resolver.NXDOMAIN:
        pass


def domainboom(url, passurl, pool_size=128):
    fp = open(passurl, 'r')
    print(f'Searching for subdomains in {url}...\nGenerating list...')
    s_list = []
    for i in fp.readlines():
        s_list.append(i.strip() + '.' + url)
    print('Booming...')
    with ThreadPoolExecutor(pool_size) as executor:
        executor.map(getrecord, s_list)
    fp.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store_true', dest='boom', help='Booming subdomains')
    parser.add_argument('-p', action='store_true', dest='port', help='Port scan mode')
    parser.add_argument('-d', dest='domain', help='Select the domain or ip')
    parser.add_argument('-m', dest='mode', default='1000', help='Select the port_scan mode (0, 50, 100, 1000)')
    parser.add_argument('-n', dest='thread_num', default='100', help='Select the thread num(port scanner)')
    parser.add_argument('-dic', dest='dic', help='Select the dictionary')
    parser.add_argument('--pool', default='12', help='Select the size of thread_pool')
    res = parser.parse_args()
    start = time.time()
    if res.boom:
        if not res.domain:
            exit('Missing subdomains')
        if not res.dic:
            exit('Missing dictionary')
        domainboom(res.domain, res.dic, int(res.pool))
        print('Done.')
    if res.port:
        if not res.domain:
            exit('Missing ip')
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
    end = time.time()
    print(f'[Use time] {end - start}')
