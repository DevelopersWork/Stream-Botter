from getuseragent import UserAgent
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from streamlink import Streamlink

import math

import random
import os
import datetime
import time
from threading import Thread
import traceback

from urllib.parse import urlparse, parse_qs
import string

TIMEOUT = (10, 60)
RETRIES = 5
YT_HEAD_URL = """http://s.youtube.com/api/stats/watchtime?ns=yt&el=detailpage&cpn=isWmmj2C9Y2vULKF&docid={0}&ver=2&cmt=7334&ei={1}&fmt=133&fs=0&rt=1003&of={2}&euri&lact=4418&live=dvr&cl={3}&state=playing&vm={4}&volume={5}&c=MWEB&cver=2.20200313.03.00&cplayer=UNIPLAYER&cbrand=apple&cbr=Safari%20Mobile&cbrver=12.1.15E148&cmodel=iphone&cos=iPhone&cosver=12_2&cplatform=MOBILE&delay=5&hl=ru&cr=GB&rtn=1303&afmt=140&lio=1556394045.182&idpj=&ldpj=&rti=1003&muted=0&st=7334&et=7634"""


def randomword(length=16):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

class Bot:
    def __init__(self, proxy = None, manager = None, browser = None):
        self.__values = {
            "proxy": proxy,
            "manager": manager,
            "browser": browser,
            "threads": 1
        }

        __backoff_factor = 0.5
        __retry_strategy = Retry(
            total=RETRIES,
            read=RETRIES,
            connect=math.ceil(RETRIES/2),
            status_forcelist=(500, 502, 504),
            backoff_factor=__backoff_factor * 2 ** (RETRIES - 1)
        )
        self.__adapter = HTTPAdapter(max_retries=__retry_strategy)

        self.__ua = UserAgent("mobile+ios", requestsPrefix=True)

        self.__platform = "youtube"
        self.__token = ""
        self.run = False

    def __getHeader(self, ua):
        headers = dict()
        headers["User-Agent"] = ua
        headers["Accept"] = "*/*"
        headers["Accept-Language"] = "en-US,en;q=0.5"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Connection"] = "keep-alive"
        headers["Pragma"] = "no-cache"
        headers["Cache-Control"] = "no-cache"

        return headers

    def __getUrl(self,args):
        url = "http://s.youtube.com/api/stats/watchtime?"
        
        for k,v in args.items():
            url += "{0}={1}&".format(k,v)

        return url

    def __getRequest(self, session, ua, proxy = None):

        request = {"url": "", "headers": "", "proxies": ""}
        header = self.__getHeader(ua)
        __url = ""
        if self.__platform == "youtube":
            __url = 'http://m.youtube.com/watch?v=' + self.__token
            header['Referer'] = __url

            try:
                header["Host"] = 'm.youtube.com'
                if proxy != None:
                    response = session.get(
                        __url,
                        headers=header,
                        proxies=proxy,
                        timeout=TIMEOUT
                    )
                else:
                    response = session.get(
                        __url,
                        headers=header,
                        timeout=TIMEOUT
                    )
                
                if response.status_code != 200:
                    raise Exception('REQUEST STATUS IS NOT 200')

                html = response.text

                url = html.split('"videostatsWatchtimeUrl":{"baseUrl":"')[1].split('"')[0]
                url = url.replace('%2C', ',').replace("\/", '/')
                url = '&'.join(url.split('\\u0026'))

                try:
                    viewCount = int(html.split('"viewCount":')[1].split('"')[1])
                except Exception as e:
                    viewCount = 1
                try:
                    watching = int("".join(html.split(' watching now')[0].split('\\x22')).split('text:')[-2].split('\\')[0])
                except Exception as e:
                    watching = 1

                try:    
                    videoTitle = html.split('"title":{"runs":[{"text":"')[1].split('"')[0]
                except Exception as e:
                    videoTitle = ""

                videoLink = __url

                parsed_url = urlparse(url)
                params = parse_qs(parsed_url.query)

                rt = random.randint(10, 200)
                rtn = rt + 300
                header["Host"] = 'www.youtube.com'

                args = {
                    "ns" : params["ns"][0],
                    "el" : params["el"][0],
                    "cpn" : randomword(),
                    "docid" : params["docid"][0],
                    "ver" : "2",
                    "cmt" : "LOAD BELOW",
                    "ei" : params["ei"][0],
                    "fmt" : "243",
                    "fs" : "0",
                    "rt" : str(rt),
                    "of" : params["of"][0],
                    "euri" : "",
                    "lact" : str(random.randint(1000, 8000)),
                    "live" : params["live"][0],
                    "cl" : params["cl"][0],
                    "state" : "playing",
                    "vm" : params["vm"][0],
                    "volume" : str(random.randint(10, 80)),
                    "cbr" : "Firefox",
                    "cbrver" : "83.0",
                    "c" : "WEB",
                    "cplayer" : "UNIPLAYER",
                    "cver" : "2.20201210.01.00",
                    "cos" : "Windows",
                    "cosver" : "10.0",
                    "cplatform" : "DESKTOP",
                    "delay" : "5",
                    "hl" : "en_US",
                    "rtn" : str(rtn),
                    "aftm" : "140",
                    "rti" : str(rt),
                    "muted" : "0",
                    "st" : str(random.randint(1000, 10000)),
                    "et" : "LOAD BELOW",
                    "lio" : "LOAD BELOW"
                }

                request = {
                    # 'url': YT_HEAD_URL.format(self.__token, ei, of, cl, vm, str(int(random.random() * 100 % 80))),
                    'args': args,
                    # 'url': self.__getUrl(args),
                    'headers': header,
                    'proxies': proxy,
                    'link': __url,
                    'viewCount': viewCount,
                    'watching': watching,
                    'link': videoLink,
                    'title': videoTitle
                }
            except Exception as e:
                raise Exception(e)
        if self.__platform == "twitch":
            pass

        return request

    def __request(self):

        agent = self.__ua.Random()['User-Agent']

        formatted_proxy = None
        if self.__values["proxy"] != None:
            formatted_proxy = self.__values["proxy"].getRandomProxy()

        http = requests.Session()
        http.mount('https://', self.__adapter)
        http.mount('http://', self.__adapter)

        request_flag = 0
        active = 0
        failed = False
        try:
            self.__values["manager"].increment("request")
            request_flag = 1

            if formatted_proxy != None:
                request = self.__getRequest(
                    http,
                    agent,
                    formatted_proxy["proxy"]
                )
            else:
                request = self.__getRequest(
                    http,
                    agent
                )
            args = request['args']

            self.__values["manager"].decrement("request")
            request_flag = 0
            self.__values["manager"].increment("active")
            active = 1
            
            origin = datetime.datetime(1970,1,1,0,0,0,0)
            now = datetime.datetime.utcnow()
            start = now - origin

            self.__sleepThread(mn=15, mx=30)
            while not self.__values["manager"].criticalSection():
                self.__sleepThread(failed = True)

            now = datetime.datetime.utcnow() - origin

            lio = format(start.total_seconds(),'.3f')
            et = format((now - start).total_seconds(),'.3f')

            args['et'] = str(et)
            args['lio'] = str(lio)
            args['cmt'] = str(et)

            http.get(
                self.__getUrl(args).replace("watchtime", "playback"),
                headers=request['headers'],
                proxies=request['proxies'],
                timeout=TIMEOUT
            )

            http.get(
                self.__getUrl(args),
                headers=request['headers'],
                proxies=request['proxies'],
                timeout=TIMEOUT
            )

            if self.__values["browser"]:
                self.__values["browser"].open(
                    request['link'], 
                    formatted_proxy['proxy']['https'], 
                    formatted_proxy['type']
                )

            self.__values["manager"].set('views', request['viewCount'])
            self.__values["manager"].set('watching', request['watching'])
            self.__values["manager"].set('link', request['link'])
            self.__values["manager"].set('title', request['title'])

            if self.__values["proxy"] != None:
                self.__values["proxy"].setProxyFailure(
                    formatted_proxy["index"], 
                    -1
                )

            self.__values["manager"].increment("success")
            self.__values["manager"].decrement("active")
            active = 0

            return True

        except (
            IndexError,
            requests.exceptions.ProxyError,
            requests.exceptions.SSLError
        ) as e:
            msg = e
            if hasattr(e, 'message'):
                msg = e.message
            if self.__values["proxy"] != None:
                self.__saveLog(msg, formatted_proxy["index"])
                self.__values["proxy"].setProxyFailure(formatted_proxy["index"], 5)
            else:
                self.__saveLog(msg)
            failed = True

        except (
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects
        ) as e:
            msg = e
            if hasattr(e, 'message'):
                msg = e.message
            if self.__values["proxy"] != None:
                self.__saveLog(msg, formatted_proxy["index"])
                self.__values["proxy"].setProxyFailure(formatted_proxy["index"], 2)
            else:
                self.__saveLog(msg)
            failed = True

        except Exception as e:
            msg = e
            if hasattr(e, 'message'):
                msg = e.message
            if self.__values["proxy"] != None:
                self.__saveLog(msg, formatted_proxy["index"])
                self.__values["proxy"].setProxyFailure(formatted_proxy["index"], 1)
            else:
                self.__saveLog(msg)
            failed = True

        finally:
            if active == 1:
                self.__values["manager"].decrement("active")

            if request_flag == 1:
                self.__values["manager"].decrement("request")

            self.__sleepThread(failed)

        return False
    
    def __sleepThread(self, mn = None, mx = None, failed = False):
        if not mx:
            mx = (self.__values["threads"] // 10) * 3

        if failed:
            mx *= 1.2

        if not mn:
            mn = (self.__values["manager"].get("active") // 10) % 6

        self.__values["manager"].increment("idle")
        try:
            time.sleep(random.randint(mn, mx))
        except Exception as e:
            time.sleep(1)
        self.__values["manager"].decrement("idle")


    def __saveLog(self, message, head="BOT"):

        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        log = "[" + head + "] " + timestamp + ":\t" + str(message) + "\n"

        __dir = self.__values['proxy'].getDir() + 'logs/'
        os.makedirs(__dir, exist_ok = True)
        __file = 'logs.txt'

        with open(__dir + __file, "a+") as file:
            file.write(log)
            file.close()

    def setThreads(self, threads):
        try:
            self.__values["threads"] = int(threads)
        except:
            self.__values["threads"] = 1

    def setBot(self, token, platform = 0):
        if platform == 0:
            self.__platform = "youtube"
        if platform == 1:
            self.__platform = "twitch"
        self.__token = token

    def spamRequests(self):
        t_id = self.__values["manager"].get("threads")
        self.__values["manager"].increment("threads")

        time.sleep(
            0.001 * (self.__values["threads"] // (t_id + 1) )
        )

        while self.run:
            self.__request()
        self.__values["manager"].decrement("threads")

    def start(self):
        for _ in range(self.__values["threads"]):
            if self.run == True:
                t = Thread(target=self.spamRequests)
                t.start()
