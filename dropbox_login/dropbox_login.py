import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Para executar:
# pip install -r requirements.txt
# python dropbox_login.py \
#   --url='https://www.dropbox.com/cli_link_nonce?nonce=f9a957a3aaffc30cdf5bfc36b3452278' \
#   --username 'dwouglas@gmail.com' \
#   --password="$DROPBOX_PASS"

# Configuração do argumento de linha de comando
parser = argparse.ArgumentParser(description='Log in to Dropbox')
parser.add_argument('--url', dest='url', required=True, help='URL para logar no Dropbox com nonce')
parser.add_argument('--username', dest='username', required=True, help='Usuário')
parser.add_argument('--password', dest='password', required=True, help='Senha')

# Parse dos argumentos de linha de comando
args = parser.parse_args()

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 20)

print(f"Acessando URL para logar: {args.url}")
driver.get(args.url)

print("Esperando os elementos aparecem na tela")
wait.until(EC.presence_of_element_located((By.NAME, "login_email")))
time.sleep(5)

print("Obtendo os inputs de username")
elements_username = driver.find_elements(By.NAME, 'login_email')
print(f"Total: {len(elements_username)}")

for element in elements_username:
    if element.is_enabled() and element.is_displayed():
        print(element)
        element.send_keys(args.username)

print("Obtendo os inputs de password")
elements_password = driver.find_elements(By.NAME, 'login_password')
print(f"Total: {len(elements_password)}")

for element in elements_password:
    if element.is_enabled() and element.is_displayed():
        print(element)
        element.send_keys(args.password)

print("Obtendo os botões de submit")
elements_button_submit = driver.find_elements(By.CSS_SELECTOR, 'button.login-button[type="submit"] div.signin-text')
print(f"Total: {len(elements_button_submit)}")

# // TODO: descomentar
# for element in elements_button_submit:
#     if element.is_enabled() and element.is_displayed():
#         print(element)
#         element.click()

# // TODO: o Dropbox manda um email com um código, que é preciso digitar
# na página. E aí ?! Talvez esse passo tenha que ser manual.

print("Esperando 5 segundos")
time.sleep(10)

# driver.quit()
