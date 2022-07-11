# pip install undetected_chromedriver selenium
import time, random, os, sys



uid=os.environ['UID']
apikey=os.environ['API_KEY']




import undetected_chromedriver as uc
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

print("Starting.........")

base_url='https://jd2020f.herokuapp.com'
# base_url = 'https://solve.shimul.me'
# base_url='https://shimuldn-hcaptcha-backend-5v5p44w4fv5qj-5050.githubpreview.dev'


website='https://shimuldn.github.io/hCaptchaSolverApi/demo_data/demo_sites/2/index.html'
website='https://shimuldn.github.io/hCaptchaSolverApi/demo_data/demo_sites/3/index.html'
website='https://shimuldn.github.io/hCaptchaSolverApi/demo_data/demo_sites/4/index.html'
website='https://signup.cloud.oracle.com/?sourceType=_ref_coc-asset-opcSignIn&language=en_US'

sites = ['https://shimuldn.github.io/hcaptcha/', 'https://shimuldn.github.io/hcaptcha/2',
  'https://shimuldn.github.io/hcaptcha/3', 'https://shimuldn.github.io/hcaptcha/4',
  'https://shimuldn.github.io/hcaptcha/5', 'https://shimuldn.github.io/hcaptcha/oracle',
  'https://shimuldn.github.io/hcaptcha/discord', 'https://shimuldn.github.io/hcaptcha/epic', 'https://signup.cloud.oracle.com/?sourceType=_ref_coc-asset-opcSignIn&language=en_US']

def main():
    try:
        options = webdriver.ChromeOptions()
        # options.binary_location = "C:\\Users\\ROG\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
        # options.binary_location = "C:\\Users\\ROG\\Documents\\Chromium-Portable-win64-codecs-sync-oracle\\bin\\chrome.exe"
        # options.binary_location="/usr/games/chromium-bsu"
        options.add_argument("start-maximized")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        options.add_argument('--disable-dev-shm-usage')
        # driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path='/home/ubuntu/python/chromedriver')
        # print("Before driver")
        try:
            driver = uc.Chrome(options=options, use_subprocess=True)
        except:
            python = sys.executable
            os.execl(python, python, *sys.argv)

        def handle_checkbox(driver):
            # print("Handling checkbox...")
            try:
                driver.get(random.choice(sites))
                # driver.get('https://accounts.hcaptcha.com/demo?sitekey=72c1c641-f24b-4749-b3fd-7955dca2c651&secret=0xcc480ac03eB7723e2471c292b2B7D4544519C49B')
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
            except:pass

        def solve_hcaptcha(driver, EC):
            # print("solve_hcaptcha.....")
            try:
                # print("Solving hcaptcha")
                _obj = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                    EC.presence_of_element_located((By.XPATH, "//h2[@class='prompt-text']"))
                )
                time.sleep(1)
                target=re.split(r"containing a", _obj.text)[-1][1:].strip()
                # print(f'hcaptcha target {target}')

                WebDriverWait(driver, 10, ignored_exceptions=ElementNotVisibleException).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='task-image']"))
                )
                images_div = driver.find_elements(By.XPATH, "//div[@class='task-image']")

                image_data={}

                # Getting the data for api server format
                for item in images_div:
                    name=item.get_attribute("aria-label")
                    number=int(name.replace("Challenge Image ", ""))-1
                    image_style = item.find_element(By.CLASS_NAME, "image").get_attribute("style")
                    url = re.split(r'[(")]', image_style)[2]
                    image_data[number]=url

                
                full_url=base_url+'/solveww?target='+target+'&site='+driver.current_url+'&data_type=image'
                

                # Sending the request to api server
                # print("Sending request to api server")
                ta=[]
                t0=time.time()
                r = requests.get(url = full_url, headers={'Content-Type': 'application/json', 'uid': uid, 'apikey': apikey}, data = json.dumps(image_data))

                # printing the response from api server
                # print(f'Response received from api server {r.json()}')

                # Clicking the images to solve the captcha
                ta.append(time.time() - t0)
                
                print(f'API took {round(sum(ta), 2)}seconds to response. Result {r.json()["success"]} targer {target}')
                if r.json()['success'] == True:
                    # print(f'Response received from api server {r.json()["success"]}. Result {r.json()["solution"]}')
                    for item in images_div:
                        name=item.get_attribute("aria-label")
                        nn=int(name.replace("Challenge Image ", ""))-1
                        if r.json()['solution'][str(nn)]:
                            time.sleep(0.05)
                            item.click()
                    
                    WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='button-submit button']"))
                    ).click()


                    try:
                        error_txt=WebDriverWait(driver, 1, 0.1).until(
                            EC.visibility_of_element_located((By.XPATH, "//div[@class='error-text']"))
                        )
                        print(f'error found {error_txt}')
                    except:
                        pass


                    for i in range(5):
                        try:
                            WebDriverWait(driver, 1).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@class='task-image']"))
                            )
                            solve_hcaptcha(driver, EC)
                        except:
                            print("hcaptcha Solved successfully", target)
                            break
                else:
                    print("This target can't be sloved for now.", target, (r.json()['success']))
            except:pass



        def is_challenge_image_clickable(driver):
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='task-image']"))
                )
                return True
            except TimeoutException:
                return False
        



        # while True:
        #     handle_checkbox(driver)
        #     solve_hcaptcha(driver, EC)


        for i in range(20):
            # print(f'Doing {i}')
            handle_checkbox(driver)
            solve_hcaptcha(driver, EC)
        
        print("all done")
        driver.close()
#         python = sys.executable
#         os.execl(python, python, *sys.argv)


        # print(is_challenge_image_clickable(driver))
        # if is_challenge_image_clickable(driver):
        #     solve_hcaptcha(driver, EC)
        # else:
        #     print("All done here")
        #     driver.close()
    except:
        print("restarting the things")
        driver.close()
        python = sys.executable
        os.execl(python, python, *sys.argv)

main()




# while True:
#     import time
#     time.sleep(1)

# if __name__ == "__main__":
#     main()
#     time.sleep(1)
