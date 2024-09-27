from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import requests
import urllib3
import logging
import time

urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

#url = 'webhook do chat google' # ambiente de teste
#url = 'webhook do chat google' # ambiente de produção

driver_options = webdriver.ChromeOptions()
driver_options.add_argument('--headless') # Não abre a janela do navegador
driver_options.add_argument("start-maximized") # abre a janela maximizado
driver_options.add_argument('--no-sandbox')
driver_options.add_argument('--disable-dev-shm-usage') # Desativa o uso do sistema de arquivos de memória compartilhada
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=driver_options)

logging.basicConfig(filename='/home/suporte/projeto/log_ar_condicionado_ala-A.txt', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def enviar_mensagem_erro(mensagem):
    json_erro = {'text': mensagem}
    requests.post(url=url, json=json_erro, stream=True, verify=False)


def clicar_elemento(elemento, elemento_tipo):
    try:
        time.sleep(2) # Aguarda 2 segundos

        if elemento_tipo == "ID":
            driver.find_element(By.ID, elemento).click()

        elif elemento_tipo == 'XPATH':
            driver.find_element(By.XPATH, elemento).click()
        
        
        print(f'Cliquei no elemento {elemento}')
        logging.info(f'Cliquei no elemento {elemento}')

    except NoSuchElementException as erro:
        mensagem_erro = f'Não encontrei o elemento {elemento}'
        print(str(datetime.now()) + mensagem_erro, erro)
        logging.error(mensagem_erro, exc_info=True)
        enviar_mensagem_erro(mensagem_erro)
        driver.quit()
        exit()

# Acessa o sistema ala A
try:
    driver.get("http://192.168.0.12")
    
except WebDriverException as erro:
    mensagem_erro = 'Erro ao acessar o sistema do ar condicionado, verifique a conexão com a internet'
    print(str(datetime.now()) + mensagem_erro, erro)
    logging.error(mensagem_erro, exc_info=True)
    enviar_mensagem_erro(mensagem_erro)
    driver.quit()
    exit()

print(driver.title)  # título da página

# MICROSCOPIA
# ❄ 07UE78 - id = 42
# ❄ 07UE79 - id = 43
# ❄ 07UE80 - id = 44
# ❄ 07UE81 - id = 45

microscopia = []

for id in range(0,57):
    # Pula um determinado id
    if id in microscopia:
    #if id == 1: #para testes
        continue
        #break #para testes 

    # Clica no ar condicionado
    clicar_elemento("ac_"+str(id), 'ID')

    # Seleciona temperatura 26
    clicar_elemento('//*[@id="pp26"]/font','XPATH')

    # Desliga o ar condicionado
    clicar_elemento("//*[@id='set']/table/tbody/tr[2]/td/table/tbody/tr[14]/td/table/tbody/tr/td[3]",'XPATH')

driver.quit()
print('Finalizado')
exit()
