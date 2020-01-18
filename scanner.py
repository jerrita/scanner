import dns.resolver
from concurrent.futures import ThreadPoolExecutor
import random
import argparse


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
    random.shuffle(s_list)
    with ThreadPoolExecutor(pool_size) as executor:
        executor.map(getrecord, s_list)
    fp.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store_true', dest='boom', help='Booming subdomains')
    parser.add_argument('-d', dest='domain', help='Select the domain or ip')
    parser.add_argument('-dic', dest='dic', help='Select the dictionary')
    parser.add_argument('--pool', default=128, help='Select the size of thread_pool')
    res = parser.parse_args()
    if res.boom:
        if not res.domain:
            exit('Missing subdomains')
        if not res.dic:
            exit('Missing dictionary')
        domainboom(res.domain, res.dic, res.pool)
        print('Done.')
