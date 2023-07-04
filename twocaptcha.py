import requests
from pprint import pprint
import json
import time   
import pyperclip
iframe_src = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-&co=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbTo0NDM.&hl=en&v=khH7Ei3klcvfRI74FvDcfuOo&size=normal&sa=action&cb=qznn2r8a141c"


def count_down(lim):
    for i in range(lim):
        print(f'{lim - i} seconds to go')
        time.sleep(1)


def solve_captcha(iframe_src , site):
    with open('twocaptchakey.txt' , 'r' , encoding = 'utf-8') as f:
        cap_key = f.read()
    print(f' The Twocaptcha api key is {cap_key}')
    iframe_recapthca_src = iframe_src
    site_key = iframe_recapthca_src.split('&')[1][2:]
    
    request_string = f"http://2captcha.com/in.php?key={cap_key}&method=userrecaptcha&googlekey={site_key}&pageurl={site}"
    
    res = requests.get(request_string)
    data = res.text
    res_status = res.status_code
    pprint(data)
    
    
    if 'OK' in data:
        loop_status = True
        while loop_status:
            count_down(5)
            the_captcha_response_request= f"http://2captcha.com/res.php?key={cap_key}&action=get&id={data[3:]}"
            response = requests.get(the_captcha_response_request)
            status = response.status_code
            print(response.text)
            pyperclip.copy(response.text)
            if status == 200:
                if response.text == 'CAPCHA_NOT_READY':
                    print('The Captcha Not Ready yet bro : - >')
                    continue
                print('The Captcha has been solved')
                solved_captcha = response.text
                pyperclip.copy(solved_captcha)
                break
            else:
                print('The captcha wasnt solved trying again')
                continue
    return solved_captcha.split('|')[1]






if __name__ == '__main__':
    solve_captcha(iframe_src , "https://www.google.com/recaptcha/api2/demo")