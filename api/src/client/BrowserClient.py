import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, EnvironmentHelper
from python_framework import Client, ClientMethod

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.keys import Keys

from config import BrowserConfig

import logging
logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel(logging.WARNING)  # or any variant from ERROR, CRITICAL or NOTSET

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'

DEFAULT_WEBDRIVER_LARGE_TIMEOUT = BrowserConfig.MAX_WAITING_TIME
DEFAULT_WEBDRIVER_TIMEOUT = DEFAULT_WEBDRIVER_LARGE_TIMEOUT * .2
DEFAULT_WEBDRIVER_TIMEOUT_FRACTION = DEFAULT_WEBDRIVER_TIMEOUT / 50

@Client()
class BrowserClient:

    @ClientMethod()
    def wait(self, sleepTime):
        time.sleep(sleepTime)


    @ClientMethod()
    def getBrowserOptions(self, anonymous=False, deteach=True, hidden=False) :
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_argument(f'user-agent={BrowserConfig.USER_AGENT}')
        chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_experimental_option('useAutomationExtension', False)
        # chromeOptions.add_argument('--disable-software-rasterizer')
        chromeOptions.add_argument('--disable-extensions')
        # chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--no-sandbox')
        if hidden :
            chromeOptions.add_argument("headless")
        if anonymous :
            chromeOptions.add_argument('--incognito')
        if deteach :
            chromeOptions.add_experimental_option('detach', True)
        return chromeOptions


    @ClientMethod()
    def getNewBrowser(self, options=None, hidden=False) :
        options = options if ObjectHelper.isNotNone(options) else self.getBrowserOptions(hidden=hidden)
        browser = None
        try:
            if EnvironmentHelper.isWindows():
                browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
            elif EnvironmentHelper.isLinux():
                browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
        except Exception as exception:
            log.info(self.getNewBrowser, 'For rasbian use the compiled version in https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi:')
            log.info(self.getNewBrowser, 'sudo apt-get install chromium-chromedriver')
            log.info(self.getNewBrowser, 'pi@raspberrypi:~ $ whereis chromedriver')
            log.info(self.getNewBrowser, 'driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")')
            raise exception
        browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f'{BrowserConfig.USER_AGENT}'})
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.maximize(browser)
        browser.hidden = hidden
        browser.originalWindowSize = browser.get_window_size()
        browser.windowSize = {}
        browser.windowSize['width'] = browser.originalWindowSize['width']
        browser.windowSize['height'] = browser.originalWindowSize['height']
        browser.zoom = 100.0
        log.debug(self.getNewBrowser, f'session_id: {browser.session_id}')
        log.debug(self.getNewBrowser, f'command_executor: {browser.command_executor._url}')
        return browser


    @ClientMethod()
    def getNewAnonymousBrowser(self, hidden=False) :
        return self.getNewBrowser(options=self.getBrowserOptions(anonymous=True, hidden=hidden))


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def accessUrl(self, url, browser) :
        try :
            browser.get(url)
            self.wait(DEFAULT_WEBDRIVER_TIMEOUT)
        except :
            browser.get(url)
            self.wait(DEFAULT_WEBDRIVER_LARGE_TIMEOUT)
        return browser


    @ClientMethod(requestClass=[str])
    def openInNewBrowser(self, url) :
        if ObjectHelper.isNotNone(url) :
            browser = self.getNewBrowser()
            return self.accessUrl(url, browser)


    @ClientMethod(requestClass=[str])
    def openInNewAnonymousBrowser(self, url, hidden=False) :
        if ObjectHelper.isNotNone(url) :
            browser = self.getNewAnonymousBrowser(hidden=hidden)
            return self.accessUrl(url, browser)


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def accessUrlInNewTab(self, url, browser):
        if ObjectHelper.isNotNone(url) :
            self.newTab(browser)
            return self.accessUrl(url, browser)


    @ClientMethod(requestClass=[webdriver.Chrome])
    def newTab(self, browser) :
        browser.execute_script("window.open();")
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT)
        browser.switch_to.window(browser.window_handles[-1])
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def typeIn(self, text, browser, element=None) :
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(text)


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def existsByXPath(self, xPath, browser) :
        exists = False
        try :
            exists = ObjectHelper.isNotNone(browser.find_element_by_xpath(xPath))
        except Exception as exception :
            log.log(self.existsByXPath, 'Not possible to evaluate existance', exception=exception)
        return exists


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def findByXPath(self, xPath, browser) :
        element = None
        try :
            element = browser.find_element_by_xpath(xPath)
        except :
            element = browser.find_element_by_xpath(xPath.lower())
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return element


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def findAllByXPath(self, xPath, browser) :
        elementList = None
        try :
            elementList = browser.find_elements_by_xpath(xPath)
        except :
            elementList = browser.find_elements_by_xpath(xPath.lower())
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return elementList


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def accessByXPath(self, xPath, browser) :
        element = self.findByXPath(xPath, browser)
        element.click()
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT)
        return element


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def existsByClass(self, className, browser) :
        exists = False
        try :
            exists = ObjectHelper.isNotNone(browser.find_element_by_xpath(className))
        except Exception as exception :
            log.log(self.existsByClass, 'Not possible to evaluate existance', exception=exception)
        return exists


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def findByClass(self, className, browser) :
        element = None
        try :
            parsedClass = f'{c.DOT}{c.DOT.join(className.split())}'
            log.debug(self.findByClass, f'find_element_by_css_selector({parsedClass})')
            element = browser.find_element_by_css_selector(parsedClass)
        except :
            parsedClass = f'{c.DOT}{c.DOT.join(className.lower().split())}'
            log.debug(self.findByClass, f'find_element_by_css_selector({parsedClass})')
            element = browser.find_element_by_css_selector(parsedClass)
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return element


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def findAllByClass(self, className, browser) :
        elementList = None
        try :
            parsedClass = f'{c.DOT}{c.DOT.join(className.split())}'
            log.debug(self.findAllByClass, f'find_elements_by_css_selector({parsedClass})')
            elementList = browser.find_elements_by_css_selector(parsedClass)
        except :
            parsedClass = f'{c.DOT}{c.DOT.join(className.lower().split())}'
            log.debug(self.findAllByClass, f'find_elements_by_css_selector({parsedClass})')
            elementList = browser.find_elements_by_css_selector(parsedClass)
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return elementList


    @ClientMethod(requestClass=[str, webdriver.Chrome])
    def accessByClass(self, className, browser) :
        element = self.findByClass(className, browser)
        element.click()
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT)
        return element


    @ClientMethod(requestClass=[webdriver.Chrome])
    def acceptAlert(self, browser):
        alert = browser.switch_to.alert
        alert.accept()
        self.wait(DEFAULT_WEBDRIVER_TIMEOUT)


    @ClientMethod(requestClass=[webdriver.Chrome])
    def maximize(self, browser, force=False):
        if force:
            self.minimize(browser)
        browser.maximize_window()


    @ClientMethod(requestClass=[webdriver.Chrome])
    def minimize(self, browser) :
        browser.minimize_window()


    @ClientMethod(requestClass=[webdriver.Chrome])
    def close(self, browser) :
        try :
            browser.close()
        except Exception as exception :
            log.warning(self.close, 'Not possible to close browser properly', exception)
