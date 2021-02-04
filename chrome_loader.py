import os
import random
import zipfile
import json
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType
from selenium import webdriver

operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value]
hardware_types = [
    HardwareType.COMPUTER.value
]
software_names = [SoftwareName.CHROME.value, SoftwareName.CHROMIUM.value, SoftwareName.FIREFOX.value]


def get_chromedriver(proxy, CHROME_DRIVER_PATH):
    PROXY_HOST = proxy.split('@')[1].split(':')[0]
    PROXY_PORT = proxy.split('@')[1].split(':')[1]
    PROXY_USER = proxy.split('@')[0].split(':')[0]
    PROXY_PASS = proxy.split('@')[0].split(':')[1]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    user_agent_rotator = UserAgent(operating_systems=operating_systems, hardware_types=hardware_types, software_names=software_names, limit=100)
    userAgent = user_agent_rotator.get_random_user_agent()

    print('User agent:', userAgent)

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_GB'})
    chrome_options.add_argument('--lang=es')

    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {"credentials_enable_service", False}
    prefs = {"profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })
    #
    if proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)

    driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
	Object.defineProperty(navigator, 'maxTouchPoints', {
	get: () => 1
	})
	"""
    })
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": userAgent})

    driver.set_window_position(0, 0)
    random_width = random.randint(1700, 1920)
    random_height = random.randint(900, 1080)
    print(f'Width: {random_width}, Height: {random_height}')
    driver.set_window_size(random_width, random_height)
    return driver
