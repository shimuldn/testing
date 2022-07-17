

import os, sys, time, random
uid=os.environ['UID']
apikey=os.environ['API_KEY']
BASE_URL=os.environ['BASE_URL']
api_url=BASE_URL+'solve'
fb_url=BASE_URL+'feedback'

total_task=50


start_ts=time.time()
tt=random.uniform(3, 7)
end_ts=start_ts+ int(tt*60)


import undetected_chromedriver as uc
from urllib.parse import urlparse
from selenium import webdriver
import re, requests, json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)

total_t=[]
s_time=time.time()

# base_url='https://jd2020f.herokuapp.com'
# base_url = 'https://solve.shimul.me'
# base_url='https://shimuldn-hcaptcha-backend-5v5p44w4fv5qj-5050.githubpreview.dev'


sites = ['https://shimuldn.github.io/hcaptcha/', 'https://shimuldn.github.io/hcaptcha/2',
  'https://shimuldn.github.io/hcaptcha/3', 'https://shimuldn.github.io/hcaptcha/4',
  'https://shimuldn.github.io/hcaptcha/5', 'https://shimuldn.github.io/hcaptcha/oracle',
  'https://shimuldn.github.io/hcaptcha/discord', 'https://shimuldn.github.io/hcaptcha/epic',]
#    'https://signup.cloud.oracle.com/?sourceType=_ref_coc-asset-opcSignIn&language=en_US']

def main():
    try:
        options = webdriver.ChromeOptions()
        # options.binary_location = "C:\\Users\\ROG\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
        # options.binary_location = "C:\\Users\\ROG\\Documents\\Chromium-Portable-win64-codecs-sync-oracle\\bin\\chrome.exe"
        # options.binary_location="/usr/games/chromium-bsu"
        # options.add_argument("start-maximized")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--lang=en_US')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        # driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path='/home/ubuntu/python/chromedriver')
        # print("Before driver")
        driver = uc.Chrome(options=options, use_subprocess=True)
        # print(driver)


        def face_the_checkbox():
            # print("face_the_checkbox")
            try:
                WebDriverWait(driver, 8, ignored_exceptions=WebDriverException).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title,'checkbox')]"))
                )
                return True
            except TimeoutException:
                return False

        def get_site_key():
            for i in range(10):
                try:
                    obj = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                                    EC.presence_of_element_located((By.XPATH, "//div[@class='h-captcha']"))
                                )
                    key=obj.get_attribute("data-sitekey")
                    return key
                except:
                    time.sleep(0.03)
                    pass
        def handle_checkbox():
            for i in range(5):
                try:
                    time.sleep(1)

                    WebDriverWait(driver, 2, ignored_exceptions=ElementNotVisibleException).until(
                        EC.frame_to_be_available_and_switch_to_it(
                            (By.XPATH, "//iframe[contains(@title,'checkbox')]")
                        )
                    )
                
                    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "checkbox"))).click()
                    driver.switch_to.default_content()
                    HOOK_CHALLENGE = "//iframe[contains(@title,'content')]"
                    WebDriverWait(driver, 15, ignored_exceptions=ElementNotVisibleException).until(
                            EC.frame_to_be_available_and_switch_to_it((By.XPATH, HOOK_CHALLENGE))
                        )
                    time.sleep(1)
                    return True
                except:pass

        def get_target():
            for i in range(3):
                try:
                    tg = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                            EC.presence_of_element_located((By.XPATH, "//h2[@class='prompt-text']"))
                        )
                    return tg.text
                except:
                    pass
            return False

        def get_data_for_api():
            for i in range(5):
                try:
                    # print("getting images data")
                    WebDriverWait(driver, 10, ignored_exceptions=ElementNotVisibleException).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='task-image']"))
                        )
                    images_div = driver.find_elements(By.XPATH, "//div[@class='task-image']")
                    image_data={}

                    # Getting the data for api server format
                    if len(images_div) == 9:
                        for item in images_div:
                            name=item.get_attribute("aria-label")
                            number=int(name.replace("Challenge Image ", ""))-1
                            image_style = item.find_element(By.CLASS_NAME, "image").get_attribute("style")
                            url = re.split(r'[(")]', image_style)[2]
                            image_data[number]=url
                        # print(image_data)
                        return image_data
                    else:
                        # print("images len not 9")
                        pass
                except:
                    time.sleep(1)


        def do_the_magic(site_key, target):
            # site_key=get_site_key()
            
            images=get_data_for_api()
            # print(images)
            site = urlparse(driver.current_url).netloc

            required_data={}
            required_data['target']=target
            required_data['data_type']='url'
            required_data['site_key']=site_key
            required_data['site']=site
            required_data['images']=images
            ta=[]
            t0=time.time()
            r = requests.post(url = api_url, headers={'Content-Type': 'application/json',
            'uid': uid, 'apikey': apikey}, data = json.dumps(required_data))


            # Clicking the images to solve the captcha
            # ta.append(time.time() - t0)
            
            # print(f'API took {round(sum(ta), 2)}seconds to response. Result {r.json()["status"]}')

            if r.json()["status"] == "new":
                images_div = driver.find_elements(By.XPATH, "//div[@class='task-image']")
                time.sleep(1)
                for i in range(20):
                    st_res=requests.get(r.json()["url"])
                    if st_res.json()['status'] == "solved":
                        for item in images_div:
                            nn=int(item.get_attribute("aria-label").replace("Challenge Image ", ""))-1
                            if nn in st_res.json()['solution']:
                                
                                # time.sleep(random.uniform(0.1, 0.5))
                                item.click()
                        # print("clicking done")
                        break
                    elif st_res.json()['status'] == "in queue'":
                        time.sleep(1)
            

            # time.sleep(1)
            WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='button-submit button']"))
            ).click()

            time.sleep(1)
            
            try:
                error_txt=WebDriverWait(driver, 1, 0.1).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@class='error-text']"))
                )
                print(f'error found {error_txt.text}')



                if error_txt.text == "Please try again.":
                    # id=r.json()['id']
                    # print(id)
                    fb={"id": r.json()['id'], "feedback": "False"}
                    requests.post(url = fb_url, headers={'Content-Type': 'application/json',
            'uid': uid, 'apikey': apikey}, data = json.dumps(fb))
                    # pass
            except:
                tg=re.split(r"containing a", target)[-1][1:].strip()
                ta.append(time.time() - t0)
                print(f"Successfully solved {tg} in {round(sum(ta), 2)}seconds")

            for i in range(5):
                try:
                    WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='task-image']"))
                    )
                    # solve_hcaptcha(driver, EC)
                    # print("There is more")
                    # time.sleep(10)
                    if get_target() != False:
                        target=get_target()
                        do_the_magic(site_key, target)
                except:
                    # print("hcaptcha Solved successfully", target)
                    break

        for i in range(total_task):
            print(f"Starting {i}")
            driver.get(random.choice(sites))

            if not face_the_checkbox:
                break
            site_key=get_site_key()
            handle_checkbox()
            if get_target() != False:
                target=get_target()
                do_the_magic(site_key, target)
            
            if int(time.time()) > end_ts:
                print("Timeout closing the browser")
                driver.close()
            else:
                print("Not time out yet")
        
        ## Close the browser

        total_t.append(time.time() - s_time)
        print(f"{total_task} done in {(round(sum(total_t), 2))/60}m. Closing browser.")
        driver.close()


    except Exception as _e:
        print(_e)
        print("Error closing browser.")
        # driver.close()

main()
