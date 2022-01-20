from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException


class Browser:
    
    def __get_chrome_options(self, proxy = None):
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if proxy:
            chrome_options.add_argument("--proxy-server={0}".format(proxy))
        
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_options.experimental_options["prefs"] = chrome_prefs

        mobile_emulation = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        
        return chrome_options

    def open(self, url, proxy = None, proxyType = None, retry = 0):
        watching = 0

        try:

            driver = webdriver.Chrome(
                options = self.__get_chrome_options(proxy)
            )
            
            # Do stuff with your driver
            driver.get(url)
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH, 
                        "//*[@id=\"count\"]/ytd-video-view-count-renderer/span[1]"
                    )
                )
            )
            watching = int(element.text.split(' ')[0])
            
            driver.close()

        except TimeoutException as te:
            if retry < 3: self.open(url, proxy, proxyType, retry + 1)
            return -1
        except Exception as e:
            return -1
        
        return watching

    