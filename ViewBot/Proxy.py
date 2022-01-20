import random
import requests
import os
import time


class Proxy:

    __source = {
        "http": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&anonymity=elite",
            "https://www.proxy-list.download/api/v1/get?type=https&anon=elite",
            "https://www.proxy-list.download/api/v1/get?type=http&anon=elite",
            "https://sunny9577.github.io/proxy-scraper/proxies.txt"
            "http://pubproxy.com/api/proxy?limit=-1&format=txt&http=true&type=http",
            "https://raw.githubusercontent.com/Agantor/viewerbot/master/Proxies_txt/good_proxy.txt"
        ],
        "socks4": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000",
            "https://www.proxy-list.download/api/v1/get?type=socks4&anon=elite"
            "http://pubproxy.com/api/proxy?limit=-1&format=txt&type=socks4"
        ],
        "socks5": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000",
            "https://www.proxy-list.download/api/v1/get?type=socks5&anon=elite"
            "http://pubproxy.com/api/proxy?limit=-1&format=txt&type=socks5"
        ],
        "dead": [
            "https://docs.google.com/uc?export=download&id=1n27MHFgoNoIErFJw5qOnZrscwGNBucnL"
        ]
    }

    def __init__(self, types=[], tmp_dir = '/tmp'):
        self.__types = []
        if "http" in types:
            self.__types.append("http")
        if "socks4" in types:
            self.__types.append("socks4")
        if "sock5" in types:
            self.__types.append("sock5")
        if len(self.__types) == 0:
            self.__types = ["http", "socks4", "socks5"]

        self.__tmp_dir = tmp_dir.rstrip('/') + '/viewbot/' 
        os.makedirs(self.__tmp_dir, exist_ok = True)

        self.__fetchProxies()
        self.__fetchDeadProxies()

        self.__fails = {}

        self.__critical = False

    def getDir(self):
        return self.__tmp_dir

    def __fetchProxies(self):
        self.__proxies = {}
        for proxyType in self.__types:
            data = []
            __dir = self.__tmp_dir + 'proxies/'
            os.makedirs(__dir, exist_ok = True)
            __file = proxyType+'.txt'
            try:
                with open(__dir + __file, 'r') as file:
                    data = file.read().split('\n')
            except:
                urls = Proxy.__source[proxyType]
                for url in urls:
                    data += self.__fetchURL(url)
                data = list(set(data))
                os.makedirs(__dir, exist_ok=True)
                with open(__dir + __file, 'w') as file:
                    file.write("\n".join(data))
                    file.close()
            finally:
                if len(data) > 0 or proxyType == "tor":
                    self.__proxies[proxyType] = data

    def __formatProxy(self, proxy, proxyType):
        _output = {"http": "", "https": ""}
        if proxyType == "http":
            _output['http'] = "http://"
            _output['https'] = "https://"
        if proxyType == "socks4":
            _output['http'] = "socks4://"
            _output['https'] = "socks4://"
        if proxyType == "socks5":
            _output['http'] = "socks5://"
            _output['https'] = "socks5://"

        _output['http'] += proxy
        _output['https'] += proxy

        return _output

    def __fetchURL(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return []
        data = response.text.rstrip()
        data = "".join([i for i in data.split("\r")])
        data = data.split("\n")
        return data

    def __fetchDeadProxies(self):
        self.__dead = []
        proxyType = "dead"
        data = []
        __dir = self.__tmp_dir + 'proxies/'
        os.makedirs(__dir, exist_ok = True)
        __file = proxyType+'.txt'
        try:
            with open(__dir + __file, 'r') as file:
                data = file.read().split('\n')
        except:
            urls = Proxy.__source[proxyType]
            for url in urls:
                data += self.__fetchURL(url)
            data = list(set(data))
            os.makedirs(__dir, exist_ok=True)
            with open(__dir + __file, 'w') as file:
                file.write("\n".join(data))
                file.close()
        finally:
            if len(data) > 0:
                self.__dead = data
            for proxyType in self.__types:
                self.__proxies[proxyType] = list(
                    set(self.__proxies[proxyType]) - set(self.__dead))

    def __deadProxy(self, proxy):
        self.__dead.append(proxy)
        
        proxyType = "dead"
        __dir = self.__tmp_dir + 'proxies/'
        os.makedirs(__dir, exist_ok = True)
        __file = proxyType+'.txt'
        with open(__dir + __file, 'a') as file:
            file.write("\n"+proxy)
            file.close()

    def getRandomProxy(self, loop=0):

        proxyType = random.choice(self.__types)
        proxy = random.choice(self.__proxies[proxyType])

        if proxy in self.__dead and loop < len(self.__proxies[proxyType]):
            return self.getRandomProxy(loop+1)

        return {"proxy": self.__formatProxy(proxy, proxyType), "index": proxy, 'type': proxyType}

    def setProxyFailure(self, proxy, priority=0):
        while self.__critical:
            time.sleep(random.randint(1, 3))
        self.__critical = True

        if proxy not in self.__fails.keys():
            self.__fails[proxy] = 0

        if priority == -1:
            self.__fails[proxy] = 0
        else:
            self.__fails[proxy] += priority + 1

        if self.__fails[proxy] > 15:
            self.__deadProxy(proxy)

        self.__critical = False

    def getProxiesCount(self):

        count = sum([len(i) for i in self.__proxies.values()])
        return count


"Proxy"
