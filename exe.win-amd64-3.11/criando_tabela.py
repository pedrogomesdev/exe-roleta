import logging
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CondicaoExperada
import os

logging.basicConfig(filename='logfile.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
tabela_numeros = []

def iniciar_driver(proxy_url):
    try:
        chrome_options = Options()
        arguments = [
                    '--lang=pt-BR',
                    '--window-size=1280,720',
                    '--incognito',
                    '--disable-gpu',
                ]
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-plugins-discovery')
        chrome_options.add_argument('--disable-save-password-bubble')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--disable-audio")

        for argument in arguments:
            chrome_options.add_argument(argument)

        chrome_options.add_argument('--log-level=3')
        chrome_options.add_experimental_option('prefs', {
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_setting_values.automatic_downloads': 1,
        })


        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--proxy-server={}'.format(proxy_url))

        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(
            driver,
            10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
                StaleElementReferenceException
            ]
        )
        return driver, wait
    except Exception as e:
        print(e)
        pass
    
def get_scrapeops_url(url):
    try:
        payload = {'api_key': 'fec4000c-48c3-4827-a41d-578f1730f4e5', 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    except Exception as e:
        pass

try:
    url= 'https://casino.betfair.com/pt-br/'
    proxy_url = get_scrapeops_url(url)
    driver, wait = iniciar_driver(proxy_url)
    driver.get(url)
except Exception as e:
    logging.exception("ERRO: %s", e)
    pass

def login():
    try:
        EMAIL = 'damonalisson15@gmail.com'
        SENHA = 'Af12546798@'
        sleep(2)
        botao_continue = wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        botao_continue.click()
        sleep(1)
        campo_email = wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@name="username"]')))
        campo_email.send_keys(EMAIL)
        sleep(2)
        campo_senha = wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@name="password"]')))
        campo_senha.send_keys(SENHA)
        sleep(2)
        botao_continue = wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@value="Login"]')))
        botao_continue.click()
        sleep(2)
        
        botao_continue = wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/section')))
        botao_continue.click()
        print('LOGIN REALIZADO')
        sleep(3)
        janelas = driver.window_handles
        segunda_aba = janelas[1]
        driver.switch_to.window(segunda_aba)
    except Exception as e:
        print('LOGIN NAO FOI REALIZADO COM SUCESSO!')
        logging.exception("ERRO: %s", e)
        pass    
login()

def construindo_tabela(): 
    try:
        sleep(3)
        botao_results = wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//*[@data-automation-locator="button.extenededHistory"]')))
        botao_results.click()
        numeros = driver.find_elements(By.XPATH, '//*[@class="roulette-history-item__value-text--siwxW"]')
        for i in range(512):
            num = numeros[i].get_attribute('innerHTML')
            tabela_numeros.append(num)  
    except Exception as e:
        logging.exception("ERRO: %s", e)
        pass
   
os.system('cls') 
    
construindo_tabela()

def gerando_txt():
    with open("tabela.txt", 'w') as arquivo:
        arquivo.write(str(tabela_numeros))
    print("ARQUIVO.TXT CRIADO COM SUCESSO!") 

driver.quit()