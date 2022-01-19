from colorama import Fore, init, Style, Back
import time
import random
import threading


class Manager:
    def __init__(self, proxy, valuesTable={}):
        self.intro = "LIVESTREAM VIEW BOT"
        self.min = 5
        self.max = 15
        self.run = False
        self.__objects = {
            "proxy": proxy
        }
        self.__resetValues(valuesTable)

    def __resetValues(self, valuesTable={}):
        self.__values = {
            "threads": 0,
            "idle": 0,
            "active": 0,
            "success": 0,
            "proxies": 0,
            "watching": 0
        }
        self.__critical = False

    def get(self, name):
        while self.__critical:
            time.sleep(random.randint(1, 5))

        if name in self.__values.keys():
            return self.__values[name]
        return ""

    def increment(self, name):
        # print("increment",self.__critical)
        while self.__critical:
            time.sleep(random.randint(1, 5))

        self.__critical = True
        if name in self.__values.keys():
            self.__values[name] += 1
        self.__critical = False
    
    def setWatching(self, value):
        
        while self.__critical:
            time.sleep(random.randint(1, 5))

        self.__critical = True
        name = 'watching'
        if name in self.__values.keys():
            self.__values[name] = value
        self.__critical = False

    def decrement(self, name):
        # print("decrement",self.__critical)
        while self.__critical:
            time.sleep(random.randint(1, 5))

        self.__critical = True
        if name in self.__values.keys():
            self.__values[name] -= 1
        self.__critical = False

    def criticalSection(self):
        while self.__critical:
            time.sleep(random.randint(1, 5))
        self.__critical = True
        __result = ((self.__values["threads"] * 25)
                    // 100) > self.__values["active"]
        self.__critical = False
        return __result

    def print(self):

        self.__values["proxies"] = self.__objects["proxy"].getProxiesCount()

        print(Fore.MAGENTA + self.intro + Style.RESET_ALL + "\n")
        print(Back.WHITE + Style.BRIGHT + Fore.LIGHTBLUE_EX +
              f" REMAKE BY Developers@Work " + Style.RESET_ALL + "\n")
        print(Fore.WHITE + f"BOTS: "+str(self.__values["threads"])+"\n")
        print(Fore.GREEN + f"ACTIVE: "+str(self.__values["active"])+"\n")
        print(Fore.YELLOW + f"IDLE: "+str(self.__values["idle"])+"\n")
        print(Fore.CYAN + f"SUCCESS: "+str(self.__values["success"])+"\n")
        print(Fore.RED + f"PROXIES: "+str(self.__values["proxies"])+"\n")
        print(Fore.BLUE + f"WATCHING: "+str(self.__values["watching"])+"\n")
        print(Style.RESET_ALL)

    def printService(self):
        while self.run:
            self.print()
            time.sleep(random.random(self.min, self.max))


"Manager"
