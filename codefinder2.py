import selenium 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import platform
import time
import random
import json
from twocaptcha import solve_captcha
from connectionStatus import is_connected
from tqdm import tqdm


#loading 7 digit codes and store in a list
with open("doc/7digitcodes.txt", 'r') as file:
    code7digits = file.readlines()
#getting the phone number from the text file
with open('doc/phonenumber.txt','r') as file:
    number = file.read().strip()

service = Service(executable_path = 'chromedriver.exe')


options = webdriver.ChromeOptions()
#options = Options()
options.add_argument("--disable-notifications")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
#to disable the extensions
options.add_argument("--disable-extensions")


#this is to make it platform independent
if platform.system().lower() == 'linux':
    options.add_argument("--user-data-dir=cookies")
elif platform.system().lower() == "windows" :
    options.add_argument("--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 6")


def main(code7):
    target_site = "https://teleconference.uc.att.com/ecm/"
    driver = webdriver.Chrome(service=service , options=options)
    driver.get(target_site)

    phone_number_input = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , "//input[@id='bp']")))
    print('Page Load Succeeded')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    actions = ActionChains(driver).send_keys(Keys.END).perform()
   
    print('Putting  the phone number')

    phone_number_input.click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
    for num in number[1:]:
        phone_number_input.send_keys(num)
        time.sleep(random.uniform(0 , 0.3))
    print('Phone number DONE')


    id_input = driver.find_element(By.XPATH , "//input[@id='mac']")
    id_input.click()
    print('Putting the CODE')
    print(f'The Code Being used is {code7.strip()[:-1]} -------- {len(code7digits)} remaining to test')
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
    for code in code7.strip()[:-1]:
        id_input.send_keys(code)
        time.sleep(random.uniform(0.1 , 0.3))
    time.sleep(random.uniform(0.3 , 1.2))
    print('CODE DONE Bruv')


    print('TIme to put the name bro')
    name_input = driver.find_element(By.XPATH , "//input[@id='userName']")
    name_input.click()
    name = 'roger'
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
    for i in name:
        name_input.send_keys(i)
        time.sleep(random.uniform(0.1 , 0.4))
    print('Name DONE Bruv')
    #time.sleep(120) --------------------------------------------------------------------------------------------------------------------
    print('scraping the source (SRC) attribute from the recaptcha frame')
    iframe = driver.find_element(By.XPATH , "//iframe[@title='reCAPTCHA']")
    iframe_src = iframe.get_attribute('src')
    print(iframe_src)
    solved_captcha = solve_captcha(iframe_src , target_site)
    #print(f'The extracte sitekey is {}')
    #locating the captcha text area
    
    #driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title='reCAPTCHA']"))
    #driver.switch_to.default_content()
    #captcha_text_area = driver.find_element(By.XPATH , "//textarea[@id='g-recaptcha-response']")
    #captcha_text_area.clear()
    #driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
    google_captcha_response_input = driver.find_element(By.ID, 'g-recaptcha-response')
    time.sleep(1)
    driver.execute_script("arguments[0].setAttribute('style','type: text; visibility:visible;');",google_captcha_response_input)
    #driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = arguments[0]', solved_captcha)
    
    
    #google_captcha_response_input.send_keys(solved_captcha)
    #driver.execute_script("arguments[0].setAttribute('style', 'display:none;');",google_captcha_response_input)
    #google_captcha_response_input.submit()
    #driver.execute_script(f"document.getElementById('g-recaptcha-response').value = '{solved_captcha}';")
    #driver.execute_script("arguments[0].value = arguments[1];", captcha_text_area, solved_captcha)
    time.sleep(2)
    continue_button = driver.find_element(By.XPATH , "//button[text()='Continue']")
    time.sleep(0.2)
    driver.execute_script("arguments[0].removeAttribute('disabled');", continue_button)
    print('The Continue button has been enabled')
    time.sleep(0.4)
    #continue_button.click()
    time.sleep(1)
    time.sleep(120)

if __name__ == '__main__':
    main(code7digits[0])