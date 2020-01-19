import threading
import dns.resolver


class Boomer(threading.Thread):
    def __init__(self, sub_queue, domain):
        threading.Thread.__init__(self)
        self.sub_queue = sub_queue
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = ['119.29.29.29', '182.254.116.116', '114.114.115.115', '114.114.114.114']
        self.resolver.timeout = 1
        self.resolver.lifetime = 1
        self.count = 0
        self.timeout = 0
        self.find = 0

    def run(self):
        while True:
            if self.sub_queue.empty():
                break
            url = self.sub_queue.get(timeout=0.5)
            self.count += 1
            try:
                a = self.resolver.query(url, 'A')
                ips = []
                for i in a.response.answer:
                    for j in i.items:
                        if j.rdtype == 1:
                            ips.append(j.address)
                print(f'Find: {url} -> {" , ".join(ips)}')
                self.find += 1
            except dns.resolver.NXDOMAIN:
                pass
            except dns.exception.Timeout:
                self.timeout += 1
