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
        time.sleep(0.5)
        ActionChains(driver).send_keys(number).send_keys(Keys.ENTER).perform()
    
    # manual code for explicitly wait and check the button is clickable or not
    # waiting for 15 sec
    for i in range(30):
        try:
            driver.find_element('xpath', "//button[@title='Enter numbers using the dial pad']").click()
            driver.find_element('xpath', "//button[@title='Close']")
            input_box = driver.find_element('xpath', "//input[@type='text']")
            # enter the 7 digit codes from text file
            for i in range(3):
                input_box.send_keys(code7digits[i].strip() + '#')
                time.sleep(1)
            input_box.send_keys('##')
            
        except:
            time.sleep(0.5)

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
