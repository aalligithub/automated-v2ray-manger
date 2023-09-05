import selenium
import json
import os
import sys
from os import path
from time import sleep
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

print("""
        ____                      ___             __ _           ___       _ _     _           
 /\   /\___ \ _ __ __ _ _   _    / __\___  _ __  / _(_) __ _    / __\_   _(_) | __| | ___ _ __ 
 \ \ / / __) | '__/ _` | | | |  / /  / _ \| '_ \| |_| |/ _` |  /__\// | | | | |/ _` |/ _ \ '__|
  \ V / / __/| | | (_| | |_| | / /__| (_) | | | |  _| | (_| | / \/  \ |_| | | | (_| |  __/ |   
   \_/ |_____|_|  \__,_|\__, | \____/\___/|_| |_|_| |_|\__, | \_____/\__,_|_|_|\__,_|\___|_|   
                        |___/                          |___/                            
""")

# opening the config file and checking if it empty
with open('config.json', 'r') as file:
    config=json.load(file)
    print(colored('Make sure you fill the config.json file with your information!', 'magenta'))


xui_ip_address = config["address"]["ip"]
xui_port_number = config["address"]["port"]
xui_username = config["credentials"]["username"]
xui_password = config["credentials"]["password"]
tls_domain = config["config"]["domain"]
tls_private_key = config["config"]["private_key"]
tls_public_key = config["config"]["public_key"]
config_remark = config["config"]["remark"]

url = 'http://' + xui_ip_address + ':' + xui_port_number

class Webdriver_setup():        
    def chromedriver_setup():
        # Configuring chromedriver, Detaching to keep browser open, Blocking all cookies by default, Disable password saver popup comment this if you want the password to save to your google account
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
        options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        driver = webdriver.Chrome(options=options)
        print(colored('Webdriver configured!', 'green'))
        return driver
        
    def firefoxdriver_setup():
        # check the webdriver and set it up here
        pass


class xui_manager:
    def login_xui(driver):
        # xpath of elements in the website for the webdriver to find
        xpath_username_field = "//input[@placeholder='username']"
        xpath_password_field = "//input[@placeholder='password']"
        xpath_login_button = '//*[@id="app"]/main/div[2]/div/form/div[3]/div/div/span/button'
        class_failedlogin_notice = 'ant-message'

        # waiting for elements to load before yielding a timeout
        wait = WebDriverWait(driver, 5)

        # loading the xui manager url with the driver
        driver.get(url)

        print(colored('Logging into v2ray XUI...', 'green'))
        # finding credential inputs and login button and loging in
        try:
            driver_username_input = driver.find_element(By.XPATH, xpath_username_field)
            driver_password_input = driver.find_element(By.XPATH, xpath_password_field)
            driver_login_button = driver.find_element(By.XPATH, xpath_login_button)
            
        except NoSuchElementException:
            print(colored('Username Input xpath was not found, waiting for it to load', 'red'))
            try:
                driver_username_input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_username_field)))
                driver_username_input = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_password_field)))
                driver_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_login_button)))

            except:
                print(colored('Element not found make sure your connection is ok and try again', 'red'))
                exit()
                
        # probably never raised
        except TimeoutException:
            print(colored('Looking for element timed out make sure your connection is ok and try again', 'red'))
            exit()

        else:
            print(colored('Inputing credentials...', 'green'))
            driver_username_input.send_keys(xui_username)
            driver_password_input.send_keys(xui_password)
            driver_login_button.click()

            # checking if the username and password were correct by checking if an error message shows up
            try:
                wait.until(EC.url_contains('xui'))
                
            except:
                print(colored('Credentials were incorrect check your username and password and input them in config file', 'red'))
                exit()

            else:
                print(colored('Login successful', 'green'))


    def make_multiple_configs(driver, encryption, number_of_configs, remark, traffic):
        xpath_inbound = '//*[@id="sider"]/div/ul/li[2]'
        xpath_plus_button = '//*[@id="content-layout"]/main/div/div/div[2]/div[1]/div/div/div/button'
        xpath_remark_input = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[2]/div/span/input'
        xpath_trafficflow_input = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[1]/div[6]/div[2]/div/span/div/div[2]/input'
        xpath_done_button = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[3]/div/button[2]'
        xpath_combobox = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[3]/div/div[2]/div/span/div/div'
        xpath_kcp_inlist = "//*[@class='ant-select-dropdown-menu-item' and contains(text(),'kcp')]"
        xpath_tls_button = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[5]/div/div[2]/div/span/button'
        xpath_domain_input = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[6]/div[1]/div[2]/div/span/input'
        xpath_public_key_input = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[6]/div[3]/div[2]/div/span/input'
        xpath_private_key_input = '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[6]/div[4]/div[2]/div/span/input'
        xpath_last_config = '//*[@id="content-layout"]/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr[last()]'

        wait = WebDriverWait(driver, 5)

        # pressing the inbound menu button
        try:
            inbound_click = driver.find_element(By.XPATH, xpath_inbound)
            
        except TimeoutException:
            print(colored('a timeout ocourred element was not found, please check your internet connection and try again...', 'red'))

        except:
            inbound_click = wait.until(EC.element_to_be_clickable(By.XPATH, xpath_inbound))

        else:
            inbound_click.click()
            print(colored('Inbound click pressed successfully', 'green'))

        # writing a loop to create multiple configs
        for i in range(number_of_configs):
            print('Making config number: ' + str(i + 1))

            # pressing plus button to create new config
            driver.find_element(By.XPATH, xpath_plus_button).click()
            print(colored('Plus button clicked successfully', 'green'))

            # since the elements load together we only wait for the first one we need, inputting the remark
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_remark_input))).send_keys(remark)
            print(colored('Remark entered successfully', 'green'))

            # entering traffic flow
            driver.find_element(By.XPATH, xpath_trafficflow_input).send_keys(traffic)
            print(colored('Traffic flow entered successfully', 'green'))
        
            if encryption == 'TCP':
                # pressing tls button
                driver.find_element(By.XPATH, xpath_tls_button).click()                
                print(colored('Tls button entered successfully', 'green'))

                # since the elements load together we only wait for the first one we need, inputting domain address
                wait.until(EC.presence_of_element_located((By.XPATH, xpath_domain_input))).send_keys(tls_domain)
                print(colored('Domain address entered successfully', 'green'))

                # inputing public key
                driver.find_element(By.XPATH, xpath_public_key_input).send_keys(tls_public_key)
                print(colored('Public key input entered successfully', 'green'))

                # inputing private key
                driver.find_element(By.XPATH, xpath_private_key_input).send_keys(tls_private_key)
                print(colored('Private key entered successfully', 'green'))

            elif encryption == 'KCP':
                # selecting kcp
                driver.find_element(By.XPATH, xpath_combobox).click()   
                print(colored('KCP chosen successfully', 'green')) 
                
                # since the elements load together we only wait for the first one we need, pressing kcp inlist
                wait.until(EC.presence_of_element_located((By.XPATH, xpath_kcp_inlist))).click() 
                print(colored('KCP chosen successfully', 'green'))  

            # pressing done button
            driver.find_element(By.XPATH, xpath_done_button).click()
            print(colored('Done button pressed successfully', 'green'))

            # waiting for up to 10 seconds untill the new config to finish saving
            sleep(3)
            # sleep for now until debuging is finished
            # for i in range(10):
            #     try:
            #         WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath_last_config)))
            #     except TimeoutError:
            #         continue
            #     else:
            #         break
            # else:
            #     # place holder
            #     print(colored('New config didnt save there must be a problem with your connection', 'red'))


    def export_config(driver):
        xpath_inbound = '//*[@id="sider"]/div/ul/li[2]'
        xpath_add_inbound_x_button = '//*[@id="inbound-modal"]/div[2]/div/div[2]/button'

        driver.get_url(url + '/xui/inbounds')

        # pressing the inbound menu button
        try:
            inbound_click = driver.find_element(By.XPATH, xpath_inbound)
            
        except NoSuchElementException:
            inbound_click = wait.until(EC.element_to_be_clickable(By.XPATH, xpath_inbound))

        except TimeoutException:
            print(colored('Internet connection inturupted, check your connection and try again', 'red'))
            exit()

        else:
            inbound_click.click()
            print(colored('Inbound click pressed successfully', 'green'))

        driver.find_element(By.XPATH, xpath_add_inbound_x_button).click()
        # work in progress
    
    def delete_configs(driver, number_of_deleted):
        # add delete from first and delete from last
        # fix unreliable xpath
        xpath_inbound = '//*[@id="sider"]/div/ul/li[2]'
        # this xpath selects the latest config and goes up
        xpath_last_config_delete = '//*[@id="content-layout"]/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr[last()]/td[1]'
        # this xpath selects the first config and goes up
        xpath_last_config_delete = '//*[@id="content-layout"]/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr[first()]/td[1]'

        xpath_config_delete_button = "/html/body/div[4]/div/div/ul/li[4]/span/i"
        xpath_config_delete_button_confirm = '/html/body/div[6]/div/div[2]/div/div[2]/div/div/div[2]/button[2]'

        wait = WebDriverWait(driver, 5)

        # pressing the inbound menu button
        try:
            inbound_click = driver.find_element(By.XPATH, xpath_inbound)
            
        except NoSuchElementException:
            inbound_click = wait.until(EC.element_to_be_clickable(By.XPATH, xpath_inbound))

        except TimeoutException:
            print(colored('Internet connection inturupted, check your connection and try again', 'red'))
            exit()

        else:
            inbound_click.click()
            print(colored('Inbound click pressed successfully', 'green'))

        for i in range(number_of_deleted): 
            # xpath is wrong non functional code, working on custom xpath
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_last_config_delete))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(27) > div > div > ul > li:nth-child(4)"))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(29) > div > div.ant-modal-wrap > div > div.ant-modal-content > div > div > div.ant-modal-confirm-btns > button.ant-btn.ant-btn-primary"))).click()

            print(colored('Config deleted\n', 'green'))
            sleep(3)


if __name__ == "__main__":  
    driver = Webdriver_setup.chromedriver_setup()

    xui_manager.login_xui(driver)

    # debug
    xui_manager.delete_configs(driver, 20)

    while True:
        match input(colored("\nFor config building input 1, To export all configs input 2, input 3 to delete configs, input 4 to exit...\n", 'magenta')):
            #   case 1, building configs
            case "1":                
                while True:
                    number_of_configs = input(colored("Enter how many configs you want (if you made a mistake input N)\n", 'yellow'))
                    trafficflow = input(colored("Enter how much traffic flow cap you want (if you made a mistake input N)\n", 'yellow'))

                    if not number_of_configs.isdigit() or not trafficflow.isdigit():
                        print(colored('Try inputing a number\n', 'red'))
                        continue

                    match input(colored("For KCP configs input 1, for TCP configs input 2...\n", 'cyan')):
                        case "1":
                            xui_manager.make_multiple_configs(driver, 'KCP', int(number_of_configs), config_remark, trafficflow)
                        
                        case "2":
                            xui_manager.make_multiple_configs(driver, 'TCP', int(number_of_configs), config_remark, trafficflow)
                        
                        case _:
                            print(colored('Enter a valid input, For KCP configs input 1, for TCP configs input 2...', 'red'))

            # case 2, exporting configs
            case "2":
                # xui_manager.export_config(driver)
                print(colored('Export configs not finished yet', 'red'))
            
            # case 3 deleting configs
            case "3":
                number_of_deleted = input(colored("Input how many configs you want deleted\n", 'cyan'))
                if number_of_deleted.isdigit:
                    xui_manager.delete_configs(driver, int(number_of_deleted))
                else:
                    print(colored('Please enter a number', 'red'))
                    continue

            # case 4, exiting
            case "4":
                print(colored("Goodbye!", "red"))
                break
                SystemExit()

            case _:
                print(colored("Input something between 1-3...", "red"))