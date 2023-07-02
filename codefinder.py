import selenium 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select
import platform
import time
import random
import json
from audioCaptcha import speech_rec


myProxy = "20.44.206.138:80"
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': ''})

## this is to make it platform independent....
options = webdriver.ChromeOptions()
options.proxy = proxy
options.add_argument("--disable-notifications")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")
#to disable the extensions
options.add_argument("--disable-extensions")

options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2, 
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })


if platform.system().lower() == 'linux':
    options.add_argument("--user-data-dir=cookies")
elif platform.system().lower() == "windows" :
    options.add_argument("--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\autoskype4")

#loading 7 digit codes and store in a list
with open("doc/7digitcodes.txt", 'r') as file:
    code7digits = file.readlines()
with open('doc/phonenumber.txt','r') as file:
    number = file.read().strip()

# creating and opening browser with user data directory to save cookies
driver = webdriver.Chrome(options=options)
driver.get("https://teleconference.uc.att.com/ecm/")
time.sleep(0.5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

pointer = 0
for code7 in code7digits:
    print('Putting  the phone number')
    phone_number_input = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , "//input[@id='bp']")))
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
    print('Working on the recaptcha bro')
    time.sleep(0.4)
    driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title='reCAPTCHA']"))
    #captcha = driver.find_element(By.XPATH , "//div[@class='recaptcha-checkbox-border']")
    captcha = WebDriverWait(driver , 3).until(EC.presence_of_element_located((By.XPATH , "//span[@id='recaptcha-anchor']")))
    time.sleep(0.2)
    captcha.click()
    driver.switch_to.default_content()
    time.sleep(4)
    driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title = 'recaptcha challenge expires in two minutes']"))
    #driver.switch_to.frame(recaptcha_box_iframe)
    time.sleep(0.6)
    audio_button = driver.find_element(By.XPATH , "//button[@id='recaptcha-audio-button']")
    audio_button.click()

    audio_src = WebDriverWait(driver , 3).until(EC.presence_of_element_located((By.XPATH , "//audio[@id='audio-source']")))
    the_audio_src = audio_src.get_attribute('src')

    print(f'The link to the audio is {the_audio_src} -------------------------------------- +++++ ')



    audio_to_text = speech_rec(the_audio_src)

    audio_captcha_input = driver.find_element(By.XPATH , "//input[@id='audio-response']")
    for i in audio_to_text:
        audio_captcha_input.send_keys(i)
        time.sleep(random.uniform(0.2 , 0.6))

    verify_button = driver.find_element(By.XPATH , "//button[@id='recaptcha-verify-button' and text()='Verify']")
    verify_button.click()
    driver.switch_to.default_content()


    time.sleep(1.2)
    print('Time to click on the CONTINUE BUTTON BRO +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    continue_button = driver.find_element(By.XPATH , "//button[@class='button button--appearance-square button--theme-dark button--role-none button--full-width button--enabled ' and text() = 'Continue']")
    continue_button.click()


    time.sleep(5)

    #correct id
    try:
        waiting_for_the_host = WebDriverWait(driver , 4).until(EC.presence_of_element_located((By.XPATH , "//div[@class='status__message']//p[text() = 'Waiting for host to join']")))
        print('A correct code is found')
        driver.refresh()
        time.sleep(5)
        
        #managing th e removal of the used code 
        pointer += 1
        with open('./doc/7digitcodes.txt' , 'w') as f:
            f.writelines(code7digits[pointer:])
            print('Code file updation complete')
        with open('./doc/rightcode.txt', 'w' ) as f:
            f.write(f'{code7}\n')
        
        
        continue
    except:
        try:
            driver.find_element(By.XPATH , "//div[@class='form__general-error-msg' and text()='Login failed. One or more of the credentials you entered is invalid.']")
            #managing th e removal of the used code 
            pointer += 1
            with open('./doc/7digitcodes.txt' , 'w') as f:
                f.writelines(code7digits[pointer:])
                print('Code file updation complete')

            
            continue
        except:
            print('This Aint no Login Failed Error Bruh Its something else : ->')
        
        finally:
            print('The Code was Incorrect Bro')
  

