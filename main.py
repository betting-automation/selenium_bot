import json
from chrome_loader import get_chromedriver

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('settings.json', 'r') as f:
        data = json.loads(f.read())
        proxy = data['PROXY']
        CHROME_DRIVER_PATH = data['CHROMEDRIVER_PATH']
        driver = get_chromedriver(proxy=proxy, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
        driver.get('https://api.myip.com')
        input('Please press enter on CMD or terminal to close the browser, or you can also simply close the CMD or Terminal::\n\n\n\n\n\n\n ')
        print('Closing Browser')
