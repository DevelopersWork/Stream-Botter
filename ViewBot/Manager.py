import colorama
from colorama import Fore, init, Style, Back
import time
import random

CONSTANT = 10

class Manager:

    def __init__(self, proxy, speed, valuesTable={}):
        colorama.init(autoreset=True)
        self.intro = "LIVESTREAM VIEW BOT"
        self.min = (3 - speed) if speed < 3 else 0
        self.max = (15 - speed) + 1
        self.run = False
        self.__objects = dict()
        if proxy:
            self.__objects["proxy"] = proxy
        self.PARALLEL = CONSTANT * speed
        self.__queue = [[] for _ in range(self.PARALLEL // (CONSTANT // 2))]
        self.__resetValues(valuesTable)

        self.speed = speed

    def __resetValues(self, valuesTable={}):
        self.__values = {
            "threads": 0,
            "request": 0,
            "failed": 0,
            "active": 0,
            "success": 0,
            "proxies": 0,
            'idle': 0,
            "watching": 1,
            'views': 1,
            'link': "",
            'title': ""
        }
        self.__critical = [False for _ in range(self.PARALLEL//CONSTANT)]
        self.__critical.append(False)
        self.__critical.append(False)
        self.__critical.append(False)

    def get(self, name):
        if name in self.__values.keys():
            return self.__values[name]
        return ""

    def increment(self, name):
        while self.__critical[-2]:
            time.sleep(random.randint(self.min, self.max))

        self.__critical[-2] = True
        if name in self.__values.keys():
            self.__values[name] += 1
        self.__critical[-2] = False
    
    def set(self, name, value):
        while self.__critical[-1]:
            time.sleep(random.randint(self.min, self.max))

        self.__critical[-1] = True
        if name in self.__values.keys():
            self.__values[name] = value
        self.__critical[-1] = False

    def decrement(self, name):
        while self.__critical[-2]:
            time.sleep(random.randint(self.min, self.max))

        self.__critical[-2] = True
        if name in self.__values.keys():
            self.__values[name] -= 1
        self.__critical[-2] = False

    def criticalSection(self):
        p_id = random.randint(0, (self.PARALLEL//CONSTANT) - 1)
        t_id = time.time() * 1000

        self.__queue[p_id].append(t_id)
        while self.__critical[p_id]:
            time.sleep(random.randint(self.min, self.max))

        self.__critical[p_id] = True

        _to_run = (self.__values["threads"] // 100) * self.PARALLEL
        _passive_workers = self.__values["request"] 
        _active_workers = self.__values["active"] 

        __result = self.__values["watching"] < self.__values["threads"]
        __result = __result and (_active_workers < self.PARALLEL)

        self.__queue[p_id].pop(0)
        self.__critical[p_id] = False

        return __result

    def print(self, printIntro = True):

        if "proxy" in self.__objects.keys():
            self.__values["proxies"] = self.__objects["proxy"].getProxiesCount()

        if printIntro:
            print(Fore.MAGENTA + self.intro + Style.RESET_ALL + "\n")
            print(Back.WHITE + Style.BRIGHT + Fore.LIGHTBLUE_EX +
                f" REMAKE BY Developers@Work " + Style.RESET_ALL + "\n")

        print(Fore.LIGHTRED_EX + f"VIDEO LINK: " + Back.LIGHTBLACK_EX + Style.BRIGHT +
                self.__values["link"] + Style.RESET_ALL + "\n")
        print(Fore.LIGHTRED_EX + f"VIDEO TITLE: " + Back.LIGHTBLACK_EX + Style.BRIGHT +
                self.__values["title"] + Style.RESET_ALL + "\n")
            
        print(Fore.WHITE + f"BOTS: "+str(self.__values["threads"])+"\n")
        print(Fore.GREEN + f"ACTIVE: "+str(self.__values["active"])+"\n")
        print(Fore.LIGHTBLACK_EX + f"CONNECTING: "+str(self.__values["request"])+"\n")
        print(Fore.YELLOW + f"IDLE: "+str(self.__values["idle"])+"\n")
        print(Fore.CYAN + f"SUCCESS: "+str(self.__values["success"])+"\n")
        print(Fore.RED + f"FAILED: "+str(self.__values["failed"])+"\n")
        print(Fore.WHITE + f"PROXIES: "+str(self.__values["proxies"])+"\n")
        print(Fore.BLUE + f"WATCHING: "+str(self.__values["watching"])+"\n")
        print(Fore.GREEN + f"VIEWS: "+str(self.__values["views"])+"\n")

        print(Style.RESET_ALL)

"Manager"
