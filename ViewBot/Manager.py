import colorama
from colorama import Fore, init, Style, Back
import time
import random


class Manager:

    def __init__(self, proxy, valuesTable={}):
        colorama.init(autoreset=True)
        self.intro = "LIVESTREAM VIEW BOT"
        self.min = 3
        self.max = 15
        self.run = False
        self.__objects = {
            "proxy": proxy
        }
        self.PARALLEL = 36
        self.__queue = [[] for _ in range(self.PARALLEL//8)]
        self.__resetValues(valuesTable)

    def __resetValues(self, valuesTable={}):
        self.__values = {
            "threads": 0,
            "idle": 0,
            "active": 0,
            "success": 0,
            "proxies": 0,
            "watching": 1,
            'views': 1,
        }
        self.__critical = [False for _ in range(self.PARALLEL//8)]
        self.__critical.append(False)
        self.__critical.append(False)
        self.__critical.append(False)

    def get(self, name):
        if name in self.__values.keys():
            return self.__values[name]
        return ""

    def increment(self, name):
        while self.__critical[-2]:
            time.sleep(random.randint(1, self.min))

        self.__critical[-2] = True
        if name in self.__values.keys():
            self.__values[name] += 1
        self.__critical[-2] = False
    
    def set(self, name, value):
        while self.__critical[-1]:
            time.sleep(random.randint(1, self.min))

        self.__critical[-1] = True
        if name in self.__values.keys():
            self.__values[name] = value
        self.__critical[-1] = False

    def decrement(self, name):
        while self.__critical[-2]:
            time.sleep(random.randint(1, self.min))

        self.__critical[-2] = True
        if name in self.__values.keys():
            self.__values[name] -= 1
        self.__critical[-2] = False

    def criticalSection(self):
        p_id = random.randint(0, (self.PARALLEL//8) - 1)
        t_id = time.time() * 1000

        self.__queue[p_id].append(t_id)
        while self.__critical[p_id] and self.__queue[p_id][0] != t_id:
            time.sleep(random.randint(1, self.min))

        self.__critical[p_id] = True

        __result = (self.__values["watching"] * 7) < self.__values["threads"]
        __result = __result or ((self.__values["active"] * 3) < self.__values["idle"])

        self.__queue[p_id].pop(0)
        self.__critical[p_id] = False

        return __result

    def print(self, printIntro = True):

        self.__values["proxies"] = self.__objects["proxy"].getProxiesCount()

        if printIntro:
            print(Fore.MAGENTA + self.intro + Style.RESET_ALL + "\n")
            print(Back.WHITE + Style.BRIGHT + Fore.LIGHTBLUE_EX +
                f" REMAKE BY Developers@Work " + Style.RESET_ALL + "\n")
        print(Fore.WHITE + f"BOTS: "+str(self.__values["threads"])+"\n")
        print(Fore.GREEN + f"ACTIVE: "+str(self.__values["active"])+"\n")
        print(Fore.YELLOW + f"IDLE: "+str(self.__values["idle"])+"\n")
        print(Fore.CYAN + f"SUCCESS: "+str(self.__values["success"])+"\n")
        print(Fore.RED + f"PROXIES: "+str(self.__values["proxies"])+"\n")
        print(Fore.BLUE + f"WATCHING: "+str(self.__values["watching"])+"\n")
        print(Fore.GREEN + f"VIEWS: "+str(self.__values["views"])+"\n")
        print(Style.RESET_ALL)


"Manager"
