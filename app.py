from selenium import webdriver
from src.whatsapp import WhatsApp

# Configurações do driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=session")
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')

browser = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

wpp = WhatsApp(browser=browser)
wpp.home()

# Depois que ler o QR pela a primeira vez comente essa linha
input('Aperte enter após ler o QR')

contato = ''  # Numero do contato exemplo: +55149987...
mensagem = 'Bom dia, tudo bem ?'

# Enviando a mensagem
wpp.send_message(
    contact=contato,
    message=mensagem
)
