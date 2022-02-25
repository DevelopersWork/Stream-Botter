import os
import sys
import time
import random
from IPython.display import clear_output
# from ViewBot.Browser import Browser

# python main.py threads <video_id>

args = {'THREADS': None, 'TOKEN': None, 'PROXY_TYPES': None, 'TEMP_DIR': None, 'SPEED': 1}
# parsing cmd args
for i in range(len(sys.argv[1::])):
    arg = sys.argv[i + 1].split('=')
    if len(arg) == 2:
        args[arg[0].upper()] = "=".join(arg[1:])
    else:
        args[list(args.keys())[i]] = sys.argv[i + 1]

types = os.environ.get('PROXY_TYPES').split(',') if os.environ.get('PROXY_TYPES') else [] # ["http"]
types = args['PROXY_TYPES'].split(',') if args['PROXY_TYPES'] else types

tmp_dir = os.environ.get('TEMP_DIR') if os.environ.get('TEMP_DIR') else "/tmp"
tmp_dir = args['TEMP_DIR'] if args['TEMP_DIR'] else tmp_dir

threads = os.environ.get('THREADS') if os.environ.get('THREADS') else "0"
threads = args['THREADS'] if args['THREADS'] else threads

token = os.environ.get('TOKEN') if os.environ.get('TOKEN') else ""
token = args['TOKEN'] if args['TOKEN'] else token

speed = os.environ.get('SPEED') if os.environ.get('SPEED') else ""
speed = args['SPEED'] if args['SPEED'] else speed

from ViewBot.Manager import Manager
from ViewBot.Proxy import Proxy
from ViewBot.Bot import Bot
from ViewBot.ProxyFilter import ProxyFilter
# from ViewBot.Browser import Browser


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

try:
    threads = int(threads)
    speed = int(speed)
except:
    threads = 0
    speed = 1

proxy = Proxy(types)
manager = Manager(proxy, speed)
manager.intro = intro
browser = None
# browser = Browser() # Required when only selinum is needed
bot = Bot(proxy, manager, browser)
proxy_filter = ProxyFilter(proxy)

clear_output(wait=True)

if __name__ == '__main__':
    bot.run = True
    bot.setBot(token)
    bot.setThreads(threads)
    bot.start()
    manager.print()

    while manager.get('active') or manager.get('request'):
        manager.print(False)
        time.sleep(random.randint((3 - speed) if speed < 3 else 0, (15 - speed) + 1))
        clear_output(wait=True)
        pass
