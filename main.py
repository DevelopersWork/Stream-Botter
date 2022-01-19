import time
import os
import random

types = os.environ.get('PROXY_TYPES').split(',') if os.environ.get('PROXY_TYPES') else [] # ["http"]
tmp_dir = os.environ.get('TEMP_DIR') if os.environ.get('TEMP_DIR') else "/tmp"
threads = os.environ.get('THREADS') if os.environ.get('THREADS') else "0"
token = os.environ.get('TOKEN') if os.environ.get('TOKEN') else ""

from ViewBot.Manager import Manager
from ViewBot.Proxy import Proxy
from ViewBot.Bot import Bot
from ViewBot.ProxyFilter import ProxyFilter
from ViewBot.Browser import Browser


intro = """
███████╗████████╗██████╗ ███████╗ █████╗ ███╗   ███╗      ██████╗  ██████╗ ████████╗████████╗███████╗██████╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗████╗ ████║      ██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
███████╗   ██║   ██████╔╝█████╗  ███████║██╔████╔██║█████╗██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝
╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║╚════╝██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
███████║   ██║   ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║      ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
 
https://github.com/KevinLage/YouTube-Livestream-Botter
"""

proxy = Proxy(types)
manager = Manager(proxy)
manager.intro = intro
browser = Browser()
bot = Bot(proxy, manager, browser)
proxy_filter = ProxyFilter(proxy)
manager.print()

try:
    threads = int(threads)
except:
    threads = 0

if __name__ == '__main__':
    bot.run = True
    bot.setBot(token)
    bot.setThreads(threads)
    bot.start()

    while manager.get('active') or manager.get('idle'):
        manager.print()
        time.sleep(random.randint(5,30))
        pass
