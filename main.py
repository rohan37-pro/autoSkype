import selenium 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import time
import random
import json



## this is to make it platform independent....
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")

#to disable the extensions
options.add_argument("--disable-extensions")

options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })


if platform.system().lower() == 'linux':
    options.add_argument("--user-data-dir=cookies")
elif platform.system().lower() == "windows" :
    options.add_argument("--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\autoskype")

#loading 7 digit codes and store in a list
with open("doc/7digitcodes.txt", 'r') as file:
    code7digits = file.readlines()
    if len(code7digits)%3 != 0:
        print("warning: the number of codes in 7digitcodes.txt are not devided by 3")



# creating and opening browser with user data directory to save cookies
driver = webdriver.Chrome(options=options)
driver.get("https://web.skype.com/?openPstnPage=true")
time.sleep(0.5)


# check if logged in or not
try:
    driver.find_element('xpath', "//input[@name='loginfmt']").click()
    print("login in progress...")
    # login with credential from credential file
    with open("doc/credential.json", 'r') as file:
        credential = json.load(file)
        username = credential['username']
        password = credential['password']
    # enter username
    ActionChains(driver).send_keys(username).send_keys(Keys.ENTER).perform()
    # enter password
    time.sleep(1.5)
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "i0118")))
    element.click()
    ActionChains(driver).send_keys(password).send_keys(Keys.ENTER).perform()
    try:
        iShowSkip = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "iShowSkip")))
        iShowSkip.click()
    except Exception as error:
        print(error)
    try:
        idSIButton9 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        idSIButton9.click()
    except Exception as error:
        print(error)
    try:
        iCancel = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "iCancel")))
        iCancel.click()
    except Exception as error:
        print(error)
except Exception as error:
    pass
    print("already logged in...")



def dial_the_num(number ,code7digit):
    # wait for the dial pad to load and dial the call
    for i in range(5):
        try:
            driver.find_element('xpath', "//button[@title='Use dial pad']")
            break
        except:
            time.sleep(0.5)
    secs = [3,4,4.5,5,5.5,6]
    time.sleep(random.choice(secs))

    try:
        driver.find_element('xpath', "//button[@title='Audio Call']").click()
    except:
        driver.find_element('xpath', "//button[@title='Use dial pad']").click()
        time.sleep(random.uniform(0.6 , 0.7))
        #ActionChains(driver).send_keys(number).send_keys(Keys.ENTER).perform()
        
        pad = driver.find_element(By.XPATH ,'//div[@class = "inputGradient"]//input[@placeholder = "Phone number"]')
        for i in number:
            pad.send_keys(i)
            time.sleep(random.uniform(0.2 , 0.8))
        pad.send_keys(Keys.ENTER)

    # manual code for explicitly wait and check the button is clickable or not
    # waiting for 15 sec
    random_wait = random.randint(3,5)
    for i in range(30):
        try:
            try:
                error_popup = driver.find_element(By.XPATH , '//div[@data-text-as-pseudo-element = "Oops, something went wrong."]')
                message = serror_popup.get_attribute("data-text-as-pseudo-element")
                print(message)
                continue
            except:
                
            
                try:
                    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="reactxp-ignore-pointer-events"]//button[@aria-label = "Captions"]')))
                    print('The call has connected')
                except:
                    print("the call didin't go through")
                    continue
                finally:
                    time.sleep(2)
                    driver.find_element('xpath', "//button[@title='Enter numbers using the dial pad']").click()
                    driver.find_element('xpath', "//button[@title='Close']")
                    input_box = driver.find_element('xpath', "//input[@type='text']")
                    #locating the hash key element on the dial pad for clicking using xpath
                    the_hash_key = driver.find_element(By.XPATH , '//div[@data-text-as-pseudo-element = "#"]')
                    # enter the 7 digit codes from text file
                    time.sleep(5)
                    count = 1
                    for i in range(3):
                        for char in code7digits[i].strip():
                            print(f'the code being used is {char}')
                            input_box.send_keys(char)
                            time.sleep(random.uniform(0.5 , 0.6))
                        time.sleep(0.4)
                        the_hash_key.click()
                        count+=1
                        
                        if count == 4:
                            break
                        time.sleep(6)
                    
                    for i in range(2):
                        the_hash_key.click()
                        time.sleep(random.uniform(0.4 , 0.8))
                
        except:
            time.sleep(0.5)
#the xpath for the error message popup text //div[@data-text-as-pseudo-element = "Oops, something went wrong."]
# 7 digit code file handling....
print("dialing the number...")
with open('doc/phonenumber.txt','r') as file:
    number = file.read().strip()
codeptr = 0
for i in range(len(code7digits)//3) :
    tempcodelist = code7digits[codeptr : codeptr+3]
    if len(tempcodelist) < 3:
        tempcodelist = code7digits[-3:]
    # dial_the_call function call
    dial_the_num(number, tempcodelist)
    codeptr += 3

time.sleep(1000)
