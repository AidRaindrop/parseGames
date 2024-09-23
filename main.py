from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha
from selenium_recaptcha_solver import RecaptchaSolver
import cred as CR
import requests
import time
from datetime import datetime

#token telegram bot
token = CR.TOKEN
chat_id = CR.CHAT_ID

test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'


def send_msg(text):
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())

options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument(f'--user-agent={test_ua}')
options.add_argument('--disable-dev-shm-usage')

# Укажите путь к веб-драйверу
#driver = webdriver.Chrome('/путь_к_webdriver/chromedriver')
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# Открыть страницу логина
#driver.implicitly_wait(10)
n=1
while 1:
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('http://rentalgames.in.ua/index.php')

        time.sleep(3)
        ex = driver.find_element(By.LINK_TEXT, "Вход").click()

        # Найти и ввести логин и пароль
        username = driver.find_element(By.NAME,'email')
        username.send_keys(CR.USER_NAME)

        password = driver.find_element(By.NAME, 'password')
        password.send_keys(CR.PASS)

        solver = RecaptchaSolver(driver=driver)
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

        time.sleep(1)

        submit_btn = driver.find_element(By.CLASS_NAME, 'btn').click()
        driver.implicitly_wait(2)
        time.sleep(1)

        while 1:

            try:
                clicks_menu = driver.find_element(By.CSS_SELECTOR, "li.user__menu").click()

                clicks = driver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div[2]/ul[1]/li/ul/li[1]/a").click()

                time.sleep(2)

                total = driver.find_element(By.CLASS_NAME, "statistic__value").get_attribute("textContent")
                total_int = total.split()[0]
                print(int(total_int))

                if int(total_int) <=4000:
                    if n!=0:
                        n=0
                        current_datetime = datetime.now()
                        print(current_datetime)
                        print("Закончилось время")
                        text = "Критичная сумма "+total_int+" .Необходимо пополнить баланс!!!"
                        send_msg(text)

                else:
                    if n!=1:
                        print(current_datetime)
                        print("Пополнен баланс")
                        text = "Баланс пополнен до " + total_int
                        send_msg(text)
                        n = 1

                    else:
                        current_datetime = datetime.now()
                        print(current_datetime)
                        print("Деньги есть!!!")


#                else:
#                    current_datetime = datetime.now()
#                    print(current_datetime)
#                    print("Деньги есть!!!")
                driver.refresh()

                time.sleep(240)
            except Exception as inst:

                print("Second Try \n")
                text = "Ошибка скрипта"
                send_msg(text)
                print(inst)
                break
        driver.quit()
        time.sleep(3600)

    except Exception as inst1:
        current_datetime = datetime.now()
        print(current_datetime)

        print("Выход из первого TRY с ошибкой \n")
        print(inst1)
        text = "Ошибка скрипта, нужно проверить и возможно перезапустить"
        send_msg(text)
        driver.quit()
        time.sleep(7200)

        #break


