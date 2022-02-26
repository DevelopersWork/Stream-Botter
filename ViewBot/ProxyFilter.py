from threading import Thread
import time
import os
import pycurl
from io import BytesIO


class ProxyFilter:

    def __init__(self, proxy, output_dir = None, output_file="failed.txt", reset = False):

        self.__proxy = None
        if proxy:
            self.__dir = proxy.getDir()
            self.__proxy = proxy
        else:
            self.__dir = "/tmp/viewbot/"

        self.__location = self.__dir + 'proxies/dead.txt'
    
        self.__output_location = output_dir if output_dir else self.__dir + 'proxy_filtered/' 
        os.makedirs(self.__output_location, exist_ok = True)

        self.__output_file = output_file

        self.__threads = []
        self.__dead = []

    def sendQuery(self, proxy=False, url=None, user=None, password=None):
        response = BytesIO()
        c = pycurl.Curl()

        c.setopt(c.URL, url or random.choice(self.proxy_judges))
        c.setopt(c.WRITEDATA, response)
        c.setopt(c.TIMEOUT, 10)

        if user is not None and password is not None:
            c.setopt(c.PROXYUSERPWD, f"{user}:{password}")

        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.SSL_VERIFYPEER, 0)

        if proxy:
            c.setopt(c.PROXY, proxy)

        # Perform request
        try:
            c.perform()
        except Exception as e:
            # print(e)
            return False

        # Return False if the status is not 200
        if c.getinfo(c.HTTP_CODE) != 200:
            return False

        # Calculate the request timeout in milliseconds
        timeout = round(c.getinfo(c.CONNECT_TIME) * 1000)

        if timeout > 8000:
            return False

        # Decode the response content
        response = response.getvalue().decode('iso-8859-1')

        return {
            'timeout': timeout,
            'response': response
        }

    def checkProxy(self, proxy, **kwargs):

        if not self.sendQuery(proxy=proxy, url="https://youtu.be/oRdxUFDoQe0?t=60"):
            self.__dead.append(proxy)
            return False
        return True

    def start(self, reset = False):
        if reset and self.__proxy:
            self.__proxy.reset()

        if not os.path.exists(self.__location):
            return False

        with open(self.__location, 'r') as file:
            data = set(file.read().split("\n"))
            for proxy in data:
                if len(proxy.split(':')) != 2: continue
                if len(proxy.split('.')) != 4: continue
                t = Thread(target=self.checkProxy, args=(proxy,))
                self.__threads.append(t)
                t.start()

        for t in self.__threads:
            t.join()

        os.makedirs(self.__output_location, exist_ok=True)
        
        with open(self.__output_location + self.__output_file, 'w') as file:
            file.write("\n".join(self.__dead))
            file.close()

        with open(self.__location, 'w') as file:
            file.write("\n".join(self.__dead))
            file.close()

    def getDead(self):
        return self.__dead
