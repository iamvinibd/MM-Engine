from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time,re


def start():
    global driver
    options = Options()
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'download.default_directory': r'D:\test\\',
        'profile': {
            'password_manager_enabled': False
            }
            })
    #options.add_argument('--incognito')
    #options.add_argument('start-fullscreen')
    #options.add_argument('download.default_directory=D:/test')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\vinicius.diniz\PycharmProjects\MM Engine\chromedriver.exe')
    driver.get('http://gpdmmc.lge.com/lge-gpdm-mc/requestPowerView.do?requestNo=RST-2102-00230')
    #driver.maximize_window()

    url = driver.command_executor._url
    session_id = driver.session_id
    print(url,session_id)
    return url,session_id


def download(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    element = driver.find_element_by_xpath('//*[@id="isc_61table"]/tbody/tr')
    element.location_once_scrolled_into_view
    time.sleep(0.5)
    row_count = len(driver.find_elements_by_xpath('//*[@id="isc_61table"]/tbody/tr'))
    for row in range(1,row_count):
        print(row)
        try:
            usageDescription = driver.find_element_by_xpath('//*[@id="isc_61table"]/tbody/tr[%x]/td[4]' % row).text
        except Exception as e:
            print(e)
        print(usageDescription)
        if usageDescription == 'LG_FOTA(.up)' or usageDescription == 'FILE_FULL IMAGE(.mot,.zip)' or \
                usageDescription == 'FILE_WEB IMAGE1/2(.cab,.exe,.kdz,.gdz)' or usageDescription == '02. Model Spec' or \
                usageDescription == '01. General Information':
            try:
                download_button = driver.find_element_by_xpath('//*[@id="isc_61table"]/tbody/tr[%x]/td[2]' % row)
                download_button.click()
            except Exception as e:
                print(e)
            time.sleep(0.8)

def validationMaster(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="LmainMenu"]')))
    except:
        print("Elemento não encontrado")
    finally:
        swValidationButton = driver.find_element_by_xpath('// *[ @ id = "LmainMenu"] / li[4] / span')
        swValidationButton.click()
        time.sleep(4)
        """swValidationTab = driver.find_element_by_xpath("/html/body")
        viewStatus = driver.find_element_by_xpath('//*[@id="top"]/div')
        viewStatus.click()
        time.sleep(4)"""

        validationMaster = swValidationButton.find_element_by_xpath('//*[@id="a_363"]')
        validationMaster.click()

#start()

#download('http://127.0.0.1:59870 ', 'a376f89ee9de897399a4b035e6bd1380')

#validationMaster('http://127.0.0.1:59870 ', 'a376f89ee9de897399a4b035e6bd1380')

def mirrorPoint(executor_url, session_id, shortFriday):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute


    window_before = driver.window_handles[0]
    hour = [0,0,'0800','1200','1300','1757']
    #rowQuantitie = len(driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/table/tbody/tr')) # quantidade de linhas na coluna
    try:
        for row in range(3,5):
            day = driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/table/tbody/tr[%x]/td[3]/font' % row).text
            if day != 'Sab' and day != 'Dom':
                data = driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/table/tbody/tr[%x]/td[1]/font/u' % row).text
                data = re.sub('/','',data)
                print(data)
                print(day)
                if data != shortFriday:
                    addHour = driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/table/tbody/tr[%x]/td[11]/a' % row).click()
                    time.sleep(3)
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    for x in range(2,5):
                        situation = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[%x]/td[4]' % x).text
                        if len(situation) == 0:
                            dataField = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[%x]/td[1]/input' % x)
                            dataField.send_keys(data + Keys.TAB)
                            time.sleep(3)
                            hourField = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[%x]/td[2]/input' % x)
                            hourField.send_keys(hour[x])
                            print(hour[x])
                            time.sleep(3)
                            add = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[5]/a').click()
                            time.sleep(3)
                        else:
                            #exit = driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/a').click()
                            driver.switch_to.window(window_before)
                            time.sleep(3)
                            break
    except Exception as e:
        driver.switch_to.window(window_before)
        print(e)







    """addHour.click()
    print(cor)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    data = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[2]').text
    exit = driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/a').click()
    driver.switch_to.window(window_before)
    print(data)
    time.sleep(3)
    addHour = driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/table/tbody/tr[4]/td[11]/a').click()"""

#mirrorPoint('http://127.0.0.1:60920', '7d27bab5c2a91bc6d879dbbddd55cbdc','08/01/2021')