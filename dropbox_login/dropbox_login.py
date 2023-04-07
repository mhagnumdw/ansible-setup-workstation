from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.dropbox.com/cli_link_nonce?nonce=748bde3d9c597951074b1377ee05b9bf')

email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'login_email')))
email_field.send_keys('dwouglas@gmail.com')

password_field = driver.find_element_by_name('login_password')
password_field.send_keys('mypassword')

login_button = driver.find_element_by_class_name('login-button')
login_button.click()

# Aqui você pode adicionar comandos para navegar na página

# driver.quit()
