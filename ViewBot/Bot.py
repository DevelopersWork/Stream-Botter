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
import logging

from urllib.parse import urlparse, parse_qs
import string

TIMEOUT = (15, 60)
RETRIES = 5
YT_HEAD_URL = """https://m.youtube.com/api/stats/watchtime?ns=yt&el=detailpage&cpn=pz_amMllaL0-PQP3&ver=2&cmt=17723.568&fmt=134&fs=0&rt=9.002&euri&lact=9255&live=dvr&cl=430552675&state=playing&volume=100&cbrand=apple&cbr=Safari%20Mobile&cbrver=10.0.14E304&c=MWEB&cver=2.20220224.07.00&cplayer=UNIPLAYER&cmodel=iphone&cos=iPhone&cosver=10_3_1&cplatform=MOBILE&delay=5&hl=en_US&cr=IN&rtn=19&afmt=140&lio=1645876585.611&idpj=-3&ldpj=-37&rti=9&st=17716.033&et=17723.568&muted=1&docid=VbL4AA7f9D8&ei=nloaYp-HDoL64-EPiOC04As&plid=AAXY7qE5IKru6wdo&of=re3rc5R2DIc7Axbc_lERng&vm=CAEQARgEOjJBS1JhaHdBOEYzYzhBQ1JNTzVGdDI4cWJXVWxHUlFEUDVsWExFSmU0aU9WT1Z5TDJyd2JMQVBta0tESWo5R3dMV2ZFdERURUlXZl9JbVNZOEZkUzVINU9CN0Z5Y0FZdDdXS0tFWGI3YVdvbDlGUGhqTzlFSmpsQlRsc0lISXlrTQ"""

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

        self.__platform = "youtube"
        self.__token = ""
        self.run = False

    def __getHeader(self, id, type = ""):

        if type == "yt_video":
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
            }
        elif type == "yt_watchtime":
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "referer": "https://m.youtube.com/watch?v={0}".format(id),
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
            }
        else:
            headers = dict()

        return headers

    def __getUrl(self, args):
        url = YT_HEAD_URL.split('?')[0] + '?'

        parsed_url = urlparse(YT_HEAD_URL)
        params = parse_qs(parsed_url.query)
        
        for k,v in params.items():
            if k in args.keys():
                if type(args[k]) == 'list':
                    url += "{0}={1}&".format(k, args[k][0])
                elif type(args[k]) == 'str':
                    url += "{0}={1}&".format(k, args[k])
            else:
                url += "{0}={1}&".format(k,v[0])

        self.__saveLog(url)

        return url

    def __getRequest(self, session, proxy = None):

        request = {"url": "", "headers": "", "proxies": ""}
        header =  self.__getHeader(self.__token, "yt_video")
        __url = ""
        if self.__platform == "youtube":
            __url = "https://m.youtube.com/watch?v={0}".format(self.__token)
            try:
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

                with open('template.html', 'w') as file:
                    # print(html)
                    file.write(html)
                    file.close()
                    # exit()

                url = html.split('"videostatsWatchtimeUrl":')[1].split('"baseUrl":')[1].split('"')[1]
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
                    videoTitle = html.split('"videoDetails":')[1].split('"title":')[1].split('"')[1]
                except Exception as e:
                    videoTitle = ""

                videoLink = __url

                parsed_url = urlparse(url)
                params = dict(parse_qs(parsed_url.query))

                request = {
                    'args': params,
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
                    formatted_proxy["proxy"]
                )
            else:
                request = self.__getRequest(
                    http
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

            header = self.__getHeader(self.__token, "yt_watchtime")

            for e in "cbr=Safari+Mobile&cbrand=apple&cbrver=10.0.14E304&ceng=WebKit&cengver=603.1.30&cmodel=iphone&cos=iPhone&cosver=10_3_1&cplatform=MOBILE".split('&'):
                k,v = e.split('=')
                args[k] = v

            response = http.get(
                self.__getUrl(args),
                headers=header,
                proxies=request['proxies'],
                timeout=TIMEOUT
            )

            if response.status_code != 204:
                raise Exception('BOT WATCHTIME STATUS IS NOT 204')

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
                self.__values["manager"].increment("failed")

            if request_flag == 1:
                self.__values["manager"].decrement("request")

            self.__sleepThread(failed=failed)

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

        if "proxy" in self.__values.keys() and self.__values['proxy']:
            __dir = self.__values['proxy'].getDir() + 'logs/'
        else:
            __dir = '/tmp/viewbot/' + 'logs/'
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
