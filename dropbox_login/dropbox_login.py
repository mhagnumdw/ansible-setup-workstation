import time
import argparse

from selenium.common.exceptions import WebDriverException

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

# por alguma viagem, o dropbox tem mais de um elemento de input de username
for element in elements_username:
    if element.is_enabled() and element.is_displayed():
        print(element)
        element.send_keys(args.username)

print("Obtendo os inputs de password")
elements_password = driver.find_elements(By.NAME, 'login_password')
print(f"Total: {len(elements_password)}")

# por alguma viagem, o dropbox tem mais de um elemento de input de password
for element in elements_password:
    if element.is_enabled() and element.is_displayed():
        print(element)
        element.send_keys(args.password)

# print("Obtendo os botões de submit")
# elements_button_submit = driver.find_elements(By.CSS_SELECTOR, 'button.login-button[type="submit"] div.signin-text')
# print(f"Total: {len(elements_button_submit)}")

# for element in elements_button_submit:
#     if element.is_enabled() and element.is_displayed():
#         print(element)
#         element.click()

body_element = driver.find_element(By.TAG_NAME, 'body')

script = """
    var modal = document.createElement('div');
    modal.innerHTML = '<h1 style="font-weight:bold; color:black;">Prossiga Manualmente</h1><p style="color:black;">O formulário abaixo já deve estar preenchido com o usuário e senha. Clique no botão Entrar/Sign in. O Dropbox envia um código para o email. Pegue o código, digite no campo abaixo e confirme.</p>';
    modal.style.position = 'fixed';
    modal.style.top = '0%';
    modal.style.left = '50%';
    modal.style.display = 'block';
    modal.style.transform = 'translate(-50%, -0)';
    modal.style.backgroundColor = 'yellow';
    modal.style.zIndex = '9999';
    modal.style.padding = '5px';
    document.getElementsByTagName('body')[0].prepend(modal);
"""

# Adiciona um modal com instruções para o usuário
driver.execute_script(script)

# Espera o usuário fechar o browser para encerrar o script
while True:
    try:
        driver.title
    except WebDriverException:
        break

# print("Esperando 60 segundos")
# time.sleep(60)

# driver.quit()
