from selenium import webdriver
from src.whatsapp import WhatsApp

browser = webdriver.Chrome(executable_path="chromedriver.exe")
browser.get('https://web.whatsapp.com')

input('Aperte enter após ler o QR')

wpp = WhatsApp(browser=browser)

contato = ''  # Numero do contato exemplo: +55149987...
mensagem = 'Bom dia, tudo bem ?'

# Enviando a mensagem
wpp.send_message(
    contact=contato,
    message=mensagem
)

