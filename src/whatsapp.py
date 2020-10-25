from selenium import webdriver
from time import sleep


class WhatsApp:
    """
    Classe responsavel por executar as função do wpp no navegador
    """

    def __init__(self):
        # Configurações do driver
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument("user-data-dir=session")
        self._chrome_options.add_argument('--no-sandbox')
        # self._chrome_options.add_argument('--headless')

        self.browser = webdriver.Chrome(
            executable_path="chromedriver.exe",
            options=self._chrome_options)

        self.home()
        self.waiting_for_qrcode()

    def send_message(self, contact, message):
        """
        Função responsável por enviar uma nova mensagem.

        :param message: Mensagem que vai ser enviada para o contato.
        :param contact: Numero do contato.
        :return: Retorna uma dict com o status.
        """

        """
        Acessando o chat do contato com uma mensagem pré-definida.
        """
        try:
            self.browser.get(f'https://web.whatsapp.com/send?phone={contact}&text={message}')
            sleep(2)

            # Encontra o botão de enviar mensagem e clica sobre ele.
            button = self.browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
            button.click()
            sleep(1)

            return {
                'status': True  # Status verdadeiro, mensagem enviada com sucesso.
            }
        except Exception as e:
            return {
                'status': False,  # Status falso, ocorreu algum erro no processo.
                'message': str(e)  # Mensagem de erro.
            }

    def contact_information(self, contact):
        """
        Função que coleta algumas informações.

        :param contact: Numero do contato.
        :return: Retorna um dict com o status, nome e recado.
        """

        """
        Acessando a conversa do contato.
        """
        try:
            self.browser.get(f'https://web.whatsapp.com/send?phone={contact}')
            sleep(2)

            # Clicando sobre o numero.
            button = self.browser.find_element_by_xpath('//*[@id="main"]/header/div[2]')
            button.click()
            sleep(3.5)

            # Coletando o nome.
            name = self.browser.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/div[2]/span/span').get_attribute(
                'textContent')

            # Coletando o recado.
            status = str(self.browser.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[4]/div[2]/div/div/span').get_attribute(
                'textContent')).replace('\u200e', '').replace("'", '')

            if status == '':
                status = False

            return {
                'status': True,  # Status verdadeiro, coletou uma ou mais informações.
                'nome': name,  # Nome do contato.
                'recado': status  # Recado do contato.
            }
        except Exception as e:
            return {
                'status': False,  # Status falso, ocorreu algum erro no processo.
                'message': str(e)  # Mensagem de erro.
            }

    def home(self):
        """
        Função que retorna para a pagina inicial do WhatsApp.

        :return:
        """
        try:
            self.browser.get('https://web.whatsapp.com')
            self.browser.switch_to.alert.accept()
            sleep(1)
        except:
            pass

    def latest_messages(self):
        """
        Função que percorre por todos os chats, filtrando apenas os chats que têm mensagem nova.

        :return: Retorna um array dos contatos junto com a mensagem e o horario.
        """
        messages = []

        # Percorre por todos os chat, pegando a ultima mensagem recebida e o horario.
        for element in self.browser.find_elements_by_class_name('_210SC'):
            chat = str(element.text).split('\n')

            # Verifica se o tamanho do array é igual a 4, se sim tem mensagem não visualizada.
            if len(chat) == 4:
                if 'digitando...' not in chat[2].lower():
                    messages.append(
                        {'numero': chat[0].replace(' ', ''),  # Se não tiver a pessoa na agenda vai retorna o numero.
                         'horario': chat[1],  # Exemplo 13:00
                         'mensagem': chat[2].lower()}  # Retorna a ultima mensagem que o contato enviou.
                    )

        return messages

    def delete_chat(self, contact):
        self.browser.get(f'https://web.whatsapp.com/send?phone={contact}')
        sleep(2)

        # Clicando nos 3 pontinhos
        button = self.browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
        button.click()
        sleep(1)

        button_delete = self.browser.find_element_by_xpath(
            '//*[@id="main"]/header/div[3]/div/div[2]/span/div/ul/li[5]/div')
        button_delete.click()
        sleep(1)
        button_confirm = self.browser.find_element_by_xpath(
            '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div[2]')
        button_confirm.click()

        sleep(1)

    def waiting_for_qrcode(self, timeout=2):
        """
        Função que verifica se o QR Code já foi escaneado, se não fica aguardando até que seja.

        :param timeout: Tempo que aguarda para cada verificação.
        :return:
        """

        print('Aguardando a leitura do QR Code...')
        while True:
            try:
                # Verifica se existe o texto "Mantenha seu celular conectado" na pagina.
                if len(self.browser.find_elements_by_class_name('_2dH1A')) == 1:
                    break
                sleep(timeout)
            except:
                pass
