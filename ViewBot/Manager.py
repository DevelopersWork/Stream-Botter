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
        self.__resetValues(valuesTable)

        self.PARALLEL = 35

    def __resetValues(self, valuesTable={}):
        self.__values = {
            "threads": 0,
            "idle": 0,
            "active": 0,
            "success": 0,
            "proxies": 0,
            "watching": 0,
            'views': 0,
        }
        self.__critical = False

    def get(self, name):
        while self.__critical:
            time.sleep(random.randint(1, self.min))

        if name in self.__values.keys():
            return self.__values[name]
        return ""

    def increment(self, name):
        while self.__critical:
            time.sleep(random.randint(1, self.min))

        self.__critical = True
        if name in self.__values.keys():
            self.__values[name] += 1
        self.__critical = False
    
    def set(self, name, value):
        while self.__critical:
            time.sleep(random.randint(1, self.min))

        self.__critical = True
        if name in self.__values.keys():
            self.__values[name] = value
        self.__critical = False

    def decrement(self, name):
        while self.__critical:
            time.sleep(random.randint(1, self.min))

        self.__critical = True
        if name in self.__values.keys():
            self.__values[name] -= 1
        self.__critical = False

    def criticalSection(self):
        while self.__critical:
            time.sleep(random.randint(1, self.min))
        self.__critical = True
        __result = ((self.__values["threads"] * self.PARALLEL) // 100) > self.__values["watching"]
        __result = __result or ((self.__values["threads"] * self.PARALLEL * 2) // 100) > self.__values["active"]
        self.__critical = False
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
