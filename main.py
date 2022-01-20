import os
import sys
import time
import random
from IPython.display import clear_output

args = {'PROXY_TYPES': None, 'TEMP_DIR': None, 'THREADS': None, 'TOKEN': None}
# parsing cmd args
for i in sys.argv[1::]:
    arg = i.split('=')
    args[arg[0].upper()] = "=".join(arg[1:])

types = os.environ.get('PROXY_TYPES').split(',') if os.environ.get('PROXY_TYPES') else [] # ["http"]
types = args['PROXY_TYPES'].split(',') if args['PROXY_TYPES'] else types

tmp_dir = os.environ.get('TEMP_DIR') if os.environ.get('TEMP_DIR') else "/tmp"
tmp_dir = args['TEMP_DIR'] if args['TEMP_DIR'] else tmp_dir

threads = os.environ.get('THREADS') if os.environ.get('THREADS') else "0"
threads = args['THREADS'] if args['THREADS'] else threads

token = os.environ.get('TOKEN') if os.environ.get('TOKEN') else ""
token = args['TOKEN'] if args['TOKEN'] else token

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
 
**OLD** https://github.com/KevinLage/YouTube-Livestream-Botter
**NEW** https://github.com/DevelopersWork/YouTube-Livestream-Botter
"""

proxy = Proxy(types)
manager = Manager(proxy)
manager.intro = intro
browser = Browser()
bot = Bot(proxy, manager, browser)
proxy_filter = ProxyFilter(proxy)

try:
    threads = int(threads)
except:
    threads = 0

if __name__ == '__main__':
    bot.run = True
    bot.setBot(token)
    bot.setThreads(threads)
    bot.start()
    manager.print()

    while manager.get('active') or manager.get('idle'):
        manager.print(False)
        time.sleep(random.randint(3,15))
        clear_output(wait=True)
        pass
